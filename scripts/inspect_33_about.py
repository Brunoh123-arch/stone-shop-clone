with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = list(re.finditer(r'<div[^>]+class=["\'][^"\']*about-product-section', html))
print("HTML occurrences of about-product-section:", len(matches))
for m in matches:
    print("Match at line:", html[:m.start()].count('\n')+1)
    print(html[m.start():m.start()+1500])
