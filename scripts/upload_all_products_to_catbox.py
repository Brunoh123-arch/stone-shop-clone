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

    with urllib.request.urlopen(req, timeout=180) as resp:
        return resp.read().decode('utf-8').strip()

def run_all_upload():
    import re
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        text = f.read()

    pattern = re.compile(r'video:\s*["\']([^"\']+)["\']')
    matches = pattern.findall(text)
    local_vids = sorted(list(set([v for v in matches if not v.startswith('http')])))

    vmap = load_map()
    print(f"Total de videos a processar: {len(local_vids)}")

    for i, v in enumerate(local_vids):
        clean = v.replace('../', '').replace('/', os.sep)
        base = os.path.basename(clean)

        if base in vmap and vmap[base].startswith('https://files.catbox.moe/'):
            print(f"[{i+1}/{len(local_vids)}] Ja no Catbox: {base} -> {vmap[base]}")
            continue

        if not os.path.exists(clean):
            print(f"[{i+1}/{len(local_vids)}] AVISO: Arquivo nao encontrado: {clean}")
            continue

        sz_mb = os.path.getsize(clean) / (1024*1024)
        print(f"[{i+1}/{len(local_vids)}] Subindo {base} ({sz_mb:.2f} MB)...")
        try:
            cat_url = upload_to_catbox(clean)
            if cat_url.startswith('https://files.catbox.moe/'):
                vmap[base] = cat_url
                save_map(vmap)
                print(f"  -> SUCESSO: {cat_url}")
            else:
                print(f"  -> RESPOSTA INESPERADA: {cat_url}")
            time.sleep(1)
        except Exception as e:
            print(f"  -> ERRO: {e}")
            time.sleep(2)

    print("\nTodos os uploads concluidos!")

if __name__ == '__main__':
    run_all_upload()
