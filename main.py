#!/usr/bin/env python3
"""
Error Solving MCP Server using FastMCP

This server provides a simplified tool for error solving that returns the template as-is
and combines provided problem information with the error solving prompt.
"""

import os
from typing import Optional

from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Error Solving Server")

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

[Default prompt content...]
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
               "file": "Template as-is",
               "prompt": "Provided information + contents of error_solving_prompt.md"
             }
    """
    try:
        import json
        
        # Get the template as-is
        template_content = read_template_file()
        
        # Create the prompt by combining provided information with prompt file contents
        prompt_file_content = read_prompt_file()
        
        combined_prompt = f"""## Problem Statement
{problem_statement}

## Steps to Reproduce
{steps_to_reproduce}

## Existing Efforts
{existing_efforts}

## Instructions
{prompt_file_content}"""
        
        # Create JSON response
        response = {
            "file": template_content.strip(),
            "prompt": combined_prompt.strip()
        }
        
        return json.dumps(response, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error defining problem: {str(e)}"}, indent=2)


if __name__ == "__main__":
    # Run the FastMCP server
    mcp.run()