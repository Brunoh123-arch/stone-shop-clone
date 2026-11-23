import json

with open('scripts/pdf_parsed_findings.json', 'r', encoding='utf-8') as f:
    findings = json.load(f)

empty_creators = []
hidden_carousel = []
catalog_reviews = []
frame_reviews = []
unrelated_media = []
duplicated_creators = []

for item in findings:
    pid = item['prod_id']
    title = item['title']
    details = item['details']
    
    if 'Não verificável: mídias sem conteúdo recebido' in details or 'retornaram vazios' in details or 'retornaram vazias' in details:
        empty_creators.append((pid, title))
        
    if 'Carrossel oculto' in details or 'oculto' in details:
        hidden_carousel.append((pid, title))
        
    if 'catálogo/divulgação' in details:
        catalog_reviews.append((pid, title))
        
    if 'capturas/frames de vídeo' in details or 'Recorte de vídeo' in details:
        frame_reviews.append((pid, title))
        
    if 'Item de outro anúncio' in details or 'não identificado' in details or 'Mistura' in details:
        unrelated_media.append((pid, title))

    # Check cartoes vs urls unicas
    import re
    m = re.search(r'(\d+)\s+cartões\s*/\s*(\d+)\s+URLs únicas', details)
    if m:
        cards, urls = int(m.group(1)), int(m.group(2))
        if cards > urls:
            duplicated_creators.append((pid, cards, urls, title))

print(f'=== 1. VÍDEOS DE CRIADORES VAZIOS/404 ({len(empty_creators)}) ===')
for pid, t in empty_creators:
    print(f'  P{pid}: {t}')

print(f'\n=== 2. CARROSSEL OCULTO ({len(hidden_carousel)}) ===')
for pid, t in hidden_carousel:
    print(f'  P{pid}: {t}')

print(f'\n=== 3. AVALIAÇÕES COM IMAGENS DE CATÁLOGO ({len(catalog_reviews)}) ===')
for pid, t in catalog_reviews:
    print(f'  P{pid}: {t}')

print(f'\n=== 4. AVALIAÇÕES COM RECORTE/FRAMES DE VÍDEO ({len(frame_reviews)}) ===')
for pid, t in frame_reviews:
    print(f'  P{pid}: {t}')

print(f'\n=== 5. MÍDIA DE OUTRO ITEM OU MISTURADA ({len(unrelated_media)}) ===')
for pid, t in unrelated_media[:15]:
    print(f'  P{pid}: {t}')

print(f'\n=== 6. CARROSSÉIS COM VÍDEOS DUPLICADOS ({len(duplicated_creators)}) ===')
print(f'Total de carrosséis duplicando vídeos: {len(duplicated_creators)}')
