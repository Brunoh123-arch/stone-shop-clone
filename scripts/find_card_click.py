with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'card\.addEventListener\([\'\"]click[\'\"]', c)]
for idx in matches:
    print(c[max(0, idx-50):min(len(c), idx+400)])
    print('='*50)
