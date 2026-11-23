import os
import re
import json
import argparse
import time

TEMPLATES_DIR = 'templates'
COMPONENTS_DIR = os.path.join(TEMPLATES_DIR, 'components')
DATA_PATH = os.path.join('data', 'produtos.json')
OUTPUT_DIR = 'pages'

def load_master_template():
    master_path = os.path.join(TEMPLATES_DIR, 'produto.template.html')
    with open(master_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Expand @include directives
    def replace_include(match):
        rel_path = match.group(1).strip()
        comp_path = os.path.join(TEMPLATES_DIR, rel_path)
        if os.path.exists(comp_path):
            with open(comp_path, 'r', encoding='utf-8') as cf:
                return cf.read()
        else:
            print(f"Warning: include not found: {comp_path}")
            return f"<!-- Missing component: {rel_path} -->"

    expanded = re.sub(r'<!--\s*@include\s*["\']([^"\']+)["\']\s*-->', replace_include, content)
    return expanded

def render_product(prod, template_html):
    pid = prod['id']
    title = prod.get('title') or f"{prod.get('nome')} - Stone Shop"
    meta_desc = prod.get('meta_desc') or f"{prod.get('nome')} com Frete Grátis na Stone Shop."

    preload_img = prod.get('img')
    if not preload_img and prod.get('imagens'):
        preload_img = prod['imagens'][0]

    price_int = prod.get('price_int', str(int(prod.get('preco', 0))))
    price_cents = prod.get('price_cents', f",{int(round((prod.get('preco', 0) % 1) * 100)):02d}")
    price_orig = prod.get('price_original', '')
    discount_badge = prod.get('discount_badge', '')
    installment = prod.get('installment', '')
    rating = prod.get('rating', '4.9')
    rating_count = prod.get('rating_count', '1.240')
    sold_count = prod.get('sold_count', '3.450 vendidos')

    # Slider images
    slider_html = []
    imagens = prod.get('imagens', [])
    for idx, img_url in enumerate(imagens):
        fetch_p = 'fetchpriority="high"' if idx == 0 else 'loading="lazy"'
        slider_html.append(f'<div class="slider-item"><img src="{img_url}" class="slider-img" alt="{prod.get("nome")} - Slide {idx+1}" decoding="async" {fetch_p}></div>')
    slider_images_rendered = '\n        '.join(slider_html)
    slider_counter = f"1/{len(imagens)}" if imagens else "1/1"

    # Details Grid
    details_html = []
    for d in prod.get('detalhes', []):
        hide_cls = " is-hidden" if d.get('is_hidden') else ""
        style_hide = ' style="display: none !important;"' if d.get('is_hidden') else ""
        details_html.append(f'''<div class="detail-attribute-row toggleable-row{hide_cls}"{style_hide}>
          <span class="detail-attribute-label">{d.get('label')}</span>
          <span class="detail-attribute-value">{d.get('value')}</span>
        </div>''')
    details_grid_rendered = '\n        '.join(details_html)

    # Reviews Block
    reviews_html = []
    for r in prod.get('reviews', []):
        stars_svg = '\n                '.join(['<svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>' for _ in range(r.get('stars', 5))])
        photos_html = ""
        if r.get('photos'):
            p_imgs = '\n            '.join([f'<img alt="Foto da avaliação" decoding="async" loading="lazy" src="{p}" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer;" onclick="openReviewModal(this.src)">' for p in r['photos']])
            photos_html = f'''
          <div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px; flex-wrap: wrap;">
            {p_imgs}
          </div>'''

        card_html = f'''
        <div class="review-card" data-author-name="{r.get('name')}" data-author-avatar="{r.get('avatar')}" data-author-stars="{r.get('stars')}" data-author-variation="{r.get('variation')}" data-author-date="{r.get('date')}" data-author-comment="{r.get('comment')}">
          <div class="review-header"><div class="review-user">
            <div class="review-avatar"><img src="{r.get('avatar')}" alt="{r.get('name')}" width="32" height="32" style="border-radius:50%;object-fit:cover;" onerror="this.src=\'../img/reviews-avatars/review-user-1.jpg\'"></div>
            <div class="review-user-info">
              <div class="review-user-name">{r.get('name')}</div>
              <div class="review-user-stars">
                {stars_svg}
              </div>
              <div class="review-date">{r.get('date')} · {r.get('variation')}</div>
            </div>
          </div></div>
          <p class="review-comment">{r.get('comment')}</p>{photos_html}
        </div>'''
        reviews_html.append(card_html)
    reviews_block_rendered = '\n'.join(reviews_html)

    # JS PRODUTO_ATUAL
    prod_js = {
        "id": pid,
        "nome": prod.get("nome"),
        "preco": prod.get("preco"),
        "preco_antigo": prod.get("preco_antigo"),
        "img": prod.get("img"),
        "imagens": prod.get("imagens", [])
    }
    prod_atual_js = json.dumps(prod_js, ensure_ascii=False, indent=2)

    # Replacements
    rendered = template_html
    rendered = rendered.replace('{{TITLE}}', title)
    rendered = rendered.replace('{{DESCRIPTION_META}}', meta_desc)
    rendered = rendered.replace('{{PRELOAD_IMAGE}}', preload_img or '')
    rendered = rendered.replace('{{PRODUCT_TITLE}}', prod.get('nome', ''))
    rendered = rendered.replace('{{PRICE_CURRENT_INT}}', price_int)
    rendered = rendered.replace('{{PRICE_CURRENT_CENTS}}', price_cents)
    rendered = rendered.replace('{{PRICE_ORIGINAL}}', price_orig)
    rendered = rendered.replace('{{DISCOUNT_PERCENT}}', discount_badge)
    rendered = rendered.replace('{{DISCOUNT_BADGE_TICKET}}', discount_badge)
    rendered = rendered.replace('{{INSTALLMENT_TEXT}}', installment)
    rendered = rendered.replace('{{RATING_AVG}}', rating)
    rendered = rendered.replace('{{RATING_COUNT}}', rating_count)
    rendered = rendered.replace('{{SOLD_COUNT}}', sold_count)
    rendered = rendered.replace('{{SLIDER_IMAGES}}', slider_images_rendered)
    rendered = rendered.replace('{{SLIDER_COUNTER}}', slider_counter)
    rendered = rendered.replace('{{DETALHES_GRID}}', details_grid_rendered)
    rendered = rendered.replace('{{REVIEWS_BLOCK}}', reviews_block_rendered)
    rendered = rendered.replace('{{PRODUTO_ATUAL_JS}}', prod_atual_js)
    rendered = rendered.replace('{{BTN_BUY_PRICE}}', f"R$ {prod.get('preco', 0):.2f}".replace('.', ','))

    # Description video
    desc_vid = prod.get('desc_video', {})
    if desc_vid.get('src'):
        vid_block = f'''<div class="product-video-block">
          <h3 class="about-subtitle">Vídeo</h3>
          <div class="tiktok-video-card" id="tt-product-video-wrapper" onclick="toggleTTVideo(event)">
            <video id="tt-product-video" src="{desc_vid['src']}" poster="{desc_vid.get('poster', '')}" loop muted playsinline webkit-playsinline></video>
            <div class="tiktok-play-overlay" id="tt-product-play-overlay">
              <svg viewBox="0 0 24 24" class="play-icon-tiktok"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
            </div>
            <div class="tiktok-video-controls" onclick="event.stopPropagation()">
              <button class="tiktok-control-btn play-pause-btn" onclick="toggleTTVideo(event)" aria-label="Play/Pause">
                <svg viewBox="0 0 24 24" class="ctrl-icon icon-play"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
                <svg viewBox="0 0 24 24" class="ctrl-icon icon-pause" style="display:none;"><rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect></svg>
              </button>
              <div class="tiktok-scrub-bar" onclick="seekTTVideo(event)">
                <div class="tiktok-scrub-fill" id="tt-scrub-fill"></div>
              </div>
              <span class="tiktok-time" id="tt-video-time">0:00 / 0:00</span>
              <button class="tiktok-control-btn fullscreen-btn" onclick="toggleTTFullscreen(event)" aria-label="Tela cheia">
                <svg viewBox="0 0 24 24" class="ctrl-icon"><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>
              </button>
            </div>
          </div>
        </div>'''
        rendered = rendered.replace('{{PRODUCT_VIDEO_BLOCK}}', vid_block)
    else:
        rendered = rendered.replace('{{PRODUCT_VIDEO_BLOCK}}', '')

    # Description content
    rendered = rendered.replace('{{DESCRICAO_HTML}}', prod.get('desc_html', ''))

    return rendered

def build_all(target_id=None):
    start_time = time.time()
    template_html = load_master_template()
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    count = 0
    for pid_str, prod in catalog.items():
        pid = int(pid_str)
        if target_id is not None and pid != target_id:
            continue

        html_out = render_product(prod, template_html)
        out_path = os.path.join(OUTPUT_DIR, f"produto-{pid}.html")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html_out)
        count += 1

    elapsed = (time.time() - start_time) * 1000
    print(f"[+] Build SSG Finalizado com Sucesso!")
    print(f"    - Total de páginas geradas: {count}")
    print(f"    - Tempo de compilação: {elapsed:.1f}ms")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="SSG Stone Shop Catalog Builder")
    parser.add_argument('--id', type=int, help="Build a specific product ID")
    parser.add_argument('--all', action='store_true', help="Build all products")
    args = parser.parse_args()

    if args.id:
        build_all(target_id=args.id)
    else:
        build_all()
