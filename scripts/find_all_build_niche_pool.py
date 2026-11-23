with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = re.findall(r'case\s+(\d+):.*?activeDataset\s*=\s*(buildNichePool\([^;]+;)', c, re.DOTALL)
print(f"Total casos usando buildNichePool: {len(matches)}")
for num, call in matches:
    print(f"Produto {num}: {call.strip()}")
