# Error Solving Process - Phase 1: Code Review

## Context
Review the error analysis in {{FILE}} which documents a basic bug description requiring initial code review to identify obvious issues.

## Phase 1 Objective
The goal of Phase 1 is to review the code and ensure there are no obvious issues that could be causing the reported problem. This phase focuses on:

1. **Code Analysis**: Examine the relevant code paths for obvious bugs, typos, or logic errors
2. **Configuration Review**: Check for obvious configuration issues or missing settings
3. **Basic Validation**: Verify that the code follows expected patterns and conventions
4. **Quick Wins**: Identify any immediately apparent issues that can be resolved

## Investigation Approach

### 1. Code Path Analysis
- Trace through the code path described in the problem statement
- Look for obvious syntax errors, typos, or logic mistakes
- Verify method signatures and parameter passing
- Check for missing imports or dependencies

### 2. Configuration Verification
- Review relevant configuration files for obvious errors
- Check environment variables and settings
- Verify database connections and external service configurations
- Look for missing or incorrect configuration values

### 3. Pattern Compliance
- Ensure code follows established patterns in the codebase
- Check for proper error handling
- Verify logging is in place where expected
- Look for obvious security or performance issues

### 4. Working Code Documentation
- Find and document working code examples that demonstrate expected behavior
- Identify similar functionality that works correctly in the codebase
- Document the differences between working and non-working code paths
- Use working examples as reference for fixing broken functionality

### 5. Unit Testing for Validation
- Create or run unit tests to validate individual components
- Use tests to isolate and verify specific functionality
- Test edge cases and boundary conditions
- Document test results to support or refute hypotheses about the problem

### 6. Quick Issue Resolution
- Fix any obvious bugs found during review
- Correct configuration errors
- Add missing error handling where clearly needed
- Implement basic logging if completely absent

## Evidence Standards for Phase 1
- **Code Review Evidence**: Direct examination of source code, configuration files, and project structure
- **Static Analysis**: Review of code patterns, imports, and basic logic flow
- **Configuration Validation**: Verification of settings and environment configurations
- **Unit Test Results**: Test outcomes that validate or invalidate component behavior
- **Working Code Examples**: Documentation of similar functionality that works correctly

## Phase 1 Completion Criteria
Phase 1 is complete when:
- All obvious code issues have been identified and resolved
- Configuration has been verified as correct
- Basic error handling and logging are in place
- No immediately apparent bugs remain in the code path

## Transition to Phase 2
Move to Phase 2 when:
- All obvious code issues have been resolved
- The user reports the issue persists after Phase 1 fixes
- No more obvious problems can be identified through code review
- The problem requires runtime observation to diagnose

## Phase 1 Investigation Pattern
Follow this pattern for Phase 1:

1. **Review Problem Statement**: Understand what the user is experiencing
2. **Identify Code Paths**: Determine which code is involved in the problem
3. **Examine Source Code**: Look for obvious bugs, typos, or logic errors
4. **Check Configuration**: Verify settings and environment variables
5. **Fix Obvious Issues**: Resolve any clear problems found
6. **Verify Fixes**: Ensure fixes are properly implemented
7. **Report Findings**: Document what was found and fixed
8. **Assess Need for Phase 2**: Determine if runtime observation is needed

## Critical Phase 1 Rules
- Focus on **obvious** issues that can be identified through code review
- Do not spend time on complex debugging that requires runtime analysis
- Fix clear bugs immediately rather than just documenting them
- If no obvious issues are found, proceed to Phase 2 for runtime observation
- Document all changes made during Phase 1 for future reference