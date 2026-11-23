# -*- coding: utf-8 -*-
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    txt = f.read()

import re
cases = re.findall(r'case\s+(\d+):\s+activeDataset\s*=\s*([A-Za-z0-9_]+);', txt)
for pid, ds in cases:
    if pid in ['57', '73', '81']:
        print(pid, '->', ds)
        # Mostrar o que tem em ds
        m = re.findall(rf'const\s+{ds}\s*=\s*([A-Za-z0-9_]+)\.map', txt)
        print('  Source map:', m)
