
import argparse
import json
import sys
import os
from .models import PresentationModel
from .renderer import PresentationRenderer

def main():
    parser = argparse.ArgumentParser(description="Generate PowerPoint from JSON")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("output_file", help="Path to the output PPTX file")

    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Validate data
        presentation_data = PresentationModel(**data)

        # Render presentation
        renderer = PresentationRenderer(presentation_data)
        renderer.render(args.output_file)

        abs_path = os.path.abspath(args.output_file)
        print(f"Successfully generated presentation at: {abs_path}")

    except FileNotFoundError:
        print(f"Error: Input file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{args.input_file}'.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
