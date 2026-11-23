with open('pages/produto-75.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
matches = re.findall(r'<div class="review-card".*?<div class="review-photos">.*?</div>.*?</div>\s*</div>', text, re.DOTALL)
for m in matches:
    print("--- CARD WITH PHOTOS ---")
    print(m)
