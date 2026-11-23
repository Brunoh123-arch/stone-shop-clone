import os
import json
import urllib.request
import urllib.parse
import mimetypes
import subprocess
import time

os.makedirs('videosprodutos', exist_ok=True)
os.makedirs('img', exist_ok=True)

# Selected 3 creators:
targets = [
    {
        "id": "12-1",
        "url": "https://www.tiktok.com/@vaninhamedeiros2/video/7586077686951595271",
        "creator": "Vaninha Medeiros",
        "username": "vaninhamedeiros2",
        "video_path": "videosprodutos/criador-12-1.mp4",
        "poster_path": "img/poster-criador-12-1.jpg"
    },
    {
        "id": "12-2",
        "url": "https://www.tiktok.com/@junior.a.alves/video/7691909822953917697",
        "creator": "Júnior Alves",
        "username": "junior.a.alves",
        "video_path": "videosprodutos/criador-12-2.mp4",
        "poster_path": "img/poster-criador-12-2.jpg"
    },
    {
        "id": "12-3",
        "url": "https://www.tiktok.com/@lucianafortes/video/7564017562179161362",
        "creator": "Luciana Fortes",
        "username": "lucianafortes",
        "video_path": "videosprodutos/criador-12-3.mp4",
        "poster_path": "img/poster-criador-12-3.jpg"
    }
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Fetch TikWM info and download
for t in targets:
    print(f"\n--- Processando {t['id']} ({t['creator']}) ---")
    api = f"https://www.tikwm.com/api/?url={urllib.parse.quote(t['url'])}"
    req = urllib.request.Request(api, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as r:
        res = json.loads(r.read().decode('utf-8'))
    
    if res.get('code') != 0:
        raise Exception(f"TikWM error for {t['url']}: {res.get('msg')}")
    
    play_url = res['data']['play']
    print(f"Baixando video sem marca d'agua de: {play_url[:60]}...")
    
    req_v = urllib.request.Request(play_url, headers=headers)
    with urllib.request.urlopen(req_v, timeout=30) as r, open(t['video_path'], 'wb') as f:
        f.write(r.read())
    
    sz_mb = os.path.getsize(t['video_path']) / (1024*1024)
    print(f"Video salvo em {t['video_path']} ({sz_mb:.2f} MB)")
    
    # 2. Extract poster at 00:00:00.2
    cmd = [
        'ffmpeg', '-y',
        '-ss', '00:00:00.2',
        '-i', t['video_path'],
        '-vframes', '1',
        '-q:v', '2',
        t['poster_path']
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Poster extraido em {t['poster_path']}")

# 3. Upload to Catbox
MAP_FILE = 'scripts/catbox_videos_map.json'
cat_map = {}
if os.path.exists(MAP_FILE):
    try:
        with open(MAP_FILE, 'r', encoding='utf-8') as f:
            cat_map = json.load(f)
    except:
        cat_map = {}

def upload_to_catbox(file_path):
    url = "https://catbox.moe/user/api.php"
    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or 'video/mp4'
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

    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read().decode('utf-8').strip()

uploaded_urls = {}
for t in targets:
    base = os.path.basename(t['video_path'])
    if base in cat_map and cat_map[base].startswith('https://files.catbox.moe/'):
        print(f"Ja no mapa: {base} -> {cat_map[base]}")
        uploaded_urls[t['id']] = cat_map[base]
        continue
    
    print(f"Enviando {base} para o Catbox...")
    for attempt in range(3):
        try:
            res_url = upload_to_catbox(t['video_path'])
            if res_url.startswith('https://files.catbox.moe/'):
                print(f"SUCCESS: {base} -> {res_url}")
                cat_map[base] = res_url
                uploaded_urls[t['id']] = res_url
                with open(MAP_FILE, 'w', encoding='utf-8') as f:
                    json.dump(cat_map, f, indent=2, ensure_ascii=False)
                break
            else:
                print(f"Tentativa {attempt+1} falhou: {res_url}")
        except Exception as e:
            print(f"Tentativa {attempt+1} erro: {e}")
            time.sleep(2)

print("\n--- RESUMO DE UPLOAD CATBOX ---")
for tid, curl in uploaded_urls.items():
    print(f"{tid}: {curl}")

with open('scripts/piscina_12_catbox_urls.json', 'w', encoding='utf-8') as f:
    json.dump(uploaded_urls, f, indent=2)
