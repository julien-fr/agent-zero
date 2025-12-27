# Tool: generate_playbook

## Purpose
Generates structured playbooks for incident response based on detected patterns.
Implements the playbook generation logic from the reliability engineering framework.

## When to Use
- When an incident is detected (infinite loop, hallucination, tool error, timeout)
- For creating standardized response procedures
- During post-mortem analysis to document resolution steps
- For training and onboarding new agents

## How to Use
1. Identify the incident type:
   - `infinite_loop`: Agent stuck in repetitive behavior
   - `hallucination`: Factual inconsistencies or invented information
   - `tool_error`: Tool execution failures
   - `timeout`: Actions exceeding time limits
2. Provide context about the incident
3. Specify severity level ('low', 'medium', 'high', 'critical')

## Expected Output
A structured playbook dictionary with:
- `title`: Playbook title
- `incident_type`: Type of incident
- `severity`: Severity level
- `triggers`: Detection triggers
- `steps`: Step-by-step resolution procedures
- `verification`: Verification steps
- `escalation`: Escalation procedures

## Integration Guidelines
- Store generated playbooks for future reference
- Use as templates for similar incidents
- Update playbooks based on real-world effectiveness
- Share playbooks across agent instances

## Example Usage
```python
playbook = generate_playbook(
    incident_type='infinite_loop',
    context={'agent_id': 'agent-123', 'error_message': 'Semantic similarity > 0.95'},
    severity='medium'
)
print(f"Playbook: {playbook['title']}")
print(f"Steps: {playbook['steps']}")
```
