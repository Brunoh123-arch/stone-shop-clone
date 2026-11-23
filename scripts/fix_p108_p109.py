import re

female_prods = [108, 109]

for pid in female_prods:
    filepath = f'pages/produto-{pid}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace any creators-avatars/creator-*.jpg or other non-validadas avatar in reviews
    # Let's see how they appear
    counter = [0]
    def repl(m):
        counter[0] += 1
        img_idx = ((counter[0] - 1) % 75) + 1
        return f'src="../img/reviews-avatars/mulheres_validadas/mulher_{img_idx}.jpg"'
    
    new_html = re.sub(r'src=["\'][^"\']*img/creators-avatars/creator-\d+\.jpg["\']', repl, html)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)
    print(f'Fixed P{pid}, replaced {counter[0]} avatars.')
