# MCP Error Solving Server - Remote Deployment Guide

This guide will help you deploy the MCP Error Solving Server on your Hetzner instance at `backend.claritybusinesssolutions.ca`.

## Prerequisites

- SSH access to your Hetzner instance
- Ubuntu/Debian-based system
- Python 3.9+ installed
- Sudo privileges for the user
- `rsync` installed on your local machine (for efficient file syncing)

## Quick Start

### 1. Configure Environment

Copy the example environment file and customize it:

```bash
cp .env.example .env
# Edit .env with your specific configuration
```

### 2. Initial Deployment

For the first deployment, use the sync script:

```bash
./sync.sh initial
```

### 3. Updates

For subsequent updates (much faster):

```bash
./sync.sh update
# or simply
./sync.sh
```

## Deployment Methods

We provide three deployment approaches:

### Method 1: Sync Script (Recommended)
- **File**: `sync.sh`
- **Use**: Both initial deployment and updates
- **Features**: Uses rsync for efficient file transfer, handles both initial setup and updates
- **Usage**:
  - Initial: `./sync.sh initial`
  - Updates: `./sync.sh update` or `./sync.sh`

### Method 2: Update Script
- **File**: `update.sh`
- **Use**: Quick updates only (assumes server is already set up)
- **Features**: Fast updates using SCP, restarts service
- **Usage**: `./update.sh`

### Method 3: Full Deploy Script
- **File**: `deploy.sh`
- **Use**: Manual deployment (run on the server)
- **Features**: Complete setup including system packages
- **Usage**: Run directly on the Hetzner instance

### 4. Verify Deployment

Check if the service is running:

```bash
sudo systemctl status mcp-error-solving
```

View logs:

```bash
sudo journalctl -u mcp-error-solving -f
```

Test the server:

```bash
curl http://localhost:8000/health
```

## Client Configuration

### Option 1: Direct HTTP Connection

The server will be accessible at:
- **Local**: `http://localhost:8000`
- **Remote**: `http://backend.claritybusinesssolutions.ca:8000`

### Option 2: MCP Client Configuration

Update your MCP client configuration to use the remote server. Add this to your MCP settings:

```json
{
  "mcpServers": {
    "error-solving-remote": {
      "command": "python",
      "args": ["-c", "import requests; import json; import sys; response = requests.post('http://backend.claritybusinesssolutions.ca:8000/mcp', json={'method': sys.argv[1], 'params': json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}}); print(response.text)"],
      "env": {}
    }
  }
}
```

## Server Management

### Start/Stop/Restart Service

```bash
# Start the service
sudo systemctl start mcp-error-solving

# Stop the service
sudo systemctl stop mcp-error-solving

# Restart the service
sudo systemctl restart mcp-error-solving

# Enable auto-start on boot
sudo systemctl enable mcp-error-solving
```

### View Logs

```bash
# View recent logs
sudo journalctl -u mcp-error-solving -n 50

# Follow logs in real-time
sudo journalctl -u mcp-error-solving -f

# View logs from today
sudo journalctl -u mcp-error-solving --since today
```

### Update the Server

To update the server code:

1. Upload new files to the server
2. Copy them to the application directory:
   ```bash
   sudo cp ~/mcp-deployment/remote_main.py /home/marcus/mcp-error-solving/main.py
   sudo systemctl restart mcp-error-solving
   ```

## Security Considerations

### Firewall Configuration

The deployment script configures UFW to allow port 8000. You can modify this:

```bash
# Allow only specific IP ranges
sudo ufw delete allow 8000/tcp
sudo ufw allow from YOUR_IP_RANGE to any port 8000

# Or use a reverse proxy with SSL (recommended for production)
```

### SSL/TLS Setup (Recommended)

For production use, consider setting up a reverse proxy with SSL:

1. Install Nginx:
   ```bash
   sudo apt install nginx certbot python3-certbot-nginx
   ```

2. Configure Nginx proxy:
   ```bash
   sudo nano /etc/nginx/sites-available/mcp-error-solving
   ```

3. Add SSL certificate:
   ```bash
   sudo certbot --nginx -d backend.claritybusinesssolutions.ca
   ```

## Troubleshooting

### Service Won't Start

1. Check the service status:
   ```bash
   sudo systemctl status mcp-error-solving
   ```

2. Check logs for errors:
   ```bash
   sudo journalctl -u mcp-error-solving -n 50
   ```

3. Verify Python environment:
   ```bash
   /home/marcus/mcp-error-solving/venv/bin/python --version
   /home/marcus/mcp-error-solving/venv/bin/pip list
   ```

### Port Already in Use

If port 8000 is already in use:

1. Find what's using the port:
   ```bash
   sudo netstat -tlnp | grep :8000
   ```

2. Either stop the conflicting service or change the port in:
   - `remote_main.py` (change the port in `mcp.run()`)
   - `mcp-error-solving.service` (update the ExecStart command)

### Connection Issues

1. Verify firewall settings:
   ```bash
   sudo ufw status
   ```

2. Test local connection:
   ```bash
   curl http://localhost:8000/health
   ```

3. Test remote connection from your local machine:
   ```bash
   curl http://backend.claritybusinesssolutions.ca:8000/health
   ```

## API Endpoints

Once deployed, the server provides these endpoints:

- **Health Check**: `GET /health`
- **MCP Protocol**: `POST /mcp`
- **Tools**: Access via MCP protocol
  - `define_problem`: Generate error investigation packages
- **Resources**: Access via MCP protocol
  - `file://error-solving-template`: Get the investigation template
  - `file://error-solving-prompt`: Get the investigation prompt

## Support

If you encounter issues:

1. Check the logs first: `sudo journalctl -u mcp-error-solving -f`
2. Verify all files are in place: `ls -la /home/marcus/mcp-error-solving/`
3. Test the Python environment: `/home/marcus/mcp-error-solving/venv/bin/python main.py`

The server should now be accessible remotely and ready to handle MCP requests for error solving investigations.