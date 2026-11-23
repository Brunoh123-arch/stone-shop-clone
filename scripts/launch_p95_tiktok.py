import asyncio
from playwright.async_api import async_playwright
import shutil
import os

async def test_profile95():
    # Copy Profile 95 to a dedicated Automation Profile so we don't conflict with main Chrome
    auto_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data P95"
    src_profile = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data\Profile 95"
    dst_profile = os.path.join(auto_dir, "Default")
    
    os.makedirs(dst_profile, exist_ok=True)
    
    # Copy essential auth files
    for item in ['Network', 'Cookies', 'Preferences', 'Secure Preferences', 'Local Storage', 'Session Storage', 'IndexedDB']:
        s = os.path.join(src_profile, item)
        d = os.path.join(dst_profile, item)
        if os.path.exists(s):
            if os.path.isdir(s):
                if not os.path.exists(d):
                    shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
                
    # Also copy Local State
    ls_src = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data\Local State"
    ls_dst = os.path.join(auto_dir, "Local State")
    if os.path.exists(ls_src):
        shutil.copy2(ls_src, ls_dst)
        
    print("Copied Profile 95 data to dedicated automation directory.")
    
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir=auto_dir,
            channel="chrome",
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox"
            ],
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        print("Navigating to https://www.tiktok.com...")
        await page.goto("https://www.tiktok.com", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        print("Title:", await page.title())
        
        # Check cookies
        cookies = await context.cookies()
        tt_cookies = [c['name'] for c in cookies if 'tiktok' in c.get('domain', '')]
        print(f"Loaded {len(tt_cookies)} TikTok cookies in session!")
        print("Has sessionid?", 'sessionid' in tt_cookies)
        
        # Now navigate to TikTok Shop PDP for beach kit / chairs
        pdp_url = "https://shop.tiktok.com/br/pdp/kit-4-cadeiras-de-praia-dobraveis-resistentes-110kg/1735375469098468434"
        print(f"Navigating to {pdp_url}...")
        await page.goto(pdp_url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)
        print("PDP Title:", await page.title())
        
        content = await page.content()
        print(f"PDP Content length: {len(content)}")
        if "Security Check" in await page.title():
            print("Still hit Security Check!")
        else:
            print("SUCCESS! Logged-in session bypassed security check!")
            
        await context.close()

if __name__ == "__main__":
    asyncio.run(test_profile95())
