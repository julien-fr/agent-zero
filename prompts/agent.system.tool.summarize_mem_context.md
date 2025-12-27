# Tool: summarize_mem_context

## Purpose
Tool for summarizing memory context to manage token limits.

This tool compresses memory entries using various strategies to fit within
context window limits while preserving key information.

## When to Use
- When memory context exceeds token limits
- For optimizing agent performance by reducing context size
- During long conversations where memory needs compression
- As part of memory management and optimization routines

## How to Use
1. Provide original memory texts (list of strings)
2. Set maximum token limit (default: 1000)
3. Choose summarization strategy:
   - 'key_points': Extract key points only
   - 'extractive': Select most important sentences
   - 'abstractive': Generate abstract summary (requires LLM)
4. Call the function to get summarized context

## Expected Output
A dictionary with:
- `summary`: The summarized text
- `compression_ratio`: Ratio of original to summary size
- `original_count`: Number of original entries
- `strategy_used`: Which strategy was applied
- `metadata`: Additional information about the summarization

## Integration Guidelines
- Use before memory context becomes too large
- Combine with memory_load for efficient retrieval
- Monitor compression ratios for quality control
- Adjust strategies based on content type

## Example Usage
python
original_texts = [
    "Long memory entry 1 with detailed information...",
    "Long memory entry 2 with more details..."
]
result = summarize_mem_context(original_texts, max_tokens=500, strategy='key_points')
print(f"Summary: {result['summary']}")
print(f"Compression ratio: {result['compression_ratio']}")
