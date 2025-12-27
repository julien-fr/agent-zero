import os
import base64
import json
from typing import Dict, Any

from python.helpers.tool import Tool, Response
from python.helpers import files, images

class DesignAnalyzer(Tool):
    """
    Analyze a UI screenshot and extract a design system (colors, typography, layout).
    Uses OpenAI GPT-4o Vision for semantic analysis.
    """
    
    async def execute(self, image_path: str = "", instruction: str = "", **kwargs):
        """
        Analyze an image and extract design tokens.
        
        Args:
            image_path: Path to the screenshot image
            instruction: Additional focus (e.g., "Focus on colors and spacing")
            
        Returns:
            Response with extracted design system JSON.
        """
        self.agent.context.log.set_progress(f"DesignAnalyzer: Analyzing {image_path}")
        
        if not os.path.exists(image_path):
            return Response(message=f"Image not found: {image_path}", break_loop=False)
        
        # Encode image to base64
        try:
            with open(image_path, "rb") as f:
                image_data = f.read()
            # Compress to reduce token usage
            compressed = images.compress_image(image_data, max_pixels=768000, quality=75)
            image_b64 = base64.b64encode(compressed).decode("utf-8")
        except Exception as e:
            return Response(message=f"Error reading image: {e}", break_loop=False)
        
        # Prepare prompt
        system_prompt = """You are a senior UI/UX designer. Analyze the provided screenshot of a user interface.
Extract a complete design system in JSON format with the following structure:
{
  "theme_name": "Descriptive name",
  "palette": {
    "primary": "#hex",
    "secondary": "#hex",
    "background": "#hex",
    "surface": "#hex",
    "text_primary": "#hex",
    "text_secondary": "#hex",
    "accent": "#hex"
  },
  "typography": {
    "font_family_heading": "Font name",
    "font_family_body": "Font name",
    "font_size_base": "16px",
    "line_height": "1.5",
    "scale_ratio": 1.25
  },
  "layout": {
    "border_radius_base": "8px",
    "spacing_base": "4px",
    "container_width": "1200px",
    "grid_columns": 12
  },
  "components": {
    "buttons": {
      "primary": {"background": "#hex", "text": "#hex", "border_radius": "px"},
      "secondary": {"background": "#hex", "text": "#hex", "border_radius": "px"}
    },
    "cards": {
      "background": "#hex", "padding": "px", "border_radius": "px"
    }
  },
  "observations": ["List of key visual characteristics"]
}

Provide ONLY valid JSON. No additional text."""
        
        user_prompt = f"Analyze this UI screenshot and extract the design system."
        if instruction:
            user_prompt += f"\nFocus: {instruction}"
        
        # Call OpenAI API
        try:
            import openai
            
            client = openai.OpenAI(api_key=os.environ.get("API_KEY_OPENAI"))
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
                    ]}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content
            
            # Parse JSON from response
            # Sometimes the response includes markdown code blocks
            import re
            json_match = re.search(r'```json\n(.*?)\n```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            else:
                # Try to find JSON object directly
                json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
                if json_match:
                    result_text = json_match.group(0)
            
            design_system = json.loads(result_text)
            
            return Response(
                message="Design analysis completed successfully",
                additional={
                    "design_system": design_system,
                    "raw_response": result_text
                },
                break_loop=False
            )
            
        except json.JSONDecodeError as e:
            return Response(message=f"Failed to parse JSON from model: {e}\nResponse: {result_text}", break_loop=False)
        except Exception as e:
            return Response(message=f"OpenAI API error: {e}", break_loop=False)

