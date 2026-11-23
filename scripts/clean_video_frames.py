import re

for pid in [5, 17, 18]:
    filepath = f'pages/produto-{pid}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove review-photos blocks
    cleaned = re.sub(r'<div class="review-photos">\s*<img[^>]+review-(?:5|18)-c\d+[^>]+>\s*</div>', '', html)
    cleaned = re.sub(r'<div class="review-photos">\s*</div>', '', cleaned)
    
    if cleaned != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f'P{pid} cleaned of video screenshots in reviews!')
    else:
        print(f'P{pid} pattern not matched directly')
