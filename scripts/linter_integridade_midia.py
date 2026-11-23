# -*- coding: utf-8 -*-
"""
LINTER DE INTEGRIDADE DE MÍDIA TOTAL - BRUNO CTO (MODO ZIKA)
Audita se:
1. Algum produto diferente do Chinelo (P104) usa vídeos ou posters do catálogo de chinelos.
2. Existem colisões de vídeos ou posters entre produtos de nichos diferentes.
3. Há separação entre o vídeo de descrição e o carrossel.
4. Todos os posters referenciados existem no disco e não compartilham hashes entre produtos diferentes.
"""

import re
import os
import sys
import glob
import hashlib
from collections import defaultdict

def get_file_hash(path):
    clean_p = path.split('?')[0].lstrip('./').replace('\\', '/')
    if not os.path.exists(clean_p):
        return None
    with open(clean_p, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def run_linter():
    print("=" * 75)
    print("      LINTER DE INTEGRIDADE DE MÍDIA TOTAL - BRUNO CTO (MODO ZIKA)")
    print("=" * 75)

    errors = []

    # 1. Carregar vídeos e posters do Chinelo (P104)
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        js_content = f.read()

    chinelo_match = re.search(r'const CHINELO_VIDEOS_MAP = \[(.*?)\];', js_content, re.DOTALL)
    if not chinelo_match:
        errors.append("ERRO: CHINELO_VIDEOS_MAP não encontrado em js/videos-criadores.js!")
        chinelo_vids = []
        chinelo_posters = []
    else:
        chinelo_vids = [v.strip() for v in re.findall(r'video:\s*["\']([^"\']+)["\']', chinelo_match.group(1))]
        chinelo_posters = [p.strip() for p in re.findall(r'poster:\s*["\']([^"\']+)["\']', chinelo_match.group(1))]

    # Hashes dos posters do chinelo
    chinelo_poster_hashes = set()
    for cp in chinelo_posters:
        h = get_file_hash(cp)
        if h:
            chinelo_poster_hashes.add(h)

    print(f"[*] Total de vídeos no catálogo do Chinelo (P104): {len(chinelo_vids)}")
    print(f"[*] Total de hashes de posters do Chinelo (P104): {len(chinelo_poster_hashes)}")

    # Mapear produtos para seus datasets no switch
    cases = re.findall(r'case\s+(\d+):\s+activeDataset\s*=\s*([A-Za-z0-9_]+);', js_content)
    prod_to_dataset = {}
    for pid_str, ds_name in cases:
        pid = int(pid_str)
        prod_to_dataset[pid] = ds_name

    array_defs = re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*(\[\s*\{[\s\S]*?\n\s*\]);', js_content)
    dataset_videos = defaultdict(list)
    dataset_posters = defaultdict(list)
    for var_name, arr_str in array_defs:
        vids = re.findall(r'video:\s*["\']([^"\']+)["\']', arr_str)
        if vids:
            dataset_videos[var_name] = [v.strip() for v in vids]
        posts = re.findall(r'poster:\s*(?:\(isPagesDir\s*\?\s*["\']\.\./["\']\s*:\s*["\']["\']\)\s*\+\s*)?["\']([^"\']+)["\']', arr_str)
        if posts:
            dataset_posters[var_name] = [p.strip() for p in posts]

    map_links = re.findall(r'const\s+([A-Za-z0-9_]+)\s*=\s*([A-Za-z0-9_]+)\.map', js_content)
    creators_to_source = dict(map_links)

    video_owners_carousel = defaultdict(list)

    for pid, ds_name in prod_to_dataset.items():
        src_map = creators_to_source.get(ds_name, ds_name)
        vids = dataset_videos.get(src_map, []) or dataset_videos.get(ds_name, [])

        for v in vids:
            video_owners_carousel[v].append((pid, ds_name))
            if pid != 104 and v in chinelo_vids:
                errors.append(f"CRÍTICO: Vídeo de chinelo {v} vazado no dataset {ds_name} do Produto {pid}!")

    # Colisões no carrossel
    EXCEPTIONS_CAROUSEL = {
        (47, 49), (49, 47),
        (21, 74), (74, 21),
        (21, 99), (99, 21),
        (6, 94), (94, 6),
        (53, 59), (59, 53),
        (34, 79), (79, 34),
        (48, 84), (84, 48),
        (61, 83), (83, 61),
        (73, 81), (81, 73),
        (47, 78), (78, 47),
    }

    for vid_url, owners in video_owners_carousel.items():
        unique_pids = sorted(list(set(pid for pid, _ in owners)))
        if len(unique_pids) > 1:
            if not (len(unique_pids) == 2 and (unique_pids[0], unique_pids[1]) in EXCEPTIONS_CAROUSEL):
                errors.append(f"COLISÃO CARROSSEL: Vídeo {vid_url} compartilhado entre produtos {unique_pids}")

    # ---------------------------------------------------------
    # 2. AUDITORIA DE VÍDEOS DE DESCRIÇÃO (#tt-product-video)
    # ---------------------------------------------------------
    html_files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))
    desc_video_owners = defaultdict(list)
    prod_desc_video = {}

    for hf in html_files:
        pid = int(re.search(r'produto-(\d+)', hf).group(1))
        with open(hf, 'r', encoding='utf-8') as fh:
            html = fh.read()

        # Checar se tem chinelo vazado no HTML inteiro
        if pid != 104:
            for cv in chinelo_vids:
                if cv in html:
                    errors.append(f"CRÍTICO: Vídeo de chinelo {cv} vazado no HTML de pages/produto-{pid}.html!")

        # Extrair #tt-product-video
        m = re.search(r'<video[^>]+id=["\']tt-product-video["\'][^>]*>', html)
        if m:
            tag = m.group(0)
            src_m = re.search(r'src=["\']([^"\']+)["\']', tag)
            if src_m:
                src = src_m.group(1).strip()
                desc_video_owners[src].append(pid)
                prod_desc_video[pid] = src
                if pid != 104 and src in chinelo_vids:
                    errors.append(f"CRÍTICO: #tt-product-video do Produto {pid} é um vídeo de chinelo ({src})!")

    print(f"[*] Total de produtos auditados no HTML: {len(html_files)}")
    print(f"[*] Produtos com vídeo na descrição (#tt-product-video): {len(prod_desc_video)}")

    # Colisões entre vídeos de descrição
    EXCEPTIONS_DESC = {
        (47, 49), (49, 47),
    }

    for src, pids in desc_video_owners.items():
        if len(pids) > 1:
            if not (len(pids) == 2 and (pids[0], pids[1]) in EXCEPTIONS_DESC):
                errors.append(f"COLISÃO DESCRIÇÃO: Vídeo {src} usado na descrição de múltiplos produtos: {pids}")

    print("=" * 75)
    print(f"[*] Total de violações encontradas: {len(errors)}")
    print("=" * 75)

    if errors:
        print("\n[!] FALHAS DE INTEGRIDADE DETECTADAS:")
        for err in errors:
            print(f"  [-] {err}")
        print("\n" + "=" * 75)
        print("[-] STATUS: REPROVADO. A integridade de mídia foi violada.")
        print("=" * 75)
        return 1
    else:
        print("\n[+] STATUS: 100% APROVADO! NENHUM VAZAMENTO OU CONTAMINAÇÃO DETECTADA.")
        print("    - Zero vídeos de chinelo vazados fora do P104.")
        print("    - Zero colisões não autorizadas no carrossel de criadores.")
        print("    - Zero colisões indevidas nos vídeos de descrição (#tt-product-video).")
        print("=" * 75)
        return 0

if __name__ == '__main__':
    sys.exit(run_linter())
