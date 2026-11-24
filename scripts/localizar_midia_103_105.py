import os, glob, json, re, urllib.request
from io import BytesIO
from PIL import Image

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

# 1. Coleta todas as URLs ibyteimg nos JSONs 103, 104, 105 e em qualquer outro JSON
url_to_local = {}
counter_by_pid = {}

def collect_urls(obj, pid):
    if isinstance(obj, str):
        if "ibyteimg.com" in obj and obj.startswith("http"):
            if obj not in url_to_local:
                counter_by_pid[pid] = counter_by_pid.get(pid, 0) + 1
                idx = counter_by_pid[pid]
                url_to_local[obj] = f"img/prod-{pid}-local-{idx}.webp"
    elif isinstance(obj, list):
        for x in obj:
            collect_urls(x, pid)
    elif isinstance(obj, dict):
        for v in obj.values():
            collect_urls(v, pid)

# Primeiro prioriza 103, 104, 105 para os nomes ficarem com o ID certo do dono da foto
for pid in ("103", "104", "105"):
    d = json.load(open(f"data/produtos/produto-{pid}.json", encoding="utf-8"))
    collect_urls(d, pid)

# Depois pega eventuais sobras em outros produtos (ex: cards relacionados apontando pro 103/104/105)
for p in sorted(glob.glob("data/produtos/produto-*.json")):
    pid = re.search(r"produto-(\d+)", p).group(1)
    d = json.load(open(p, encoding="utf-8"))
    collect_urls(d, pid)

print(f"Total URLs externas ibyteimg encontradas: {len(url_to_local)}")

downloaded_map = {}
failed = []

for url, local_rel in url_to_local.items():
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Referer": "https://www.tiktok.com/"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
        if len(raw) < 1500:
            raise ValueError(f"Arquivo muito pequeno ({len(raw)} bytes)")
        im = Image.open(BytesIO(raw))
        im.load()
        if im.mode not in ("RGB", "RGBA"):
            im = im.convert("RGB")
        im.save(local_rel, "WEBP", quality=86, method=4)
        downloaded_map[url] = "../" + local_rel
        print(f"  OK: {local_rel} ({os.path.getsize(local_rel)//1024} KB, {im.size[0]}x{im.size[1]})")
    except Exception as e:
        failed.append((url, local_rel, str(e)))
        print(f"  FAIL: {local_rel} -> {e}")

if failed:
    print(f"\n⚠️ {len(failed)} falhas no download:")
    for f in failed:
        print(" ", f)
    raise SystemExit(1)

# 2. Substitui em todos os JSONs de data/produtos/
def replace_urls(obj):
    if isinstance(obj, str):
        return downloaded_map.get(obj, obj)
    elif isinstance(obj, list):
        return [replace_urls(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: replace_urls(v) for k, v in obj.items()}
    return obj

updated_jsons = 0
for p in sorted(glob.glob("data/produtos/produto-*.json")):
    raw_txt = open(p, encoding="utf-8").read()
    if "ibyteimg.com" not in raw_txt:
        continue
    d = json.loads(raw_txt)
    d2 = replace_urls(d)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d2, f, ensure_ascii=False, indent=2)
    updated_jsons += 1

# 3. Atualiza tambem em js/catalogo.js e index.html se existirem URLs ibyteimg
for extra_file in ("js/catalogo.js", "index.html"):
    if os.path.exists(extra_file):
        txt = open(extra_file, encoding="utf-8").read()
        changed = False
        for old_u, new_rel in downloaded_map.items():
            # Em js/catalogo.js e index.html na raiz, o caminho pode ser sem ../ ou com img/
            target_path = new_rel.replace("../", "") if extra_file == "index.html" else new_rel.replace("../", "")
            if old_u in txt:
                txt = txt.replace(old_u, target_path)
                changed = True
        if changed:
            open(extra_file, "w", encoding="utf-8").write(txt)
            print(f"  Atualizado também: {extra_file}")

print(f"\n✅ {len(downloaded_map)} imagens hospedadas localmente em img/ e {updated_jsons} JSONs atualizados!")
