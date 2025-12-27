"""Standalone design scout."""
import asyncio
import os
from datetime import datetime
from playwright.async_api import async_playwright

def build_search_url(query: str, platform: str) -> str:
    """Build search URL for given platform and query."""
    query_encoded = query.replace(" ", "+")
    if platform == "dribbble":
        return f"https://dribbble.com/search/{query_encoded}"
    elif platform == "behance":
        return f"https://www.behance.net/search/projects?search={query_encoded}"
    elif platform == "awwwards":
        return f"https://www.awwwards.com/websites/search/?q={query_encoded}"
    else:
        return f"https://example.com"  # fallback

async def capture_screenshot(url: str, output_dir: str = "captures") -> str:
    """Capture a screenshot of the given URL."""
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = os.path.join(output_dir, f"capture_{timestamp}.png")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        await page.goto(url, wait_until="networkidle", timeout=15000)
        await asyncio.sleep(1)
        await page.screenshot(path=screenshot_path, full_page=True)
        await browser.close()
    
    return screenshot_path

async def search_design(query: str, platform: str = "dribbble", max_results: int = 1) -> dict:
    """Search for design inspiration and capture screenshots."""
    print(f"🔍 Searching '{query}' on {platform}")
    url = build_search_url(query, platform)
    print(f"   URL: {url}")
    
    try:
        screenshot = await capture_screenshot(url)
        print(f"   Screenshot saved: {screenshot}")
        return {
            "query": query,
            "platform": platform,
            "screenshot": screenshot,
            "url": url
        }
    except Exception as e:
        print(f"   Error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    import sys
    query = sys.argv[1] if len(sys.argv) > 1 else "dark ui"
    platform = sys.argv[2] if len(sys.argv) > 2 else "dribbble"
    result = asyncio.run(search_design(query, platform))
    print(result)
