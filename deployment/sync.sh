#!/bin/bash

# MCP Error Solving Server Sync Script
# This script handles the complete deployment workflow using rsync for efficient file transfer
# Usage: ./sync.sh [initial|update]

set -e

# Load environment variables if .env file exists
if [ -f ".env" ]; then
    echo "📋 Loading configuration from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️  No .env file found, using defaults..."
fi

# Configuration from environment variables with defaults
DEPLOY_USER="${DEPLOY_USER:-marcus}"
SSH_HOST="${SSH_HOST:-backend.claritybusinesssolutions.ca}"
SSH_PORT="${SSH_PORT:-22}"
APP_DIR="${DEPLOY_PATH:-/home/marcus/mcp-error-solving}"
SERVICE_NAME="${SERVICE_NAME:-mcp-error-solving}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Determine deployment mode
DEPLOY_MODE="${1:-update}"

if [ "$DEPLOY_MODE" = "initial" ]; then
    echo "🚀 Starting initial MCP Error Solving Server deployment..."
else
    echo "🔄 Starting MCP Error Solving Server update..."
fi

# Check if we have SSH access
print_step "Testing SSH connection..."
if ! ssh -o ConnectTimeout=10 -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "echo 'SSH connection successful'" > /dev/null 2>&1; then
    print_error "Cannot connect to $DEPLOY_USER@$SSH_HOST:$SSH_PORT"
    print_error "Please check your SSH configuration and ensure the server is accessible"
    exit 1
fi
print_status "✅ SSH connection verified"

# Create application directory on remote server if it doesn't exist
print_step "Ensuring application directory exists..."
ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "mkdir -p $APP_DIR"

# Sync files using rsync (much more efficient than scp)
print_step "Syncing files to server..."

# Create rsync exclude file
cat > /tmp/rsync_exclude << EOF
.git/
.gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.DS_Store
.vscode/
.idea/
*.swp
*.swo
.env
deploy.sh
update.sh
sync.sh
README.md
client_config.json
EOF

# Sync the files
rsync -avz --progress --delete \
    --exclude-from=/tmp/rsync_exclude \
    -e "ssh -p $SSH_PORT" \
    ./ $DEPLOY_USER@$SSH_HOST:$APP_DIR/

# Copy the remote_main.py as main.py
ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "
    cd $APP_DIR
    if [ -f remote_main.py ]; then
        cp remote_main.py main.py
        echo 'Copied remote_main.py to main.py'
    fi
"

# Handle .env file separately (if it exists locally)
if [ -f ".env" ]; then
    print_step "Uploading .env file..."
    scp -P $SSH_PORT .env $DEPLOY_USER@$SSH_HOST:$APP_DIR/
    print_status "✅ .env file uploaded"
elif [ -f ".env.example" ]; then
    print_step "Creating .env from .env.example..."
    scp -P $SSH_PORT .env.example $DEPLOY_USER@$SSH_HOST:$APP_DIR/.env
    print_warning "⚠️  Created .env from .env.example - please customize it on the server"
fi

print_status "✅ Files synced successfully"

# Cleanup temporary file
rm -f /tmp/rsync_exclude

if [ "$DEPLOY_MODE" = "initial" ]; then
    # Initial deployment - set up everything
    print_step "Setting up Python environment..."
    ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "
        cd $APP_DIR
        
        # Create virtual environment if it doesn't exist
        if [ ! -d 'venv' ]; then
            python3 -m venv venv
            echo 'Created Python virtual environment'
        fi
        
        # Activate and install dependencies
        source venv/bin/activate
        pip install --upgrade pip
        pip install -r requirements.txt
        
        # Set permissions
        chmod +x main.py
        
        echo 'Python environment setup complete'
    "
    
    # Install systemd service
    print_step "Installing systemd service..."
    scp -P $SSH_PORT mcp-error-solving.service $DEPLOY_USER@$SSH_HOST:/tmp/
    ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "
        sudo cp /tmp/mcp-error-solving.service /etc/systemd/system/
        sudo systemctl daemon-reload
        sudo systemctl enable $SERVICE_NAME
        rm /tmp/mcp-error-solving.service
        echo 'Systemd service installed and enabled'
    "
    
    # Configure firewall
    print_step "Configuring firewall..."
    ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "
        sudo ufw allow ${SERVER_PORT:-8000}/tcp comment 'MCP Error Solving Server'
        echo 'Firewall configured'
    "
    
else
    # Update deployment - just update dependencies if needed
    print_step "Updating Python dependencies..."
    ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "
        cd $APP_DIR
        source venv/bin/activate
        pip install -r requirements.txt --upgrade
    "
fi

# Start/Restart the service
print_step "Starting MCP Error Solving Server..."
ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "
    sudo systemctl restart $SERVICE_NAME
    sleep 3
"

# Check service status
print_step "Verifying service status..."
if ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "sudo systemctl is-active --quiet $SERVICE_NAME"; then
    print_status "✅ MCP Error Solving Server is running successfully!"
    
    # Get brief service status
    ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "sudo systemctl status $SERVICE_NAME --no-pager -l | head -15"
    
    print_status "🌐 Server is accessible at:"
    print_status "   - Remote: http://$SSH_HOST:${SERVER_PORT:-8000}"
    
else
    print_error "❌ Service failed to start properly"
    print_error "Checking recent logs..."
    ssh -p $SSH_PORT $DEPLOY_USER@$SSH_HOST "sudo journalctl -u $SERVICE_NAME -n 20 --no-pager"
    exit 1
fi

# Optional: Test the server endpoint
print_step "Testing server endpoint..."
if command -v curl > /dev/null; then
    sleep 2  # Give the server a moment to fully start
    if curl -s --connect-timeout 10 "http://$SSH_HOST:${SERVER_PORT:-8000}" > /dev/null 2>&1; then
        print_status "✅ Server endpoint is responding"
    else
        print_warning "⚠️  Server endpoint test failed (server might still be starting up)"
    fi
else
    print_warning "curl not available, skipping endpoint test"
fi

if [ "$DEPLOY_MODE" = "initial" ]; then
    print_status "🎉 Initial deployment completed successfully!"
else
    print_status "🎉 Update completed successfully!"
fi

print_status "📋 Useful commands for monitoring:"
print_status "   - Check status: ssh $DEPLOY_USER@$SSH_HOST 'sudo systemctl status $SERVICE_NAME'"
print_status "   - View logs: ssh $DEPLOY_USER@$SSH_HOST 'sudo journalctl -u $SERVICE_NAME -f'"
print_status "   - Restart: ssh $DEPLOY_USER@$SSH_HOST 'sudo systemctl restart $SERVICE_NAME'"
print_status "   - Update: ./sync.sh update"