# -*- coding: utf-8 -*-
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

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    os.makedirs('temp_videos_lote2', exist_ok=True)
    os.makedirs('videosprodutos/posters', exist_ok=True)

    p92_raw = json.load(open('scripts/data/extracted_lote2/p92_panelas_ferro_92.json', 'r', encoding='utf-8'))
    p72_raw = json.load(open('scripts/data/extracted_lote2/p72_panelas_ferro_72.json', 'r', encoding='utf-8'))

    candidates = [
        ("panela92_1", 92, 1, p92_raw[4]),  # diycomvivi
        ("panela92_2", 92, 2, p72_raw[11])  # fernandapenteado_
    ]

    new_p92_creators = []

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )

        for prefix, pid, idx, c in candidates:
            tmp_video = f"temp_videos_lote2/{prefix}_{c['username']}.mp4"
            poster_rel = f"videosprodutos/posters/poster-criador-{pid}-{idx}.jpg"
            print(f"[*] Baixando video de @{c['username']}...")

            body = None
            for attempt in range(3):
                try:
                    res = await ctx.request.get(c['playAddr'], headers={'Referer': 'https://www.tiktok.com/'}, timeout=20000)
                    if res.status == 200:
                        body = await res.body()
                        break
                    else:
                        print(f"    Tentativa {attempt+1} status {res.status}")
                except Exception as e:
                    print(f"    Tentativa {attempt+1} err: {e}")
                await asyncio.sleep(2)

            if not body:
                print(f"[!] Falha no download de {c['username']}")
                continue

            with open(tmp_video, 'wb') as f:
                f.write(body)
            print(f"    [+] Baixado {len(body)} bytes")

            extract_poster(tmp_video, poster_rel)
            print(f"    [+] Poster gerado: {poster_rel}")

            catbox_url = upload_catbox(tmp_video, f"{prefix}_{c['username']}.mp4")
            print(f"    [+] Catbox: {catbox_url}")

            avatar_path = c.get('avatar')
            if not avatar_path or 'p16' not in avatar_path:
                avatar_path = f"img/reviews-avatars/tiktok_real/tt_avatar_{10 + (pid + idx) % 20}.jpg"

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
            new_p92_creators.append(creator_obj)

        await ctx.close()

    # Agora carrega lote2_ready.json e atualiza P92
    ready_file = 'scripts/data/lote2_ready.json'
    all_ready = json.load(open(ready_file, 'r', encoding='utf-8'))

    # P92 tinha [camilafrankliin, silvanacaldasmotta, achadinhosshope783]
    # Mantém o terceiro que era achadinhosshope783 (já único)
    p92_existing = all_ready.get('92', [])
    achadinhos = None
    for x in p92_existing:
        if x['username'] == 'achadinhosshope783':
            achadinhos = x
            break

    if not achadinhos and len(p92_existing) >= 3:
        achadinhos = p92_existing[2]

    # Ajusta poster do achadinhos para index 3
    if achadinhos:
        achadinhos['poster'] = 'videosprodutos/posters/poster-criador-92-3.jpg'
        final_p92 = [new_p92_creators[0], new_p92_creators[1], achadinhos]
    else:
        final_p92 = new_p92_creators

    all_ready['92'] = final_p92

    with open(ready_file, 'w', encoding='utf-8') as f:
        json.dump(all_ready, f, indent=2, ensure_ascii=False)

    print("\n[+] P92 atualizado com sucesso em lote2_ready.json:")
    for x in final_p92:
        print(f"    - {x['username']} ({x['name']}) -> {x['video']}")

if __name__ == '__main__':
    asyncio.run(main())
