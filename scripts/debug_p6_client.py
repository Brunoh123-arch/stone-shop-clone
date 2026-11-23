import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe"
        )
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        
        file_path = os.path.abspath('pages/produto-6.html')
        await page.goto(f'file:///{file_path}', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        cards_data = await page.evaluate("""() => {
            const cards = document.querySelectorAll('.review-card');
            return Array.from(cards).slice(0, 3).map((c, i) => {
                const comment = c.querySelector('.review-comment');
                const contentWrap = c.querySelector('.review-content-wrap');
                return {
                    i,
                    outerHTML: c.outerHTML.substring(0, 500),
                    hasComment: !!comment,
                    commentText: comment ? comment.textContent : 'NULL',
                    commentDisplay: comment ? window.getComputedStyle(comment).display : 'NONE',
                    commentVisibility: comment ? window.getComputedStyle(comment).visibility : 'NONE',
                    commentColor: comment ? window.getComputedStyle(comment).color : 'NONE',
                    contentWrapChildren: contentWrap ? Array.from(contentWrap.children).map(ch => ch.className) : 'NO CONTENT WRAP'
                };
            });
        }""")
        
        import pprint
        pprint.pprint(cards_data)
        
        await browser.close()

asyncio.run(run())
