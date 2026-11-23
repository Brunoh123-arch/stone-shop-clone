# -*- coding: utf-8 -*-
"""
Processa e sobe para o Catbox os vídeos reais capturados do TikTok
para os 5 produtos: P7, P35, P76, P82 e P98.
Gera os posters com ffmpeg e monta o dicionário pronto para injetar em videos-criadores.js.
"""
import os
import sys
import json
import subprocess
import urllib.request

sys.path.append(os.path.abspath('scripts'))
from tiktok_catbox_downloader import HEADERS, COOKIES

def download_video(play_addr, dest_path):
    req = urllib.request.Request(play_addr, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=40) as r:
        video_bytes = r.read()
    with open(dest_path, 'wb') as f:
        f.write(video_bytes)
    return len(video_bytes)

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
    {"prodId": 7, "file": "scripts/data/extracted_zeros/p7_aiwa_7.json", "prefix": "aiwa7"},
    {"prodId": 35, "file": "scripts/data/extracted_zeros/p35_jbl_35.json", "prefix": "jbl35"},
    {"prodId": 76, "file": "scripts/data/extracted_zeros/p76_aparelho_76.json", "prefix": "porto76"},
    {"prodId": 82, "file": "scripts/data/extracted_zeros/p82_hisense_82.json", "prefix": "hisense82"},
    {"prodId": 98, "file": "scripts/data/extracted_zeros/p98_copos_98.json", "prefix": "copos98"}
]

os.makedirs('temp_videos', exist_ok=True)
os.makedirs('videosprodutos/posters', exist_ok=True)

all_ready = {}

for p in PRODUCTS:
    prod_id = p["prodId"]
    json_path = p["file"]
    prefix = p["prefix"]
    print(f"\n==========================================")
    print(f"[*] Processando P{prod_id} a partir de {json_path}")
    print(f"==========================================")
    
    if not os.path.exists(json_path):
        print(f"[-] Arquivo {json_path} nao existe!")
        continue
        
    with open(json_path, 'r', encoding='utf-8') as f:
        items = json.load(f)
        
    print(f"[*] Total de itens no JSON: {len(items)}")
    
    # Seleciona ate 4 itens distintos
    selected = []
    seen_users = set()
    for it in items:
        u = it['username']
        if u not in seen_users and len(it.get('desc', '')) > 5:
            seen_users.add(u)
            selected.append(it)
        if len(selected) >= 4:
            break
            
    print(f"[*] Selecionados {len(selected)} criadores para P{prod_id}")
    
    prod_creators = []
    for idx, c in enumerate(selected, 1):
        tmp_video = f"temp_videos/{prefix}_{idx}_{c['username']}.mp4"
        poster_rel = f"videosprodutos/posters/poster-criador-{prod_id}-{idx}.jpg"
        
        print(f"  [-] ({idx}/{len(selected)}) Baixando video de @{c['username']}...")
        try:
            download_video(c['playAddr'], tmp_video)
            print(f"      [+] Video baixado com sucesso.")
            
            # Extrair poster
            extract_poster(tmp_video, poster_rel)
            print(f"      [+] Poster gerado em {poster_rel}")
            
            # Subir pro Catbox
            catbox_url = upload_catbox(tmp_video, f"{prefix}_{idx}_{c['username']}.mp4")
            print(f"      [+] Catbox URL: {catbox_url}")
            
            # Avatar fallback se avatar for vazio ou temporário
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
                "poster": f"videosprodutos/posters/poster-criador-{prod_id}-{idx}.jpg",
                "video": catbox_url,
                "startTime": 0.2,
                "desc": clean_desc
            }
            prod_creators.append(creator_obj)
        except Exception as ex:
            print(f"      [!] Falha no criador {c['username']}: {ex}")
            
    all_ready[str(prod_id)] = prod_creators

with open('scripts/data/zeros_ready.json', 'w', encoding='utf-8') as f:
    json.dump(all_ready, f, indent=2, ensure_ascii=False)

print("\n[+] TODOS OS VÍDEOS PROCESSADOS E SALVOS EM scripts/data/zeros_ready.json!")
