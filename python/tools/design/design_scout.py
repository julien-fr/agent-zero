import os
import asyncio
import tempfile
from datetime import datetime
from typing import Optional

from agent import Agent, UserMessage
from python.helpers.tool import Tool, Response
from python.helpers import files, runtime

class DesignScout(Tool):
    """
    Scout for design inspiration on platforms like Dribbble, Behance, etc.
    Uses Playwright to capture screenshots of search results.
    """
    
    async def execute(self, query: str = "", platform: str = "dribbble", max_results: int = 3, **kwargs):
        """
        Search for design inspiration based on a query.
        
        Args:
            query: Search query (e.g., "dark automotive dashboard")
            platform: One of "dribbble", "behance", "awwwards" (default dribbble)
            max_results: Maximum number of screenshots to capture
            
        Returns:
            Response with list of captured image paths and metadata.
        """
        self.agent.context.log.set_progress(f"DesignScout: Searching '{query}' on {platform}")
        
        # Map platform to URL
        url = self._build_search_url(query, platform)
        if not url:
            return Response(message=f"Platform {platform} not supported yet", break_loop=False)
        
        # Create temporary directory for screenshots
        tmp_dir = files.get_abs_path("tmp/design_scout")
        os.makedirs(tmp_dir, exist_ok=True)
        
        # Use Playwright to capture screenshot
        try:
            from playwright.async_api import async_playwright
            
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.set_viewport_size({"width": 1280, "height": 800})
                
                self.agent.context.log.set_progress(f"Navigating to {url}")
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await asyncio.sleep(2)  # Let page stabilize
                
                # For MVP, just capture the whole page
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_path = os.path.join(tmp_dir, f"{platform}_{timestamp}.png")
                await page.screenshot(path=screenshot_path, full_page=True)
                
                await browser.close()
                
                # Return result
                result = {
                    "query": query,
                    "platform": platform,
                    "screenshot_path": screenshot_path,
                    "message": f"Captured screenshot of {url}"
                }
                return Response(
                    message=f"DesignScout completed: {result['message']}",
                    additional=result,
                    break_loop=False
                )
                
        except Exception as e:
            return Response(message=f"DesignScout error: {e}", break_loop=False)
    
    def _build_search_url(self, query: str, platform: str) -> Optional[str]:
        """Build search URL for given platform and query."""
        query_encoded = query.replace(" ", "+")
        
        if platform == "dribbble":
            return f"https://dribbble.com/search/{query_encoded}"
        elif platform == "behance":
            return f"https://www.behance.net/search/projects?search={query_encoded}"
        elif platform == "awwwards":
            return f"https://www.awwwards.com/websites/search/?q={query_encoded}"
        else:
            return None

