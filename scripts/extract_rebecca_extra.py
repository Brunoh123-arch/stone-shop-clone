# -*- coding: utf-8 -*-
import asyncio
import json
import os
from playwright.async_api import async_playwright

async def search_rebecca():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    output_file = "scripts/data/rebecca_extra_extracted.json"
    
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
        
        captured_items = []
        async def handle_response(response):
            url = response.url
            if 'item_list' in url or 'search/general' in url or 'search/item' in url:
                try:
                    ct = response.headers.get('content-type', '')
                    if 'application/json' in ct:
                        data = await response.json()
                        items = []
                        if 'data' in data and isinstance(data['data'], list):
                            for d in data['data']:
                                if 'item' in d:
                                    items.append(d['item'])
                        elif 'item_list' in data and isinstance(data['item_list'], list):
                            items = data['item_list']
                        
                        for it in items:
                            author = it.get('author', {})
                            desc = it.get('desc', '')
                            video = it.get('video', {})
                            # Filtro estrito: Rebecca Bonbon
                            txt = desc.lower()
                            if 'rebecca' in txt or 'bonbon' in txt:
                                captured_items.append({
                                    'username': author.get('uniqueId', ''),
                                    'nickname': author.get('nickname', ''),
                                    'avatar': author.get('avatarThumb', '') or author.get('avatarLarger', ''),
                                    'desc': desc,
                                    'playAddr': video.get('playAddr', ''),
                                    'cover': video.get('cover', ''),
                                    'duration': video.get('duration', 0)
                                })
                                print(f"  [+] Capturado Rebecca: @{author.get('uniqueId')} - {desc[:60]}...")
                except Exception as e:
                    pass

        page.on('response', handle_response)
        
        search_url = "https://www.tiktok.com/search?q=mochila%20rebecca%20bonbon%20unboxing"
        print(f"[*] Navegando para {search_url}...")
        try:
            await page.goto(search_url, wait_until='networkidle', timeout=30000)
        except:
            pass
        
        await asyncio.sleep(4)
        for scroll_idx in range(4):
            print(f"[*] Rolando scroll ({scroll_idx+1}/4)...")
            await page.evaluate("window.scrollBy(0, 1000)")
            await asyncio.sleep(3)
            
        print(f"[*] Total capturados: {len(captured_items)}")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(captured_items, f, ensure_ascii=False, indent=2)
            
        await context.close()

if __name__ == '__main__':
    asyncio.run(search_rebecca())
