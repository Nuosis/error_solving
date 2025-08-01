# Error Solving MCP Server

A Model Context Protocol (MCP) server that provides systematic error solving using null hypothesis testing methodology.

## Overview

This MCP server helps create structured error investigation documents and provides guidance for systematic debugging using the null hypothesis testing approach. It generates investigation templates based on problem statements and provides step-by-step methodology for eliminating potential causes.

## Features

### Tools Provided

1. **create_error_solving_document**
   - Creates a structured error investigation document based on a problem statement
   - Generates hypotheses and null hypotheses automatically
   - Follows the systematic investigation template format

2. **get_investigation_prompt**
   - Returns the complete investigation methodology prompt
   - Provides guidelines for null hypothesis testing approach
   - Includes evidence collection standards and investigation rules

3. **generate_investigation_instructions**
   - Provides complete step-by-step instructions for error solving
   - Combines document creation with investigation methodology
   - Includes implementation checklist and critical reminders

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

## Usage

The server provides three main tools for systematic error investigation:

### Creating an Error Investigation Document

Use the `create_error_solving_document` tool with a problem statement to generate a structured investigation document with automatically generated hypotheses.

### Getting Investigation Guidance

Use the `get_investigation_prompt` tool to get the complete methodology for systematic error investigation using null hypothesis testing.

### Complete Investigation Instructions

Use the `generate_investigation_instructions` tool to get step-by-step directions for the entire error-solving process.

## Methodology

This server implements a systematic approach to error solving based on:

1. **Null Hypothesis Testing**: Each potential cause is formulated as a hypothesis with a corresponding null hypothesis
2. **Live Application Evidence**: Only accepts direct log evidence from live application execution
3. **Systematic Elimination**: Proves or disproves each null hypothesis systematically
4. **Complete Investigation**: Continues until ALL hypotheses are tested

## Evidence Standards

- **ONLY** accepts live application log evidence with timestamps and actual data values
- **REJECTS** testing results, code analysis, inferences, or simulated behavior
- **REQUIRES** dedicated logging evidence for each hypothesis
- **CONTINUES** investigation until all hypotheses are systematically tested

## Configuration

The server includes local copies of the template and prompt files:
- Template: `error_solving_template.md`
- Prompt: `error_solving_prompt.md`

These files define the structure and methodology for systematic error investigation.

## License

MIT License