with open('scripts/pdf_extracted.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find sections
pages = text.split('--- PAGE ')

for p in pages[1:]:
    lines = p.split('\n')
    header = lines[0] if lines else ''
    content = '\n'.join(lines[1:15])
    print(f'=== PAGE {header} ===')
    # search for key tables or product mentions
    prod_matches = re.findall(r'(produto-\d+|Produto \d+|\b\d{1,3}\b)', '\n'.join(lines[:5]))
    print(lines[1:5])
