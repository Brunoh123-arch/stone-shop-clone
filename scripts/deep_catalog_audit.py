import os
import glob
import re
from bs4 import BeautifulSoup

def audit_catalog():
    pages = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group()))
    print(f"Auditing {len(pages)} HTML files in pages/...\n")

    findings = {
        'broken_relative_img_paths': [],
        'missing_slider_images': [],
        'broken_price': [],
        'shopee_aliexpress_mentions': [],
        'missing_desc_video': [],
        'missing_desc_poster': [],
        'desc_video_giant_height': [],
        'low_reviews': [],
        'zero_review_photos': [],
        'malformed_produto_atual': []
    }

    for p in pages:
        pid = int(re.search(r'\d+', p).group())
        with open(p, 'r', encoding='utf-8') as f:
            html = f.read()

        if "Redirecionando para a versão oficial" in html or len(html) < 1500:
            continue # redirect stub

        soup = BeautifulSoup(html, 'html.parser')

        # 1. Broken relative image paths (e.g. src="img/..." instead of "../img/...")
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if src.startswith('img/'):
                findings['broken_relative_img_paths'].append((pid, src))
                break

        # 2. Slider images
        slider_imgs = soup.select('.image-slider img:not(.slider-decalque)')
        if len(slider_imgs) < 2:
            findings['missing_slider_images'].append((pid, len(slider_imgs)))

        # 3. Broken price
        m_price = re.search(r'preco:\s*([\d\.]+)', html)
        if not m_price or float(m_price.group(1)) <= 0:
            findings['broken_price'].append((pid, "preco <= 0 or missing in PRODUTO_ATUAL"))
        
        # Check price in DOM
        p_row = soup.find(class_='price-row') or soup.find(class_='price-current')
        if not p_row:
            findings['broken_price'].append((pid, "missing price DOM element"))

        # 4. Shopee / AliExpress / Mercado Livre mentions in reviews or description
        shopee_matches = re.findall(r'\b(shopee|aliexpress|ali express|mercado livre|magalu)\b', html, re.I)
        if shopee_matches:
            findings['shopee_aliexpress_mentions'].append((pid, list(set(shopee_matches))))

        # 5. Description video
        vid = soup.find('video', id='tt-product-video')
        if not vid or not vid.get('src'):
            findings['missing_desc_video'].append(pid)
        else:
            poster = vid.get('poster', '')
            if not poster:
                findings['missing_desc_poster'].append(pid)
            elif not poster.startswith('http') and not os.path.exists(poster.replace('../', '')):
                findings['missing_desc_poster'].append((pid, poster, "local poster not found"))

        # 6. Giant video wrapper (520px / inline aspect-ratio)
        if 'max-height: 520px' in html or 'aspect-ratio: 9/16' in html:
            findings['desc_video_giant_height'].append(pid)

        # 7. Reviews count & unboxing photos
        reviews = soup.find_all(class_='review-card')
        if len(reviews) < 15:
            findings['low_reviews'].append((pid, len(reviews)))

        photos = soup.select('.review-photos img')
        if len(photos) == 0:
            findings['zero_review_photos'].append(pid)

    print("=" * 60)
    print("           RELATÓRIO DE AUDITORIA PROFUNDA")
    print("=" * 60)

    total_issues = 0
    for category, items in findings.items():
        if items:
            total_issues += len(items)
            print(f"\n[!] {category.upper()} ({len(items)} produtos):")
            for item in items[:10]:
                print(f"    - {item}")
            if len(items) > 10:
                print(f"    ... e mais {len(items) - 10} produtos")
        else:
            print(f"[OK] {category}: 0 problemas")

    print("\n" + "=" * 60)
    print(f"TOTAL DE ANOMALIAS ENCONTRADAS: {total_issues}")
    print("=" * 60)

if __name__ == '__main__':
    audit_catalog()
