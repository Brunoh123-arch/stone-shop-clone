import os, re, json

pages = [f"pages/produto-{i}.html" for i in range(1, 115) if os.path.exists(f"pages/produto-{i}.html")]

catalog = []
for p in pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()

    # Extrai o titulo H1 ou Title
    m_h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.DOTALL)
    if m_h1:
        title = re.sub(r'<[^>]+>', '', m_h1.group(1)).strip()
    else:
        m_t = re.search(r'<title>(.*?)</title>', html)
        title = m_t.group(1).strip() if m_t else 'Sem Titulo'

    # Preco
    m_price = re.search(r'class="[^"]*price-current[^"]*"[^>]*>(.*?)</div>', html)
    price = m_price.group(1).strip() if m_price else 'N/A'

    # Tem criadores
    has_creators = ('videos-criadores.js' in html) or ('carousel-video' in html)

    # Reviews
    rev_count = html.count('class="review-card"')

    # Shopee / Padrao
    has_shopee = 'susercontent.com' in html
    has_padrao = ('· Padrão' in html) or ('>Padrão<' in html)

    catalog.append({
        'id': int(re.search(r'\d+', p).group()),
        'file': p,
        'title': title,
        'price': price,
        'creators': has_creators,
        'reviews': rev_count,
        'shopee': has_shopee,
        'padrao': has_padrao
    })

catalog.sort(key=lambda x: x['id'])

with open('catalog_classified.json', 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)

print(f"Total auditado: {len(catalog)} produtos.")
