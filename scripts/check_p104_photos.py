txt = open('pages/produto-104.html', encoding='utf-8').read()
import re
for m in re.finditer(r'<div class="review-photos"[^>]*>([\s\S]*?)</div>', txt):
    print("Found review-photos block:", m.group(0)[:300])
