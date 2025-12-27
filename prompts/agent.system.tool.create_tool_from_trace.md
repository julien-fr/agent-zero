# Tool: create_tool_from_trace

## Purpose
Creates new tools from repetitive action sequences to implement the DRY principle.
Implements the Tool Forging heuristic from the reliability engineering framework.

## When to Use
- When detecting repetitive action sequences (same tool called multiple times)
- To automate frequently performed tasks
- When optimizing agent performance and reducing token usage
- As part of agent self-improvement routines

## How to Use
1. Collect action trace (list of action dictionaries)
2. Set minimum repetitions threshold (default: 3)
3. Optionally suggest a tool name
4. Call the tool to analyze patterns and generate code

## Expected Output
A dictionary with:
- `created`: Boolean indicating if tool was created
- `tool_name`: Name of created tool
- `code`: Python code for the new tool
- `pattern`: Information about the detected pattern
- `recommendation`: How to use the new tool

## Integration Guidelines
- Review generated code before deployment
- Test new tools in sandbox environment
- Add successful tools to the agent's tool registry
- Monitor tool usage and effectiveness

## Example Usage
```python
action_trace = [
    {'tool_name': 'read_file', 'args': {'path': '/tmp/data.txt'}},
    {'tool_name': 'read_file', 'args': {'path': '/tmp/data.txt'}},
    {'tool_name': 'read_file', 'args': {'path': '/tmp/data.txt'}}
]
result = create_tool_from_trace(action_trace, min_repetitions=2)
if result['created']:
    print(f"Created tool: {result['tool_name']}")
    print(f"Code: {result['code'][:200]}...")
```
