with open('pages/produto-19.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx = c.find('reviews-section')
sub = c[idx:idx+80000]

# achar o primeiro card de cliente
import re
cards = re.findall(r'<div style="[^"]*border-bottom[^"]*"[^>]*>(.*?)</div>\s*</div>', sub, re.DOTALL)
print("Total cards achados:", len(cards))
if cards:
    print("\n--- Card 1 ---")
    print(cards[0][:1000])
