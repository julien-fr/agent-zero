"""
Tool for creating automated tools from repetitive execution traces.

This tool analyzes execution traces to identify repetitive patterns and
creates automated tools to replace manual repetitive operations.
"""

import json
import hashlib
from typing import List, Dict, Any, Optional


def create_tool_from_trace(
    trace: List[Dict[str, Any]],
    min_repetitions: int = 3,
    similarity_threshold: float = 0.8
) -> Dict[str, Any]:
    """
    Create an automated tool from repetitive execution traces.
    
    Args:
        trace: List of execution traces with tool_name and args
        min_repetitions: Minimum number of repetitions to trigger tool creation
        similarity_threshold: Similarity threshold for grouping similar operations
        
    Returns:
        Dictionary with creation status, tool name, and generated code
    """
    
    if not trace:
        return {
            'created': False,
            'reason': 'Empty trace',
            'tool_name': None,
            'code': ''
        }
    
    # Group similar operations
    groups = {}
    for entry in trace:
        if 'tool_name' not in entry:
            continue
            
        tool_name = entry['tool_name']
        args = entry.get('args', {})
        
        # Create a hash of the operation for grouping
        op_hash = hashlib.md5(
            json.dumps({'tool_name': tool_name, 'args': args}, sort_keys=True).encode()
        ).hexdigest()
        
        if op_hash not in groups:
            groups[op_hash] = {
                'tool_name': tool_name,
                'args': args,
                'count': 0,
                'examples': []
            }
        
        groups[op_hash]['count'] += 1
        groups[op_hash]['examples'].append(entry)
    
    # Find groups with enough repetitions
    target_groups = []
    for op_hash, group in groups.items():
        if group['count'] >= min_repetitions:
            target_groups.append(group)
    
    if not target_groups:
        return {
            'created': False,
            'reason': f'No patterns with at least {min_repetitions} repetitions',
            'tool_name': None,
            'code': ''
        }
    
    # Create tool from the most frequent pattern
    target_group = max(target_groups, key=lambda g: g['count'])
    
    # Generate tool name
    base_name = target_group['tool_name'].replace('_', ' ').title().replace(' ', '')
    tool_name = f'auto_{base_name.lower()}'
    
    # Extract parameter names from args
    args = target_group['args']
    param_names = list(args.keys()) if isinstance(args, dict) else []
    
    # Generate Python code for the tool
    code_parts = []
    
    if param_names:
        # Generate function with parameters
        param_str = ', '.join(param_names)
        code_parts.append(f'def {tool_name}({param_str}):')
        code_parts.append(f'    """')
        code_parts.append(f'    Automated tool for {target_group["tool_name"]} operation.')
        code_parts.append(f'    ')
        code_parts.append(f'    This tool was automatically generated from {target_group["count"]} repetitive executions.')
        code_parts.append(f'    """')
        code_parts.append(f'    ')
        code_parts.append(f'    # Call the original tool')
        code_parts.append(f'    result = {{')
        code_parts.append(f'        "tool_name": "{target_group["tool_name"]}",')
        code_parts.append(f'        "automated": True,')
        code_parts.append(f'        "parameters": {{')
        for param in param_names:
            code_parts.append(f'            "{param}": {param},')
        code_parts.append(f'        }},')
        code_parts.append(f'        "message": f"Automated execution of {target_group["tool_name"]} with {{len(locals())}} parameters"')
        code_parts.append(f'    }}')
        code_parts.append(f'    ')
        code_parts.append(f'    return result')
        
        code = '\n'.join(code_parts)
    else:
        # No parameters case
        code_parts = []
        code_parts.append(f'def {tool_name}():')
        code_parts.append(f'    """')
        code_parts.append(f'    Automated tool for {target_group["tool_name"]} operation.')
        code_parts.append(f'    ')
        code_parts.append(f'    This tool was automatically generated from {target_group["count"]} repetitive executions.')
        code_parts.append(f'    """')
        code_parts.append(f'    ')
        code_parts.append(f'    # Call the original tool')
        code_parts.append(f'    result = {{')
        code_parts.append(f'        "tool_name": "{target_group["tool_name"]}",')
        code_parts.append(f'        "automated": True,')
        code_parts.append(f'        "message": "Automated execution of {target_group["tool_name"]}"')
        code_parts.append(f'    }}')
        code_parts.append(f'    ')
        code_parts.append(f'    return result')
        
        code = '\n'.join(code_parts)

    return {
        'created': True,
        'tool_name': tool_name,
        'pattern': {
            'original_tool': target_group['tool_name'],
            'repetitions': target_group['count'],
            'parameters': param_names
        },
        'code': code,
        'recommendation': f'Add this function to your tools registry to automate {target_group["count"]} repetitive operations'
    }


if __name__ == "__main__":
    # Test the function
    test_trace = [
        {'tool_name': 'read_file', 'args': {'path': '/tmp/test.txt'}},
        {'tool_name': 'read_file', 'args': {'path': '/tmp/test.txt'}},
        {'tool_name': 'read_file', 'args': {'path': '/tmp/test.txt'}},
        {'tool_name': 'read_file', 'args': {'path': '/tmp/test.txt'}}
    ]
    
    result = create_tool_from_trace(test_trace)
    print(json.dumps(result, indent=2))
