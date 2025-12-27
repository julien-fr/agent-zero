"""
Tool for summarizing memory context to manage token limits.

This tool compresses memory entries using various strategies to fit within
context window limits while preserving key information.
"""

import re
from typing import List, Dict, Any, Optional


def summarize_mem_context(
    original_texts: List[str],
    max_tokens: int = 1000,
    strategy: str = 'key_points'
) -> Dict[str, Any]:
    """
    Summarize memory context to fit within token limits.
    
    Args:
        original_texts: List of original memory text entries
        max_tokens: Maximum tokens for the summary (approximate)
        strategy: Summarization strategy ('key_points', 'extractive', 'abstractive')
        
    Returns:
        Dictionary with summary, compression ratio, and metadata
    """
    
    if not original_texts:
        return {
            'original_count': 0,
            'original_tokens': 0,
            'summary_tokens': 0,
            'compression_ratio': 1.0,
            'summary': '',
            'strategy': strategy
        }
    
    # Simple token estimation (approximate)
    def estimate_tokens(text: str) -> int:
        # Rough approximation: 1 token ≈ 4 characters for English
        return len(text) // 4
    
    original_tokens = sum(estimate_tokens(text) for text in original_texts)
    
    if original_tokens <= max_tokens:
        # No compression needed
        return {
            'original_count': len(original_texts),
            'original_tokens': original_tokens,
            'summary_tokens': original_tokens,
            'compression_ratio': 1.0,
            'summary': '\n'.join(original_texts),
            'strategy': 'none'
        }
    
    summary = ''
    
    if strategy == 'key_points':
        # Extract key points from each entry
        key_points = []
        for i, text in enumerate(original_texts[:5]):  # Limit to first 5 entries
            # Simple heuristic: lines with important keywords
            lines = text.split('\n')
            for line in lines:
                line_lower = line.lower()
                if any(keyword in line_lower for keyword in ['important', 'key', 'critical', 'must', 'should', 'note', 'warning']):
                    key_points.append(f'Entry {i+1}: {line.strip()}')
                elif len(line.strip()) > 50 and len(line.strip()) < 200:  # Medium length lines
                    key_points.append(f'Entry {i+1}: {line.strip()[:100]}...')
        
        # Add entry count summary
        if len(original_texts) > 5:
            key_points.append(f'... and {len(original_texts) - 5} more entries')
        
        summary = '\n'.join(key_points[:20])  # Limit to 20 key points
        
    elif strategy == 'extractive':
        # Simple extractive summarization: take first sentences
        summary_parts = []
        for i, text in enumerate(original_texts[:10]):  # Limit to first 10 entries
            sentences = re.split(r'[.!?]+', text)
            if sentences:
                summary_parts.append(f'[{i+1}] {sentences[0].strip()}')
        
        if len(original_texts) > 10:
            summary_parts.append(f'... truncated from {len(original_texts)} entries')
        
        summary = '\n'.join(summary_parts)
        
    elif strategy == 'abstractive':
        # Simulated abstractive summarization
        word_count = sum(len(text.split()) for text in original_texts[:3])
        entry_count = len(original_texts)
        
        summary = f'Summary of {entry_count} memory entries:\n'
        summary += f'- Total approximate words: {word_count}\n'
        summary += f'- Topics covered: {min(5, entry_count)} key topics\n'
        summary += f'- Time range: Recent entries prioritized\n'
        summary += f'- Compression: {original_tokens // max_tokens}:1 ratio'
    
    else:
        # Default strategy
        summary = f'Memory context: {len(original_texts)} entries, ~{original_tokens} tokens\n'
        summary += f'First entry: {original_texts[0][:100]}...' if original_texts else ''
    
    summary_tokens = estimate_tokens(summary)
    
    return {
        'original_count': len(original_texts),
        'original_tokens': original_tokens,
        'summary_tokens': summary_tokens,
        'compression_ratio': original_tokens / max(1, summary_tokens),
        'summary': summary,
        'strategy': strategy
    }


if __name__ == "__main__":
    # Test the function
    test_memories = [
        "This is a very long and detailed report about system performance metrics.",
        "Another document with important information about database optimization.",
        "Critical warning: The system is approaching memory limits."
    ]
    
    result = summarize_mem_context(test_memories, max_tokens=50)
    print(f"Original: {result['original_count']} entries, {result['original_tokens']} tokens")
    print(f"Summary: {result['summary_tokens']} tokens, ratio: {result['compression_ratio']:.2f}")
    print(f"Strategy: {result['strategy']}")
    print(f"Summary:\n{result['summary']}")
