#!/usr/bin/env python3
"""
Error Solving MCP Server using FastMCP

This server provides a single streamlined tool for systematic error solving using null hypothesis testing methodology.
It generates complete error investigation packages with both structured documents and investigation prompts.
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Optional

from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("Error Solving Server")

# Template and prompt file paths (local copies)
TEMPLATE_PHASE1_PATH = os.path.join(os.path.dirname(__file__), "error_solving_template_phase1.md")
TEMPLATE_PHASE2_PATH = os.path.join(os.path.dirname(__file__), "error_solving_template_phase2.md")
TEMPLATE_PHASE3_PATH = os.path.join(os.path.dirname(__file__), "error_solving_template_phase3.md")
PROMPT_PHASE1_PATH = os.path.join(os.path.dirname(__file__), "error_solving_prompt_phase1.md")
PROMPT_PHASE2_PATH = os.path.join(os.path.dirname(__file__), "error_solving_prompt_phase2.md")
PROMPT_PHASE3_PATH = os.path.join(os.path.dirname(__file__), "error_solving_prompt_phase3.md")

def read_template_file(phase: int = 3) -> str:
    """Read the error solving template file for the specified phase."""
    phase_paths = {
        1: TEMPLATE_PHASE1_PATH,
        2: TEMPLATE_PHASE2_PATH,
        3: TEMPLATE_PHASE3_PATH
    }
    
    template_path = phase_paths.get(phase, TEMPLATE_PHASE3_PATH)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Return default content based on phase
        if phase == 1:
            return """# {{PROBLEM_NAME}} Investigation - Phase 1: Code Review

## Problem Statement
{{PROBLEM_STATEMENT}}

## Steps to Reproduce
{{STEPS_TO_REPRODUCE}}

## Existing Resolution Efforts
{{EXISTING_EFFORTS}}

## Phase 1: Code Review Analysis
[Phase 1 template content...]
"""
        elif phase == 2:
            return """# {{PROBLEM_NAME}} Investigation - Phase 2: Observability & Logging

## Problem Statement
{{PROBLEM_STATEMENT}}

## Steps to Reproduce
{{STEPS_TO_REPRODUCE}}

## Phase 1 Results Summary
{{PHASE1_SUMMARY}}

## Phase 2: Logging Strategy & Implementation
[Phase 2 template content...]
"""
        else:
            return """# Error Investigation Template

## Symptom
[Describe the observed problem without explanation - just the facts]

## Hypotheses

1. **[Hypothesis Name]** (Most Fundamental)
   - hypothesis: [What might be wrong]
   - null hypothesis: [What should be working correctly]

[Continue with additional hypotheses...]
"""

def read_prompt_file(phase: int = 3) -> str:
    """Read the error solving prompt file for the specified phase."""
    phase_paths = {
        1: PROMPT_PHASE1_PATH,
        2: PROMPT_PHASE2_PATH,
        3: PROMPT_PHASE3_PATH
    }
    
    prompt_path = phase_paths.get(phase, PROMPT_PHASE3_PATH)
    
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Return default content based on phase
        if phase == 1:
            return """# Error Solving Process - Phase 1: Code Review

## Context
Review the error analysis which documents a basic bug description requiring initial code review.

## Phase 1 Objective
Review the code and ensure there are no obvious issues.

[Default Phase 1 content...]
"""
        elif phase == 2:
            return """# Error Solving Process - Phase 2: Observability & Logging

## Context
Review the error analysis which documents a bug requiring runtime observation.

## Phase 2 Objective
Add targeted logging to expose the problem through observation.

