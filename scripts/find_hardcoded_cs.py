# -*- coding: utf-8 -*-
import glob
import re

html_files = glob.glob('pages/produto-*.html')
hardcoded_pages = []

for f in html_files:
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()
    
    m = re.search(r'<div[^>]*id=["\']creators-section["\'][^>]*>(.*?)</div\s*>', html, re.DOTALL)
    if m:
        inner = m.group(1).strip()
        if len(inner) > 10:
            hardcoded_pages.append((f, len(inner)))

print(f"Total de paginas com cards hardcoded dentro de #creators-section: {len(hardcoded_pages)}")
for p, length in hardcoded_pages:
    print(f"  [-] {p} ({length} caracteres de HTML hardcoded)")
