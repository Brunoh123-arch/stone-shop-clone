with open('pages/produto-115.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<script[\s\S]*?</script>', html)
for s in matches:
    if 'toggleProductDescription' in s or 'toggleProductDetails' in s or 'toggleDescricao' in s:
        print("--- SCRIPT FOUND IN 115 ---")
        print(s)
