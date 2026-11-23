import os, time, glob, re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ts = int(time.time() * 1000)
count = 0

files_to_update = glob.glob(os.path.join(ROOT_DIR, 'pages', 'produto-*.html')) + [
    os.path.join(ROOT_DIR, 'pages', 'resumo.html'),
    os.path.join(ROOT_DIR, 'pages', 'carrinho.html'),
    os.path.join(ROOT_DIR, 'pages', 'checkout.html'),
    os.path.join(ROOT_DIR, 'index.html'),
    os.path.join(ROOT_DIR, 'real.html'),
    os.path.join(ROOT_DIR, 'stone.html'),
    os.path.join(ROOT_DIR, 'admin.html')
]

for p in files_to_update:
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    
    orig = c
    
    # Safe regex for script/link tags only
    c = re.sub(r'(src=["\'][^"\']*?app)\.js(?:\?v=[^"\']*)?', r'\1.js?v=' + str(ts), c)
    c = re.sub(r'(href=["\'][^"\']*?style)\.css(?:\?v=[^"\']*)?', r'\1.css?v=' + str(ts), c)
    c = re.sub(r'(src=["\'][^"\']*?videos-criadores(?:-v3)?)\.js(?:\?v=[^"\']*)?', r'\1.js?v=' + str(ts), c)
    c = re.sub(r'(src=["\'][^"\']*?catalogo)\.js(?:\?v=[^"\']*)?', r'\1.js?v=' + str(ts), c)
    c = re.sub(r'(review-109-real-\d+\.(?:jpg|webp))(?:\?v=[^"\']*)?', r'\1?v=' + str(ts), c)
    c = re.sub(r'(review-114-(?:real|c\d)-\d+\.(?:jpg|webp))(?:\?v=[^"\']*)?', r'\1?v=' + str(ts), c)
    c = re.sub(r'(review-108-\d+\.(?:jpg|webp))(?:\?v=[^"\']*)?', r'\1?v=' + str(ts), c)
    c = re.sub(r'(guia-tamanhos-\d+\.png)(?:\?v=[^"\']*)?', r'\1?v=' + str(ts), c)
    c = re.sub(r'(seller-\d+\.png)(?:\?v=[^"\']*)?', r'\1?v=' + str(ts), c)
    c = re.sub(r'(mulher_\d+\.jpg)(?:\?v=[^"\']*)?', r'\1?v=' + str(ts), c)
    c = re.sub(r'(poster-chinelo-oficial\.jpg)(?:\?v=[^"\']*)?', r'\1?v=' + str(ts), c)
    
    if c != orig:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)
        count += 1

print(f'Atualizado cache buster global blindado em {count} arquivos HTML com ?v={ts}')
