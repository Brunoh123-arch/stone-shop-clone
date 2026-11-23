# -*- coding: utf-8 -*-
import asyncio
import json
import os
from playwright.async_api import async_playwright

async def run_p7():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    output_dir = "scripts/data/extracted_zeros"
    
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
                            video = it.get('video', {})
                            desc = it.get('desc', '')
                            play_addr = video.get('playAddr') or video.get('downloadAddr')
                            if play_addr and author.get('uniqueId'):
                                captured.append({
                                    'username': author.get('uniqueId', ''),
                                    'nickname': author.get('nickname', ''),
                                    'avatar': author.get('avatarThumb', '') or author.get('avatarMedium', ''),
                                    'desc': desc,
                                    'playAddr': play_addr,
                                    'cover': video.get('cover', '') or video.get('originCover', ''),
                                    'id': it.get('id', '')
                                })
                        if items:
                            print(f"[+] P7: {len(items)} itens recebidos (total: {len(captured)})")
                except:
                    pass
        
        page.on('response', handle_response)
        query = "aiwa boombox plus"
        await page.goto(f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}", wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(4000)
        for _ in range(3):
            await page.evaluate("window.scrollBy(0, 1000)")
            await page.wait_for_timeout(2000)
            
        seen = set()
        unique = []
        for it in captured:
            vid = it['id'] or it['playAddr'][:40]
            if vid not in seen:
                seen.add(vid)
                unique.append(it)
                
        print(f"[*] P7 total unico: {len(unique)}")
        with open(os.path.join(output_dir, "p7_aiwa_7.json"), "w", encoding="utf-8") as f:
            json.dump(unique, f, indent=2, ensure_ascii=False)
            
        await context.close()

if __name__ == "__main__":
    asyncio.run(run_p7())
