"""
Performs post-action critique to identify errors and improve future performance.

This function implements the reflexive critique mechanism from the reliability
engineering framework, analyzing agent actions to identify errors, biases,
and improvement opportunities.

Args:
    action_sequence (list): Sequence of actions taken by the agent
    expected_outcome (dict, optional): Expected outcome for comparison
    critique_focus (str): Focus area for critique ('errors', 'efficiency', 'strategy', 'all')

Returns:
    dict: Critique results with keys:
        - 'score' (float): Overall performance score 0-1
        - 'errors' (list): List of identified errors
        - 'improvements' (list): Suggested improvements
        - 'patterns' (list): Detected behavioral patterns
        - 'recommendations' (list): Specific recommendations for future actions
"""

def reflexive_critique(action_sequence, expected_outcome=None, critique_focus='all'):
    """
    Performs post-action critique to identify errors and improve future performance.

    Implements reflexive critique for autonomous agents.
    """
    from typing import List, Dict, Any

    if not action_sequence:
        return {
            'score': 0.0,
            'errors': ['No actions to critique'],
            'improvements': ['Provide action sequence for critique'],
            'patterns': [],
            'recommendations': []
        }

    errors = []
    improvements = []
    patterns = []
    recommendations = []

    # Analyze action sequence
    tool_usage = {}
    error_count = 0
    success_count = 0

    for i, action in enumerate(action_sequence):
        # Track tool usage
        tool_name = action.get('tool_name', 'unknown')
        tool_usage[tool_name] = tool_usage.get(tool_name, 0) + 1

        # Check for errors in action results
        if 'result' in action and isinstance(action['result'], dict):
            result = action['result']
            if 'error' in str(result).lower() or 'failed' in str(result).lower():
                error_count += 1
                errors.append(f'Action {i+1} ({tool_name}): Result indicates error')
            else:
                success_count += 1

        # Check for efficiency issues
        if i > 0:
            prev_action = action_sequence[i-1]
            if tool_name == prev_action.get('tool_name'):
                patterns.append(f'Tool repetition: {tool_name} used consecutively')
                improvements.append(f'Consider batching {tool_name} operations')

    # Calculate score
    total_actions = len(action_sequence)
    if total_actions > 0:
        error_ratio = error_count / total_actions
        score = 1.0 - error_ratio
    else:
        score = 0.0

    # Analyze patterns
    for tool, count in tool_usage.items():
        if count > 3:
            patterns.append(f'High usage of {tool}: {count} times')
            recommendations.append(f'Consider creating automated tool for {tool}')

    # Check for strategic issues
    if len(action_sequence) > 10:
        patterns.append('Long action sequence detected')
        improvements.append('Break complex tasks into smaller subtasks')

    # Check tool diversity
    unique_tools = len(tool_usage)
    if unique_tools < 2 and total_actions > 3:
        patterns.append('Low tool diversity')
        recommendations.append('Explore alternative tools or approaches')

    # Compare with expected outcome if provided
    if expected_outcome:
        # Simple comparison logic
        last_action = action_sequence[-1] if action_sequence else {}
        last_result = last_action.get('result', {})

        if 'expected_key' in expected_outcome:
            expected_key = expected_outcome['expected_key']
            if expected_key not in str(last_result):
                errors.append(f'Expected key "{expected_key}" not found in result')
                score *= 0.7  # Penalty for missing expected outcome

    # Focus-specific analysis
    if critique_focus == 'errors':
        improvements = [imp for imp in improvements if 'error' in imp.lower()]
        recommendations = [rec for rec in recommendations if 'error' in rec.lower()]
    elif critique_focus == 'efficiency':
        improvements = [imp for imp in improvements if 'efficiency' in imp.lower() or 'batch' in imp.lower() or 'optimize' in imp.lower()]
        recommendations = [rec for rec in recommendations if 'efficiency' in rec.lower() or 'optimize' in rec.lower()]
    elif critique_focus == 'strategy':
        improvements = [imp for imp in improvements if 'strategy' in imp.lower() or 'approach' in imp.lower() or 'break' in imp.lower()]
        recommendations = [rec for rec in recommendations if 'strategy' in rec.lower() or 'approach' in rec.lower()]

    # Ensure we have at least some recommendations
    if not recommendations:
        if score > 0.8:
            recommendations.append('Good performance. Consider documenting this successful approach.')
        else:
            recommendations.append('Review action sequence for optimization opportunities.')

    return {
        'score': round(score, 2),
        'errors': errors[:5],  # Limit to 5 errors
        'improvements': improvements[:5],  # Limit to 5 improvements
        'patterns': patterns[:5],  # Limit to 5 patterns
        'recommendations': recommendations[:5]  # Limit to 5 recommendations
    }
