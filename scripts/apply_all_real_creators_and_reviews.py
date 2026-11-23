import json
import re
import os

with open('scripts/creators_metas_110_to_114.json', 'r', encoding='utf-8') as f:
    creators_data = json.load(f)

# 1. ATUALIZAR js/videos-criadores.js
with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    vc_code = f.read()

# Remover a trava temporária que ocultava o carrossel dos produtos 110-114
old_guard = """    // Produtos recentes sem múltiplos criadores humanos distintos: oculta carrossel para evitar repetição
    if (isKappa || isProjetorNatal || isCaminhao || isComedouro || isArcade) {
      if (targetContainer) targetContainer.style.display = 'none';
      return;
    }"""
new_guard = """    // Criadores 100% humanos reais do TikTok ativos para produtos 110 a 114
    if (targetContainer) targetContainer.style.display = '';"""

if old_guard in vc_code:
    vc_code = vc_code.replace(old_guard, new_guard)
    print("[OK] Trava de ocultamento removida de js/videos-criadores.js")
else:
    print("[INFO] Trava nao encontrada exatamente como texto, verificando regex...")
    vc_code = re.sub(
        r'if\s*\(\s*isKappa\s*\|\|\s*isProjetorNatal\s*\|\|\s*isCaminhao\s*\|\|\s*isComedouro\s*\|\|\s*isArcade\s*\)\s*\{[^}]*return;[^}]*\}',
        '// Criadores reais ativos\n    if (targetContainer) targetContainer.style.display = "";',
        vc_code
    )

# Atualizar os MAPS em js/videos-criadores.js
def build_js_map(items, prod_id):
    lines = []
    for it in items:
        clean_desc = it['title'].replace('"', '\\"').replace('\n', ' ')[:120]
        lines.append(f"""    {{
      name: "{it['name']}",
      username: "{it['user']}",
      avatar: "{it['avatar']}",
      poster: "../videosprodutos/posters/{it['posterFile']}",
      video: "../videosprodutos/{it['videoFile']}",
      startTime: 0.2,
      desc: "{clean_desc}"
    }}""")
    return "[\n" + ",\n".join(lines) + "\n  ]"

# Substituir KAPPA_110_VIDEOS_MAP
kappa_js = build_js_map(creators_data['110'], 110)
vc_code = re.sub(r'const KAPPA_110_VIDEOS_MAP = \[.*?\];', f'const KAPPA_110_VIDEOS_MAP = {kappa_js};', vc_code, flags=re.DOTALL)

# Substituir PROJETOR_111_VIDEOS_MAP
proj_js = build_js_map(creators_data['111'], 111)
vc_code = re.sub(r'const PROJETOR_111_VIDEOS_MAP = \[.*?\];', f'const PROJETOR_111_VIDEOS_MAP = {proj_js};', vc_code, flags=re.DOTALL)

# Substituir CAMINHAO_112_VIDEOS_MAP
cam_js = build_js_map(creators_data['112'], 112)
vc_code = re.sub(r'const CAMINHAO_112_VIDEOS_MAP = \[.*?\];', f'const CAMINHAO_112_VIDEOS_MAP = {cam_js};', vc_code, flags=re.DOTALL)

# Substituir COMEDOURO_113_VIDEOS_MAP
com_js = build_js_map(creators_data['113'], 113)
vc_code = re.sub(r'const COMEDOURO_113_VIDEOS_MAP = \[.*?\];', f'const COMEDOURO_113_VIDEOS_MAP = {com_js};', vc_code, flags=re.DOTALL)

# Substituir ARCADE_114_VIDEOS_MAP
arc_js = build_js_map(creators_data['114'], 114)
vc_code = re.sub(r'const ARCADE_114_VIDEOS_MAP = \[.*?\];', f'const ARCADE_114_VIDEOS_MAP = {arc_js};', vc_code, flags=re.DOTALL)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(vc_code)
print("[OK] js/videos-criadores.js atualizado com criadores 100% reais do TikTok!")

# 2. ATUALIZAR scripts/rebuild_products_official_parity.py COM FOTOS REAIS
with open('scripts/rebuild_products_official_parity.py', 'r', encoding='utf-8') as f:
    rp_code = f.read()

# Substituir fotos das avaliacoes em cada produto para usar review-[PID]-real-[1..4].jpg
for pid in [110, 111, 112, 113, 114]:
    rp_code = rp_code.replace(f'"../img/review-{pid}-clean-1.jpg"', f'"../img/review-{pid}-real-1.jpg"')
    rp_code = rp_code.replace(f'"../img/review-{pid}-clean-2.jpg"', f'"../img/review-{pid}-real-2.jpg"')
    rp_code = rp_code.replace(f'"../img/review-{pid}-clean-3.jpg"', f'"../img/review-{pid}-real-3.jpg"')
    rp_code = rp_code.replace(f'"../img/review-{pid}-clean-4.jpg"', f'"../img/review-{pid}-real-4.jpg"')
    rp_code = rp_code.replace(f'"../img/review-{pid}-clean-5.jpg"', f'"../img/review-{pid}-real-1.jpg"')
    rp_code = rp_code.replace(f'"../img/review-{pid}-clean-6.jpg"', f'"../img/review-{pid}-real-2.jpg"')

with open('scripts/rebuild_products_official_parity.py', 'w', encoding='utf-8') as f:
    f.write(rp_code)
print("[OK] scripts/rebuild_products_official_parity.py mapeado para fotos reais de unboxing!")
