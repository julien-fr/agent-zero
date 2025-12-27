"""
Generates structured playbooks for incident response based on detected patterns.

This function implements the playbook generation logic from the reliability engineering
framework, creating actionable procedures for common failure modes in autonomous agents.

Args:
    incident_type (str): Type of incident ('infinite_loop', 'hallucination', 'tool_error', 'timeout')
    context (dict): Contextual information about the incident
    severity (str): Severity level ('low', 'medium', 'high', 'critical')

Returns:
    dict: Structured playbook with keys:
        - 'title' (str): Playbook title
        - 'incident_type' (str): Type of incident
        - 'severity' (str): Severity level
        - 'triggers' (list): Detection triggers
        - 'steps' (list): Step-by-step resolution procedures
        - 'verification' (list): Verification steps
        - 'escalation' (dict): Escalation procedures
"""

def generate_playbook(incident_type, context=None, severity='medium'):
    """
    Generates structured playbooks for incident response.

    Based on the reliability engineering framework, creates actionable procedures
    for common failure modes in autonomous agents.
    """
    from typing import Dict, List, Any

    if context is None:
        context = {}

    # Base playbook structure
    playbook = {
        'title': f'Playbook for {incident_type.replace("_", " ").title()}',
        'incident_type': incident_type,
        'severity': severity,
        'triggers': [],
        'steps': [],
        'verification': [],
        'escalation': {
            'on_failure': 'Notify human operator',
            'timeout_minutes': 15 if severity == 'critical' else 30,
            'contact': 'sre-team@example.com'
        }
    }

    # Define playbooks based on incident type
    if incident_type == 'infinite_loop':
        playbook['triggers'] = [
            'Semantic similarity > 0.95 for 3 consecutive steps',
            'Same tool called 3+ times with identical arguments',
            'State hash unchanged after 2+ modifying actions'
        ]
        playbook['steps'] = [
            '1. HALT: Immediately suspend agent execution',
            '2. ANALYZE: Inject diagnostic prompt to analyze root cause',
            '3. VARIATE: Increase temperature (0.2 → 0.7) or add negative constraint',
            '4. PRUNE: Remove redundant iterations from context window',
            '5. RESTART: Resume with new approach and monitoring'
        ]
        playbook['verification'] = [
            'Check that semantic similarity drops below 0.8',
            'Verify state hash changes after next action',
            'Confirm progress toward objective'
        ]

    elif incident_type == 'hallucination':
        playbook['triggers'] = [
            'Factual inconsistency detected via cross-validation',
            'Reference to non-existent files/APIs',
            'Self-consistency check fails (majority voting disagreement)'
        ]
        playbook['steps'] = [
            '1. VERIFY: Check existence of referenced entities via external tools',
            '2. VOTE: Generate 3 independent diagnoses and compare',
            '3. REFLECT: Perform post-action critique loop',
            '4. CORRECT: Mark previous attempt as erroneous in memory',
            '5. RETRY: Use verified information only'
        ]
        playbook['verification'] = [
            'All referenced entities exist and are accessible',
            'Majority agreement (2/3) on diagnosis',
            'No factual contradictions in final output'
        ]

    elif incident_type == 'tool_error':
        playbook['triggers'] = [
            'Tool execution returns error code',
            'JSON parsing failure',
            'Syntax error in generated code'
        ]
        playbook['steps'] = [
            '1. CAPTURE: Preserve full error context and stack trace',
            '2. DEBUG: Apply delta debugging to isolate minimal failing case',
            '3. DOCUMENT: Consult tool documentation via introspection',
            '4. CORRECT: Iteratively fix with max 3 attempts',
            '5. WORKAROUND: If correction fails, seek alternative approach'
        ]
        playbook['verification'] = [
            'Tool executes successfully with corrected parameters',
            'No syntax errors in generated code',
            'Output matches expected format'
        ]

    elif incident_type == 'timeout':
        playbook['triggers'] = [
            'Action exceeds configured timeout threshold',
            'Resource consumption spikes (CPU/memory)',
            'No progress indicators for extended period'
        ]
        playbook['steps'] = [
            '1. TERMINATE: Kill unresponsive process',
            '2. ANALYZE: Check logs for resource saturation',
            '3. OPTIMIZE: Simplify task or break into smaller chunks',
            '4. FALLBACK: Switch to faster model/alternative service',
            '5. RETRY: With reduced complexity and monitoring'
        ]
        playbook['verification'] = [
            'Action completes within timeout on retry',
            'Resource usage within acceptable limits',
            'Progress indicators show steady advancement'
        ]

    else:
        # Generic playbook for unknown incident types
        playbook['triggers'] = ['Anomalous behavior detected']
        playbook['steps'] = [
            '1. ISOLATE: Contain the incident to prevent spread',
            '2. DOCUMENT: Record all available context and symptoms',
            '3. DIAGNOSE: Use available tools to identify root cause',
            '4. MITIGATE: Apply standard corrective actions',
            '5. MONITOR: Watch for recurrence'
        ]
        playbook['verification'] = [
            'System returns to normal operation',
            'No recurrence within observation window',
            'All metrics within baseline ranges'
        ]

    # Add context-specific adaptations
    if 'agent_id' in context:
        playbook['steps'].insert(0, f'Target Agent: {context["agent_id"]}')

    if 'error_message' in context:
        playbook['steps'].append(f'Error context: {context["error_message"][:100]}...')

    return playbook
