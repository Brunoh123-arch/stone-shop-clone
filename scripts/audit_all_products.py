import os
import glob
import re

def audit():
    pages = sorted(glob.glob('pages/produto-*.html'))
    print(f"Total de paginas auditadas: {len(pages)}")
    
    issues = {
        'img_404': [],
        'no_video_poster': [],
        'single_slider': [],
        'broken_variations': [],
        'shopee_aliexpress': [],
        'zero_or_broken_price': [],
        'missing_creators_mount': [],
        'overflow_tables': []
    }
    
    for p in pages:
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
            
        # 1. Checar imagens relativas
        imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
        for src in imgs:
            if src.startswith(('data:', 'http:', 'https:')):
                continue
            clean_src = src.split('?')[0].split('#')[0]
            real_path = os.path.normpath(os.path.join('pages', clean_src))
            if not os.path.exists(real_path):
                issues['img_404'].append((p, src))
                
        # 2. Vídeo de descrição sem poster
        vids = re.findall(r'<video[^>]+id=["\']tt-product-video["\'][^>]*>', html)
        for v in vids:
            if 'poster=' not in v:
                issues['no_video_poster'].append(p)
                
        # 3. Slider com 1 ou 0 imagens
        slider_imgs = re.findall(r'class=["\']slider-image["\']', html)
        # Se não usar a classe slider-image, checa .image-slider img
        if len(slider_imgs) == 0:
            slider_box = re.search(r'<div class=["\']image-slider["\'][^>]*>(.*?)</div>', html, re.DOTALL)
            if slider_box:
                slider_imgs = re.findall(r'<img', slider_box.group(1))
        if len(slider_imgs) < 2 and 'window.location.replace' not in html: # ignorar redirects
            issues['single_slider'].append((p, len(slider_imgs)))
            
        # 4. Checar variações quebradas (ex: img vazia ou sem data-image)
        var_btns = re.findall(r'<button[^>]+class=["\'][^"\']*variation-option[^"\']*["\'][^>]*>', html)
        for b in var_btns:
            if 'data-image=""' in b or 'src=""' in b:
                issues['broken_variations'].append((p, b[:80]))
                
        # 5. Menções proibidas
        for bad_word in ['shopee', 'aliexpress', 'moedas shopee', 'ali express']:
            if bad_word in html.lower():
                issues['shopee_aliexpress'].append((p, bad_word))
                
        # 6. Preço zerado ou bugado
        preco_match = re.search(r'class=["\']product-price["\'][^>]*>(.*?)</div>', html, re.DOTALL)
        if preco_match:
            preco_text = preco_match.group(1)
            if 'R$ 0,00' in preco_text or '0.0' in preco_text or 'NaN' in preco_text:
                issues['zero_or_broken_price'].append((p, preco_text.strip()))
                
        # 7. Creators section
        if 'creators-section' not in html and 'window.location.replace' not in html:
            issues['missing_creators_mount'].append(p)

        # 8. Tabelas com largura fixa em px que estouram no mobile (> 360px)
        wide_tables = re.findall(r'<table[^>]+width=["\']([0-9]+)["\']', html)
        for w in wide_tables:
            if int(w) > 360:
                issues['overflow_tables'].append((p, f"table width={w}"))

    print("\n================== RELATÓRIO DE AUDITORIA COMPLETA ==================")
    for key, lst in issues.items():
        print(f"\n[!] {key.upper()}: {len(lst)} casos encontrados")
        for item in lst[:8]:
            print(f"   -> {item}")
        if len(lst) > 8:
            print(f"   ... e mais {len(lst)-8}")

if __name__ == '__main__':
    audit()
