import asyncio
from playwright.async_api import async_playwright
import json

async def capture_search_api():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            channel="chrome",
            headless=False,
            args=[
                "--profile-directory=Profile 42",
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ],
            viewport={"width": 1280, "height": 900}
        )
        page = await context.new_page()
        
        captured = []
        async def handle_response(response):
            url = response.url
            if any(k in url for k in ['search', 'feed', 'item_list', 'recommend', 'review', 'product']):
                try:
                    ct = response.headers.get('content-type', '')
                    if 'application/json' in ct:
                        data = await response.json()
                        captured.append({'url': url, 'data': data})
                        print(f"Captured: {url[:80]}")
                except:
                    pass
                    
        page.on('response', handle_response)
        
        print("Navigating to TikTok search...")
        await page.goto("https://www.tiktok.com/search?q=kit%20praia%20mor", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(4000)
        
        # Scroll down to trigger results loading
        await page.evaluate("window.scrollBy(0, 800)")
        await page.wait_for_timeout(3000)
        
        with open("tiktok_search_captured.json", "w", encoding="utf-8") as f:
            json.dump(captured, f, indent=2, ensure_ascii=False)
            
        print(f"Total API responses captured: {len(captured)}")
        await context.close()

if __name__ == "__main__":
    asyncio.run(capture_search_api())
