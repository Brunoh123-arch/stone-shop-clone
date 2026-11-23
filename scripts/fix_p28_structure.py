# -*- coding: utf-8 -*-
with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove a tag extra de fechamento de div e o script no meio do HTML se houver
old_block = '''<!-- VÍDEOS DE CRIADORES -->
<div class="creators-section" id="creators-section"></div>
</div>
<script src="../js/videos-criadores-v3.js?v=20261121_prod_v3"></script>
<!-- AVALIAÇÕES -->'''

new_block = '''<!-- VÍDEOS DE CRIADORES OFICIAL TIKTOK SHOP -->
<div class="creators-section" id="creators-section"></div>
<!-- AVALIAÇÕES -->'''

if old_block in html:
    html = html.replace(old_block, new_block)
    print("[+] Bloco de criadores corrigido para padrao P104!")
else:
    print("[-] Bloco exato nao bateu, ajustando de forma flexivel...")
    import re
    html = re.sub(
        r'<div class="creators-section" id="creators-section"></div>\s*</div>\s*<script src="[^"]*videos-criadores[^"]*"></script>',
        '<div class="creators-section" id="creators-section"></div>',
        html
    )

# Garante que o script videos-criadores-v3.js esteja no final do body
if '<script src="../js/videos-criadores-v3.js' not in html:
    html = html.replace('</body>', '<script src="../js/videos-criadores-v3.js?v=20261121_p28_fix"></script>\n</body>')
    print("[+] Script adicionado antes de </body>!")
else:
    # Atualiza a versao do script
    import re
    html = re.sub(r'videos-criadores-v3\.js\?v=[^"\']+', 'videos-criadores-v3.js?v=20261121_p28_fix', html)

with open('pages/produto-28.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[+] pages/produto-28.html finalizado com sucesso!")
