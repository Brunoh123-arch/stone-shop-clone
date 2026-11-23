# -*- coding: utf-8 -*-
import re

text = open('js/videos-criadores-v3.js', 'r', encoding='utf-8').read()
for pid in [47, 49, 78]:
    m = re.search(r'case\s+["\']?' + str(pid) + r'["\']?:[\s\S]*?break;', text)
    if m:
        print(f"P{pid}: {m.group(0)}")
