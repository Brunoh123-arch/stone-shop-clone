with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    h104 = f.read()

with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    h33 = f.read()

import re

for label, html in [('104', h104), ('33', h33)]:
    print(f"\n=== BLOCOS DE P{label} ===")
    matches = re.findall(r'<div[^>]+class=["\']([^"\']+)["\']', html)
    for m in matches:
        first_cls = m.split()[0]
        if any(w in first_cls for w in ['header', 'slider', 'price', 'product-info', 'protection', 'protecao', 'creators', 'review', 'seller', 'store', 'about', 'details', 'video', 'description', 'related', 'bottom']):
            print(f"  P{label}: {first_cls}")
