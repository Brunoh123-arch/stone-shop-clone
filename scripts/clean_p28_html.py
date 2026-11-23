# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

# Substitui todo o bloco de #creators-section por div limpa
new_html = re.sub(
    r'<div class="creators-section" id="creators-section">.*?</div\s*>\s*</div\s*>\s*</div\s*>',
    '<div class="creators-section" id="creators-section"></div>',
    html,
    flags=re.DOTALL
)

# Verifica se substituiu
if new_html != html:
    print("[+] Substituido com sucesso por div limpa!")
    with open('pages/produto-28.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
else:
    print("[-] Regex nao bateu, fazendo busca exata...")
    idx1 = html.find('<div class="creators-section" id="creators-section">')
    idx2 = html.find('<!-- AVALIAÇÕES DOS CLIENTES -->', idx1)
    if idx2 == -1:
        idx2 = html.find('Avaliações dos clientes', idx1)
        # acha a div anterior
        idx2 = html.rfind('</div>', 0, idx2) + 6
    print("Trecho a substituir:")
    print(html[idx1:idx1+300])
    
    # Substitui
    clean_snippet = '<div class="creators-section" id="creators-section"></div>\n\n'
    # Procura onde termina o creators-section
    # Ele termina antes da proxima secao
    end_idx = html.find('<div class="reviews-section"', idx1)
    if end_idx == -1:
        end_idx = html.find('id="reviews"', idx1)
    if end_idx == -1:
        end_idx = html.find('Avaliações dos clientes', idx1)
        end_idx = html.rfind('<div', 0, end_idx)
    
    html = html[:idx1] + clean_snippet + html[end_idx:]
    with open('pages/produto-28.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("[+] Substituicao cirurgica realizada!")
