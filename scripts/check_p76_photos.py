with open('pages/produto-76.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
rev_photos = re.findall(r'<div class="review-photos".*?</div>', text, re.DOTALL)
for rp in rev_photos:
    print(rp)
