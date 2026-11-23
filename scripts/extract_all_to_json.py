import os
import glob
import re
import json
from bs4 import BeautifulSoup

def clean_text(s):
    if not s: return ""
    return re.sub(r'\s+', ' ', s).strip()

def extract_product_data(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip stubs
    if "Redirecionando para a versão oficial" in html or len(html) < 1500:
        return None

    pid_match = re.search(r'produto-(\d+)\.html', html_path)
    pid = int(pid_match.group(1)) if pid_match else 0

    soup = BeautifulSoup(html, 'html.parser')

    # 1. Meta & Title
    title = clean_text(soup.title.string) if soup.title else ""
    meta_desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
    meta_desc = meta_desc_tag.get('content', '') if meta_desc_tag else ""

    # 2. PRODUTO_ATUAL
    # Matches const PRODUTO_ATUAL = { ... } or window.PRODUTO_ATUAL = { ... }
    m_prod = re.search(r'(?:const|window\.)PRODUTO_ATUAL\s*=\s*(\{[\s\S]*?\n\s*\});', html)
    prod_atual = {}
    if m_prod:
        p_str = m_prod.group(1)
        # Extract fields using regex for robustness
        m_id = re.search(r'id:\s*(\d+)', p_str)
        m_name = re.search(r'nome:\s*["\']([^"\']+)["\']', p_str)
        m_preco = re.search(r'preco:\s*([\d\.]+)', p_str)
        m_antigo = re.search(r'preco_antigo:\s*([\d\.]+)', p_str)
        m_img = re.search(r'img:\s*["\']([^"\']+)["\']', p_str)
        
        # imagens
        m_imgs = re.search(r'imagens:\s*\[([\s\S]*?)\]', p_str)
        imagens = []
        if m_imgs:
            for item in m_imgs.group(1).split(','):
                cleaned = item.strip().strip('"').strip("'")
                if cleaned:
                    imagens.append(cleaned)

        prod_atual = {
            "id": int(m_id.group(1)) if m_id else pid,
            "nome": m_name.group(1) if m_name else title,
            "preco": float(m_preco.group(1)) if m_preco else 0.0,
            "preco_antigo": float(m_antigo.group(1)) if m_antigo else 0.0,
            "img": m_img.group(1) if m_img else "",
            "imagens": imagens
        }

    # If imagens is empty, fallback to slider imgs
    if not prod_atual.get('imagens'):
        slider_imgs = [img.get('src') for img in soup.select('.image-slider img') if img.get('src')]
        prod_atual['imagens'] = slider_imgs
    if not prod_atual.get('img') and prod_atual.get('imagens'):
        prod_atual['img'] = prod_atual['imagens'][0]

    # 3. Pricing
    price_int_el = soup.find(class_='price-current-int')
    price_int = price_int_el.text.strip() if price_int_el else str(int(prod_atual.get('preco', 0)))
    price_cents_el = soup.find(class_='price-current-cents')
    price_cents = price_cents_el.text.strip() if price_cents_el else f",{int(round((prod_atual.get('preco', 0) % 1) * 100)):02d}"

    price_orig_el = soup.find(class_='price-original')
    price_orig = price_orig_el.text.strip() if price_orig_el else ""

    discount_badge_el = soup.find(class_='discount-badge') or soup.find(class_='price-discount-tag')
    discount_badge = discount_badge_el.text.strip() if discount_badge_el else ""

    installment_el = soup.find(class_='installment-text') or soup.find(class_='price-installment')
    installment = clean_text(installment_el.text) if installment_el else ""

    # 4. Rating & Sold
    rating_el = soup.find(class_='rating-score') or soup.find(class_='review-avg')
    rating = clean_text(rating_el.text) if rating_el else "4.9"

    rating_count_el = soup.find(class_='rating-count')
    rating_count = clean_text(rating_count_el.text) if rating_count_el else "1.240"

    sold_el = soup.find(class_='sold-count')
    sold_count = clean_text(sold_el.text) if sold_el else "3.450 vendidos"

    # 5. Video block
    vid_el = soup.find('video', id='tt-product-video')
    desc_video = {
        "src": vid_el.get('src', '') if vid_el else "",
        "poster": vid_el.get('poster', '') if vid_el else ""
    }

    # 6. Technical details grid
    details = []
    for row in soup.select('.details-attributes-grid .detail-attribute-row'):
        label_el = row.find(class_='detail-attribute-label')
        val_el = row.find(class_='detail-attribute-value')
        if label_el and val_el:
            details.append({
                "label": clean_text(label_el.text),
                "value": clean_text(val_el.text),
                "is_hidden": "is-hidden" in row.get('class', [])
            })

    # 7. Reviews
    reviews = []
    for c in soup.find_all(class_='review-card'):
        name = c.get('data-author-name', '')
        avatar = c.get('data-author-avatar', '')
        stars = int(c.get('data-author-stars', '5'))
        var = c.get('data-author-variation', '')
        date = c.get('data-author-date', '')
        comment = c.get('data-author-comment', '')
        if not comment:
            comm_el = c.find(class_='review-comment')
            comment = clean_text(comm_el.text) if comm_el else ""

        photos = []
        p_div = c.find(class_='review-photos')
        if p_div:
            for img in p_div.find_all('img'):
                src = img.get('src')
                if src: photos.append(src)

        reviews.append({
            "name": name,
            "avatar": avatar,
            "stars": stars,
            "variation": var,
            "date": date,
            "comment": comment,
            "photos": photos
        })

    # 8. Description content
    desc_section = soup.find(id='sobre-produto-desc-section') or soup.find(class_='description-section')
    desc_html = ""
    if desc_section:
        desc_html = str(desc_section)

    return {
        "id": pid,
        "title": title,
        "meta_desc": meta_desc,
        "nome": prod_atual.get('nome', title),
        "preco": prod_atual.get('preco', 0.0),
        "preco_antigo": prod_atual.get('preco_antigo', 0.0),
        "price_int": price_int,
        "price_cents": price_cents,
        "price_original": price_orig,
        "discount_badge": discount_badge,
        "installment": installment,
        "rating": rating,
        "rating_count": rating_count,
        "sold_count": sold_count,
        "img": prod_atual.get('img', ''),
        "imagens": prod_atual.get('imagens', []),
        "desc_video": desc_video,
        "detalhes": details,
        "reviews_count": len(reviews),
        "reviews": reviews,
        "desc_html": desc_html
    }

def build_catalog_database():
    files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group()))
    catalog = {}
    active_count = 0
    for f in files:
        data = extract_product_data(f)
        if data:
            catalog[str(data['id'])] = data
            active_count += 1

    out_path = 'data/produtos.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, ensure_ascii=False, indent=2)

    print(f"Extraction complete! {active_count} active products extracted into {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == '__main__':
    build_catalog_database()
