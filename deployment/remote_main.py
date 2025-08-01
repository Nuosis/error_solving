#!/usr/bin/env python3
"""
Error Solving MCP Server using FastMCP - Remote Deployment Version

This server provides a single streamlined tool for systematic error solving using null hypothesis testing methodology.
It generates complete error investigation packages with both structured documents and investigation prompts.

Modified for remote deployment with proper host binding and CORS support.
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Get configuration from environment variables
SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))
SERVER_NAME = os.getenv('SERVER_NAME', 'Error Solving Server')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Initialize the FastMCP server with remote configuration
mcp = FastMCP(SERVER_NAME)

# Template and prompt file paths (local copies)
TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "error_solving_template.md")
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "error_solving_prompt.md")

def read_template_file() -> str:
    """Read the error solving template file."""
    try:
        with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """# Error Investigation Template

## Symptom
[Describe the observed problem without explanation - just the facts]

## Hypotheses

1. **[Hypothesis Name]** (Most Fundamental)
   - hypothesis: [What might be wrong]
   - null hypothesis: [What should be working correctly]

[Continue with additional hypotheses...]
"""

def read_prompt_file() -> str:
    """Read the error solving prompt file."""
    try:
        with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """# Error Solving Process Using Null Hypothesis Testing

## Context
Review the error analysis which documents a systematic debugging investigation using null hypothesis testing.

## Objective
Using the null hypothesis testing approach to systematically investigate and eliminate potential causes.

## Investigation Rules
1. Only use live application logs as evidence
2. Test one hypothesis at a time
3. Document all findings
4. Move from most fundamental to most dependent hypotheses

## Success Criteria
- Root cause identified and verified
- Solution implemented and tested
- Documentation updated
"""

@mcp.resource("file://error-solving-template")
def get_error_solving_template() -> str:
    """
    Get the error solving template that provides the structured format for documenting
    systematic error investigations using null hypothesis testing methodology.
    
    This template includes sections for:
    - Symptom documentation (facts without explanation)
    - Hypothesis generation with null hypothesis pairs
    - Priority ordering from most fundamental to most dependent
    
    Returns:
        The complete error solving template in Markdown format
    """
    return read_template_file()

@mcp.resource("file://error-solving-prompt")
def get_error_solving_prompt() -> str:
    """
    Get the error solving investigation prompt that guides systematic debugging
    using null hypothesis testing methodology.
    
    This prompt provides:
    - Evidence collection standards (live application logs only)
    - Systematic investigation patterns
    - Hypothesis testing procedures
    - Critical investigation rules and success criteria
    
    Returns:
        The complete error solving methodology prompt in Markdown format
    """
    return read_prompt_file()

@mcp.tool()
def define_problem(
    problem_statement: str,
    steps_to_reproduce: str,
    existing_efforts: str
) -> str:
    """
    Define a problem and generate a complete error-solving investigation package.
    
    This tool creates both a structured error investigation document and the investigation
    methodology prompt, returning them as JSON for immediate use by an LLM.
    
    Args:
        problem_statement (str): A clear, concise description of the problem or error being experienced.
                               Should focus on observable symptoms without speculation about causes.
                               Example: "User authentication fails with 500 error on login attempt"
        
        steps_to_reproduce (str): Detailed, sequential steps that consistently reproduce the error.
                                Should be specific enough for someone else to follow exactly.
                                Example: "1. Navigate to /login 2. Enter valid credentials 3. Click submit button"
        
        existing_efforts (str): Comprehensive description of all troubleshooting attempts made so far,
                              including what was tried, what results were observed, and what was ruled out.
                              Example: "Checked server logs, verified database connectivity, tested with different users"
    
    Returns:
        str: JSON string containing both the error investigation file and prompt with the following structure:
             {
               "file": "Complete investigation document with symptom and generated hypotheses",
               "prompt": "Methodology prompt customized for this specific investigation"
             }
    """
    try:
        import json
        
        # Generate title from problem statement
        words = re.findall(r'\b[A-Z][a-z]+\b|\b[a-z]+\b', problem_statement)
        key_words = [word.title() for word in words[:4] if len(word) > 3]
        title = f"{' '.join(key_words)} Investigation" if key_words else "Error Investigation"
        
        # Create comprehensive symptom description
        symptom_description = f"""{problem_statement}

**Steps to Reproduce:**
{steps_to_reproduce}

**Existing Resolution Efforts:**
{existing_efforts}"""
        
        # Generate hypotheses based on all provided information
        combined_context = f"{problem_statement} {steps_to_reproduce} {existing_efforts}"
        hypotheses = generate_hypotheses(combined_context)
        
        # Create the error investigation document
        document = f"""# {title}

