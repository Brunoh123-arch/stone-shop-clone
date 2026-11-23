import re

for pid, pat in [(21, r'<div class="review-photos">\s*<img[^>]+review-21-c3-1[^>]+>\s*</div>'),
                 (74, r'<div class="review-photos">\s*<img[^>]+review-74-real-\d+[^>]+>\s*</div>'),
                 (99, r'<div class="review-photos">\s*<img[^>]+review-99-real-\d+[^>]+>\s*</div>')]:
    filepath = f'pages/produto-{pid}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    new_html = re.sub(pat, '', html)
    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'P{pid}: Cleaned catalog photos successfully.')
    else:
        print(f'P{pid}: No match found for pattern.')
