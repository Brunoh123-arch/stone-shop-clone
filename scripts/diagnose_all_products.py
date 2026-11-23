import glob
import re
from bs4 import BeautifulSoup

vc = open('js/videos-criadores.js', encoding='utf-8').read()

report = []
for f in sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1))):
    pid = int(re.search(r'produto-(\d+)', f).group(1))
    soup = BeautifulSoup(open(f, encoding='utf-8').read(), 'html.parser')
    
    # 1. Checar fotos nas avaliações
    review_photos = soup.select('.review-photo, .review-photos img')
    catalog_photos_in_reviews = []
    local_unboxing_photos = []
    other_photos = []
    for img in review_photos:
        src = img.get('src') or ''
        if 'reviews-unboxing' in src or 'unboxing' in src:
            local_unboxing_photos.append(src)
        elif any(k in src for k in ['mlstatic.com', 'susercontent.com', 'slide_', 'produtos/p']):
            catalog_photos_in_reviews.append(src)
        else:
            other_photos.append(src)
            
    # 2. Checar dataset em videos-criadores.js
    has_creators_case = bool(re.search(rf'prodId\s*===?\s*{pid}\b', vc))
    
    # 3. Contar reviews
    reviews_count = len(soup.select('.review-card'))
    
    # 4. Checar anomalias de detalhes
    details_rows = soup.select('.detail-row')
    has_details_anomaly = False
    for r in details_rows:
        lbl = r.select_one('.detail-label')
        val = r.select_one('.detail-value')
        lbl_t = lbl.text.strip() if lbl else ''
        val_t = val.text.strip() if val else ''
        if '?' in lbl_t or len(lbl_t) > 35 or len(val_t) > 90 or '+' in val_t or 'Caçarola' in val_t:
            has_details_anomaly = True

    report.append({
        'pid': pid,
        'file': f,
        'title': (soup.find('title').text.strip()[:35] if soup.find('title') else 'Sem titulo'),
        'reviews_count': reviews_count,
        'unboxing_photos': len(local_unboxing_photos),
        'catalog_in_reviews': len(catalog_photos_in_reviews),
        'other_photos': len(other_photos),
        'has_creators_case': has_creators_case,
        'has_details_anomaly': has_details_anomaly
    })

print(f"Total de produtos analisados: {len(report)}")

sem_criadores = [r for r in report if not r['has_creators_case']]
com_catalogo_em_review = [r for r in report if r['catalog_in_reviews'] > 0]
sem_fotos_review = [r for r in report if r['unboxing_photos'] == 0 and r['catalog_in_reviews'] == 0 and r['other_photos'] == 0]
poucas_reviews = [r for r in report if r['reviews_count'] < 15]

print(f"\n1. Produtos SEM case explícito em videos-criadores.js: {len(sem_criadores)}")
for r in sem_criadores[:10]:
    print(f"  P{r['pid']}: {r['title']}")

print(f"\n2. Produtos com fotos de CATÁLOGO nas avaliações: {len(com_catalogo_em_review)}")
for r in com_catalogo_em_review[:10]:
    print(f"  P{r['pid']}: {r['title']} ({r['catalog_in_reviews']} fotos catálogo)")

print(f"\n3. Produtos com ZERO fotos nas avaliações: {len(sem_fotos_review)}")
for r in sem_fotos_review[:15]:
    print(f"  P{r['pid']}: {r['title']}")

print(f"\n4. Produtos com menos de 15 avaliações: {len(poucas_reviews)}")
for r in poucas_reviews[:10]:
    print(f"  P{r['pid']}: {r['title']} ({r['reviews_count']} reviews)")