[Default Phase 2 content...]
"""
        else:
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
    return read_template_file(3)

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
    return read_prompt_file(3)

def determine_phase(steps_to_reproduce: str, existing_efforts: str) -> int:
    """
    Determine which phase to use based on the steps to reproduce and existing efforts.
    
    Args:
        steps_to_reproduce: Description of steps to reproduce the issue
        existing_efforts: Description of existing troubleshooting efforts
        
    Returns:
        int: Phase number (1, 2, or 3)
    """
    # Normalize inputs for analysis
    steps_lower = steps_to_reproduce.lower().strip()
    efforts_lower = existing_efforts.lower().strip()
    
    # Check for "unverified" or minimal steps to reproduce
    minimal_steps_indicators = [
        "unverified", "not reproduced", "unable to reproduce",
        "cannot reproduce", "no steps", "unknown", "unclear"
    ]
    
    has_minimal_steps = (
        len(steps_lower) < 50 or  # Very short description
        any(indicator in steps_lower for indicator in minimal_steps_indicators) or
        steps_lower in ["", "none", "n/a", "unknown"]
    )
    
    # Check for minimal existing efforts
    minimal_efforts_indicators = [
        "none", "no attempts", "not attempted", "no effort",
        "nothing tried", "no troubleshooting"
    ]
    
    has_minimal_efforts = (
        len(efforts_lower) < 30 or  # Very short description
        any(indicator in efforts_lower for indicator in minimal_efforts_indicators) or
        efforts_lower in ["", "none", "n/a", "nothing"]
    )
    
    # Check for evidence of code review
    code_review_indicators = [
        "reviewed code", "checked code", "examined", "analyzed",
        "looked at", "inspected", "code review"
    ]
    
    has_code_review = any(indicator in efforts_lower for indicator in code_review_indicators)
    
    # Check for evidence of logging/observability work
    logging_indicators = [
        "added logging", "checked logs", "log analysis", "logging",
        "observed", "monitored", "traced", "debugging output"
    ]
    
    has_logging_work = any(indicator in efforts_lower for indicator in logging_indicators)
    
    # Phase 1: Basic bug description, no code review conducted
    if has_minimal_steps and has_minimal_efforts and not has_code_review:
        return 1
    
    # Phase 2: Some reproduction steps, some code review, but little logging
    if not has_minimal_steps and has_code_review and not has_logging_work:
        return 2
    
    # Phase 3: Detailed understanding, sufficient logging, but bug persists
    return 3

@mcp.tool()
def define_problem(
    problem_statement: str,
    steps_to_reproduce: str,
    existing_efforts: str,
    phase: Optional[int] = None
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
                                Report "unverified" if the problem has not been reproduced and observed in code or logs.
                                Example: "1. Navigate to /login 2. Enter valid credentials 3. Click submit button"
        
        existing_efforts (str): Comprehensive description of all troubleshooting attempts made so far,
                              including what was tried, what results were observed, and what was ruled out.
                              Report "None" if no active attempts have been made to solve the bug.
                              Example: "Checked server logs, verified database connectivity, tested with different users"
        
        phase (Optional[int]): Override the automatic phase selection. If not provided, phase will be
                             automatically determined based on steps_to_reproduce and existing_efforts.
                             Phase 1: Basic code review (minimal steps/efforts, no code review done)
                             Phase 2: Observability/logging (some steps/review, but little logging)
                             Phase 3: Full systematic investigation (detailed steps, sufficient logging)
    
    Returns:
        str: JSON string containing both the error investigation file and prompt with the following structure:
             {
               "phase": "Selected phase number",
               "file": "Complete investigation document appropriate for the phase",
               "prompt": "Methodology prompt customized for this specific investigation and phase"
             }
    """
    try:
        import json
        
        # Determine the appropriate phase
        selected_phase = phase if phase is not None else determine_phase(steps_to_reproduce, existing_efforts)
        
        # Generate title from problem statement
        words = re.findall(r'\b[A-Z][a-z]+\b|\b[a-z]+\b', problem_statement)
        key_words = [word.title() for word in words[:4] if len(word) > 3]
        title = f"{' '.join(key_words)} Investigation" if key_words else "Error Investigation"
        
        # Get the appropriate template and prompt for the selected phase
        template_content = read_template_file(selected_phase)
        prompt_content = read_prompt_file(selected_phase)
        
        # Replace template placeholders
        document = template_content.replace("{{PROBLEM_NAME}}", title.replace(" Investigation", ""))
        document = document.replace("{{PROBLEM_STATEMENT}}", problem_statement)
        document = document.replace("{{STEPS_TO_REPRODUCE}}", steps_to_reproduce)
        document = document.replace("{{EXISTING_EFFORTS}}", existing_efforts)
        
        # For Phase 2 and 3, we may need additional placeholders
        if selected_phase == 2:
            document = document.replace("{{PHASE1_SUMMARY}}", "Phase 1 results will be summarized here")
            document = document.replace("{{PHASE1_FIXES}}", "Phase 1 fixes will be documented here")
            document = document.replace("{{PHASE2_JUSTIFICATION}}", "Phase 2 is needed because the issue persists after Phase 1")
        elif selected_phase == 3:
            # For Phase 3, generate hypotheses as before
            combined_context = f"{problem_statement} {steps_to_reproduce} {existing_efforts}"
            hypotheses = generate_hypotheses(combined_context)
            
            # Create comprehensive symptom description for Phase 3
            symptom_description = f"""{problem_statement}

**Steps to Reproduce:**
{steps_to_reproduce}

**Existing Resolution Efforts:**
{existing_efforts}"""
            
            # Create Phase 3 document with hypotheses
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
        
        # Replace prompt placeholders
        prompt_content = prompt_content.replace("{{FILE}}", f"{title.replace(' Investigation', '')}_phase{selected_phase}_report.md")
        prompt_content = prompt_content.replace("{{Name}}", title.replace(" Investigation", ""))
        
        # Create JSON response
        response = {
            "phase": selected_phase,
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
    # Run the FastMCP server
    mcp.run()