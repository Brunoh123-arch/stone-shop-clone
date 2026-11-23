with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re
matches = re.findall(r'.{0,50}(?:display\s*=\s*[\'"]none[\'"]|remove\(\)|hide|hidden).{0,50}', js)
for m in matches[:15]:
    print('-->', m.strip())
