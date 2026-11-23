import json
import os
import urllib.request

data = json.load(open('scripts/valid_piscina_videos.json', encoding='utf-8'))
out_dir = 'videosprodutos/piscina_raw'
os.makedirs(out_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

downloaded = []
for i, v in enumerate(data):
    url = v.get('play')
    out_path = os.path.join(out_dir, f"pool_{i+1:02d}.mp4")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"[{i+1:>2}] Ja existe: {out_path} ({os.path.getsize(out_path)}b)")
        downloaded.append((out_path, v))
        continue
    try:
        print(f"[{i+1:>2}] Baixando @{v.get('username')}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            content = resp.read()
            with open(out_path, 'wb') as f:
                f.write(content)
        print(f"  -> Salvo: {out_path} ({len(content)}b)")
        downloaded.append((out_path, v))
    except Exception as e:
        print(f"  -> Erro ao baixar {i+1}: {e}")

print(f"\nTotal baixados com sucesso: {len(downloaded)}/{len(data)}")
