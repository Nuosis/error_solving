```example
# Report Card Model Binding Investigation

## Symptom
When clicking "View Report Card", the policy check fails . We know this because:
- No logs from Student::resolveRouteBinding
- No logs from ReportCardPolicy::view
- URL contains correct StudentID (392513)

## Steps to recreate
{{the steps to recreate the problem}}

## Attempts to Solve the Problem
{{efforts to resolve the problem}}

## Hypotheses

1. **FMModel Base Class** (Most Fundamental)
   - hypothesis: FMModel base class overrides or interferes with standard binding
   - null hypothesis: FMModel preserves standard binding behavior

2. **Model Key Field**
   - hypothesis: StudentID field name mismatch between URL and FileMaker
   - null hypothesis: Field names match correctly

3. **Route Parameter Format**
   - hypothesis: Route parameter format `{student:StudentID}` is incorrect for FileMaker models
   - null hypothesis: Route parameter format is correct and compatible

4. **Middleware Order**
   - hypothesis: Policy middleware runs before model binding can complete
   - null hypothesis: Middleware order allows binding to complete first

5. **FileMaker Model Binding**
   - hypothesis: FileMaker models require different binding approach than standard Eloquent
   - null hypothesis: FileMaker models use standard binding process

6. **Route Cache** (Most Dependent)
   - hypothesis: Route caching prevents new binding configuration from taking effect
   - null hypothesis: Route caching is not affecting binding
```

## Context

## Definitions
- **Valid Evidence**: ONLY direct log output from live application execution showing actual runtime behavior, timestamps, and data values
- **Invalid Evidence**: Testing results, code analysis, inferences, logic deductions, or any simulated/mocked behavior
- **Log Evidence Requirements**: Must include timestamps, actual data values, and demonstrate real application flow during normal operation

## Objective
Using the null hypothesis testing approach:

1. Analyze each hypothesis by:
   - Understanding the stated hypothesis
   - Reviewing its corresponding null hypothesis
   - Examining the evidence required to prove/disprove
   - Following the evidence collection process

2. Evaluate evidence by:
   - **ONLY accepting direct log evidence from live application execution**
   - Rejecting any testing, mocking, or simulated evidence as invalid
   - Determining if log evidence supports or refutes the null hypothesis
   - Assessing if log evidence is conclusive with timestamps and actual data
   - Identifying gaps requiring additional log evidence collection
   - Considering alternative explanations supported by log data

3. Process of elimination:
   - For each proven null hypothesis, eliminate that cause
   - For each disproven null hypothesis, focus investigation there
   - Document reasoning for elimination
   - Maintain clear evidence chain

4. Investigation ordering:
   - Start with most fundamental hypotheses
   - Prove/disprove completely before moving on
   - Use evidence to guide next focus
   - Document decision process

## Expected Outcome
A clear determination of which hypotheses can be eliminated through proven null hypotheses, and which remain as potential root causes requiring further investigation.

**CRITICAL**: The investigation is NOT complete until ALL hypotheses have been systematically tested with live application evidence. Eliminating some hypotheses does NOT mean the problem is solved - it means you must continue investigating the remaining hypotheses.

## Solution Implementation and Verification
Once the root cause has been identified through systematic hypothesis testing:

1. **Solution Identification**: Present the proposed solution based on the evidence gathered
2. **User Agreement**: Obtain explicit user confirmation that they agree with the proposed solution
3. **Solution Implementation**: Implement the solution using the same live application approach:
   - Make the necessary code changes to the live application
   - Add logging to verify the solution is working correctly
   - Execute the application to generate verification evidence
   - Analyze live log output to confirm the solution resolves the issue
4. **Solution Verification**: Use **ONLY live application logs** to verify the solution works - no testing frameworks or simulated evidence

## Documentation of Gotchas and Context Updates
If the solution reveals "gotchas" or important insights that future developers need to be aware of, update the appropriate context files:

### Framework/Library Level Issues
- **Target**: `.roo/rules/roo.md`
- **When**: The issue is related to high-level framework behavior (Python, libraries, external dependencies)
- **Content**: Document the gotcha, why it occurs, and how to avoid/handle it

### Project-Specific Issues
- **Target**: `DEVELOPMENT_GUIDELINES.md`
- **When**: The issue is specific to this project's architecture, patterns, or conventions
- **Content**: Add guidelines to prevent similar issues in the future

### Component-Specific Issues
- **Target**: `roo.md` file in the relevant folder (service, api, schema, etc.)
- **When**: The issue is specific to a particular part of the project
- **Content**: Create or update local roo.md file with component-specific gotchas and best practices

### Documentation Requirements
- Clearly explain the gotcha and its symptoms
- Provide the root cause explanation
- Include prevention strategies or workarounds
- Reference the investigation that uncovered the issue
- Use concrete examples where applicable

## Success Criteria
- Each null hypothesis has been rigorously tested with **live application log evidence only**
- Evidence chain consists entirely of timestamped log entries from actual application execution
- Elimination decisions are justified by direct log observations, not testing or inference
- Investigation order is logical and explained
- Remaining hypotheses require additional log evidence collection
- **NO testing, mocking, or simulated evidence is accepted as valid**
- **CONTINUE until ALL hypotheses are tested** - do not stop after eliminating some hypotheses

## Evidence Collection Methodology
**CRITICAL**: Only the following evidence collection methods are acceptable:

1. **Add logging statements to live application code** to capture runtime behavior
2. **Execute the actual application** to generate log evidence
3. **Extract log entries** showing timestamps, data values, and execution flow
4. **Analyze log patterns** to determine actual system behavior

**FORBIDDEN**: Testing frameworks, mocking, simulated data, code analysis, or logical inference

## Investigation Process
We are going to attempt to solve this issue systematically. To this end:
1) when a null hypotheses is or remains false then the hypothesis remains true
2) as long as an hypothesis is true it remain **AN ISSUE TO BE SOLVED**
3) Solve issues in order. Once an issue is solved (by proving the null hypothesis is true), verify the problem persists. If it does proceed to the next hypothesis
4) **ALL evidence must come from live application logs, not tests**

## Systematic Investigation Pattern
Follow this exact pattern for EACH hypothesis:

1. **State the Hypothesis**: What might be wrong
2. **State the Null Hypothesis**: What should be working correctly
3. **Add Targeted Logging**: Insert logging statements in live application code to capture runtime behavior
4. **Execute Application**: Trigger the application to generate log evidence
5. **Analyze Live Evidence**: Review actual log output with timestamps and data values
6. **Prove/Disprove Null Hypothesis**: Based ONLY on live application logs
7. **Eliminate or Continue**: If null hypothesis is proven true, eliminate and move to next hypothesis

## Critical Investigation Rules

**DO NOT STOP** after eliminating some hypotheses. The pattern of systematic elimination is:
- ✅ **Eliminated hypotheses** = Null hypothesis proven true = That component works correctly
- ❓ **Remaining hypotheses** = Still require investigation with live application evidence
- 🔍 **Continue investigating** until ALL hypotheses are tested

**NEVER conclude the investigation is complete** until:
- ALL hypotheses have been systematically tested with live application evidence
- The actual root cause has been identified and verified
- The symptom has been resolved or the true cause is definitively proven

**Evidence Standards**:
- ONLY accept direct log output from live application execution
- Reject testing results, code analysis, or logical inference
- Require timestamps, actual data values, and real application flow
- Each hypothesis must have dedicated logging evidence, not reused evidence