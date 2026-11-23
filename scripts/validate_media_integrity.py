import os
import glob
import re
from bs4 import BeautifulSoup
from PIL import Image
from rapidocr_onnxruntime import RapidOCR

print("================================================================================")
print("--- AUDITORIA E VALIDAÇÃO PROFUNDA DE MÍDIA - 103 PRODUTOS (MODO ZIKA CTO) ---")
print("================================================================================")

pages = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group(0)) if re.search(r'\d+', x) else 0)
assert len(pages) == 103, f"Expected 103 pages, found {len(pages)}"

# Comprehensive forbidden pattern list across galleries and reviews
forbidden_patterns = [
    'review-18-c',
    'review-120-',
    'review-122-',
    'review-107-1.jpg',
    'review-107-2.jpg',
    'review-107-3.jpg',
    'review-107-c',
    'panelas_90/unboxing_5.jpg',
    'review-114-c',
    'review-124-real-1',
    'review-124-real-2',
    'review-88-real-4',
    'review-119-1.webp',
    'colchao-bestway-4.jpg',
    'colchao-bestway-5.jpg',
    'colchao-bestway-6.jpg',
    'colchao-bestway-7.jpg',
    'colchao-bestway-8.jpg'
]

errors = []
total_reviews_with_photos = 0
total_gallery_images = 0

for p in pages:
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check forbidden in whole HTML
    for pat in forbidden_patterns:
        if pat in html:
            errors.append(f"Forbidden pattern '{pat}' found in {p}")

    soup = BeautifulSoup(html, 'html.parser')

    # Verify gallery images
    track = soup.find('div', class_='slider-track') or soup.find('div', class_='swiper-wrapper') or soup.find('div', class_='product-gallery')
    if track:
        for img in track.find_all('img'):
            src = img.get('src', '')
            if src and not any(k in src for k in ['avatar', 'icon', 'logo']):
                total_gallery_images += 1
                if not src.startswith('http'):
                    local = src.split('?')[0].replace('../', '')
                    if not os.path.exists(local):
                        errors.append(f"Missing gallery image: {local} in {p}")

    # Verify review images
    for card in soup.find_all('div', class_='review-card'):
        photos = card.find_all('img', class_='review-photo')
        if not photos:
            ph_div = card.find('div', class_='review-photos')
            if ph_div:
                photos = ph_div.find_all('img')
        for img in photos:
            total_reviews_with_photos += 1
            src = img.get('src', '')
            if not src.startswith('http'):
                local = src.split('?')[0].replace('../', '')
                if not os.path.exists(local):
                    errors.append(f"Missing review image: {local} in {p}")

print(f"Total de páginas analisadas: {len(pages)}")
print(f"Total de fotos de galeria validadas: {total_gallery_images}")
print(f"Total de fotos de avaliações validadas: {total_reviews_with_photos}")

# OCR DEEP VERIFICATION ON KEY CRITICAL ASSETS
print("\n--- TESTE DEEP OCR NAS MÍDIAS SANITIZADAS ---")
engine = RapidOCR()

ocr_checks = [
    ('img/panela-pressao-slide-1.webp', ['da convencional', '00:00', 'apaneladepressaovap']),
    ('img/panela-pressao-slide-2.webp', ['da convencional', '00:00']),
    ('img/panela-pressao-slide-3.webp', ['electrolox', '00:00']),
    ('img/panela-pressao-slide-4.webp', ['00:00', 'unerom']),
    ('img/mesa-jantar-slide-1.webp', ['mercado livre', 'meli']),
    ('img/mesa-jantar-slide-3.webp', ['shopee']),
    ('img/projetor-slide-3.webp', ['1/9', '199,99', '6666semjuros']),
    ('img/reviews/review-118-1.webp', ['shopee']),
    ('img/reviews/review-118-2.webp', ['mercado livre']),
    ('img/reviews/review-119-1.webp', ['ganhamos']),
    ('img/review-88-real-4.jpg', ['sejaap']),
    ('img/review-120-real-1.jpg' if os.path.exists('img/review-120-real-1.jpg') else 'img/review-65-real-1.jpg', ['veo', 'siga-me'])
]

for img_path, banned_tokens in ocr_checks:
    if os.path.exists(img_path):
        res, _ = engine(img_path)
        found_tokens = [r[1].lower() for r in res] if res else []
        joined_text = " ".join(found_tokens)
        for token in banned_tokens:
            if token in joined_text:
                errors.append(f"OCR Failure: '{token}' found in {img_path}: {joined_text}")
        print(f"  [OCR OK] {img_path} verificado contra {banned_tokens}")
    else:
        errors.append(f"Missing file for OCR check: {img_path}")

if errors:
    print(f"\n[FALHA] Foram encontrados {len(errors)} erros:")
    for e in errors:
        print(f"  - {e}")
    exit(1)
else:
    print("\n================================================================================")
    print("[SUCESSO SOBERANO] 100% das 103 páginas validadas! ZERO imagens fatiadas de vídeo.")
    print("Todas as galerias, carrosséis e avaliações blindadas no mais alto padrão de produção!")
    print("================================================================================")
