# -*- coding: utf-8 -*-
import re

for p_num in [108, 109]:
    fname = f'pages/produto-{p_num}.html'
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Substitui qualquer conteudo interno de #creators-section
    new_html = re.sub(
        r'<div[^>]*id=["\']creators-section["\'][^>]*>.*?</div\s*>',
        '<div class="creators-section" id="creators-section"></div>',
        html,
        flags=re.DOTALL
    )
    if new_html != html:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_html)
        print(f"[+] {fname} limpo para padrao P104!")
