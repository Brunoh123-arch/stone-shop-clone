with open('js/app.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
for w in ['camila', 'chinelo']:
    matches = [m.start() for m in re.finditer(re.escape(w), c, re.IGNORECASE)]
    for idx in matches:
        print(f"--- MATCH {w} ---")
        print(c[max(0, idx-100):min(len(c), idx+200)])
