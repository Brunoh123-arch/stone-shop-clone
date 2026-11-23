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

vmap = load_map()

# Upload video-chinelo-oficial.mp4
oficial_path = 'img/video-chinelo-oficial.mp4'
if os.path.exists(oficial_path):
    base = os.path.basename(oficial_path)
    if base not in vmap:
        sz = os.path.getsize(oficial_path) / (1024*1024)
        print(f"Uploading {base} ({sz:.2f} MB)...")
        u = upload_to_catbox(oficial_path)
        vmap[base] = u
        save_map(vmap)
        print(f"Uploaded: {u}")
    else:
        print(f"Already mapped: {vmap[base]}")

print("Mapa completo atual:")
print(json.dumps(vmap, indent=2))
