import re

for pid in [117, 118, 123]:
    filepath = f'pages/produto-{pid}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    cleaned = re.sub(r'<div class="review-photos">\s*</div>', '', html)
    if cleaned != html:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f'P{pid}: Cleaned empty review-photos tags.')
