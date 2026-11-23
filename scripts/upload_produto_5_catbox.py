import os
import json
import urllib.request
import mimetypes
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

vmap = load_map()
vids = [
    'videosprodutos/criador-5-1.mp4',
    'videosprodutos/criador-5-2.mp4',
    'videosprodutos/criador-5-3.mp4'
]

results = {}

for v in vids:
    base = os.path.basename(v)
    if base in vmap and vmap[base].startswith('https://files.catbox.moe/'):
        print(f"Ja no map: {base} -> {vmap[base]}")
        results[base] = vmap[base]
        continue
    sz_mb = os.path.getsize(v) / (1024*1024)
    print(f"Uploading {base} ({sz_mb:.2f} MB) to Catbox...")
    for attempt in range(3):
        try:
            cat_url = upload_to_catbox(v)
            if cat_url.startswith('https://files.catbox.moe/'):
                print(f"SUCCESS: {base} -> {cat_url}")
                vmap[base] = cat_url
                results[base] = cat_url
                save_map(vmap)
                break
            else:
                print(f"Unexpected response: {cat_url}")
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)

print("\nFinal Results:")
print(json.dumps(results, indent=2))
