
import os
import base64
import asyncio
from mimetypes import guess_type
from playwright.async_api import async_playwright

from agent import Agent, UserMessage
from initialize import initialize_agent
from python.helpers.tool import Tool, Response
from python.helpers import files, images, runtime, history
from python.tools.imagen_generate import ImagenGenerate

class UiUxArchitect(Tool):
    async def execute(self, target: str = "", instruction: str = "", generate_prompt: str = "", **kwargs):

        # 1. Acquire Image
        image_path = target
        temp_file = False

        # If generate_prompt is provided, generate an image first
        if generate_prompt:
            self.agent.context.log.set_progress(f"Generating image from prompt: {generate_prompt}")
            image_path = files.get_abs_path(f"tmp/ui_ux_generated_{self.agent.context.generate_id()}.png")
            temp_file = True

            # Use imagen_generate tool via the agent's tool execution
            try:
                # Prepare tool arguments
                tool_args = {
                    "prompt": generate_prompt,
                    "number_of_images": 1,
                    "aspect_ratio": "1:1",
                    "model": "imagen-4.0-fast-generate-001",
                    "output_dir": "/a0/tmp/generated_images",
                    "display_image": False
                }
                # Execute the tool using the agent's context tool manager
                from python.helpers.tool import Response as ToolResponse
                from python.tools.imagen_generate import ImagenGenerate
                # Create a proper Tool instance with required parameters
                imagen_tool = ImagenGenerate(
                    agent=self.agent,
                    name="imagen_generate",
                    method=None,
                    args=tool_args,
                    message="",
                    loop_data=None
                )
                result = await imagen_tool.execute(**tool_args)
                # The result's additional dict contains saved_files list
                saved_files = result.additional.get("saved_files", [])
                if not saved_files:
                    return Response(message="Image generation failed: no file saved", break_loop=False)
                # Move the generated file to our desired location
                import shutil
                shutil.move(saved_files[0], image_path)
            except Exception as e:
                return Response(message=f"Error generating image: {e}", break_loop=False)

        elif target.startswith("http://") or target.startswith("https://"):
            self.agent.context.log.set_progress(f"Capturing screenshot of {target}...")
            image_path = files.get_abs_path(f"tmp/ui_ux_{self.agent.context.generate_id()}.png")
            temp_file = True

            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True, executable_path="/root/.cache/ms-playwright/chromium-1200/chrome-linux64/chrome")
                    page = await browser.new_page()
                    await page.set_viewport_size({"width": 1280, "height": 800})
                    await page.goto(target, wait_until="networkidle", timeout=60000)
                    await asyncio.sleep(2) # Stabilize
                    await page.screenshot(path=image_path, full_page=True)
                    await browser.close()
            except Exception as e:
                return Response(message=f"Error capturing URL: {e}", break_loop=False)

        if not os.path.exists(image_path):
            return Response(message=f"Error: Image file not found at {image_path}", break_loop=False)

        # 2. Prepare Subordinate Agent
        self.agent.context.log.set_progress("Initializing UI/UX Expert Agent...")

        # Initialize config with specific profile
        config = initialize_agent()
        config.profile = "ui_ux_architect"

        # Create subordinate
        sub = Agent(self.agent.number + 1, config, self.agent.context)
        sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)

        # 3. Inject Image (VisionLoad logic)
        try:
            file_content = await runtime.call_development_function(files.read_file_base64, image_path)
            file_content = base64.b64decode(file_content)
            compressed = images.compress_image(file_content, max_pixels=768000, quality=75)
            file_content_b64 = base64.b64encode(compressed).decode("utf-8")

            content = [{
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{file_content_b64}"}
            }]

            msg = history.RawMessage(raw_content=content, preview="<UI Screenshot>")
            sub.hist_add_message(False, content=msg, tokens=1500)

        except Exception as e:
            return Response(message=f"Error processing image: {e}", break_loop=False)

        # 4. Execute Analysis
        user_msg = "Analyze this UI and generate the design blueprint."
        if instruction:
            user_msg += f"\nFocus: {instruction}"

        sub.hist_add_user_message(UserMessage(message=user_msg, attachments=[]))

        self.agent.context.log.set_progress("Running analysis (this may take a moment)...")
        result = await sub.monologue()

        # Cleanup temp file
        if temp_file and os.path.exists(image_path):
            os.remove(image_path)

        return Response(message=result, break_loop=False)
