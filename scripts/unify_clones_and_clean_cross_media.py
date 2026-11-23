import re, json, os
from bs4 import BeautifulSoup

def main():
    print("=== UNIFICANDO OS 5 PRODUTOS CLONES E EXPURGANDO DUPLICATAS ===")
    
    # 1. ATUALIZAR OS 5 PRODUTOS MASTER COM DADOS CONSOLIDADOS
    
    # Pair 1: P34 (Master) <- P79 (Clone) [Lava-Loucas Praxis]
    print("\n--- 1. Unificando Lava-Loucas Praxis (P34 <- P79) ---")
    with open('pages/produto-79.html', 'r', encoding='utf-8') as f:
        p79_html = f.read()
    p79_soup = BeautifulSoup(p79_html, 'html.parser')
    p79_reviews = p79_soup.find('div', class_='reviews-section')
    
    with open('pages/produto-34.html', 'r', encoding='utf-8') as f:
        p34_html = f.read()
    p34_soup = BeautifulSoup(p34_html, 'html.parser')
    
    # Se P79 tem mais reviews que P34, injetar as reviews de P79 em P34 mantendo ID 34
    if p79_reviews and len(p79_soup.find_all('div', class_='review-card')) > len(p34_soup.find_all('div', class_='review-card')):
        old_rev = p34_soup.find('div', class_='reviews-section')
        if old_rev:
            old_rev.replace_with(p79_reviews)
            # Atualizar caminhos e referencias se houver
            p34_html = str(p34_soup)
            with open('pages/produto-34.html', 'w', encoding='utf-8') as f:
                f.write(p34_html)
            print("  P34 atualizado com reviews consolidadas de P79.")
            
    # Pair 2: P80 (Master) <- P84 (Clone) [Panificadora Gallant 19 Programas]
    print("\n--- 2. Unificando Panificadora Gallant (P80 <- P84) ---")
    with open('pages/produto-80.html', 'r', encoding='utf-8') as f:
        p80_html = f.read()
    p80_soup = BeautifulSoup(p80_html, 'html.parser')
    h1_p80 = p80_soup.find('h1')
    if h1_p80:
        h1_p80.string = "Panificadora 19 Programas Gallant 600w Inox / Antiaderente Bivolt (Branca ou Preta)"
    title_p80 = p80_soup.find('title')
    if title_p80:
        title_p80.string = "Panificadora 19 Programas Gallant 600w Inox / Antiaderente Bivolt - Stone Shop"
    with open('pages/produto-80.html', 'w', encoding='utf-8') as f:
        f.write(str(p80_soup))
    print("  P80 atualizado como mestre para cores Branca e Preta.")

    # Pair 3: P73 (Master) <- P81 (Clone) [Caixa WAAW Hyperboom 1000]
    print("\n--- 3. Unificando Caixa WAAW Hyperboom 1000 (P73 <- P81) ---")
    with open('pages/produto-81.html', 'r', encoding='utf-8') as f:
        p81_html = f.read()
    p81_soup = BeautifulSoup(p81_html, 'html.parser')
    p81_reviews = p81_soup.find('div', class_='reviews-section')
    
    with open('pages/produto-73.html', 'r', encoding='utf-8') as f:
        p73_html = f.read()
    p73_soup = BeautifulSoup(p73_html, 'html.parser')
    h1_p73 = p73_soup.find('h1')
    if h1_p73:
        h1_p73.string = "Caixa de Som Bluetooth WAAW by Alok Hyperboom 1000 180W IPX7 TWS Bivolt"
    title_p73 = p73_soup.find('title')
    if title_p73:
        title_p73.string = "Caixa de Som Bluetooth WAAW by Alok Hyperboom 1000 180W IPX7 TWS Bivolt - Stone Shop"
    if p81_reviews:
        old_rev = p73_soup.find('div', class_='reviews-section')
        if old_rev:
            old_rev.replace_with(p81_reviews)
    with open('pages/produto-73.html', 'w', encoding='utf-8') as f:
        f.write(str(p73_soup))
    print("  P73 atualizado com título completo e reviews de P81.")

    # Pair 4: P61 (Master) <- P83 (Clone) [Caixa Joog Break X1 com Tela Touch]
    print("\n--- 4. Unificando Caixa Joog Break X1 (P61 <- P83) ---")
    with open('pages/produto-61.html', 'r', encoding='utf-8') as f:
        p61_html = f.read()
    p61_soup = BeautifulSoup(p61_html, 'html.parser')
    h1_p61 = p61_soup.find('h1')
    if h1_p61:
        h1_p61.string = "Caixa de Som Joog Amplificada Break X1 c/ Tela Touch 13 800W Bivolt com 2 Microfones Sem Fio"
    with open('pages/produto-61.html', 'w', encoding='utf-8') as f:
        f.write(str(p61_soup))
    print("  P61 consolidado como mestre.")

    # Pair 5: P47 (Master) <- P78 (Clone) [Extratora Portatil]
    print("\n--- 5. Unificando Extratora Portatil (P47 <- P78) ---")
    with open('pages/produto-47.html', 'r', encoding='utf-8') as f:
        p47_html = f.read()
    p47_soup = BeautifulSoup(p47_html, 'html.parser')
    h1_p47 = p47_soup.find('h1')
    if h1_p47:
        h1_p47.string = "Extratora e Higienizadora Portátil WAP Spot Cleaner 1400W Borrifa Esfrega e Extrai Sujeira"
    with open('pages/produto-47.html', 'w', encoding='utf-8') as f:
        f.write(str(p47_soup))
    print("  P47 consolidado como mestre.")

    # 2. INJETAR REDIRECIONAMENTO LIMPO NAS PÁGINAS CLONES
    redirect_pairs = [
        (79, 34, "Lava Louças Praxis"),
        (84, 80, "Panificadora Gallant"),
        (81, 73, "Caixa WAAW Hyperboom"),
        (83, 61, "Caixa Joog Break X1"),
        (78, 47, "Extratora Portatil")
    ]
    for clone_id, master_id, name in redirect_pairs:
        clone_file = f'pages/produto-{clone_id}.html'
        redir_html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0; url=produto-{master_id}.html">
