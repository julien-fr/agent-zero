import sys
import os
import json

# Ensure we can import the sibling package 'ppt_tool'
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from ppt_tool.models import PresentationModel
    from ppt_tool.renderer import PresentationRenderer
except ImportError as e:
    # Fallback if run from a different context
    try:
        from .ppt_tool.models import PresentationModel
        from .ppt_tool.renderer import PresentationRenderer
    except ImportError:
        raise e

def generate(json_data, output_file):
    """
    Generates a PowerPoint presentation from JSON data.
    
    Args:
        json_data (dict or str): The presentation data structure.
        output_file (str): The path to save the generated .pptx file.
        
    Returns:
        str: The absolute path of the generated file or an error message.
    """
    try:
        # Parse JSON if string
        if isinstance(json_data, str):
            data_dict = json.loads(json_data)
        else:
            data_dict = json_data
            
        # Validate and Create Model
        presentation_data = PresentationModel(**data_dict)

        # Ensure output directory exists
        output_dir = os.path.dirname(os.path.abspath(output_file))
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Render
        renderer = PresentationRenderer(presentation_data)
        renderer.render(output_file)
        
        return os.path.abspath(output_file)

    except Exception as e:
        import traceback
        return f"Error generating presentation: {str(e)}\n{traceback.format_exc()}"

# Simple CLI for testing
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python ppt_generate.py <input_json_file> <output_pptx_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, 'r') as f:
        data = json.load(f)
        
    result = generate(data, output_file)
    print(result)
