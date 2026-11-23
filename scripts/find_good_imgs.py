import re

missing_ids = [6, 9, 20, 25, 36, 50, 53, 55, 56, 59, 65, 82, 89, 94, 96, 97, 100, 101, 102, 106, 107, 118, 119, 120, 121, 122, 123, 124]

for pid in missing_ids:
    hpath = f'pages/produto-{pid}.html'
    with open(hpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # Buscar todas as imagens jpg/webp/png
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
    # Filtrar imagens relevantes (ignorar logo, icons, flags, reviews)
    good_imgs = [i for i in imgs if not any(k in i.lower() for k in ['logo', 'icon', 'star', 'review', 'avatar', 'selo', 'flag', 'bandeira'])]
    
    print(f"P#{pid:03d} (total {len(imgs)} imgs) -> Boas: {good_imgs[:3]}")
