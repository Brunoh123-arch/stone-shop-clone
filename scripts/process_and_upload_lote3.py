# -*- coding: utf-8 -*-
"""
Processa, baixa via Playwright Profile 42, extrai posters via FFmpeg e sobe no Catbox
para o Lote 3 de Tech & Casa: P52, P53, P55, P59, P63, P65, P78, P116.
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
    with urllib.request.urlopen(catbox_req, timeout=90) as res:
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
    {"prodId": 52, "file": "scripts/data/extracted_lote3/p52_pad11_tablet_52.json", "prefix": "pad11_52"},
    {"prodId": 53, "file": "scripts/data/extracted_lote3/p53_starlink_v4_53.json", "prefix": "starlink_53"},
    {"prodId": 55, "file": "scripts/data/extracted_lote3/p55_nintendo_switch_55.json", "prefix": "switch_55"},
    {"prodId": 59, "file": "scripts/data/extracted_lote3/p59_starlink_mini_59.json", "prefix": "starmini_59"},
    {"prodId": 63, "file": "scripts/data/extracted_lote3/p63_redmi_watch_63.json", "prefix": "redmi63"},
    {"prodId": 65, "file": "scripts/data/extracted_lote3/p65_sofa_inbox_65.json", "prefix": "sofa65"},
    {"prodId": 78, "file": "scripts/data/extracted_lote3/p78_wap_spotcleaner_78.json", "prefix": "wap78"},
    {"prodId": 116, "file": "scripts/data/extracted_lote3/p116_philco_roku_116.json", "prefix": "roku116"}
]

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    os.makedirs('temp_videos_lote3', exist_ok=True)
    os.makedirs('videosprodutos/posters', exist_ok=True)
    
    out_ready = "scripts/data/lote3_ready.json"
    all_ready = {}
    if os.path.exists(out_ready):
        with open(out_ready, 'r', encoding='utf-8') as f:
            all_ready = json.load(f)
            
    # Carrega criadores já usados em v3 e lote2 para evitar colisão
    existing_text = open('js/videos-criadores-v3.js', 'r', encoding='utf-8').read()
    global_seen_users = set()
    for m in existing_text.splitlines():
        if 'username:' in m:
            clean_u = m.split('username:')[1].replace('"', '').replace("'", '').replace(',', '').strip()
            global_seen_users.add(clean_u.lower())

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )
        
        for prod in PRODUCTS:
            prod_id = prod["prodId"]
            pid_str = str(prod_id)
            if len(all_ready.get(pid_str, [])) >= 3:
                print(f"[*] P{prod_id} ja tem {len(all_ready[pid_str])} videos prontos, pulando!")
                continue

            json_path = prod["file"]
            prefix = prod["prefix"]
            print(f"\n==========================================")
            print(f"[*] Processando P{prod_id} ({json_path})")
            print(f"==========================================")
            
            if not os.path.exists(json_path):
                print(f"[-] Arquivo {json_path} nao existe!")
                continue
                
            with open(json_path, 'r', encoding='utf-8') as f:
                items = json.load(f)
                
            selected = []
            for it in items:
                u = it.get('username', '').lower()
                desc = it.get('desc', '')
                if u and u not in global_seen_users and len(desc) > 8 and it.get('playAddr'):
                    global_seen_users.add(u)
                    selected.append(it)
                if len(selected) >= 3:
                    break
                    
            print(f"[*] Total selecionados para P{prod_id}: {len(selected)}")
            prod_creators = []
            
            for idx, c in enumerate(selected, 1):
                tmp_video = f"temp_videos_lote3/{prefix}_{idx}_{c['username']}.mp4"
                poster_rel = f"videosprodutos/posters/poster-criador-{prod_id}-{idx}.jpg"
                
                print(f"  [-] ({idx}/{len(selected)}) Baixando video de @{c['username']}...")
                body = None
                for attempt in range(3):
                    try:
                        res = await ctx.request.get(c['playAddr'], headers={'Referer': 'https://www.tiktok.com/'}, timeout=20000)
                        if res.status == 200:
                            body = await res.body()
                            break
                        else:
                            print(f"      [!] Tentativa {attempt+1} falhou com status {res.status}")
                    except Exception as err:
                        print(f"      [!] Tentativa {attempt+1} erro: {err}")
                    await asyncio.sleep(2)
                    
                if not body:
                    print(f"      [!] Falha definitiva no download de @{c['username']}")
                    continue
                    
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
                
            all_ready[pid_str] = prod_creators
            with open(out_ready, "w", encoding="utf-8") as f:
                json.dump(all_ready, f, indent=2, ensure_ascii=False)
            print(f"[+] P{prod_id} salvo com {len(prod_creators)} videos!")
            
        await ctx.close()
        
    print(f"\n[+] TUDO PRONTO! Salvo em {out_ready}")

if __name__ == '__main__':
    asyncio.run(main())