<title>Redirecionando - Stone Shop</title>
<script>window.location.replace("produto-{master_id}.html");</script>
</head>
<body>
<p>Redirecionando para a versão oficial de <a href="produto-{master_id}.html">{name}</a>...</p>
</body>
</html>'''
        with open(clone_file, 'w', encoding='utf-8') as f:
            f.write(redir_html)
        print(f"  Página clone {clone_file} convertida para redirect 0s para produto-{master_id}.html.")

    # 3. EXPURGAR OS CLONES DE js/catalogo.js
    print("\n--- 3. Expurgo dos 5 clones de js/catalogo.js ---")
    with open('js/catalogo.js', 'r', encoding='utf-8') as f:
        cat_lines = f.readlines()
        
    clones_to_remove = {79, 84, 81, 83, 78}
    new_cat_lines = []
    removed_count = 0
    for line in cat_lines:
        m = re.search(r'id:\s*(\d+)', line)
        if m and int(m.group(1)) in clones_to_remove:
            removed_count += 1
            print(f"  Removido ID {m.group(1)} de js/catalogo.js")
            continue
        new_cat_lines.append(line)
        
    with open('js/catalogo.js', 'w', encoding='utf-8') as f:
        f.writelines(new_cat_lines)
    print(f"  Total de clones expurgados de catalogo.js: {removed_count}")

    # Atualizar títulos dos mestres no catalogo.js
    with open('js/catalogo.js', 'r', encoding='utf-8') as f:
        cat_text = f.read()
    
    # Atualizar P80
    cat_text = re.sub(
        r"(\{id:80,nome:')[^']+(',preco:)",
        r"\g<1>Panificadora 19 Programas Gallant 600w Inox / Antiaderente (Branca ou Preta)\g<2>",
        cat_text
    )
    # Atualizar P73
    cat_text = re.sub(
        r"(\{id:73,nome:')[^']+(',preco:)",
        r"\g<1>Caixa de Som Bluetooth WAAW by Alok Hyperboom 1000 180W IPX7 TWS Bivolt\g<2>",
        cat_text
    )
    # Atualizar P47
    cat_text = re.sub(
        r"(\{id:47,nome:')[^']+(',preco:)",
        r"\g<1>Extratora e Higienizadora Portátil WAP Spot Cleaner 1400W Borrifa Esfrega e Extrai\g<2>",
        cat_text
    )
    with open('js/catalogo.js', 'w', encoding='utf-8') as f:
        f.write(cat_text)

    # 4. EXPURGAR OS CLONES DE index.html
    print("\n--- 4. Expurgo dos 5 clones de index.html ---")
    with open('index.html', 'r', encoding='utf-8') as f:
        index_html = f.read()
        
    soup = BeautifulSoup(index_html, 'html.parser')
    cards_removed = 0
    for cid in clones_to_remove:
        target_href = f'pages/produto-{cid}.html'
        links = soup.find_all('a', href=re.compile(r'pages/produto-' + str(cid) + r'\.html'))
        for a in links:
            # O card pode ser o <a> ou o parent dele
            card = a.find_parent('div', class_=re.compile(r'card')) or a
            card.decompose()
            cards_removed += 1
            print(f"  Removido card do clone P{cid} de index.html")
            
    # Garantir que P104 e P13 nao estejam duplicados dentro da mesma secao recommended-grid
    rec_grid = soup.find(id='recommended-grid')
    if rec_grid:
        seen_pids = set()
        for a in rec_grid.find_all('a', href=re.compile(r'pages/produto-(\d+)\.html')):
            m = re.search(r'produto-(\d+)\.html', a['href'])
            if m:
                pid = int(m.group(1))
                if pid in seen_pids:
                    print(f"  Removida duplicata interna no grid recomendado: P{pid}")
                    a.decompose()
                else:
                    seen_pids.add(pid)
                    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"  Total de cards clones removidos de index.html: {cards_removed}")

    # 5. SINCRONIZAR CLONES DE index.html (real.html, stone.html, api/stone_content.js)
    print("\n--- 5. Sincronizando real.html, stone.html e APIs ---")
    with open('index.html', 'r', encoding='utf-8') as f:
        synced_html = f.read()
    with open('real.html', 'w', encoding='utf-8') as f:
        f.write(synced_html)
    with open('stone.html', 'w', encoding='utf-8') as f:
        f.write(synced_html)
    with open('api/stone_content.js', 'w', encoding='utf-8') as f:
        f.write('module.exports = ' + json.dumps(synced_html) + ';\n')
    with open('api/_lib/stone_content.js', 'w', encoding='utf-8') as f:
        f.write('module.exports = ' + json.dumps(synced_html) + ';\n')
    print("  Sincronizacao concluida.")

    # 6. EXPURGAR VÍDEOS CRUZADOS NOS PRODUTOS ÓBVIOS
    print("\n--- 6. Expurgo de videos cruzados em HTML ---")
    # P100 (iPhone 15) com video de Tablet Stitch (8octvc.mp4)
    # P36 (Poco X7) com video de Tablet Stitch (8octvc.mp4)
    for bad_pid in [100, 36]:
        p_path = f'pages/produto-{bad_pid}.html'
        with open(p_path, 'r', encoding='utf-8') as f:
            c = f.read()
        p_soup = BeautifulSoup(c, 'html.parser')
        v = p_soup.find('video', id='tt-product-video')
        if v and '8octvc.mp4' in v.get('src', ''):
            v_block = v.find_parent('div', class_='product-video-block')
            if v_block:
                v_block.decompose()
                with open(p_path, 'w', encoding='utf-8') as f:
                    f.write(str(p_soup))
                print(f"  Removido bloco de video falso do Stitch de P{bad_pid}!")

    # P38 (Perfume Yara Lattafa) com video de calca jeans (80bwka.mp4)
    with open('pages/produto-38.html', 'r', encoding='utf-8') as f:
        c = f.read()
    p38_soup = BeautifulSoup(c, 'html.parser')
    v = p38_soup.find('video', id='tt-product-video')
    if v and '80bwka.mp4' in v.get('src', ''):
        v_block = v.find_parent('div', class_='product-video-block')
        if v_block:
            v_block.decompose()
            with open('pages/produto-38.html', 'w', encoding='utf-8') as f:
                f.write(str(p38_soup))
            print("  Removido bloco de video de calca jeans do Perfume Yara P38!")

    # P40 (Micro-ondas Mondial) com video de panela de pressao (t5xtp1.mp4)
    with open('pages/produto-40.html', 'r', encoding='utf-8') as f:
        c = f.read()
    p40_soup = BeautifulSoup(c, 'html.parser')
    v = p40_soup.find('video', id='tt-product-video')
    if v and 't5xtp1.mp4' in v.get('src', ''):
        v_block = v.find_parent('div', class_='product-video-block')
        if v_block:
            v_block.decompose()
            with open('pages/produto-40.html', 'w', encoding='utf-8') as f:
                f.write(str(p40_soup))
            print("  Removido bloco de video de panela de pressao do Micro-ondas P40!")

    # P76 e P91: Expurgo de fotos de forno eletrico HQ nas avaliacoes
    print("\n--- 7. Expurgo de fotos de forno eletrico em Aparelho de Jantar (P76) e Pipoqueira (P91) ---")
    for bad_pid in [76, 91]:
        p_path = f'pages/produto-{bad_pid}.html'
        with open(p_path, 'r', encoding='utf-8') as f:
            c = f.read()
        p_soup = BeautifulSoup(c, 'html.parser')
        rev_sec = p_soup.find('div', class_='reviews-section')
        if rev_sec:
            # encontrar imgs com forno-hq ou shopee oven
            oven_imgs = rev_sec.find_all('img', src=re.compile(r'forno-hq|br-11134207-7r98o-lqnmb7oulw6f02|sg-11134201-7rceh-lrrqafsspb32c2|sg-11134201-7reng-m1ya6at9aqw05a|sg-11134201-7reoq-m8kskp1ohv2vcf'))
            for oi in oven_imgs:
                parent_photos = oi.find_parent('div', class_='review-photos')
                oi.decompose()
                if parent_photos and len(parent_photos.find_all('img')) == 0:
                    parent_photos.decompose()
            with open(p_path, 'w', encoding='utf-8') as f:
                f.write(str(p_soup))
            print(f"  Fotos de forno eletrico purgadas das avaliacoes de P{bad_pid}!")

    print("\n=== UNIFICACAO E HIGIENIZACAO CONCLUIDA COM SUCESSO! ===")

if __name__ == '__main__':
    main()
