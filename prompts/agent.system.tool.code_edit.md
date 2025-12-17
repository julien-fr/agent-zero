### code_edit:
A tool for making precise, surgical edits to source code files using SEARCH/REPLACE blocks.
This tool applies changes by matching a block of existing code (SEARCH) and replacing it with new code (REPLACE).
It uses flexible matching that tolerates minor whitespace differences and can handle missing leading whitespace.
This is the same editing mechanism used by AIDER, ensuring reliable and safe code modifications.

**When to use this tool**:
- You need to modify an existing file without rewriting the entire file
- You want to add, remove, or change specific lines of code
- You need to ensure the change is applied exactly where intended
- You are working with large files where a full rewrite would be inefficient
- You need to make multiple independent edits across different files
- You want to avoid introducing formatting changes unrelated to the edit

**Key features**:
- **Surgical precision**: Only the matched block is changed; the rest of the file stays identical
- **Flexible matching**: Handles variations in indentation and whitespace automatically
- **Multiple edits**: Can apply several SEARCH/REPLACE blocks in a single call
- **New file creation**: If SEARCH is empty, the REPLACE block is appended to a new or existing file
- **Error detection**: If SEARCH cannot be matched, the tool returns an error without modifying the file
- **Supports ... lines**: You can use `...` lines to indicate omitted code sections (like AIDER)

**SEARCH/REPLACE block Rules (adapted from AIDER)**:
Every SEARCH/REPLACE block must follow this format:
1. The SEARCH block must *EXACTLY MATCH* the existing file content, character for character, including all comments, docstrings, etc.
2. Include enough lines in the SEARCH section to uniquely match the location you want to change.
3. Keep SEARCH/REPLACE blocks concise. Include just the changing lines, and a few surrounding lines if needed for uniqueness.
4. Do not include long runs of unchanging lines in SEARCH/REPLACE blocks.
5. If you need to move code within a file, use 2 SEARCH/REPLACE blocks: one to delete it from its current location, one to insert it in the new location.
6. To create a new file, use an empty SEARCH block and put the new file's contents in the REPLACE block.
7. The tool automatically strips any filename headers and triple backticks; you can provide the raw SEARCH and REPLACE text.

**Format of SEARCH/REPLACE blocks in AIDER**:
In AIDER, the assistant returns blocks like this:
```
path/to/file.py
```python
<<<<<<< SEARCH
existing lines
=======
new lines
>>>>>>> REPLACE
```
For this tool, you need to extract the `search` and `replace` parts (the content between `<<<<<<< SEARCH` and `=======`, and between `=======` and `>>>>>>> REPLACE`). The filename is already provided in `file_path`. You can omit the triple backticks and language specifier.

**Parameters explained**:
- `file_path`: (required for single edit) Path to the file to edit, relative to the project root.
- `search`: The exact block of code to search for (SEARCH block). If empty, the REPLACE block will be appended.
- `replace`: The new block of code to replace the SEARCH block with (REPLACE block).
- `edits`: (alternative to single edit) A list of edit objects, each containing `file_path`, `search`, `replace`. Use this for multiple edits across files.

**You should**:
0. **When you need to edit a file, you MUST respond with SEARCH/REPLACE blocks** exactly as AIDER does. Provide the `search` and `replace` parameters as described below.
1. **Identify the exact lines** you want to change in the current file.
2. **Copy those lines exactly** (including indentation) into the `search` parameter.
3. **Write the new lines** you want to appear instead, with the same indentation, into the `replace` parameter.
4. **If you need to omit irrelevant lines** within the block, you can use a line containing only `...` (three dots). This works exactly like AIDER's SEARCH/REPLACE blocks.
5. **For new files** or appending to a file, leave `search` empty and provide only `replace`.
6. **When making multiple changes** across different files, use the `edits` list.
7. **Always verify** that the SEARCH block uniquely matches the intended location in the file. If there are multiple identical blocks, the tool will match the first one (or the most similar one).
8. **If the change fails**, check the error message and adjust the SEARCH block to be more specific (e.g., include a few extra lines of context).

**Example usage (single edit)**:
~~~json
{
    "thoughts": [
        "I need to add a new function to utils.py.",
        "I'll locate the existing import section and insert the function after it."
    ],
    "headline": "Add helper function to utils.py",
    "tool_name": "code_edit",
    "tool_args": {
        "file_path": "src/utils.py",
        "search": "import os\nimport sys\n",
        "replace": "import os\nimport sys\nimport json\n\ndef helper():\n    return \"help\"\n"
    }
}
~~~

**Example usage (multiple edits)**:
~~~json
{
    "thoughts": [
        "I need to update two files: config.yaml and main.py."
    ],
    "headline": "Update configuration and main entry point",
    "tool_name": "code_edit",
    "tool_args": {
        "edits": [
            {
                "file_path": "config.yaml",
                "search": "debug: false\n",
                "replace": "debug: true\n"
            },
            {
                "file_path": "main.py",
                "search": "def main():\n    print(\"Hello\")",
                "replace": "def main():\n    print(\"Hello, world!\")"
            }
        ]
    }
}
~~~

**Example with ... lines (omitting intermediate lines)**:
~~~json
{
    "thoughts": [
        "I need to change the middle of a long function without copying the whole function."
    ],
    "headline": "Modify middle of long function",
    "tool_name": "code_edit",
    "tool_args": {
        "file_path": "src/processor.py",
        "search": "def process(data):\n    # step 1\n    clean = data.strip()\n    ...\n    # step 3\n    return result\n",
        "replace": "def process(data):\n    # step 1\n    clean = data.strip()\n    # step 2 (new)\n    validated = validate(clean)\n    ...\n    # step 3\n    return result\n"
    }
}
~~~

**Response format**:
The tool returns a JSON object with:
- `success`: boolean indicating whether all edits were applied successfully
- `message`: human‑readable summary of what happened
- `results`: (for multiple edits) list of individual edit results, each containing:
   - `file_path`: the file edited
   - `success`: boolean
   - `message`: details about that edit

If an edit fails, the tool will not modify any file (atomic behavior for multiple edits is not guaranteed; failures may leave earlier successful edits applied).

**Important notes**:
- The SEARCH/REPLACE blocks should NOT be wrapped in triple backticks or include filenames. The tool automatically strips such wrapping.
- Indentation is preserved; the tool will try to match the SEARCH block even if the leading whitespace differs slightly.
- If the SEARCH block is empty, the REPLACE block is appended to the file (or creates a new file).
- Use this tool for code edits; for other file types (JSON, YAML, text) it works as well, but be careful with exact formatting.
- This tool is designed to be used iteratively: you can make a small edit, see the result, then make another edit.

**When NOT to use this tool**:
- When you need to completely rewrite a file from scratch (use `code_execution_tool` with `cat` or `write_file`).
- When you want to search and replace across many files with a regex (use `search_engine` tool or `code_execution_tool` with `sed`).
- When you are unsure of the exact code to change (first examine the file with `document_query` or `code_execution_tool` with `cat`).