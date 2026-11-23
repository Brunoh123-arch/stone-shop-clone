import os, glob, re

pages = glob.glob('pages/produto-*.html')

print(f"Total pages: {len(pages)}")

desc_videos = {}
for p in pages:
    pid = re.search(r'produto-(\d+)\.html', p).group(1)
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # find tt-product-video or product-video-block
    m = re.search(r'<video[^>]+id=["\']tt-product-video["\'][^>]*src=["\']([^"\']+)["\']', c)
    if not m:
        m = re.search(r'<video[^>]*src=["\']([^"\']+)["\'][^>]+id=["\']tt-product-video["\']', c)
    if not m:
        m = re.search(r'class=["\']tiktok-video-card["\'].*?<video[^>]*src=["\']([^"\']+)["\']', c, re.DOTALL)
    
    src = m.group(1) if m else 'SEM_VIDEO'
    
    # check poster
    mp = re.search(r'<video[^>]+id=["\']tt-product-video["\'][^>]*poster=["\']([^"\']+)["\']', c)
    if not mp:
        mp = re.search(r'<video[^>]*poster=["\']([^"\']+)["\'][^>]+id=["\']tt-product-video["\']', c)
    poster = mp.group(1) if mp else 'SEM_POSTER'
    
    desc_videos[int(pid)] = {'file': p, 'src': src, 'poster': poster}

# Group by src to see duplicates
from collections import defaultdict
by_src = defaultdict(list)
for pid, info in desc_videos.items():
    if info['src'] != 'SEM_VIDEO':
        by_src[info['src']].append(pid)

print("\n--- VÍDEOS DE DESCRIÇÃO DUPLICADOS / COMPARTILHADOS ---")
duplicates = {k: v for k, v in by_src.items() if len(v) > 1}
for src, pids in sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True):
    print(f"Vídeo {src} compartilhado por {len(pids)} produtos: {pids}")

print(f"\nTotal vídeos únicos de descrição: {len(by_src)}")
print(f"Total com vídeo de descrição: {sum(len(v) for v in by_src.values())}")
print(f"Total sem vídeo de descrição: {sum(1 for v in desc_videos.values() if v['src'] == 'SEM_VIDEO')}")

# Check specific P33
print(f"\nP33 info: {desc_videos.get(33)}")
