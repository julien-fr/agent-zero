import os
import shutil
import sys
import traceback
from pptxtoimages.tools import PPTXToImageConverter

def visualize(pptx_path, output_dir=None):
    """
    Converts a PPTX file to images for visual inspection.
    
    Args:
        pptx_path (str): Path to the .pptx file.
        output_dir (str, optional): Directory to save images. Defaults to {pptx_dir}/{filename}_visuals.
        
    Returns:
        list: List of absolute paths to the generated images.
    """
    try:
        if not os.path.exists(pptx_path):
            raise FileNotFoundError(f"PPTX file not found: {pptx_path}")
            
        # Determine output directory
        if output_dir is None:
            base_name = os.path.splitext(os.path.basename(pptx_path))[0]
            parent_dir = os.path.dirname(os.path.abspath(pptx_path))
            output_dir = os.path.join(parent_dir, f"{base_name}_visuals")
            
        # Create directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Initialize converter
        # Note: PPTXToImageConverter takes output_dir in __init__
        converter = PPTXToImageConverter(pptx_path, output_dir=output_dir)
        
        # Run conversion
        # Note: convert() returns a list of image paths
        images = converter.convert()
        
        # Ensure paths are absolute
        abs_images = [os.path.abspath(img) for img in images]
        return sorted(abs_images)
        
    except Exception as e:
        print(f"Error visualizing presentation: {e}")
        traceback.print_exc()
        return []

if __name__ == "__main__":
    # CLI for testing
    if len(sys.argv) < 2:
        print("Usage: python ppt_visualize.py <pptx_path> [output_dir]")
        sys.exit(1)
        
    pptx_file = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = visualize(pptx_file, out_dir)
    if result:
        print("Visualization successful. Images generated:")
        for img in result:
            print(img)
    else:
        print("Visualization failed.")
        sys.exit(1)
