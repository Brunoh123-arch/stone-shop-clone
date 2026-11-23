import glob, re, os

female_files = [
    'pages/produto-28.html',
    'pages/produto-38.html',
    'pages/produto-39.html',
    'pages/produto-45.html',
    'pages/produto-87.html',
    'pages/produto-88.html',
    'pages/produto-103.html',
    'pages/produto-104.html',
    'pages/produto-106.html',
    'pages/produto-108.html',
    'pages/produto-109.html',
]

print("=== AUDITORIA DAS AVALIAÇÕES NOS PRODUTOS FEMININOS ===")

for p in female_files:
    if not os.path.exists(p):
        continue
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    
    # Extrair todos os cards de review
    cards = html.split('class="review-card"')
    print(f"\n[{p}] - {len(cards)-1} reviews encontradas")
    
    shopee_terms = ['aroma:', 'usabilidade:', 'forma e tamanho:', 'shopee', 'moedas', 'pontos', 'desempenho:']
    shopee_found = 0
    non_female_avatars = 0
    
    for idx, card in enumerate(cards[1:], 1):
        m_img = re.search(r'<img[^>]+src="([^"]+)"', card)
        m_name = re.search(r'class="review-user-name">([^<]+)<', card)
        m_comm = re.search(r'class="review-comment">([^<]+)<', card)
        
        img = m_img.group(1) if m_img else ''
        name = m_name.group(1) if m_name else ''
        comm = m_comm.group(1) if m_comm else ''
        
        # Checar se avatar e de mulheres_validadas
        if 'mulheres_validadas' not in img:
            non_female_avatars += 1
            print(f"  ALERTA AVATAR #{idx}: {name} -> {img}")
        
        # Checar shopee
        if any(t in comm.lower() for t in shopee_terms):
            shopee_found += 1
            print(f"  ALERTA SHOPEE #{idx}: {comm[:70]}")

    print(f"  Resumo {p}: {non_female_avatars} avatares fora de mulheres_validadas | {shopee_found} textos formato Shopee")
