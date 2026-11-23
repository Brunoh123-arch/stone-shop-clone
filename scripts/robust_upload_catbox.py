import os
import json
import urllib.request
import mimetypes
import time
import re

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

def upload_single_file(file_path):
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

    with urllib.request.urlopen(req, timeout=300) as resp:
        return resp.read().decode('utf-8').strip()

def upload_with_retry(file_path, max_retries=3):
    for attempt in range(1, max_retries + 1):
        try:
            res = upload_single_file(file_path)
            if res.startswith('https://files.catbox.moe/'):
                return res
            else:
                print(f"    Tentativa {attempt}: resposta inesperada '{res}'")
        except Exception as e:
            print(f"    Tentativa {attempt} falhou: {e}")
            time.sleep(3 * attempt)
    return None

def patch_videos_criadores():
    vmap = load_map()
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        js = f.read()

    replaced_count = 0
    for base, cat_url in vmap.items():
        if cat_url.startswith('https://files.catbox.moe/'):
            # Replace any relative path ending in base
            patterns = [
                f'../videosprodutos/{base}',
                f'videosprodutos/{base}',
                f'../img/{base}',
                f'img/{base}'
            ]
            for p in patterns:
                if p in js:
                    js = js.replace(p, cat_url)
                    replaced_count += 1

    with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print(f"js/videos-criadores.js atualizado com {replaced_count} substituicoes para Catbox!")

def main():
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        text = f.read()

    pattern = re.compile(r'video:\s*["\']([^"\']+)["\']')
    matches = pattern.findall(text)
    local_vids = sorted(list(set([v for v in matches if not v.startswith('http')])))

    vmap = load_map()

    to_upload = []
    for v in local_vids:
        clean = v.replace('../', '').replace('/', os.sep)
        base = os.path.basename(clean)
        if base not in vmap or not vmap[base].startswith('https://files.catbox.moe/'):
            to_upload.append((base, clean))

    # Sort ascending by file size so small/fast files upload first!
    to_upload.sort(key=lambda x: os.path.getsize(x[1]) if os.path.exists(x[1]) else 0)

    print(f"Total de videos restantes para subir: {len(to_upload)}")

    success_count = 0
    fail_count = 0

    for i, (base, clean) in enumerate(to_upload):
        if not os.path.exists(clean):
            print(f"[{i+1}/{len(to_upload)}] PULAR: {clean} nao existe")
            continue

        sz_mb = os.path.getsize(clean) / (1024*1024)
        print(f"[{i+1}/{len(to_upload)}] Subindo {base} ({sz_mb:.2f} MB)...")

        cat_url = upload_with_retry(clean)
        if cat_url:
            vmap[base] = cat_url
            save_map(vmap)
            print(f"  -> SUCESSO: {cat_url}")
            success_count += 1
            # Auto patch incremental
            patch_videos_criadores()
            time.sleep(1)
        else:
            print(f"  -> ERRO DEFINITIVO em {base}")
            fail_count += 1

    print(f"\nFinalizado lote! Sucessos: {success_count}, Falhas: {fail_count}")

if __name__ == '__main__':
    main()
