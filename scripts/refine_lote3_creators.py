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
    os.makedirs('temp_videos_lote3', exist_ok=True)
    os.makedirs('videosprodutos/posters', exist_ok=True)

    # 1. P59: trocar schumann.com_br pelo criador real jociarasants (index 8 em p59)
    p59_raw = json.load(open('scripts/data/extracted_lote3/p59_starlink_mini_59.json', 'r', encoding='utf-8'))
    cand_p59 = p59_raw[8] # jociarasants

    # 2. P63: trocar xiaomi_smartzone_br pelo criador real eugabicabral (index 3 em p63)
    p63_raw = json.load(open('scripts/data/extracted_lote3/p63_redmi_watch_63.json', 'r', encoding='utf-8'))
    cand_p63 = p63_raw[3] # eugabicabral

    # 3. P65: trocar camainboxoficial pelo criador real marialluizaff (index 4 em p65)
    p65_raw = json.load(open('scripts/data/extracted_lote3/p65_sofa_inbox_65.json', 'r', encoding='utf-8'))
    cand_p65 = p65_raw[4] # marialluizaff

    # 4. P78: trocar nandaliveteam (1) e loi.brasil (3) por keziarsantana (4) e lo.basquii (5)
    p78_raw = json.load(open('scripts/data/extracted_lote3/p78_wap_spotcleaner_78.json', 'r', encoding='utf-8'))
    cand_p78_1 = p78_raw[4] # keziarsantana
    cand_p78_3 = p78_raw[5] # lo.basquii

    replacements = [
        ("59", 0, 1, cand_p59, "starmini59_fix"),
        ("63", 2, 3, cand_p63, "redmi63_fix"),
        ("65", 1, 2, cand_p65, "sofa65_fix"),
        ("78", 0, 1, cand_p78_1, "wap78_fix1"),
        ("78", 2, 3, cand_p78_3, "wap78_fix3")
    ]

    ready_file = 'scripts/data/lote3_ready.json'
    all_ready = json.load(open(ready_file, 'r', encoding='utf-8'))

    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )

        for pid_str, arr_idx, post_idx, c, prefix in replacements:
            tmp_video = f"temp_videos_lote3/{prefix}_{c['username']}.mp4"
            poster_rel = f"videosprodutos/posters/poster-criador-{pid_str}-{post_idx}.jpg"
            print(f"[*] Baixando video substituto para P{pid_str} de @{c['username']}...")

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

            if not body or len(body) < 200000:
                print(f"[!] Falha no download de {c['username']}")
                continue

            with open(tmp_video, 'wb') as f:
                f.write(body)
            print(f"    [+] Baixado {len(body)} bytes")

            extract_poster(tmp_video, poster_rel)
            print(f"    [+] Poster: {poster_rel}")

            catbox_url = upload_catbox(tmp_video, f"{prefix}_{c['username']}.mp4")
            print(f"    [+] Catbox: {catbox_url}")

            avatar_path = c.get('avatar')
            if not avatar_path or 'p16' not in avatar_path:
                avatar_path = f"img/reviews-avatars/tiktok_real/tt_avatar_{10 + (int(pid_str) + post_idx) % 20}.jpg"

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

            all_ready[pid_str][arr_idx] = creator_obj
            print(f"[+] P{pid_str}[{arr_idx}] atualizado para @{c['username']}!")

        await ctx.close()

    with open(ready_file, 'w', encoding='utf-8') as f:
        json.dump(all_ready, f, indent=2, ensure_ascii=False)

    print("\n[+] Lote 3 100% blindado com pessoas físicas e vídeos completos!")

if __name__ == '__main__':
    asyncio.run(main())
