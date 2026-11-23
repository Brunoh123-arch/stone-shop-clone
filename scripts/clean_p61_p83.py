import re

for pid in [61, 83]:
    filepath = f'pages/produto-{pid}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Remove review-photos with review-61-real or review-83-real
    pattern = rf'<div class="review-photos">\s*<img[^>]+review-{pid}-real-\d+[^>]+>\s*</div>'
    new_html = re.sub(pattern, '', html)
    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'P{pid} cleaned of fake renders!')
    else:
        print(f'P{pid} pattern not matched directly')
