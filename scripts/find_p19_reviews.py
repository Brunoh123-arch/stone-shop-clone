import re

with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Procurar onde fica a seção de reviews
m = re.search(r'<div[^>]+id=["\']reviews-container["\'][^>]*>(.*?)</div>', c, re.DOTALL)
if not m:
    m = re.search(r'class=["\']reviews-section["\'][^>]*>(.*?)</section>', c, re.DOTALL)
if not m:
    m = re.search(r'class=["\']reviews-section["\'][^>]*>(.*?)<!--', c, re.DOTALL)

if m:
    print("Reviews section length:", len(m.group(0)))
    print(m.group(0)[:1500])
else:
    print("Não achou reviews-section com regex")
