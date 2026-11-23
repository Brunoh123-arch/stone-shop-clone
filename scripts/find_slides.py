import re
import os

def get_product_slide1(pid):
    path = f'pages/produto-{pid}.html'
    if not os.path.exists(path):
        return 'NOT_FOUND'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    m = re.findall(r'<div class="slider-track">[\s\S]*?</div>', html)
    if m:
        imgs = re.findall(r'src="([^"]+)"', m[0])
        return imgs[0] if imgs else 'NONE'
    return 'NO_TRACK'

for p in [9, 10, 24, 68, 95]:
    slide1 = get_product_slide1(p)
    print(f'Product {p} primary slide1: {slide1}')
