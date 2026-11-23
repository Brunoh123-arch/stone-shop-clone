import os, json, mimetypes, urllib.request, time

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
        json.dump(m, f, indent=2)

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

chinelo_vids = [
    'img/video-chinelo-real-1.mp4',
    'img/video-chinelo-real-2.mp4',
    'img/video-chinelo-real-3.mp4',
    'img/video-chinelo-real-4.mp4',
    'img/video-chinelo-real-5.mp4'
]

vmap = load_map()
vmap['video-chinelo-real-1.mp4'] = 'https://files.catbox.moe/tsjc1l.mp4'

for vp in chinelo_vids:
    base = os.path.basename(vp)
    if base in vmap:
        print(f"Already in map: {base} -> {vmap[base]}")
        continue
    if os.path.exists(vp):
        sz_mb = os.path.getsize(vp) / (1024*1024)
        print(f"Uploading {base} ({sz_mb:.2f} MB)...")
        try:
            cur_url = upload_to_catbox(vp)
            vmap[base] = cur_url
            save_map(vmap)
            print(f"  -> SUCCESS: {cur_url}")
            time.sleep(1)
        except Exception as e:
            print(f"  -> FAILED: {e}")
    else:
        print(f"File not found: {vp}")

print("\nFinal chinelo map:")
for k, v in vmap.items():
    print(f"  {k} : {v}")
