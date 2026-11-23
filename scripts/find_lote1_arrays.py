# -*- coding: utf-8 -*-
with open('js/videos-criadores-v3.js', 'r', encoding='utf-8') as f:
    txt = f.read()

import re
for pid in [57, 58, 60, 61, 73, 85]:
    m = re.findall(rf'const\s+([A-Za-z0-9_]*{pid}[A-Za-z0-9_]*_VIDEOS_MAP)\s*=', txt)
    print(f"P{pid} array name:", m)