## Symptom
{symptom_description}

## Hypotheses

"""
        
        # Add generated hypotheses with proper priority ordering
        for i, hypothesis in enumerate(hypotheses, 1):
            priority = hypothesis.get('priority', 'Medium')
            document += f"""{i}. **{hypothesis['name']}** ({priority})
   - hypothesis: {hypothesis['hypothesis']}
   - null hypothesis: {hypothesis['null_hypothesis']}

"""
        
        # Get the investigation prompt
        prompt_content = read_prompt_file()
        prompt_content = prompt_content.replace("{{Name}}", title.replace(" Investigation", ""))
        
        # Create JSON response
        response = {
            "file": document.strip(),
            "prompt": prompt_content.strip()
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error defining problem: {str(e)}"}, indent=2)

def generate_hypotheses(problem_statement: str) -> List[Dict[str, str]]:
    """
    Generate hypotheses based on the problem statement.
    
    Args:
        problem_statement: The problem description
        
    Returns:
        List of hypothesis dictionaries with name, hypothesis, null_hypothesis, and priority
    """
    hypotheses = []
    
    # Analyze problem statement for common patterns
    problem_lower = problem_statement.lower()
    
    # Database/Model related issues
    if any(term in problem_lower for term in ['model', 'database', 'binding', 'eloquent', 'query']):
        hypotheses.append({
            'name': 'Model Binding Issue',
            'hypothesis': 'Model binding is failing or not working as expected',
            'null_hypothesis': 'Model binding works correctly and follows standard behavior',
            'priority': 'Most Fundamental'
        })
    
    # Authentication/Authorization issues
    if any(term in problem_lower for term in ['policy', 'auth', 'permission', 'access', 'login']):
        hypotheses.append({
            'name': 'Authorization Policy',
            'hypothesis': 'Authorization policy is preventing access or failing to execute',
            'null_hypothesis': 'Authorization policy executes correctly and grants appropriate access',
            'priority': 'High'
        })
    
    # Route/URL issues
    if any(term in problem_lower for term in ['route', 'url', 'parameter', 'endpoint']):
        hypotheses.append({
            'name': 'Route Configuration',
            'hypothesis': 'Route configuration or parameter handling is incorrect',
            'null_hypothesis': 'Route configuration correctly handles parameters and mapping',
            'priority': 'Medium'
        })
    
    # Middleware issues
    if any(term in problem_lower for term in ['middleware', 'request', 'response', 'pipeline']):
        hypotheses.append({
            'name': 'Middleware Order',
            'hypothesis': 'Middleware execution order or configuration is causing issues',
            'null_hypothesis': 'Middleware executes in correct order without interference',
            'priority': 'Medium'
        })
    
    # Caching issues
    if any(term in problem_lower for term in ['cache', 'cached', 'caching']):
        hypotheses.append({
            'name': 'Cache Configuration',
            'hypothesis': 'Caching is preventing updates or causing stale data issues',
            'null_hypothesis': 'Cache configuration works correctly and serves fresh data',
            'priority': 'Most Dependent'
        })
    
    # Configuration issues
    if any(term in problem_lower for term in ['config', 'setting', 'environment', 'env']):
        hypotheses.append({
            'name': 'Configuration Issue',
            'hypothesis': 'Application configuration or environment settings are incorrect',
            'null_hypothesis': 'Configuration and environment settings are correct and loaded properly',
            'priority': 'High'
        })
    
    # If no specific patterns found, add generic hypotheses
    if not hypotheses:
        hypotheses = [
            {
                'name': 'Core Functionality',
                'hypothesis': 'The core functionality is not working as expected',
                'null_hypothesis': 'The core functionality works correctly under normal conditions',
                'priority': 'Most Fundamental'
            },
            {
                'name': 'Data Flow',
                'hypothesis': 'Data is not flowing correctly through the system',
                'null_hypothesis': 'Data flows correctly through all system components',
                'priority': 'High'
            },
            {
                'name': 'External Dependencies',
                'hypothesis': 'External dependencies or services are causing the issue',
                'null_hypothesis': 'External dependencies are available and responding correctly',
                'priority': 'Medium'
            }
        ]
    
    return hypotheses

if __name__ == "__main__":
    # Run the FastMCP server with configuration from environment variables
    print(f"Starting {SERVER_NAME} on {SERVER_HOST}:{SERVER_PORT}")
    mcp.run(host=SERVER_HOST, port=SERVER_PORT)