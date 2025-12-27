import sys
sys.path.insert(0, '/a0/python/tools')

tools = [
    'detect_repetition_pattern',
    'generate_playbook',
    'create_tool_from_trace',
    'swap_out_context',
    'reflexive_critique',
    'summarize_mem_context'
]

for tool in tools:
    try:
        __import__(tool)
        print(f'✅ {tool} imported successfully')
    except Exception as e:
        print(f'❌ {tool} import failed: {e}')
