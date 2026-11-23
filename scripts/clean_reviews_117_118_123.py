import re

# 1. P118: remove review-118-1 and review-118-2
with open('pages/produto-118.html', 'r', encoding='utf-8') as f:
    h118 = f.read()

h118 = re.sub(r'<div class="review-photos">\s*<img[^>]+review-118-[12]\.webp[^>]+>\s*</div>', '', h118)
# If single photos block has both
h118 = re.sub(r'<img[^>]+review-118-[12]\.webp[^>]+>', '', h118)
with open('pages/produto-118.html', 'w', encoding='utf-8') as f:
    f.write(h118)
print('P118 cleaned!')

# 2. P117: remove review-117-1 and review-117-4
with open('pages/produto-117.html', 'r', encoding='utf-8') as f:
    h117 = f.read()

h117 = re.sub(r'<div class="review-photos">\s*<img[^>]+review-117-[14]\.webp[^>]+>\s*</div>', '', h117)
h117 = re.sub(r'<img[^>]+review-117-[14]\.webp[^>]+>', '', h117)
with open('pages/produto-117.html', 'w', encoding='utf-8') as f:
    f.write(h117)
print('P117 cleaned!')

# 3. P123: remove review-123-1 and review-123-4
with open('pages/produto-123.html', 'r', encoding='utf-8') as f:
    h123 = f.read()

h123 = re.sub(r'<div class="review-photos">\s*<img[^>]+review-123-[14]\.webp[^>]+>\s*</div>', '', h123)
h123 = re.sub(r'<img[^>]+review-123-[14]\.webp[^>]+>', '', h123)
with open('pages/produto-123.html', 'w', encoding='utf-8') as f:
    f.write(h123)
print('P123 cleaned!')
