# -*- coding: utf-8 -*-
import re

html = open('pages/produto-87.html', 'r', encoding='utf-8').read()

# Procura o bloco de rating / reviews / vendidos no topo
m = re.search(r'class=["\']product-rating[\s\S]*?</div>\s*</div>', html)
if m:
    print("product-rating block:")
    print(m.group(0))

# Procura qualquer coisa com "avali" ou "vend"
matches = re.findall(r'<div[^>]*class=["\'][^"\']*(?:rating|review|sold|vendido|sales)[^"\']*["\'][^>]*>[\s\S]*?</div>', html)
for i, x in enumerate(matches[:5]):
    print(f"Match {i}: {x}")
