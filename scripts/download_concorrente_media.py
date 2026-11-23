import json
import os
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

base_dir = r"criativos_concorrente\1033811266480714"
json_path = os.path.join(base_dir, "anuncios_concorrente.json")

with open(json_path, 'r', encoding='utf-8') as f:
    ads = json.load(f)

print(f"Total de anúncios para processar: {len(ads)}")

# Função para extrair slug limpo do produto a partir da URL
def get_product_slug(url):
    if not url:
        return "produtos_diversos"
    parsed = urlparse(url)
    path = parsed.path.strip('/')
    parts = path.split('/')
    slug = parts[-1] if parts else "geral"
    # Limpa sufixos de datas como 13out, 14out, 28out
    slug_clean = re.sub(r'\d{1,2}(out|nov|dez|jan|fev).*$', '', slug)
    return slug_clean or slug or "geral"

# Agrupa por produto
produtos_map = {}
for ad in ads:
    dest = ad.get('cleanDestUrl', '')
    slug = get_product_slug(dest)
    if slug not in produtos_map:
        produtos_map[slug] = {
            'slug': slug,
            'destUrl': dest,
            'adsCount': 0,
            'adIds': [],
            'videos': [],
            'images': []
        }
    produtos_map[slug]['adsCount'] += 1
    produtos_map[slug]['adIds'].append(ad.get('adId'))
    for v in ad.get('videoUrls', []):
        if v not in produtos_map[slug]['videos']:
            produtos_map[slug]['videos'].append(v)
    for img in ad.get('imgUrls', []):
        if img not in produtos_map[slug]['images']:
            produtos_map[slug]['images'].append(img)

print(f"\nIdentificados {len(produtos_map)} produtos distintos anunciados!")

def download_file(url, out_path):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        return out_path, True
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp, open(out_path, 'wb') as f:
            f.write(resp.read())
        return out_path, True
    except Exception as e:
        return out_path, False

# Fila de downloads
tasks = []
for slug, pdata in produtos_map.items():
    prod_folder = os.path.join(base_dir, slug)
    os.makedirs(prod_folder, exist_ok=True)
    
    for idx, v_url in enumerate(pdata['videos']):
        v_name = f"video_{idx + 1}.mp4"
        out_v = os.path.join(prod_folder, v_name)
        tasks.append((v_url, out_v, slug, 'video'))

    for idx, img_url in enumerate(pdata['images']):
        img_name = f"imagem_{idx + 1}.jpg"
        out_img = os.path.join(prod_folder, img_name)
        tasks.append((img_url, out_img, slug, 'imagem'))

print(f"Iniciando download paralelo de {len(tasks)} criativos (vídeos e imagens)...")

success_count = 0
failed_count = 0

with ThreadPoolExecutor(max_workers=6) as executor:
    future_to_task = {executor.submit(download_file, t[0], t[1]): t for t in tasks}
    for future in as_completed(future_to_task):
        t = future_to_task[future]
        out_path, ok = future.result()
        if ok:
            success_count += 1
        else:
            failed_count += 1
        if (success_count + failed_count) % 10 == 0 or (success_count + failed_count) == len(tasks):
            print(f"Progresso: {success_count + failed_count}/{len(tasks)} ({success_count} sucessos, {failed_count} falhas)")

print(f"\nFinalizado! Total baixado: {success_count} arquivos em {base_dir}")

# Salva sumário estruturado
summary = []
for slug, pdata in sorted(produtos_map.items(), key=lambda x: x[1]['adsCount'], reverse=True):
    prod_folder = os.path.join(base_dir, slug)
    local_videos = [f for f in os.listdir(prod_folder) if f.endswith('.mp4')] if os.path.exists(prod_folder) else []
    summary.append({
        'produto': slug,
        'anuncios_ativos': pdata['adsCount'],
        'link_destino': pdata['destUrl'],
        'videos_baixados': len(local_videos),
        'pasta_local': prod_folder
    })

summary_file = os.path.join(base_dir, "resumo_produtos.json")
with open(summary_file, 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"Sumário de produtos salvo em: {summary_file}")
