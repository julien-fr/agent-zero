# Tool: reflexive_critique

## Purpose
Performs post-action critique to identify errors and improve future performance.
Implements the reflexive critique mechanism from the reliability engineering framework.

## When to Use
- After completing a task or action sequence
- During debugging and error analysis
- For performance optimization
- As part of learning and improvement cycles

## How to Use
1. Provide action sequence (list of actions taken)
2. Optionally provide expected outcome for comparison
3. Choose critique focus:
   - `errors`: Focus on error identification
   - `efficiency`: Focus on performance optimization
   - `strategy`: Focus on strategic decisions
   - `all`: Comprehensive critique (default)

## Expected Output
A dictionary with:
- `score`: Overall performance score 0-1
- `errors`: List of identified errors
- `improvements`: Suggested improvements
- `patterns`: Detected behavioral patterns
- `recommendations`: Specific recommendations

## Integration Guidelines
- Use regularly for continuous improvement
- Store critique results for trend analysis
- Adjust agent behavior based on critique insights
- Combine with other monitoring tools

## Example Usage
```python
action_sequence = [
    {'tool_name': 'read_file', 'result': {'success': True}},
    {'tool_name': 'process_data', 'result': {'error': 'Invalid format'}}
]
result = reflexive_critique(action_sequence, critique_focus='errors')
print(f"Performance score: {result['score']}")
print(f"Errors: {result['errors']}")
print(f"Recommendations: {result['recommendations']}")
```
