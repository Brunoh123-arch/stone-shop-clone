# -*- coding: utf-8 -*-
import re

text = open('js/videos-criadores-v3.js', 'r', encoding='utf-8').read()
m = re.search(r'const\s+WAP_EXTRATORA_78_VIDEOS_MAP\s*=\s*\[([\s\S]*?)\];', text)
if m:
    print(m.group(0))
