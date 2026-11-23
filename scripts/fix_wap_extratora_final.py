# -*- coding: utf-8 -*-
import os
import sys
import json
import asyncio
import subprocess
import urllib.request
import re
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
    os.makedirs('temp_videos_lote4', exist_ok=True)
    os.makedirs('videosprodutos/posters', exist_ok=True)

    p78_raw = json.load(open('scripts/data/extracted_lote3/p78_wap_spotcleaner_78.json', 'r', encoding='utf-8'))

    # alarmvix (index 6 no p78), minharotinanadaperfeita (index 7), cadicuh (index 3)
    target_users = ['alarmvix', 'minharotinanadaperfeita', 'cadicuh']
    selected = [x for x in p78_raw if x['username'] in target_users]

    new_creators = []

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )

        for idx, c in enumerate(selected, 1):
            tmp_video = f"temp_videos_lote4/extratora47_{idx}_{c['username']}.mp4"
            poster_rel = f"videosprodutos/posters/poster-criador-47-{idx}.jpg"
            print(f"[*] Baixando video de @{c['username']}...")

            body = None
            for attempt in range(3):
                try:
                    res = await ctx.request.get(c['playAddr'], headers={'Referer': 'https://www.tiktok.com/'}, timeout=20000)
                    if res.status == 200:
                        body = await res.body()
                        break
                except Exception as e:
                    pass
                await asyncio.sleep(2)

            if not body:
                print(f"[!] Falha no download de {c['username']}")
                continue

            with open(tmp_video, 'wb') as f:
                f.write(body)
            print(f"    [+] Baixado {len(body)} bytes")

            extract_poster(tmp_video, poster_rel)
            print(f"    [+] Poster: {poster_rel}")

            catbox_url = upload_catbox(tmp_video, f"extratora47_{idx}_{c['username']}.mp4")
            print(f"    [+] Catbox: {catbox_url}")

            avatar_path = c.get('avatar')
            if not avatar_path or 'p16' not in avatar_path:
                avatar_path = f"img/reviews-avatars/tiktok_real/tt_avatar_{10 + (47 + idx) % 20}.jpg"

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
            new_creators.append(creator_obj)

        await ctx.close()

    # Aplica em WAP_EXTRATORA_78_VIDEOS_MAP nos dois arquivos
    for js_file in ['js/videos-criadores.js', 'js/videos-criadores-v3.js']:
        content = open(js_file, 'r', encoding='utf-8').read()
        pattern = r'(const\s+WAP_EXTRATORA_78_VIDEOS_MAP\s*=\s*\[)([\s\S]*?)(\];)'
        m = re.search(pattern, content)
        if not m:
            continue
        existing_body = m.group(2).strip()
        if existing_body.endswith(','):
            existing_body = existing_body[:-1].strip()

        lines = []
        for it in new_creators:
            lines.append("  {\n")
            lines.append(f"    name: {json.dumps(it['name'], ensure_ascii=False)},\n")
            lines.append(f"    username: {json.dumps(it['username'], ensure_ascii=False)},\n")
            lines.append(f"    avatar: {json.dumps(it['avatar'], ensure_ascii=False)},\n")
            lines.append(f"    poster: (typeof isPagesDir !== 'undefined' && isPagesDir ? '../' : '') + {json.dumps(it['poster'], ensure_ascii=False)},\n")
            lines.append(f"    video: {json.dumps(it['video'], ensure_ascii=False)},\n")
            lines.append(f"    startTime: {it.get('startTime', 0.2)},\n")
            lines.append(f"    desc: {json.dumps(it['desc'], ensure_ascii=False)}\n")
            lines.append("  }")

        combined = existing_body + ",\n" + ",\n".join(lines)
        content = re.sub(pattern, r'\g<1>\n' + combined + r'\n\g<3>', content, count=1)
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[+] WAP_EXTRATORA_78_VIDEOS_MAP expandido em {js_file}!")

if __name__ == '__main__':
    asyncio.run(main())
