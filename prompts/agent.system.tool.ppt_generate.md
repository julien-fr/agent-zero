### ppt_generate:
Generate a PowerPoint presentation (.pptx) from a JSON structure or file.
This tool uses a structured JSON input to define slides, content, and themes.

#### Arguments
*   json_data (string or dict, required) - The presentation data. Can be a JSON string, a dictionary, or a path to a JSON file.
*   output_file (string, required) - The path where the generated .pptx file will be saved.

#### JSON Structure
The input JSON must follow this structure:
- title (str): Main title of the presentation.
- author (str, optional): Author name.
- theme (str, optional): Theme name (e.g., 'default', 'corporate-blue', 'cyber-dark').
- slides (list): List of slide objects.

**Slide Types**:
1.  **Title**: { "type": "title", "content": "...", "subcontent": "..." }
2.  **Bullet**: { "type": "bullet", "title": "...", "bullets": ["Item 1", "Item 2"] }
3.  **Quote**: { "type": "quote", "text": "...", "author": "..." }
4.  **Image**: { "type": "image", "path": "/path/to/img.png", "title": "...", "caption": "..." }
5.  **Chart**: { "type": "chart", "title": "...", "chart_type": "BAR_CLUSTERED" | "LINE" | "PIE", "categories": [...], "series": [{ "name": "...", "values": [...] }] }

#### Usage
##### 1. Generate from JSON data
~~~
{
    "thoughts": [
        "I need to create a presentation about AI."
    ],
    "headline": "Generating AI presentation",
    "tool_name": "ppt_generate",
    "tool_args": {
        "json_data": {
            "title": "AI Overview",
            "slides": [
                { "type": "title", "content": "Intro to AI" },
                { "type": "bullet", "title": "Key Concepts", "bullets": ["ML", "DL", "NLP"] }
            ]
        },
        "output_file": "/path/to/presentation.pptx"
    }
}
~~~

##### 2. Generate from a JSON file
~~~
{
    "thoughts": [
        "Generating presentation from existing data file."
    ],
    "headline": "Generating presentation from file",
    "tool_name": "ppt_generate",
    "tool_args": {
        "json_data": "/path/to/data.json",
        "output_file": "/path/to/output.pptx"
    }
}
~~~
