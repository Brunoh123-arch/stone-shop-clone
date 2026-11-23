with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'camila', c, re.IGNORECASE)]
print(f"Total camila matches in videos-criadores.js: {len(matches)}")
for idx in matches[:10]:
    line_start = c.rfind('\n', 0, idx)
    line_end = c.find('\n', idx)
    # find which variable or dataset contains this line
    var_idx = c.rfind('const ', 0, idx)
    var_name = c[var_idx:var_idx+50].split('=')[0].strip() if var_idx != -1 else 'N/A'
    print(f"Dataset {var_name} | Line: {c[line_start:line_end].strip()[:80]}")
