with open('pages/produto-75.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
rev_cards = re.findall(r'<div class="review-card".*?</div>\s*</div>', text, re.DOTALL)
for idx, r in enumerate(rev_cards[:5]):
    print(f"--- P75 Review {idx+1} ---")
    print(r[:250])
