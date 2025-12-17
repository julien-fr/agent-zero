import asyncio
import os
import sys
import time
import importlib
from typing import Any, Dict, List, Optional

# Ensure the correct path for imports
sys.path.insert(0, '/a0')

from python.helpers.tool import Tool, Response

# Check for google-genai library
try:
    import google.genai as genai
    GOOGLE_GENAI_AVAILABLE = True
except ImportError:
    GOOGLE_GENAI_AVAILABLE = False

class DeepResearchTool(Tool):
    """
    Perform deep research using Google Gemini Deep Research API.
    """

    def _ensure_google_genai(self) -> bool:
        """Ensure google.genai is available."""
        if GOOGLE_GENAI_AVAILABLE:
            return True
        
        self.set_progress("[DeepResearch] google-genai not found. Please install it: pip install google-genai")
        return False

    async def execute(self, **kwargs) -> Response:
        """
        Execute deep research with the given query and parameters.
        
        Required argument:
            query (str): The research question or topic.
        
        Optional arguments:
            background (bool, default True): Whether to run research in background (asynchronous).
            stream (bool, default False): Whether to stream results in real-time.
            tools (list, optional): Additional tools like file search.
            format (str, optional): Instructions for output formatting.
            previous_interaction_id (str, optional): For follow-up questions.
            agent_config (dict, optional): Configuration for the agent.
        """
        # Aggressively unload google.genai to ensure latest version is used
        if GOOGLE_GENAI_AVAILABLE:
            try:
                modules_to_unload = [m for m in sys.modules if m.startswith("google.genai")]
                for m in modules_to_unload:
                    del sys.modules[m]
                import google.genai as genai
                self.set_progress(f"Reloaded google.genai. Version: {genai.__version__}")
            except Exception as e:
                self.set_progress(f"Warning: Could not reload google.genai: {e}")

        if not self._ensure_google_genai():
            return Response(
                message="Error: google-genai package is required. Please install it.",
                break_loop=False
            )

        # Get API key from environment
        api_key = os.environ.get("API_KEY_GOOGLE")
        if not api_key:
            return Response(
                message="Error: API_KEY_GOOGLE environment variable is not set",
                break_loop=False
            )
        
        try:
            client = genai.Client(api_key=api_key)
        except Exception as e:
            return Response(
                message=f"Error creating Google GenAI client: {str(e)}",
                break_loop=False
            )
            
        if not hasattr(client, 'interactions'):
             return Response(
                message=f"Error: client has no 'interactions' attribute. \nClient dir: {dir(client)} \nModule: {genai.__file__} \nVersion: {genai.__version__}",
                break_loop=False
            )

        # Check for polling request
        poll_id = kwargs.get("poll_id")
        if poll_id:
            return await self._check_status(client, poll_id)

        # Extract parameters
        query = kwargs.get("query")
        if not query:
            return Response(
                message="Error: 'query' argument is required",
                break_loop=False
            )
        
        background = kwargs.get("background", True)
        stream = kwargs.get("stream", False)
        tools = kwargs.get("tools")
        format_instructions = kwargs.get("format")
        previous_interaction_id = kwargs.get("previous_interaction_id")
        agent_config = kwargs.get("agent_config", {"type": "deep-research", "thinking_summaries": "auto"})
        
        # Build input with optional formatting instructions
        input_text = query
        if format_instructions:
            input_text = f"{format_instructions}\n\n{query}"
        
        try:
            # Prepare interaction parameters
            interaction_params = {
                "input": input_text,
                "agent": "deep-research-pro-preview-12-2025",
                "background": background,
                "agent_config": agent_config
            }
            
            if tools:
                interaction_params["tools"] = tools
            
            if previous_interaction_id:
                interaction_params["previous_interaction_id"] = previous_interaction_id
            
            self.set_progress("Starting deep research...")
            
            detach = kwargs.get("detach", False)

            if stream and not detach:
                interaction_params["stream"] = True
                return await self._handle_streaming(client, interaction_params)
            else:
                interaction = client.interactions.create(**interaction_params)
                interaction_id = interaction.id
                
                if detach:
                    return Response(
                        message=f"Research started in background. ID: {interaction_id}",
                        break_loop=False,
                        additional={"interaction_id": interaction_id}
                    )

                self.set_progress(f"Research started. ID: {interaction_id}")
                return await self._poll_for_completion(client, interaction_id)
            
        except Exception as e:
            return Response(
                message=f"Error in deep research: {str(e)}",
                break_loop=False
            )
    
    async def _check_status(self, client: Any, interaction_id: str) -> Response:
        """Check status of an existing interaction."""
        try:
            interaction = client.interactions.get(id=interaction_id)
            status = interaction.status
            
            if status == "completed":
                output_text = "No output text available."
                if interaction.outputs and len(interaction.outputs) > 0:
                    output_text = interaction.outputs[-1].text
                
                return Response(
                    message=output_text,
                    break_loop=False,
                    additional={"interaction_id": interaction_id, "status": "completed"}
                )
            elif status == "failed":
                error_msg = getattr(interaction, "error", "Unknown error")
                return Response(
                    message=f"Research failed: {error_msg}",
                    break_loop=False,
                    additional={"interaction_id": interaction_id, "status": "failed"}
                )
            
            return Response(
                message=f"Research in progress. Status: {status}",
                break_loop=False,
                additional={"interaction_id": interaction_id, "status": status}
            )
        except Exception as e:
            return Response(
                message=f"Error checking status: {str(e)}",
                break_loop=False
            )

    async def _handle_streaming(self, client: Any, interaction_params: Dict) -> Response:
        """Handle streaming research events."""
        try:
            stream = client.interactions.create(**interaction_params)
            interaction_id = None
            stream_messages = []
            
            for chunk in stream:
                if chunk.event_type == "interaction.start":
                    interaction_id = chunk.interaction.id
                    self.set_progress(f"Interaction started: {interaction_id}")
                
                if chunk.event_type == "content.delta":
                    if chunk.delta.type == "text":
                        stream_messages.append(chunk.delta.text)
                        self.add_progress(chunk.delta.text)
                    elif chunk.delta.type == "thought_summary":
                        thought_text = chunk.delta.content.text
                        stream_messages.append(f"\nThought: {thought_text}\n")
                        self.add_progress(f"Thought: {thought_text}")
                
                elif chunk.event_type == "interaction.complete":
                    self.set_progress("Research completed.")
                    break
                elif chunk.event_type == "error":
                    return Response(
                        message=f"Streaming error: {chunk.error}",
                        break_loop=False
                    )
            
            full_result = "".join(stream_messages)
            return Response(
                message=full_result,
                break_loop=False,
                additional={"interaction_id": interaction_id}
            )
        except Exception as e:
            return Response(
                message=f"Error during streaming: {str(e)}",
                break_loop=False
            )
    
    async def _poll_for_completion(self, client: Any, interaction_id: str) -> Response:
        """Poll for completion of background research."""
        max_poll_attempts = 120  # 20 minutes
        poll_interval = 10  # seconds
        
        for attempt in range(max_poll_attempts):
            try:
                interaction = client.interactions.get(id=interaction_id)
                status = interaction.status
                
                if status == "completed":
                    output_text = "No output text available."
                    if interaction.outputs and len(interaction.outputs) > 0:
                        output_text = interaction.outputs[-1].text
                    
                    return Response(
                        message=output_text,
                        break_loop=False,
                        additional={"interaction_id": interaction_id}
                    )
                elif status == "failed":
                    error_msg = getattr(interaction, "error", "Unknown error")
                    return Response(
                        message=f"Research failed: {error_msg}",
                        break_loop=False
                    )
                
                self.set_progress(f"Research in progress... ({status})")
                await asyncio.sleep(poll_interval)
            except Exception as e:
                self.set_progress(f"Polling error: {e}")
                await asyncio.sleep(poll_interval)
        
        return Response(
            message="Research timed out.",
            break_loop=False
        )
