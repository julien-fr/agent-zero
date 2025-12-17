
### ui_ux_architect
Analyze a UI screenshot or URL to generate a professional JSON design blueprint.
Use this tool when the user asks to analyze an interface, reverse engineer a design, or extract UI specs.

**Arguments**:
- `target`: (string, required) The file path to a local image OR a URL (http/https) to capture.
- `instruction`: (string, optional) Specific focus for the analysis (e.g., "Focus on the header", "Check accessibility").

**Usage**:
~~~
{
    "thoughts": [
        "The user wants to analyze this website..."
    ],
    "tool_name": "ui_ux_architect",
    "tool_args": {
        "target": "https://example.com",
        "instruction": "Extract the color palette and layout"
    }
}
~~~
