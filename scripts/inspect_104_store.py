with open('pages/produto-104.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = list(re.finditer(r'(?:seller|loja|stone)', html, re.I))
print("Occurrences in 104:", len(matches))
for m in matches[:10]:
    line_no = html[:m.start()].count('\n') + 1
    print(f"Line {line_no}: {html[m.start()-20:m.start()+60]}")
