with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'function openTikTokVideo', c)]
for idx in matches:
    print(c[idx:idx+1500])
