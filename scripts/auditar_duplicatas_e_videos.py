import os
import re
import json
from collections import defaultdict

# 1. Carregar catálogo
catalog_file = 'js/catalogo.js'
with open(catalog_file, 'r', encoding='utf-8') as f:
    cat_text = f.read()

# Extrair lista de produtos do catalogo: {id:115,nome:'...'}
items_raw = re.findall(r'\{\s*id:\s*(\d+)\s*,\s*nome:\s*[\'"]([^\'"]+)[\'"]', cat_text)
print(f'=== TOTAL DE PRODUTOS NO CATALOGO: {len(items_raw)} ===')

catalog_map = {int(pid): nome for pid, nome in items_raw}

# Checar títulos muito parecidos no catálogo
print('\n--- 1. CHECANDO PRODUTOS COM NOMES PARECIDOS NO CATALOGO ---')
names = {}
for pid, name in catalog_map.items():
    words = set([w for w in re.findall(r'[a-zA-Z0-9]+', name.lower()) if len(w) > 3])
    names[pid] = (name, words)

similar_count = 0
checked = set()
for p1, (t1, w1) in names.items():
    for p2, (t2, w2) in names.items():
        if p1 >= p2 or (p1, p2) in checked:
            continue
        checked.add((p1, p2))
        if w1 and w2:
            intersection = w1.intersection(w2)
            union = w1.union(w2)
            sim = len(intersection) / len(union)
            if sim >= 0.5:
                similar_count += 1
                print(f'P{p1} ({t1[:45]}) <---> P{p2} ({t2[:45]}) [Similaridade: {sim:.2f}]')

if similar_count == 0:
    print('Nenhum produto suspeito de duplicidade por nome.')

# 2. Checar switch case em js/videos-criadores.js
print('\n--- 2. CHECANDO DATASETS DE CRIADORES EM js/videos-criadores.js ---')
vc_file = 'js/videos-criadores.js'
with open(vc_file, 'r', encoding='utf-8') as f:
    vc_text = f.read()

# Extrair todos os cases: case 14:\n activeDataset = ...;
switch_match = re.search(r'switch\s*\(\s*prodId\s*\)\s*\{(.*?)\n\s*default:', vc_text, re.DOTALL)
cases = {}
if switch_match:
    cases_raw = re.findall(r'case\s+(\d+):\s*activeDataset\s*=\s*([A-Za-z0-9_]+);', switch_match.group(1))
    for pid, ds in cases_raw:
        cases[int(pid)] = ds

print(f'Total de produtos com dataset de criadores no switch: {len(cases)}')

# Produtos do catálogo que NÃO tem case no switch:
missing_switch = []
for pid in sorted(catalog_map.keys()):
    if pid not in cases:
        missing_switch.append((pid, catalog_map[pid]))

print(f'\nPRODUTOS DO CATALOGO SEM CASE EM videos-criadores.js ({len(missing_switch)}):')
for pid, nome in missing_switch:
    print(f'   P{pid}: {nome[:50]}')

# Checar se dois produtos apontam para o MESMO dataset
ds_map = defaultdict(list)
for pid, ds in cases.items():
    ds_map[ds].append(pid)

print('\nDATASETS COMPARTILHADOS ENTRE PRODUTOS DIFERENTES:')
shared_ds_count = 0
for ds, pids in ds_map.items():
    if len(pids) > 1:
        shared_ds_count += 1
        prods_info = [f'P{p} ({catalog_map.get(p, "Off-catalog")[:25]})' for p in pids]
        print(f'Dataset [{ds}] compartilhado por: {", ".join(prods_info)}')

if shared_ds_count == 0:
    print('Nenhum dataset compartilhado!')

# 3. Extrair URLs de vídeos dentro de CADA dataset de criadores e checar colisão
print('\n--- 3. CHECANDO URLs DE VIDEOS COMPARTILHADAS ENTRE DATASETS ---')
# Achar definições const CREATORS_... = [ ... ];
video_to_prods = defaultdict(set)
datasets_defs = re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*\[(.*?)\];', vc_text, re.DOTALL)

for ds_name, ds_body in datasets_defs:
    vurls = re.findall(r'videoUrl:\s*[\'"]([^\'"]+)[\'"]', ds_body)
    # Quais produtos usam esse dataset?
    using_prods = ds_map.get(ds_name, [])
    for u in vurls:
        clean_u = u.strip()
        if clean_u:
            for p in using_prods:
                video_to_prods[clean_u].add(p)

cross_videos = 0
for u, pids in video_to_prods.items():
    if len(pids) > 1:
        cross_videos += 1
        prods_info = [f'P{p} ({catalog_map.get(p, "?")[:20]})' for p in pids]
        print(f'Video {u} usado em produtos diferentes: {", ".join(prods_info)}')

if cross_videos == 0:
    print('Zero vídeos de criadores compartilhados entre produtos diferentes!')
else:
    print(f'Total de {cross_videos} vídeos de criadores compartilhados entre produtos diferentes!')

# 4. Checar vídeos da descrição (.product-video-block / tt-product-video) nos HTMLs
print('\n--- 4. CHECANDO VIDEOS DE DESCRICAO NO HTML ---')
html_desc_vids = defaultdict(list)
for pid in sorted(catalog_map.keys()):
    hfile = f'pages/produto-{pid}.html'
    if os.path.exists(hfile):
        with open(hfile, 'r', encoding='utf-8') as f:
            content = f.read()
        vids = re.findall(r'<video[^>]+src=[\'"]([^\'"]+)[\'"]', content)
        for v in vids:
            if 'catbox' in v or '.mp4' in v:
                html_desc_vids[v].append(pid)

cross_desc = 0
for v, pids in html_desc_vids.items():
    if len(pids) > 1:
        cross_desc += 1
        prods_info = [f'P{p} ({catalog_map.get(p, "?")[:25]})' for p in pids]
        print(f'Vídeo {v} na descrição de múltiplos produtos: {", ".join(prods_info)}')

if cross_desc == 0:
    print('Zero vídeos de descrição compartilhados!')

# 5. Auditoria de Fotos de Unboxing nas Avaliações
print('\n--- 5. AUDITORIA DE FOTOS DE UNBOXING NAS AVALIACOES ---')
sem_unboxing = []
com_unboxing = []
for pid in sorted(catalog_map.keys()):
    hfile = f'pages/produto-{pid}.html'
    if os.path.exists(hfile):
        with open(hfile, 'r', encoding='utf-8') as f:
            content = f.read()
        # Verificar tags img dentro de review-photo ou review-photos ou data-unboxing
        # ou se há imagens de review que não sejam avatar
        has_review_photo = False
        # Checar seletor .review-photos ou .review-photo ou img dentro da lista de reviews
        rev_section = re.search(r'id=[\'"]reviews-list[\'"].*?</div>\s*</div>', content, re.DOTALL)
        if rev_section:
            imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', rev_section.group(0))
            unboxing_imgs = [img for img in imgs if 'avatar' not in img and 'logo' not in img and 'star' not in img]
            if len(unboxing_imgs) >= 1:
                has_review_photo = True
                com_unboxing.append((pid, len(unboxing_imgs)))
            else:
                sem_unboxing.append((pid, catalog_map[pid]))
        else:
            sem_unboxing.append((pid, catalog_map[pid]))

print(f'Produtos com fotos reais de unboxing: {len(com_unboxing)}')
print(f'Produtos SEM fotos de unboxing nas avaliações: {len(sem_unboxing)}')
print('\nPrimeiros 15 produtos sem unboxing:')
for pid, nome in sem_unboxing[:15]:
    print(f'   P{pid}: {nome[:50]}')
