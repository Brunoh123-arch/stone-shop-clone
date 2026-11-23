# -*- coding: utf-8 -*-
import re

text = open('js/videos-criadores-v3.js', 'r', encoding='utf-8').read()
ids = [6, 12, 20, 21, 87, 94]

for pid in ids:
    pat = r'(case\s+["\']?' + str(pid) + r'["\']?:[\s\S]*?)(case\s+|default:)'
    m = re.search(pat, text)
    if m:
        block = m.group(1).strip()
        print(f"--- P{pid} ---")
        print(block[:200])
    else:
        print(f"P{pid} not found")
