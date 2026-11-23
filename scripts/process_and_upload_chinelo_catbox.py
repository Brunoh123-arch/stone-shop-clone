import os
import json
import urllib.request
import urllib.parse
import mimetypes
import subprocess
import time

MAP_FILE = 'scripts/catbox_videos_map.json'

def load_map():
    if os.path.exists(MAP_FILE):
        try:
            with open(MAP_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_map(m):
    with open(MAP_FILE, 'w', encoding='utf-8') as f:
        json.dump(m, f, indent=2, ensure_ascii=False)

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or 'application/octet-stream'
    boundary = '----WebKitFormBoundaryX7bW9t8h1Z9q7y2L'

    with open(file_path, 'rb') as f:
        file_bytes = f.read()

    header = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="reqtype"\r\n\r\n'
        f'fileupload\r\n'
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="fileToUpload"; filename="{filename}"\r\n'
        f'Content-Type: {mime_type}\r\n\r\n'
    ).encode('utf-8')

    footer = f'\r\n--{boundary}--\r\n'.encode('utf-8')
    data = header + file_bytes + footer

    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'Content-Type': f'multipart/form-data; boundary={boundary}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        }
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode('utf-8').strip()

def download_file(url, dest):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        with open(dest, 'wb') as f:
            f.write(resp.read())

os.makedirs('temp_chinelo_vids', exist_ok=True)
os.makedirs('img/creators-chinelo', exist_ok=True)
os.makedirs('img/posters-chinelo', exist_ok=True)

with open('temp_chinelo_meta/valid_creators.json', 'r', encoding='utf-8') as f:
    items = json.load(f)

vmap = load_map()

processed_creators = []

for idx, it in enumerate(items):
    c_num = idx + 1
    vid_name = f"video-chinelo-criadora{c_num}.mp4"
    poster_name = f"poster-chinelo-criadora{c_num}.jpg"
    avatar_name = f"creator-104-{c_num}.jpg"

    vid_path = os.path.join('temp_chinelo_vids', vid_name)
    poster_path = os.path.join('img', 'posters-chinelo', poster_name)
    avatar_path = os.path.join('img', 'creators-chinelo', avatar_name)

    print(f"\n--- [{c_num}/32] Processando @{it['username']} ---")

    # 1. Download video
    if not os.path.exists(vid_path):
        print(f"Baixando video MP4 de: {it['play_url'][:60]}...")
        try:
            download_file(it['play_url'], vid_path)
            print(f"  Salvo: {os.path.getsize(vid_path) / (1024*1024):.2f} MB")
        except Exception as e:
            print(f"  Falha no download do video: {e}")
            continue

    # 2. Extract poster
    if not os.path.exists(poster_path):
        print("Gerando poster via FFmpeg...")
        cmd = f'ffmpeg -y -ss 00:00:00.2 -i "{vid_path}" -vframes 1 -q:v 2 "{poster_path}"'
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if not os.path.exists(poster_path) or os.path.getsize(poster_path) == 0:
            # Fallback to 00:00:01
            cmd2 = f'ffmpeg -y -ss 00:00:01 -i "{vid_path}" -vframes 1 -q:v 2 "{poster_path}"'
            subprocess.run(cmd2, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # 3. Download avatar
    if not os.path.exists(avatar_path) and it.get('avatar'):
        try:
            download_file(it['avatar'], avatar_path)
        except Exception as e:
            print(f"  Falha no avatar: {e}")

    # 4. Upload video to Catbox
    if vid_name in vmap and vmap[vid_name].startswith('https://files.catbox.moe/'):
        catbox_url = vmap[vid_name]
        print(f"Video ja no Catbox: {catbox_url}")
    else:
        print(f"Subindo {vid_name} para o Catbox...")
        try:
            catbox_url = upload_to_catbox(vid_path)
            vmap[vid_name] = catbox_url
            save_map(vmap)
            print(f"  -> UPLOAD SUCESSO: {catbox_url}")
            time.sleep(1)
        except Exception as e:
            print(f"  -> FALHA CATBOX: {e}")
            continue

    # Build creator record
    clean_desc = it['title'].replace('\n', ' ').strip()
    if not clean_desc or len(clean_desc) < 10:
        clean_desc = "Meninas, esse chinelo de strass é muito lindo e macio nos pés! Brilho perfeito! 👡✨"

    processed_creators.append({
        'name': it['author_name'] or 'Criadora',
        'username': it['username'] or 'criadora',
        'avatar': f"../img/creators-chinelo/{avatar_name}",
        'poster': f"../img/posters-chinelo/{poster_name}",
        'video': catbox_url,
        'desc': clean_desc,
        'likes': it['likes'],
        'comments': it['comments']
    })

print(f"\nFinalizado! Total de criadoras prontas: {len(processed_creators)}")
with open('scripts/chinelo_32_creators_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(processed_creators, f, indent=2, ensure_ascii=False)
