# -*- coding: utf-8 -*-
"""
Processa, baixa via Playwright Profile 42, extrai posters via FFmpeg e sobe no Catbox
para o Lote 1 de Audio: P57, P58, P60, P61, P73 e P85.
"""
import os
import sys
import json
import asyncio
import subprocess
import urllib.request
from playwright.async_api import async_playwright

def upload_catbox(file_path, filename):
    with open(file_path, 'rb') as f:
        video_bytes = f.read()

    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
    body = bytearray()
    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(b'Content-Disposition: form-data; name="reqtype"\r\n\r\n')
    body.extend(b'fileupload\r\n')

    body.extend(f'--{boundary}\r\n'.encode('utf-8'))
    body.extend(f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"\r\n'.encode('utf-8'))
    body.extend(b'Content-Type: video/mp4\r\n\r\n')
    body.extend(video_bytes)
    body.extend(b'\r\n')
    body.extend(f'--{boundary}--\r\n'.encode('utf-8'))

    catbox_req = urllib.request.Request(
        'https://catbox.moe/user/api.php',
        data=body,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Content-Type': f'multipart/form-data; boundary={boundary}'
        }
    )
    with urllib.request.urlopen(catbox_req, timeout=60) as res:
        url = res.read().decode('utf-8').strip()
    return url

def extract_poster(video_path, poster_path):
    os.makedirs(os.path.dirname(poster_path), exist_ok=True)
    cmd = [
        'ffmpeg', '-y', '-ss', '00:00:01',
        '-i', video_path,
        '-vframes', '1',
        '-q:v', '2',
        poster_path
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

PRODUCTS = [
    {"prodId": 57, "file": "scripts/data/extracted_lote1/p57_joog_one_57.json", "prefix": "joog57"},
    {"prodId": 58, "file": "scripts/data/extracted_lote1/p58_echo_dot_58.json", "prefix": "echo58"},
    {"prodId": 60, "file": "scripts/data/extracted_lote1/p60_sabala_60.json", "prefix": "sabala60"},
    {"prodId": 61, "file": "scripts/data/extracted_lote1/p61_joog_break_61.json", "prefix": "joog61"},
    {"prodId": 73, "file": "scripts/data/extracted_lote1/p73_waaw_73.json", "prefix": "waaw73"},
    {"prodId": 85, "file": "scripts/data/extracted_lote1/p85_joog_x2_85.json", "prefix": "joog85"}
]

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    os.makedirs('temp_videos', exist_ok=True)
    os.makedirs('videosprodutos/posters', exist_ok=True)
    
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )
        
        all_ready = {}
        
        for prod in PRODUCTS:
            prod_id = prod["prodId"]
            json_path = prod["file"]
            prefix = prod["prefix"]
            print(f"\n==========================================")
            print(f"[*] Processando P{prod_id} via Profile 42 ({json_path})")
            print(f"==========================================")
            
            if not os.path.exists(json_path):
                print(f"[-] Arquivo {json_path} nao existe!")
                continue
                
            with open(json_path, 'r', encoding='utf-8') as f:
                items = json.load(f)
                
            selected = []
            seen_users = set()
            for it in items:
                u = it['username']
                if u not in seen_users and len(it.get('desc', '')) > 5:
                    seen_users.add(u)
                    selected.append(it)
                if len(selected) >= 3:
                    break
                    
            print(f"[*] Total selecionados para P{prod_id}: {len(selected)}")
            prod_creators = []
            
            for idx, c in enumerate(selected, 1):
                tmp_video = f"temp_videos/{prefix}_{idx}_{c['username']}.mp4"
                poster_rel = f"videosprodutos/posters/poster-criador-{prod_id}-{idx}.jpg"
                
                print(f"  [-] ({idx}/{len(selected)}) Baixando video de @{c['username']}...")
                try:
                    res = await ctx.request.get(c['playAddr'], headers={'Referer': 'https://www.tiktok.com/'})
                    if res.status != 200:
                        print(f"      [!] Falha status {res.status}")
                        continue
                    body = await res.body()
                    with open(tmp_video, 'wb') as vf:
                        vf.write(body)
                    print(f"      [+] Baixou {len(body)} bytes.")
                    
                    extract_poster(tmp_video, poster_rel)
                    print(f"      [+] Poster gerado: {poster_rel}")
                    
                    catbox_url = upload_catbox(tmp_video, f"{prefix}_{idx}_{c['username']}.mp4")
                    print(f"      [+] Catbox URL: {catbox_url}")
                    
                    avatar_path = c.get('avatar')
                    if not avatar_path or 'p16' not in avatar_path:
                        avatar_path = f"img/reviews-avatars/tiktok_real/tt_avatar_{10 + (prod_id + idx) % 20}.jpg"
                        
                    clean_desc = c.get('desc', '').replace('"', "'").replace('\n', ' ')
                    if len(clean_desc) > 140:
                        clean_desc = clean_desc[:137] + "..."
                        
                    creator_obj = {
                        "name": c.get('nickname') or c.get('username'),
                        "username": c.get('username'),
                        "avatar": avatar_path,
                        "poster": poster_rel,
                        "video": catbox_url,
                        "startTime": 0.2,
                        "desc": clean_desc
                    }
                    prod_creators.append(creator_obj)
                except Exception as ex:
                    print(f"      [!] Erro criador {c['username']}: {ex}")
                    
            all_ready[str(prod_id)] = prod_creators
            
        await ctx.close()
        
    with open('scripts/data/lote1_ready.json', 'w', encoding='utf-8') as f:
        json.dump(all_ready, f, indent=2, ensure_ascii=False)
        
    print("\n[+] LOTE 1 PRONTO COM SUCESSO EM scripts/data/lote1_ready.json!")

if __name__ == '__main__':
    asyncio.run(main())
