# Error Solving Process - Phase 2: Observability & Logging

## Context
Review the error analysis in {{FILE}} which documents a bug that has passed Phase 1 code review but requires runtime observation to diagnose.

## Phase 2 Objective
The goal of Phase 2 is to expose the problem through specific, targeted logging. This phase focuses on:

1. **Strategic Logging**: Add minimal but sufficient logging to observe runtime behavior
2. **Data Flow Tracking**: Monitor how data moves through the system
3. **State Observation**: Capture system state at critical points
4. **Problem Isolation**: Use logs to narrow down where the issue occurs

## Investigation Approach

### 1. Targeted Logging Strategy
- Add logging at key decision points in the code path
- Log input parameters and return values for critical functions
- Capture state changes and data transformations
- Monitor external service interactions

### 2. Minimal but Sufficient Logging
- Focus on logging that will provide insight into the specific problem
- Avoid excessive logging that creates noise
- Include timestamps and relevant context in log messages
- Use appropriate log levels (DEBUG, INFO, WARN, ERROR)

### 3. Runtime Behavior Analysis
- Execute the application to generate log evidence
- Analyze log patterns to understand actual system behavior
- Compare expected vs. actual behavior based on logs
- Identify where the system deviates from expected flow

### 4. Problem Isolation
- Use logs to narrow down the problem area
- Eliminate components that are working correctly
- Focus investigation on areas showing unexpected behavior
- Prepare for systematic hypothesis testing if needed

## Evidence Standards for Phase 2
- **Live Application Logs**: Direct log output from actual application execution
- **Timestamped Evidence**: All logs must include timestamps for sequence analysis
- **Actual Data Values**: Logs must show real data, not simulated or test data
- **Runtime Flow**: Evidence must demonstrate actual application execution paths

## Logging Implementation Guidelines

### Essential Logging Points
1. **Function Entry/Exit**: Log when entering and exiting critical functions
2. **Parameter Values**: Log input parameters for key operations
3. **State Changes**: Log before and after state modifications
4. **External Calls**: Log requests to and responses from external services
5. **Error Conditions**: Log all error conditions with context
6. **Decision Points**: Log the outcome of conditional logic

### Log Message Format
```
[TIMESTAMP] [LEVEL] [COMPONENT] Message with relevant data
Example: [2024-01-15 10:30:45] [DEBUG] [UserAuth] Login attempt for user: john@example.com
```

### Logging Best Practices
- Include relevant context (user ID, request ID, etc.)
- Log actual values, not just "processing user"
- Use structured logging when possible
- Avoid logging sensitive information
- Make log messages searchable and meaningful

## Phase 2 Completion Criteria
Phase 2 is complete when:
- Sufficient logging has been added to observe the problem
- Log evidence clearly shows where the issue occurs
- The problem has been isolated to specific components or operations
- Either the issue is resolved or systematic investigation (Phase 3) is needed

## Transition to Phase 3
Move to Phase 3 when:
- Logging has been implemented and executed 2-3 times
- Log evidence shows the problem but doesn't immediately reveal the solution
- The issue requires systematic hypothesis testing to resolve
- Multiple potential causes need to be systematically eliminated

## Phase 2 Investigation Pattern
Follow this pattern for Phase 2:

1. **Analyze Phase 1 Results**: Review what was found and fixed in Phase 1
2. **Identify Logging Points**: Determine where to add strategic logging
3. **Implement Logging**: Add minimal but sufficient logging statements
4. **Execute Application**: Run the application to generate log evidence
5. **Analyze Log Output**: Review logs to understand runtime behavior
6. **Iterate if Needed**: Add more logging if initial attempt is insufficient
7. **Isolate Problem Area**: Use logs to narrow down the issue location
8. **Assess Resolution**: Determine if issue is resolved or needs Phase 3

## Critical Phase 2 Rules
- Add **targeted** logging, not excessive logging
- Focus on **runtime behavior** observation
- Use **actual application execution**, not tests
- Limit to **2-3 logging iterations** before moving to Phase 3
- Document **what the logs reveal** about the problem
- Prepare for **systematic investigation** if the issue persists

## Logging Iteration Guidelines
- **First Iteration**: Add basic logging at entry/exit points
- **Second Iteration**: Add more detailed logging based on first results
- **Third Iteration**: Add specific logging for remaining unknowns
- **After 3 Iterations**: Move to Phase 3 for systematic hypothesis testing