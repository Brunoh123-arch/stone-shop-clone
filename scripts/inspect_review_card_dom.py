import re

with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

m = re.search(r'<div class=["\']review-card["\'][^>]*>.*?</div>\s*</div>\s*</div>', c, re.DOTALL)
if m:
    print("Estrutura do Card em P19:")
    print(m.group(0)[:1200])
