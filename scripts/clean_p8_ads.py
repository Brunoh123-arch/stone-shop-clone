import re

filepath = 'pages/produto-8.html'
with open(filepath, 'r', encoding='utf-8') as f:
    html = f.read()

# Bad images in P8: c1, c4, c6, c7, c9, c10, c11, c12, c13, c14, c15
bad_indices = [1, 4, 6, 7, 9, 10, 11, 12, 13, 14, 15]

for idx in bad_indices:
    pattern = rf'<div class="review-photos">\s*<img[^>]+review-8-c{idx}-1\.jpg[^>]+>\s*</div>'
    html = re.sub(pattern, '', html)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(html)

print('P8 cleaned of promotional ad banners in reviews!')
