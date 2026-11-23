import re

# 1. P101: Pneus Pirelli
with open('pages/produto-101.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'(id=["\']tt-product-video["\'][^>]*src=["\'])https://files\.catbox\.moe/8octvc\.mp4(["\'])', r'\g<1>https://files.catbox.moe/ukmosr.mp4\g<2>', c)
c = re.sub(r'(src=["\'])https://files\.catbox\.moe/8octvc\.mp4(["\'][^>]*id=["\']tt-product-video["\'])', r'\g<1>https://files.catbox.moe/ukmosr.mp4\g<2>', c)
with open('pages/produto-101.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("[OK] P101 description video updated to ukmosr.mp4")

# P9: Ar Condicionado HQ
with open('pages/produto-9.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'(id=["\']tt-product-video["\'][^>]*src=["\'])https://files\.catbox\.moe/t42yc4\.mp4(["\'])', r'\g<1>https://files.catbox.moe/p7r4vc.mp4\g<2>', c)
c = re.sub(r'(src=["\'])https://files\.catbox\.moe/t42yc4\.mp4(["\'][^>]*id=["\']tt-product-video["\'])', r'\g<1>https://files.catbox.moe/p7r4vc.mp4\g<2>', c)
with open('pages/produto-9.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("[OK] P9 description video updated to p7r4vc.mp4")

# 2. P111: Projetor Natalino
with open('pages/produto-111.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'(id=["\']tt-product-video["\'][^>]*src=["\'])https://files\.catbox\.moe/facj5t\.mp4(["\'])', r'\g<1>https://files.catbox.moe/d7tqme.mp4\g<2>', c)
c = re.sub(r'(src=["\'])https://files\.catbox\.moe/facj5t\.mp4(["\'][^>]*id=["\']tt-product-video["\'])', r'\g<1>https://files.catbox.moe/d7tqme.mp4\g<2>', c)
with open('pages/produto-111.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("[OK] P111 description video updated to d7tqme.mp4")

# 3. P121: Travesseiro Cervical
with open('pages/produto-121.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = re.sub(r'(id=["\']tt-product-video["\'][^>]*src=["\'])https://files\.catbox\.moe/55n8uo\.mp4(["\'])', r'\g<1>https://files.catbox.moe/0trj7i.mp4\g<2>', c)
c = re.sub(r'(src=["\'])https://files\.catbox\.moe/55n8uo\.mp4(["\'][^>]*id=["\']tt-product-video["\'])', r'\g<1>https://files.catbox.moe/0trj7i.mp4\g<2>', c)
c = re.sub(r'poster-produto-117\.jpg', r'poster-produto-121.jpg', c)
with open('pages/produto-121.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("[OK] P121 description video updated to 0trj7i.mp4")

# 4. Products 118, 119, 120, 122, 123
updates = [
    {
        'pid': 118,
        'title': 'Conjunto Sala de Jantar Mesa com 4 Cadeiras Estofadas Veludo Slim',
        'prefix': 'mesa-jantar-slide-',
        'count': 5,
        'vid': 'https://files.catbox.moe/uhw9mi.mp4',
        'poster': '../videosprodutos/posters/poster-produto-118.jpg'
    },
    {
        'pid': 119,
        'title': 'Combo Fardo Mega Fraldas Huggies Supreme Care & Pampers Pants',
        'prefix': 'fraldas-slide-',
        'count': 5,
        'vid': 'https://files.catbox.moe/6prl09.mp4',
        'poster': '../videosprodutos/posters/poster-produto-119.jpg'
    },
    {
        'pid': 120,
        'title': 'Sofá Retrátil e Reclinável 3 Lugares 2,10m Suede Veludo Premium',
        'prefix': 'sofa-slide-',
        'count': 4,
        'vid': 'https://files.catbox.moe/qdufjg.mp4',
        'poster': '../videosprodutos/posters/poster-produto-120.jpg'
    },
    {
        'pid': 122,
        'title': 'Panela de Pressão Elétrica Digital 5L Painel Touch Multifunções Inox',
        'prefix': 'panela-pressao-slide-',
        'count': 4,
        'vid': 'https://files.catbox.moe/h6lcpu.mp4',
        'poster': '../videosprodutos/posters/poster-produto-122.jpg'
    },
    {
        'pid': 123,
        'title': 'Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta',
        'prefix': 'lavadora-slide-',
        'count': 4,
        'vid': 'https://files.catbox.moe/iopyod.mp4',
        'poster': '../videosprodutos/posters/poster-produto-123.jpg'
    }
]

for up in updates:
    pid = up['pid']
    p_path = f'pages/produto-{pid}.html'
    with open(p_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Update Video & Poster
    html = re.sub(r'(id=["\']tt-product-video["\'][^>]*src=["\'])https://files\.catbox\.moe/55n8uo\.mp4(["\'])', rf'\g<1>{up["vid"]}\g<2>', html)
    html = re.sub(r'(src=["\'])https://files\.catbox\.moe/55n8uo\.mp4(["\'][^>]*id=["\']tt-product-video["\'])', rf'\g<1>{up["vid"]}\g<2>', html)
    html = re.sub(r'poster-produto-117\.jpg', f'poster-produto-{pid}.jpg', html)
    
    # 2. Update Slider track
    # Generate new slides HTML
    slides_html = []
    for i in range(1, up['count'] + 1):
        fetch_attr = 'decoding="async" fetchpriority="high"' if i == 1 else 'decoding="async" loading="lazy"'
        slides_html.append(f'<img alt="{up["title"]} - {i}" class="slider-img" {fetch_attr} onerror="this.style.display=\'none\'" src="../img/{up["prefix"]}{i}.webp"/>')
    
    # Replace slider-track contents
    pattern = r'(<div class="slider-track">)[\s\S]*?(<div class="slider-counter">)'
    replacement = r'\1\n' + '\n'.join(slides_html) + rf'\n\2'
    html = re.sub(pattern, replacement, html)
    
    # Update counter
    html = re.sub(r'<div class="slider-counter">\s*1\s*/\s*\d+\s*</div>', f'<div class="slider-counter">1 / {up["count"]}</div>', html)
    
    with open(p_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"[OK] P{pid} slides & video updated cleanly!")
