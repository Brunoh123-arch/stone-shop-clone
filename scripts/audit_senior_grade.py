import os
import glob
import re
import json

def audit_all():
    pages = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group()))
    print(f"Total product pages found: {len(pages)}")

    issues = {
        'supplier_debris': [],
        'missing_tt_video': [],
        'non_standard_video_card': [],
        'low_reviews': [],
        'empty_creator_section_missing': []
    }

    debris_regexes = [
        re.compile(r'\b0\d{2,}\b'),
        re.compile(r'\bshopee\b', re.I),
        re.compile(r'\baliexpress\b', re.I),
        re.compile(r'\bshein\b', re.I),
        re.compile(r'\bwholesale\b', re.I),
        re.compile(r'novo\s+lisa\s+sem\s+rascada', re.I),
        re.compile(r'\[.*?\]'),
        re.compile(r'\bSKU\b', re.I),
    ]

    active_products = 0
    redirect_stubs = 0

    for p in pages:
        pid = int(re.search(r'\d+', p).group())
        txt = open(p, encoding='utf-8').read()

        # Check if redirect stub
        if 'Redirecionando para a versão oficial' in txt or (len(txt) < 1500 and 'window.location.replace' in txt):
            redirect_stubs += 1
            continue

        active_products += 1

        # 1. Check title / name debris
        m_nome = re.search(r'nome:\s*["\']([^"\']+)["\']', txt)
        prod_name = m_nome.group(1) if m_nome else ""
        for rgx in debris_regexes:
            if rgx.search(prod_name):
                issues['supplier_debris'].append((pid, prod_name, rgx.pattern))
                break

        # 2. Check description video
        has_video_tag = '<video id="tt-product-video"' in txt
        has_video_card = 'class="tiktok-video-card"' in txt
        if not has_video_tag:
            issues['missing_tt_video'].append(pid)
        elif not has_video_card or 'max-height: 520px' in txt:
            issues['non_standard_video_card'].append(pid)

        # 3. Check review count
        reviews = re.findall(r'class="review-card\b', txt)
        review_count = len(reviews)
        if review_count < 15:
            issues['low_reviews'].append((pid, review_count))

        # 4. Check creators section placeholder
        if '<div class="creators-section" id="creators-section"></div>' not in txt:
            if not re.search(r'<div\s+[^>]*id=["\']creators-section["\'][^>]*>\s*</div>', txt):
                issues['empty_creator_section_missing'].append(pid)

    print("\n" + "="*60)
    print("      AUDITORIA SÊNIOR TOTAL - CATÁLOGO STONE SHOP")
    print("="*60)
    print(f"[*] Total de páginas HTML: {len(pages)}")
    print(f"[*] Páginas Ativas de Produtos: {active_products}")
    print(f"[*] Redirecionamentos Canônicos / Stubs: {redirect_stubs}")
    print(f"[*] Supplier Debris no Título: {len(issues['supplier_debris'])}")
    print(f"[*] Vídeos de Descrição Faltantes: {len(issues['missing_tt_video'])}")
    print(f"[*] Cards de Vídeo Fora do Padrão (230px): {len(issues['non_standard_video_card'])}")
    print(f"[*] Produtos com Baixas Avaliações (<15): {len(issues['low_reviews'])}")
    print(f"[*] Seção de Criadores Não-Canônica: {len(issues['empty_creator_section_missing'])}")
    print("="*60)

    total_issues = sum(len(v) for v in issues.values())
    if total_issues == 0:
        print("[+] STATUS: 100% PADRÃO SÊNIOR APROVADO! ZERO NÃO-CONFORMIDADES.")
    else:
        print(f"[-] STATUS: {total_issues} pendências encontradas:")
        for k, v in issues.items():
            if v:
                print(f"    - {k}: {v}")

if __name__ == '__main__':
    audit_all()
