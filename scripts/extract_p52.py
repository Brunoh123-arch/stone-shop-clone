# -*- coding: utf-8 -*-
import asyncio
import json
import os
from playwright.async_api import async_playwright

async def run():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    out_file = "scripts/data/extracted_lote3/p52_pad11_tablet_52.json"
    
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
        async def handle_response(response, captured=captured_items):
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
                except Exception as e:
                    pass
        
        page.on('response', handle_response)
        
        queries = ["ipad 11 unboxing brasil", "ipad pro 11 unboxing brasil"]
        for q in queries:
            print(f"[*] Buscando P52: '{q}'")
            search_url = f"https://www.tiktok.com/search?q={q.replace(' ', '%20')}"
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(3000)
                for _ in range(4):
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await page.wait_for_timeout(1500)
            except Exception as ex:
                print(f"[-] Erro na busca: {ex}")
                
        page.remove_listener('response', handle_response)
        
        seen_ids = set()
        unique_items = []
        for item in captured_items:
            v_id = item['id'] or item['playAddr'][:40]
            if v_id not in seen_ids:
                seen_ids.add(v_id)
                unique_items.append(item)
                
        print(f"[*] Total unico capturado para P52: {len(unique_items)}")
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(unique_items, f, indent=2, ensure_ascii=False)
        print(f"[+] Salvo em {out_file}")
        
        await context.close()

if __name__ == '__main__':
    asyncio.run(run())
