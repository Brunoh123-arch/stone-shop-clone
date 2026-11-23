# -*- coding: utf-8 -*-
import glob
import re

files = glob.glob('pages/produto-*.html')
zero_sold = []
for f in files:
    content = open(f, 'r', encoding='utf-8').read()
    m = re.search(r'(\d+[\.,]?\d*k?\s*vendidos?)', content, re.IGNORECASE)
    if m:
        text = m.group(1).lower()
        if '0 vendido' in text or '0 vend' in text:
            zero_sold.append((f, m.group(1)))

print(f"Total files with '0 vendido': {len(zero_sold)}")
for f, s in zero_sold:
    print(f"  {f}: {s}")
