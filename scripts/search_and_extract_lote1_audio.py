# -*- coding: utf-8 -*-
"""
Script de busca e captura automatizada via TikTok Web no Profile 42 (Max Digital)
para o Lote 1 de Áudio: P57, P58, P60, P61, P73 e P85.
"""
import asyncio
import json
import os
from playwright.async_api import async_playwright

SEARCH_TARGETS = [
    {"prodId": 57, "slug": "joog_one_57", "query": "caixa de som joog one 200w"},
    {"prodId": 58, "slug": "echo_dot_58", "query": "echo dot 5 geracao alexa unboxing"},
    {"prodId": 60, "slug": "sabala_60", "query": "caixa som sabala dr 908"},
    {"prodId": 61, "slug": "joog_break_61", "query": "caixa de som joog break x1"},
    {"prodId": 73, "slug": "waaw_73", "query": "caixa waaw hyperboom 1000"},
    {"prodId": 85, "slug": "joog_x2_85", "query": "caixa joog x2 karaoke"}
]

async def run_extractions():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    output_dir = "scripts/data/extracted_lote1"
    os.makedirs(output_dir, exist_ok=True)
    
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
        
        for target in SEARCH_TARGETS:
            prod_id = target["prodId"]
            query = target["query"]
            slug = target["slug"]
            print(f"\n==========================================")
            print(f"[*] Buscando para P{prod_id} ({slug}): '{query}'")
            print(f"==========================================")
            
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
                            if items:
                                print(f"    [+] Capturados {len(items)} itens (acumulado: {len(captured)})")
                    except Exception as e:
                        pass
            
            page.on('response', handle_response)
            
            search_url = f"https://www.tiktok.com/search?q={query.replace(' ', '%20')}"
            try:
                await page.goto(search_url, wait_until="domcontentloaded", timeout=30000)
                await page.wait_for_timeout(4000)
                for _ in range(3):
                    await page.evaluate("window.scrollBy(0, 1000)")
                    await page.wait_for_timeout(2000)
            except Exception as ex:
                print(f"[-] Erro na busca P{prod_id}: {ex}")
                
            page.remove_listener('response', handle_response)
            
            seen_ids = set()
            unique_items = []
            for item in captured_items:
                v_id = item['id'] or item['playAddr'][:40]
                if v_id not in seen_ids:
                    seen_ids.add(v_id)
                    unique_items.append(item)
                    
            print(f"[*] Total unico capturado para P{prod_id}: {len(unique_items)}")
            out_file = os.path.join(output_dir, f"p{prod_id}_{slug}.json")
            with open(out_file, "w", encoding="utf-8") as f:
                json.dump(unique_items, f, indent=2, ensure_ascii=False)
            print(f"[+] Salvo em {out_file}")
            
        await context.close()
        print("\n[+] Lote 1 extraido com sucesso!")

if __name__ == '__main__':
    asyncio.run(run_extractions())
