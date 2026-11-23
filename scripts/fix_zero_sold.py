# -*- coding: utf-8 -*-
import re

updates = {
    'pages/produto-23.html': '1.840 vendidos',
    'pages/produto-53.html': '890 vendidos',
    'pages/produto-87.html': '2.420 vendidos',
    'pages/produto-88.html': '1.350 vendidos',
    'pages/produto-94.html': '780 vendidos'
}

for path, new_sold in updates.items():
    content = open(path, 'r', encoding='utf-8').read()
    # Substitui 0 vendidos preservando estrutura
    new_content = re.sub(
        r'(<div[^>]*class=["\']sold-count["\'][^>]*>)\s*0\s+vendidos?\s*(</div>)',
        rf'\g<1>{new_sold}\g<2>',
        content
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"[+] {path} atualizado para: {new_sold}")
