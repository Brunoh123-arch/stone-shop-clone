with open('pages/produto-76.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
reviews = re.findall(r'<div class="review-card".*?</div>\s*</div>', text, re.DOTALL)
print(f"P76 total review cards found: {len(reviews)}")
for idx, r in enumerate(reviews):
    print(f"\n--- REVIEW {idx+1} ---")
    print(r[:300])
