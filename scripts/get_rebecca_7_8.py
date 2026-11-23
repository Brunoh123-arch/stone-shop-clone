# -*- coding: utf-8 -*-
import json
import os
import subprocess
import urllib.request
import asyncio
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

async def main():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    with open('scripts/data/rebecca_extra_extracted.json', 'r', encoding='utf-8') as f:
        extra = json.load(f)

    # Pegar mavi2.04 e josianeteixeira00
    targets = [it for it in extra if it['username'] in ['mavi2.04', 'josianeteixeira00']]

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )

        results = []
        for idx, c in enumerate(targets, 7): # indices 7 e 8
            u = c['username']
            tmp_video = f"temp_videos/rebecca_28_{idx}_{u}.mp4"
            poster_path = f"videosprodutos/posters/poster-rebecca-28-c{idx}.jpg"

            print(f"[*] ({idx}/8) Baixando video de @{u}...")
            res = await ctx.request.get(c['playAddr'], headers={'Referer': 'https://www.tiktok.com/'}, timeout=60000)
            if res.status != 200:
                print(f"    [!] Falha status {res.status}")
                continue
            body = await res.body()
            with open(tmp_video, 'wb') as vf:
                vf.write(body)
            print(f"    [+] Baixou {len(body)} bytes.")

            print(f"    [*] Extraindo poster para {poster_path}...")
            extract_poster(tmp_video, poster_path)

            print(f"    [*] Subindo para o Catbox...")
            catbox_url = upload_catbox(tmp_video, f"rebecca_28_c{idx}_{u}.mp4")
            print(f"    [+] Catbox URL: {catbox_url}")

            results.append({
                'name': c.get('nickname') or u,
                'username': u,
                'avatar': c.get('avatar', ''),
                'poster': f"../{poster_path}",
                'video': catbox_url,
                'desc': c.get('desc', '')
            })

        await ctx.close()

    with open('scripts/data/rebecca_7_8_ready.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n[+] SUCESSO! 7 e 8 prontos!")

if __name__ == '__main__':
    asyncio.run(main())
