import asyncio
from playwright.async_api import async_playwright

async def test_launch():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    try:
        async with async_playwright() as p:
            context = await p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                channel="chrome",
                headless=True,
                args=[
                    "--profile-directory=Profile 42",
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox"
                ]
            )
            print("Successfully launched persistent context on Profile 42!")
            page = await context.new_page()
            await page.goto("https://www.tiktok.com", timeout=15000)
            title = await page.title()
            print(f"Page title: {title}")
            await context.close()
    except Exception as e:
        print(f"Error launching: {e}")

asyncio.run(test_launch())
