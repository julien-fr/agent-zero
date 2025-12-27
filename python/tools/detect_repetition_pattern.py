"""
Detects repetitive patterns in agent logs using semantic similarity and state hashing.

This function implements the detection logic from Playbook S1 (Infinite Loop Detection)
using sequence similarity and state hashing to identify when an agent
is stuck in repetitive behavior.

Args:
    logs (list): List of log entries, each containing 'thoughts', 'actions', or 'state'
    similarity_threshold (float): Sequence similarity threshold for detection (default: 0.95)
    window_size (int): Number of recent entries to analyze (default: 5)

Returns:
    dict: Detection results with keys:
        - 'detected' (bool): True if repetition detected
        - 'pattern_type' (str): 'semantic', 'state', 'tool_repetition', or 'combined'
        - 'confidence' (float): Confidence score 0-1
        - 'recommended_action' (str): Suggested resolution strategy
"""

def detect_repetition_pattern(logs, similarity_threshold=0.95, window_size=5):
    """
    Detects repetitive patterns in agent logs.

    Implementation of brute logic detection for infinite loops and repetitive behavior.
    Uses multiple detection methods for robustness, requiring at least two
    positive detections to reduce false positives.
    """
    import hashlib
    import difflib
    import json
    from typing import List, Dict, Any

    if len(logs) < window_size:
        return {
            'detected': False,
            'pattern_type': 'insufficient_data',
            'confidence': 0.0,
            'recommended_action': 'Continue monitoring'
        }

    # Extract recent entries
    recent_logs = logs[-window_size:]

    # Method 1: Semantic similarity using SequenceMatcher
    texts = []
    for log in recent_logs:
        if 'thoughts' in log:
            texts.append(' '.join(log['thoughts']) if isinstance(log['thoughts'], list) else str(log['thoughts']))
        elif 'action' in log:
            texts.append(str(log['action']))
        else:
            texts.append(str(log))

    # Exclude semantic detection if thoughts contain progression keywords
    progression_keywords = {'étape', 'suivant', 'corriger', 'ajuster', 'améliorer', 'réviser', 'progresser', 'avancer', 'continuer'}
    has_progression = any(any(keyword in text.lower() for keyword in progression_keywords) for text in texts)

    similarities = []
    for i in range(len(texts) - 1):
        if texts[i] and texts[i+1]:
            similarity = difflib.SequenceMatcher(None, texts[i].lower(), texts[i+1].lower()).ratio()
            similarities.append(similarity)

    semantic_detected = False
    if similarities and not has_progression:
        avg_similarity = sum(similarities) / len(similarities)
        semantic_detected = avg_similarity > similarity_threshold

    # Method 2: State hashing
    state_detected = False
    if all('state_hash' in log for log in recent_logs):
        state_hashes = [log['state_hash'] for log in recent_logs]
        state_detected = len(set(state_hashes)) == 1  # All states identical

    # Method 3: Tool repetition with argument comparison
    tool_detected = False
    if all('tool_name' in log for log in recent_logs):
        tool_names = [log['tool_name'] for log in recent_logs]
        # Check if tool_args are identical (hash comparison)
        tool_args_hashes = []
        for log in recent_logs:
            args = log.get('tool_args', {})
            # Convert to canonical JSON string for hashing
            args_str = json.dumps(args, sort_keys=True)
            tool_args_hashes.append(hashlib.md5(args_str.encode()).hexdigest())
        # Tool repetition only if both name and args are identical
        tool_detected = (len(set(tool_names)) == 1) and (len(set(tool_args_hashes)) == 1)

    # Determine overall detection: require at least two positive detections
    detection_count = sum([semantic_detected, state_detected, tool_detected])
    detected = detection_count >= 2

    if detected:
        # Determine pattern type
        if detection_count == 3:
            pattern_type = 'combined'
        elif semantic_detected and tool_detected:
            pattern_type = 'semantic_tool'
        elif semantic_detected and state_detected:
            pattern_type = 'semantic_state'
        elif tool_detected and state_detected:
            pattern_type = 'tool_state'
        elif semantic_detected:
            pattern_type = 'semantic'
        elif state_detected:
            pattern_type = 'state'
        else:
            pattern_type = 'tool_repetition'

        # Confidence based on detection count and individual strengths
        base_confidence = {
            'semantic': 0.7,
            'state': 0.8,
            'tool_repetition': 0.6,
            'semantic_tool': 0.8,
            'semantic_state': 0.85,
            'tool_state': 0.75,
            'combined': 0.9
        }.get(pattern_type, 0.7)
        # Boost confidence with more detections
        confidence = min(0.95, base_confidence + (detection_count - 2) * 0.1)

        # Recommended actions based on pattern type
        action_map = {
            'semantic': 'Increase temperature or inject stochastic variation',
            'state': 'Check if actions modify environment; try alternative approach',
            'tool_repetition': 'Limit tool retries; consider creating automated tool',
            'semantic_tool': 'Vary both thought patterns and tool selection',
            'semantic_state': 'Change environment or introduce new state variables',
            'tool_state': 'Try different tool or modify environment',
            'combined': 'Agent appears stuck; consider full reset or human intervention'
        }
        action = action_map.get(pattern_type, 'Review recent actions and adjust strategy')

        return {
            'detected': True,
            'pattern_type': pattern_type,
            'confidence': confidence,
            'recommended_action': action
        }
    else:
        return {
            'detected': False,
            'pattern_type': 'no_pattern',
            'confidence': 0.0,
            'recommended_action': 'Continue normal operation'
        }
