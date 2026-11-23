with open('pages/produto-58.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if 'amazon' in line.lower()]
for m in matches:
    print(m)
