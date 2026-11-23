with open('pages/produto-33.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
revs = re.findall(r'<div class="review-card"[\s\S]*?</div>\s*</div>', html)
print(f"Total reviews in 33: {len(revs)}")
for i, r in enumerate(revs):
    author = re.search(r'data-author-name="([^"]+)"', r)
    stars = re.search(r'data-author-stars="([^"]+)"', r)
    photo = 'review-photo' in r
    print(f"Review {i+1}: {author.group(1) if author else 'None'} | {stars.group(1) if stars else 'None'} stars | Has photo: {photo}")
