import os
import re
import glob

def audit_all():
    pages = sorted(glob.glob('pages/produto-*.html'), key=lambda p: int(re.search(r'\d+', p).group()))
    print(f"=== AUDITORIA GERAL DE PRODUTOS ({len(pages)} páginas encontradas) ===\n")
    
    # 1. Carregar js/videos-criadores.js
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    # Mapear datasets em js/videos-criadores.js
    blocks = dict(re.findall(r'if\s*\(\s*prodId\s*===\s*(\d+)\s*\)\s*return\s*([A-Za-z0-9_]+);', js_code))
    
    datasets = {}
    for m in re.finditer(r'const\s+([A-Za-z0-9_]+)\s*=\s*\[([\s\S]*?)\];', js_code):
        ds_name = m.group(1)
        body = m.group(2)
        vids = re.findall(r'video:\s*["\']([^"\']+)["\']', body)
        posters = re.findall(r'poster:\s*["\']([^"\']+)["\']', body)
        datasets[ds_name] = {'videos': vids, 'posters': posters}

    report = []
    
    for page in pages:
        pid = int(re.search(r'\d+', page).group())
        with open(page, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
            
        title_m = re.search(r'<title>(.*?)</title>', html)
        title = title_m.group(1).replace(' - Stone Shop', '').strip() if title_m else f'Produto {pid}'
        
        # Unboxing photos
        has_review_photos = 'review-photos' in html and ('img/review-' in html or 'review-user-' in html)
        review_img_count = len(re.findall(r'class="review-img"', html))
        
        # Creator videos in JS
        ds_name = blocks.get(str(pid))
        vid_issues = []
        creator_vids_count = 0
        poster_mismatch = False
        poster_404 = False
        duplicate_vids = 0
        
        if ds_name and ds_name in datasets:
            ds = datasets[ds_name]
            vids = ds['videos']
            creator_vids_count = len(vids)
            unique_vids = len(set(vids))
            if creator_vids_count != unique_vids:
                duplicate_vids = creator_vids_count - unique_vids
                vid_issues.append(f"{duplicate_vids} vídeos duplicados")
                
            posters = set(ds['posters'])
            for pos in posters:
                clean_pos = pos.replace('../', '')
                if not os.path.exists(clean_pos):
                    poster_404 = True
                    vid_issues.append(f"Poster 404: {pos}")
                m_pos = re.search(r'video-produto-(\d+)\.jpg', pos)
                if m_pos and int(m_pos.group(1)) != pid:
                    poster_mismatch = True
                    vid_issues.append(f"Poster de outro ID: {pos}")
        elif ds_name:
            vid_issues.append(f"Dataset {ds_name} não definido no JS")
        else:
            vid_issues.append("Sem mapeamento em videos-criadores.js")
            
        # Description video
        desc_vid_m = re.search(r'id="tt-product-video"[^>]*src="([^"]+)"', html)
        desc_vid = desc_vid_m.group(1) if desc_vid_m else None
        
        report.append({
            'id': pid,
            'title': title,
            'has_unboxing': has_review_photos,
            'unboxing_count': review_img_count,
            'creators_count': creator_vids_count,
            'duplicate_vids': duplicate_vids,
            'poster_mismatch': poster_mismatch,
            'poster_404': poster_404,
            'vid_issues': vid_issues,
            'desc_vid': desc_vid
        })

    total = len(report)
    with_unboxing = [r for r in report if r['has_unboxing']]
    without_unboxing = [r for r in report if not r['has_unboxing']]
    with_vid_issues = [r for r in report if r['vid_issues']]
    
    print(f"Total de produtos: {total}")
    print(f"Com unboxing nas avaliações: {len(with_unboxing)}")
    print(f"SEM unboxing nas avaliações: {len(without_unboxing)}")
    print(f"Com problemas em vídeos de criadores / posters: {len(with_vid_issues)}")
    print("\n--- DETALHE DOS PROBLEMAS DE VÍDEOS / POSTERS ---")
    for r in with_vid_issues:
        print(f"P{r['id']:<3} | {r['title'][:40]:<40} | Issues: {', '.join(r['vid_issues'])}")

    print("\n--- AMOSTRA DE PRODUTOS SEM UNBOXING (PRIMEIROS 25) ---")
    for r in without_unboxing[:25]:
        print(f"P{r['id']:<3} | {r['title'][:45]}")

if __name__ == '__main__':
    audit_all()
