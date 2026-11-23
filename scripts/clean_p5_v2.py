import re

with open('pages/produto-5.html', 'r', encoding='utf-8') as f:
    h5 = f.read()

# Remove review-photos blocks containing review-5-c
h5 = re.sub(r'<div class="review-photos">\s*<img[^>]+review-5-c\d+[^>]+>.*?</div>', '', h5, flags=re.DOTALL)
h5 = re.sub(r'<div class="review-photos">\s*</div>', '', h5)

with open('pages/produto-5.html', 'w', encoding='utf-8') as f:
    f.write(h5)

print('P5 cleaned of video screenshots!')
