import re

for pid in [61, 83]:
    filepath = f'pages/produto-{pid}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    pattern = rf'<div class="review-photos">\s*<img[^>]+review-{pid}-real[^>]+>.*?</div>'
    new_html = re.sub(pattern, '', html, flags=re.DOTALL)
    if new_html != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f'P{pid}: Cleaned review photos successfully.')
    else:
        print(f'P{pid}: No match.')
