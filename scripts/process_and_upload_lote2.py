# -*- coding: utf-8 -*-
"""
Processa, baixa via Playwright Profile 42, extrai posters via FFmpeg e sobe no Catbox
para o Lote 2 de Eletro & Cozinha: P05, P70, P91, P95, P72, P89, P92, P96, P97.
Preserva itens já concluídos e adiciona retry para garantir 100% de sucesso.
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
    {"prodId": 5, "file": "scripts/data/extracted_lote2/p5_airfryer_elgin_5.json", "prefix": "elgin5"},
    {"prodId": 70, "file": "scripts/data/extracted_lote2/p70_secadora_mueller_70.json", "prefix": "mueller70"},
    {"prodId": 91, "file": "scripts/data/extracted_lote2/p91_pipoqueira_91.json", "prefix": "pipoca91"},
    {"prodId": 95, "file": "scripts/data/extracted_lote2/p95_maquina_gelo_95.json", "prefix": "gelo95"},
    {"prodId": 72, "file": "scripts/data/extracted_lote2/p72_panelas_ferro_72.json", "prefix": "panela72"},
    {"prodId": 89, "file": "scripts/data/extracted_lote2/p89_panelas_ferro_89.json", "prefix": "panela89"},
    {"prodId": 92, "file": "scripts/data/extracted_lote2/p92_panelas_ferro_92.json", "prefix": "panela92"},
    {"prodId": 96, "file": "scripts/data/extracted_lote2/p96_oxford_ryo_96.json", "prefix": "oxford96"},
    {"prodId": 97, "file": "scripts/data/extracted_lote2/p97_canyon_tramontina_97.json", "prefix": "canyon97"}
]

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    os.makedirs('temp_videos_lote2', exist_ok=True)
    os.makedirs('videosprodutos/posters', exist_ok=True)
    
    out_ready = "scripts/data/lote2_ready.json"
    all_ready = {}
    if os.path.exists(out_ready):
        with open(out_ready, 'r', encoding='utf-8') as f:
            all_ready = json.load(f)
            
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
            seen_users = set()
            for it in items:
                u = it['username']
                desc = it.get('desc', '')
                if u not in seen_users and len(desc) > 8 and it.get('playAddr'):
                    seen_users.add(u)
                    selected.append(it)
                if len(selected) >= 3:
                    break
                    
            print(f"[*] Total selecionados para P{prod_id}: {len(selected)}")
            prod_creators = []
            
            for idx, c in enumerate(selected, 1):
                tmp_video = f"temp_videos_lote2/{prefix}_{idx}_{c['username']}.mp4"
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
            # Salva progresso imediatamente
            with open(out_ready, "w", encoding="utf-8") as f:
                json.dump(all_ready, f, indent=2, ensure_ascii=False)
            print(f"[+] P{prod_id} salvo com {len(prod_creators)} videos!")
            
        await ctx.close()
        
    print(f"\n[+] TUDO PRONTO! Salvo em {out_ready}")

if __name__ == '__main__':
    asyncio.run(main())
