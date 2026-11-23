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

def main():
    files = [
        ('criador-6-1', 'videosprodutos/criador-6-1.mp4'),
        ('criador-6-2', 'videosprodutos/criador-6-2.mp4'),
        ('criador-6-3', 'videosprodutos/criador-6-3.mp4')
    ]

    vmap = load_map()
    uploaded = {}

    for key, path in files:
        if not os.path.exists(path):
            print(f"Arquivo não existe: {path}")
            continue

        size_mb = os.path.getsize(path) / (1024 * 1024)
        print(f"Fazendo upload de {path} ({size_mb:.2f} MB)...")

        for attempt in range(3):
            try:
                catbox_url = upload_to_catbox(path)
                if catbox_url.startswith('http'):
                    print(f"Sucesso: {catbox_url}")
                    uploaded[key] = catbox_url
                    vmap[f"../{path}"] = catbox_url
                    vmap[path] = catbox_url
                    save_map(vmap)
                    break
                else:
                    print(f"Resposta inesperada: {catbox_url}")
            except Exception as e:
                print(f"Erro tentativa {attempt+1}: {e}")
                time.sleep(3)

    with open('scripts/product_6_catbox_urls.json', 'w', encoding='utf-8') as f:
        json.dump(uploaded, f, indent=2)

    print("\nUpload completo:")
    print(json.dumps(uploaded, indent=2))

if __name__ == '__main__':
    main()
