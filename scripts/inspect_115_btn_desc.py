with open('pages/produto-115.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
m = re.search(r'class=["\'][^"\']*btn-toggle-desc[^"\']*["\'][^>]*>', html)
if m:
    print(m.group(0))
