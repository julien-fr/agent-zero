### ppt_visualize:
Convert a PowerPoint presentation (.pptx) into a series of images (PNG) for visual inspection.
Use this tool to verify the layout, design, and content of a generated presentation.

#### Arguments
* `pptx_path` (string, required) - The absolute path to the .pptx file to visualize.
* `output_dir` (string, optional) - The directory where images will be saved. If omitted, a folder named `{filename}_visuals` will be created next to the pptx file.

#### Usage
##### 1. Visualize a presentation
~~~
{
    "thoughts": [
        "I need to check if the generated slides look correct."
    ],
    "headline": "Visualizing generated presentation",
    "tool_name": "ppt_visualize",
    "tool_args": {
        "pptx_path": "/path/to/presentation.pptx"
    }
}
~~~
