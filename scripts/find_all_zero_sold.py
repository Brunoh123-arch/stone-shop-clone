# -*- coding: utf-8 -*-
import glob
import re

files = glob.glob('pages/produto-*.html')
all_zero = []
for f in files:
    content = open(f, 'r', encoding='utf-8').read()
    if re.search(r'>\s*0\s+vendidos?\s*<', content, re.IGNORECASE):
        all_zero.append(f)

print("Files with '> 0 vendidos <':", all_zero)
