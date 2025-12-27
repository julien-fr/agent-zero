# Tool: detect_repetition

## Purpose
Advanced detection of repetitive patterns in agent execution logs.
Implements the detection logic from Playbook S1 (Infinite Loop Detection)
using semantic similarity, state hashing, and tool repetition counting.

## When to Use
- When monitoring agent behavior for signs of infinite loops
- For detecting stuck patterns in long-running tasks
- During reliability audits and performance optimization
- As part of reflexive critique mechanisms

## How to Use
1. Provide execution logs (list of log entries)
2. Set similarity threshold (default: 0.95)
3. Set window size for analysis (default: 3)
4. Call the function to get detection results

## Expected Output
A dictionary with:
- `detected`: Boolean indicating if repetition detected
- `pattern_type`: Type of pattern ('semantic', 'state', 'tool_repetition')
- `confidence`: Confidence score 0-1
- `recommended_action`: Suggested resolution strategy
- `details`: Detailed analysis of detected pattern

## Integration Guidelines
- Integrate into agent monitoring systems
- Use as a preventive measure before loops become critical
- Combine with generate_playbook for automated response
- Log detection events for trend analysis

## Example Usage
python
logs = [
    {'thoughts': ['Step 1', 'Step 2'], 'tool_name': 'read_file'},
    {'thoughts': ['Step 1', 'Step 2'], 'tool_name': 'read_file'},
    {'thoughts': ['Step 1', 'Step 2'], 'tool_name': 'read_file'}
]
result = detect_repetition(logs, similarity_threshold=0.95, window_size=3)
if result['detected']:
    print(f"Pattern detected: {result['pattern_type']} with confidence {result['confidence']}")
