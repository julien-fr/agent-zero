"""
Dynamically swaps context elements to maintain working memory within limits.

This function implements the context management techniques from the reliability
engineering framework, rotating context elements in and out of working memory
based on relevance and recency to stay within token limits.

Args:
    current_context (list): Current context elements
    new_elements (list): New elements to incorporate
    max_elements (int): Maximum number of elements to maintain (default: 10)
    strategy (str): Swapping strategy ('fifo', 'lru', 'relevance', 'hybrid')

Returns:
    dict: Context swap result with keys:
        - 'new_context' (list): Updated context after swapping
        - 'removed_elements' (list): Elements removed from context
        - 'added_elements' (list): Elements added to context
        - 'swap_reason' (dict): Reason for each swap decision
"""

def swap_out_context(current_context, new_elements, max_elements=10, strategy='hybrid'):
    """
    Dynamically swaps context elements to maintain working memory within limits.

    Implements context management for autonomous agents.
    """
    from typing import List, Dict, Any
    import time

    if not isinstance(current_context, list):
        current_context = []
    if not isinstance(new_elements, list):
        new_elements = []

    # Initialize tracking if not present
    for i, elem in enumerate(current_context):
        if isinstance(elem, dict):
            if 'last_accessed' not in elem:
                elem['last_accessed'] = time.time()
            if 'access_count' not in elem:
                elem['access_count'] = 1
        else:
            # Convert to dict for tracking
            current_context[i] = {
                'content': elem,
                'last_accessed': time.time(),
                'access_count': 1
            }

    # Add new elements with tracking
    added_elements = []
    for elem in new_elements:
        if isinstance(elem, dict):
            elem['last_accessed'] = time.time()
            elem['access_count'] = 1
            added_elements.append(elem)
        else:
            new_elem = {
                'content': elem,
                'last_accessed': time.time(),
                'access_count': 1
            }
            added_elements.append(new_elem)

    # Combine current and new
    combined = current_context + added_elements

    # If within limits, return everything
    if len(combined) <= max_elements:
        return {
            'new_context': combined,
            'removed_elements': [],
            'added_elements': added_elements,
            'swap_reason': {'decision': 'no_swap_needed', 'reason': 'Within limits'}
        }

    # Apply swapping strategy
    removed_elements = []
    swap_reason = {}

    if strategy == 'fifo':
        # First-In-First-Out: remove oldest by addition time
        # We don't have addition time, so use last_accessed as proxy
        combined.sort(key=lambda x: x.get('last_accessed', 0))
        removed_elements = combined[:-max_elements]
        new_context = combined[-max_elements:]
        swap_reason = {
            'decision': 'fifo',
            'removed_count': len(removed_elements),
            'criteria': 'oldest_accessed_first'
        }

    elif strategy == 'lru':
        # Least Recently Used: remove elements with oldest last_accessed
        combined.sort(key=lambda x: x.get('last_accessed', 0))
        removed_elements = combined[:-max_elements]
        new_context = combined[-max_elements:]
        swap_reason = {
            'decision': 'lru',
            'removed_count': len(removed_elements),
            'criteria': 'least_recently_used'
        }

    elif strategy == 'relevance':
        # Remove elements with lowest access count
        # Simple relevance heuristic
        for elem in combined:
            # Calculate simple relevance score
            elem['relevance_score'] = elem.get('access_count', 1) * 0.7 +                                      (time.time() - elem.get('last_accessed', 0)) / 3600 * 0.3

        combined.sort(key=lambda x: x.get('relevance_score', 0))
        removed_elements = combined[:-max_elements]
        new_context = combined[-max_elements:]
        swap_reason = {
            'decision': 'relevance',
            'removed_count': len(removed_elements),
            'criteria': 'lowest_relevance_score'
        }

    else:  # 'hybrid'
        # Hybrid strategy: balance recency, frequency, and content type
        for elem in combined:
            # Calculate hybrid score
            recency = 1.0 / (1.0 + (time.time() - elem.get('last_accessed', 0)) / 60)  # minutes
            frequency = min(elem.get('access_count', 1) / 10, 1.0)  # normalized

            # Content type bonus (heuristic)
            content_type_bonus = 0.0
            content = str(elem.get('content', ''))
            if any(keyword in content.lower() for keyword in ['error', 'critical', 'important']):
                content_type_bonus = 0.3
            elif any(keyword in content.lower() for keyword in ['result', 'output', 'success']):
                content_type_bonus = 0.2

            elem['hybrid_score'] = recency * 0.4 + frequency * 0.4 + content_type_bonus * 0.2

        combined.sort(key=lambda x: x.get('hybrid_score', 0))
        removed_elements = combined[:-max_elements]
        new_context = combined[-max_elements:]
        swap_reason = {
            'decision': 'hybrid',
            'removed_count': len(removed_elements),
            'criteria': 'lowest_hybrid_score',
            'score_components': ['recency(0.4)', 'frequency(0.4)', 'content_type(0.2)']
        }

    # Clean up tracking fields from removed elements for output
    cleaned_removed = []
    for elem in removed_elements:
        if 'content' in elem:
            cleaned_removed.append(elem['content'])
        else:
            # Remove tracking fields
            cleaned_elem = {k: v for k, v in elem.items() 
                           if k not in ['last_accessed', 'access_count', 'relevance_score', 'hybrid_score']}
            cleaned_removed.append(cleaned_elem)

    # Clean up tracking fields from new context
    cleaned_context = []
    for elem in new_context:
        if 'content' in elem:
            cleaned_context.append(elem['content'])
        else:
            cleaned_elem = {k: v for k, v in elem.items() 
                           if k not in ['last_accessed', 'access_count', 'relevance_score', 'hybrid_score']}
            cleaned_context.append(cleaned_elem)

    return {
        'new_context': cleaned_context,
        'removed_elements': cleaned_removed,
        'added_elements': added_elements,
        'swap_reason': swap_reason
    }
