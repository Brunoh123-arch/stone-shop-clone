import glob
import re
from collections import Counter

def deduplicate_product_reviews(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Encontrar todas as fotos de reviews
    photos = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>', html)
    rev_photos = [src for src in photos if any(k in src.lower() for k in ['review', 'unboxing', 'avaliacao']) and not any(k in src.lower() for k in ['avatar', 'icon', 'star', 'logo', 'seller', 'ranking'])]
    c = Counter(rev_photos)
    dups = {k: v for k, v in c.items() if v > 1}

    if not dups:
        return 0

    print(f"[*] Processando {html_path}: {len(dups)} fotos duplicadas -> {dups}")

    seen_srcs = set()

    # Função que substitui cada tag <img ...> mantendo a primeira e removendo as repetidas
    def img_replacer(match):
        tag = match.group(0)
        src_match = re.search(r'src=[\'"]([^\'"]+)[\'"]', tag)
        if not src_match:
            return tag
        src = src_match.group(1)
        # Se for foto de review
        if any(k in src.lower() for k in ['review', 'unboxing', 'avaliacao']) and not any(k in src.lower() for k in ['avatar', 'icon', 'star', 'logo', 'seller', 'ranking']):
            if src in seen_srcs:
                # Já vimos! Remove esta tag img
                return ''
            else:
                seen_srcs.add(src)
                return tag
        return tag

    # Substitui tags img
    new_html = re.sub(r'<img[^>]+>', img_replacer, html)

    # Limpar contêineres vazios de fotos: <div class="review-photos"[^>]*>\s*</div>
    new_html = re.sub(r'<div\s+class=[\'"][^\'"]*review-photo[^\'"]*[\'"][^>]*>\s*</div>', '', new_html)

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return len(dups)

pages = sorted(glob.glob('pages/produto-*.html'), key=lambda p: int(re.search(r'produto-(\d+)', p).group(1)))
total_modified = 0

for p in pages:
    mod = deduplicate_product_reviews(p)
    if mod > 0:
        total_modified += 1

print(f"\n[SUCESSO] Total de produtos corrigidos: {total_modified}")

# Auditoria de pós-execução
remaining_dups = 0
for p in pages:
    pid = int(re.search(r'produto-(\d+)', p).group(1))
    text = open(p, 'r', encoding='utf-8').read()
    photos = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"][^>]*>', text)
    rev_photos = [src for src in photos if any(k in src.lower() for k in ['review', 'unboxing', 'avaliacao']) and not any(k in src.lower() for k in ['avatar', 'icon', 'star', 'logo', 'seller', 'ranking'])]
    c = Counter(rev_photos)
    dups = {k: v for k, v in c.items() if v > 1}
    if dups:
        print(f"[ALERTA] P{pid} ainda tem duplicatas: {dups}")
        remaining_dups += 1

if remaining_dups == 0:
    print("[PERFEITO] ZERO fotos de unboxing duplicadas em todo o catalogo de 103 produtos!")
