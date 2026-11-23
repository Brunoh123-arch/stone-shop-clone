import glob, re, json

files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))

count_fixable = 0
fixable_list = []
no_extra_imgs = []

for fpath in files:
    pid = int(re.search(r'produto-(\d+)', fpath).group(1))
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    m_track = re.search(r'<div class="slider-track">([\s\S]*?)</div>', c)
    num_imgs = len(re.findall(r'<img\s+', m_track.group(1))) if m_track else 0
    
    if num_imgs <= 1:
        img_m = re.search(r'imagens:\s*(\[[\s\S]*?\])\s*[,;}\n]', c)
        cat_len = 0
        cat_imgs = []
        if img_m:
            try:
                cat_imgs = json.loads(img_m.group(1))
                cat_imgs = [img for img in cat_imgs if not img.lower().endswith('.mp4')]
                cat_len = len(cat_imgs)
            except Exception:
                pass
        title_m = re.search(r'<h1[^>]*product-title[^>]*>([\s\S]*?)</h1>', c)
        t = title_m.group(1).strip() if title_m else ''
        t = re.sub(r'\s+', ' ', t)[:40]
        
        if cat_len > 1:
            count_fixable += 1
            fixable_list.append((pid, cat_len, fpath, cat_imgs, t))
        else:
            no_extra_imgs.append((pid, t, fpath))

print(f"Total com imagens já no PRODUTO_ATUAL prontas para ir pro slider: {len(fixable_list)}")
print(f"Total sem lista de imagens no PRODUTO_ATUAL (precisam de extração): {len(no_extra_imgs)}")
for pid, t, _ in no_extra_imgs:
    print(f"  P{pid:02d}: {t}")

