import re

missing_ids = [6, 9, 20, 25, 36, 50, 53, 55, 56, 59, 65, 82, 89, 94, 96, 97, 100, 101, 102, 106, 107, 118, 119, 120, 121, 122, 123, 124]

cards_data = []
for pid in missing_ids:
    hpath = f'pages/produto-{pid}.html'
    with open(hpath, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # 1. Titulo
    m_title = re.search(r'<title>([^<]+)</title>', html)
    t = m_title.group(1).strip() if m_title else f'Produto {pid}'
    t = re.sub(r'\s*-\s*Stone\s*Shop.*$', '', t, flags=re.I)
    
    # 2. Imagem principal
    # Procurar primeiro no swiper
    m_img = re.search(r'<div class="swiper-slide"[^>]*>.*?<img[^>]+src="([^"]+)"', html, re.DOTALL)
    if not m_img:
        m_img = re.search(r'<img[^>]+class="product-main-img"[^>]+src="([^"]+)"', html)
    if not m_img:
        m_img = re.search(r'<img[^>]+src="([^"]+)"[^>]+class="product-main-img"', html)
    if not m_img:
        # pegar primeira imagem do body
        m_img = re.search(r'<main.*?>.*?<img[^>]+src="([^"]+)"', html, re.DOTALL)
        
    img_src = m_img.group(1) if m_img else 'img/logo.png'
    # Ajustar caminho relativo de ../img para img
    if img_src.startswith('../'):
        img_src = img_src[3:]
        
    # 3. Preco
    m_preco = re.search(r'class="price-cur"[^>]*>.*?R\$\s*([\d,.]+)', html, re.DOTALL)
    if not m_preco:
        m_preco = re.search(r'R\$\s*([\d,.]+)', html)
    preco_cur = m_preco.group(1).strip() if m_preco else '99,90'
    
    # 4. Preco antigo
    m_old = re.search(r'class="price-old"[^>]*>.*?R\$\s*([\d,.]+)', html, re.DOTALL)
    preco_old = m_old.group(1).strip() if m_old else '199,90'
    
    # 5. Desconto
    m_disc = re.search(r'class="price-discount"[^>]*>([^<]+)<', html)
    disc = m_disc.group(1).strip() if m_disc else '-50%'
    
    # 6. Vendas
    m_sales = re.search(r'([\d.]+[Kk]?\s*vendido\(s\))', html)
    sales = m_sales.group(1) if m_sales else '1.2K vendido(s)'
    
    cards_data.append({
        'id': pid,
        'title': t,
        'img': img_src,
        'price_cur': preco_cur,
        'price_old': preco_old,
        'disc': disc,
        'sales': sales
    })
    print(f"P#{pid:03d}: {t[:40]} | R$ {preco_cur} | {img_src[:40]}")

print(f"\nTotal extraído com sucesso: {len(cards_data)} produtos!")
