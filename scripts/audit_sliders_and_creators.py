import os, re, glob, json

html_files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))

print(f"Total de produtos encontrados: {len(html_files)}")

single_slide = []
creator_counts = {}

# Read videos-criadores-v3.js
with open('js/videos-criadores-v3.js', 'r', encoding='utf-8') as f:
    vc_content = f.read()

# Map product id to video count in videos-criadores
# Look for: case 28: return CREATORS_REBECCA_BONBON_28;
# or CREATORS_... = [ ... ]
for m in re.finditer(r'const\s+([A-Za-z0-9_]+)\s*=\s*(\[\s*\{[\s\S]*?\n\s*\]);', vc_content):
    var_name = m.group(1)
    # count objects in array
    items = re.findall(r'\{\s*username:', m.group(2))
    # find pid if in name
    pid_m = re.search(r'_(\d+)$', var_name)
    if pid_m:
        creator_counts[int(pid_m.group(1))] = len(items)

for fpath in html_files:
    pid = int(re.search(r'produto-(\d+)', fpath).group(1))
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # check slider counter
    m_counter = re.search(r'class="slider-counter">([^<]+)</div>', content)
    counter_txt = m_counter.group(1).strip() if m_counter else 'N/A'
    
    # check number of img in slider-track
    m_track = re.search(r'<div class="slider-track">([\s\S]*?)</div>', content)
    if m_track:
        imgs = re.findall(r'<img\s+', m_track.group(1))
        num_imgs = len(imgs)
    else:
        num_imgs = 0
        
    title_m = re.search(r'<h1[^>]*product-title[^>]*>([\s\S]*?)</h1>', content)
    title = title_m.group(1).strip() if title_m else 'Sem título'
    title = re.sub(r'\s+', ' ', title)[:50]

    if num_imgs <= 1 or counter_txt in ['1 / 1', '1/1']:
        single_slide.append((pid, os.path.basename(fpath), counter_txt, num_imgs, title))

print(f"\n[*] PRODUTOS COM APENAS 1 FOTO NO SLIDER ({len(single_slide)} encontrados):")
for pid, fname, ctxt, n, t in single_slide[:25]:
    c_count = creator_counts.get(pid, 'N/A')
    print(f"  P{pid:02d}: Slider={n} foto(s) | Vídeos Criadores={c_count} | {t}")

print(f"\n[*] VÍDEOS DE CRIADORES POR CONTAGEM:")
low_creators = {k: v for k, v in creator_counts.items() if v <= 1}
print(f"  Total de produtos com apenas 1 vídeo de criador: {len(low_creators)}")
for pid, cnt in sorted(low_creators.items())[:20]:
    print(f"  P{pid:02d}: {cnt} vídeo")
