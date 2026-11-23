import glob
import re

pages = sorted(glob.glob('pages/produto-*.html'))
no_poster = []
has_poster = []
no_video = []

for p in pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    if 'window.location.replace' in html:
        continue
    m = re.search(r'<video[^>]+id=["\']tt-product-video["\'][^>]*>', html)
    if not m:
        no_video.append(p)
    else:
        tag = m.group(0)
        if 'poster=' in tag:
            # extrair o poster
            p_m = re.search(r'poster=["\']([^"\']+)["\']', tag)
            has_poster.append((p, p_m.group(1) if p_m else ''))
        else:
            no_poster.append((p, tag))

print(f"Total produtos ativos auditados: {len(has_poster) + len(no_poster) + len(no_video)}")
print(f"Com video E com poster: {len(has_poster)}")
print(f"Com video MAS SEM POSTER (caixa preta no celular!): {len(no_poster)}")
print(f"Sem video de descrição: {len(no_video)}")

print("\nExemplo dos sem poster:")
for p, t in no_poster[:10]:
    print(f"  {p}: {t}")
