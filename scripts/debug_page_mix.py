import re

for pid in [108, 110, 113]:
    path = f'pages/produto-{pid}.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    title_m = re.search(r'<title>(.*?)</title>', html)
    title = title_m.group(1) if title_m else 'None'
    
    # Busca h1 ou product-title
    pt_m = re.search(r'class="product-title[^>]*>(.*?)</', html)
    pt = pt_m.group(1).strip() if pt_m else 'None'
    
    # Slider images
    slider_imgs = re.findall(r'<div class="slide[^>]*>\s*<img[^>]*src="([^"]+)"', html)
    if not slider_imgs:
        slider_imgs = re.findall(r'<div class="slider-track"[^>]*>.*?<img[^>]*src="([^"]+)"', html, re.DOTALL)
    
    # Scripts at the bottom
    scripts = re.findall(r'<script[^>]*src="([^"]+)"', html)
    
    # Inline scripts
    inline_scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', html, re.DOTALL)
    
    print(f"=== PRODUTO {pid} ===")
    print(f"Title: {title}")
    print(f"Product Title: {pt}")
    print(f"Slider Images: {slider_imgs[:3]}")
    print(f"Scripts: {scripts}")
    print(f"Inline script count: {len(inline_scripts)}")
    for i, s in enumerate(inline_scripts):
        if 'id' in s or 'catalogo' in s or 'load' in s or 'produto' in s:
            print(f"  Inline script {i+1} snippet: {s.strip()[:200]}")
    print()
