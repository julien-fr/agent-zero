import os
import uuid
import base64
from google import genai
from google.genai import types
from python.helpers import tool
from python.helpers.notification import NotificationType

class ImagenGenerate(tool.Tool):
    async def execute(self, prompt, number_of_images=1, aspect_ratio="1:1", model="imagen-4.0-fast-generate-001", output_dir="/a0/tmp/generated_images", display_image=True, **kwargs):
        api_key = os.environ.get("API_KEY_GOOGLE")
        if not api_key:
            return tool.Response(message="Error: API_KEY_GOOGLE environment variable not set.", break_loop=False)

        try:
            # Validate inputs
            valid_ratios = ["1:1", "3:4", "4:3", "16:9", "9:16"]
            if aspect_ratio not in valid_ratios:
                return tool.Response(message=f"Error: Invalid aspect_ratio. Must be one of {valid_ratios}", break_loop=False)

            if not isinstance(number_of_images, int) or not (1 <= number_of_images <= 4):
                 return tool.Response(message="Error: number_of_images must be an integer between 1 and 4", break_loop=False)

            # Initialize client
            client = genai.Client(api_key=api_key)

            # Generate images
            response = client.models.generate_images(
                model=model,
                prompt=prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=number_of_images,
                    aspect_ratio=aspect_ratio
                )
            )

            # Ensure output directory exists
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            saved_files = []

            # Check if response has generated images
            if not hasattr(response, 'generated_images') or not response.generated_images:
                return tool.Response(message=f"Error: No images were returned by the API. Response: {response}", break_loop=False)

            for img in response.generated_images:
                # Generate unique filename
                filename = f"{uuid.uuid4()}.png"
                file_path = os.path.join(output_dir, filename)

                # Save image bytes
                with open(file_path, "wb") as f:
                    f.write(img.image.image_bytes)

                saved_files.append(file_path)

            # Display images if requested
            if display_image and saved_files:
                try:
                    html_content = ""
                    for file_path in saved_files:
                        with open(file_path, "rb") as image_file:
                            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                            html_content += f'<img src="data:image/png;base64,{encoded_string}" style="max-width: 100%; margin-bottom: 10px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /><br/>'

                    self.agent.context.get_notification_manager().add_notification(
                        title="Image Generated",
                        detail=html_content,
                        type=NotificationType.SUCCESS
                    )
                except Exception as notify_error:
                    # Log error but don't fail the tool execution
                    print(f"Failed to display images: {notify_error}")

            return tool.Response(
                message=f"Successfully generated {len(saved_files)} images. Saved to: {', '.join(saved_files)}",
                break_loop=False,
                additional={'saved_files': saved_files}
            )

        except Exception as e:
            return tool.Response(message=f"Error: Image generation failed: {str(e)}", break_loop=False)
