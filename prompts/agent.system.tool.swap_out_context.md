# Tool: swap_out_context

## Purpose
Dynamically swaps context elements to maintain working memory within limits.
Implements context management techniques from the reliability engineering framework.

## When to Use
- When managing large context windows
- For implementing memory rotation strategies
- When incorporating new information while preserving limits
- During long conversations or tasks

## How to Use
1. Provide current context elements
2. Provide new elements to incorporate
3. Set maximum elements to maintain (default: 10)
4. Choose swapping strategy:
   - `fifo`: First-In-First-Out
   - `lru`: Least Recently Used
   - `relevance`: Based on relevance scores
   - `hybrid`: Balanced approach (default)

## Expected Output
A dictionary with:
- `new_context`: Updated context after swapping
- `removed_elements`: Elements removed from context
- `added_elements`: Elements added to context
- `swap_reason`: Reason for each swap decision

## Integration Guidelines
- Integrate into the agent's memory management system
- Monitor swap effectiveness
- Adjust strategies based on task requirements
- Log swap decisions for analysis

## Example Usage
```python
current_context = ["item1", "item2", "item3"]
new_elements = ["item4", "item5"]
result = swap_out_context(current_context, new_elements, max_elements=4, strategy='hybrid')
print(f"New context: {result['new_context']}")
print(f"Removed: {result['removed_elements']}")
```
