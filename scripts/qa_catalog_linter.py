import os, sys, re, glob, json
from PIL import Image

try:
    from rapidocr_onnxruntime import RapidOCR
    ocr_engine = RapidOCR()
except Exception:
    ocr_engine = None

BANNED_OCR_MARKETING_TERMS = [
    'descubra', 'compre agora', 'frete gratis', 'frete grátis', 
    'desconto', '% off', 'oferta especial', 'compre ja', 'compre já',
    'envio imediato', '4.98', '4.99', 'super oferta', 'garanta o seu'
]

def check_image_ocr(img_path):
    if not ocr_engine or not os.path.exists(img_path):
        return None
    try:
        res, _ = ocr_engine(img_path)
        if not res:
            return None
        detected_text = " ".join([item[1].lower() for item in res])
        for term in BANNED_OCR_MARKETING_TERMS:
            if term in detected_text:
                return f"Banner publicitário detectado no OCR ('{term}') em foto de unboxing: {img_path}"
    except Exception as e:
        pass
    return None

def run_linter(target_files=None, check_ocr=True):
    if not target_files:
        target_files = sorted(glob.glob('pages/produto-*.html'))
    
    print(f"=== INICIANDO QA CATALOG LINTER EM {len(target_files)} PRODUTOS ===")
    if check_ocr and ocr_engine:
        print("[OCR ATIVO] RapidOCR integrado para detecção de banners de marketing e falsos unboxings.")
    
    # Load videos-criadores.js
    with open('js/videos-criadores.js', 'r', encoding='utf-8', errors='ignore') as f:
        vjs = f.read()

    total_errors = 0
    results = {}

    for path in target_files:
        errors = []
        warnings = []
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            html = f.read()
            
        pid_m = re.search(r'produto-(\d+)\.html', path)
        pid = int(pid_m.group(1)) if pid_m else 0
        
        # 1. SLIDER CHECK (Prevenção do bug 1/0)
        track_match = re.search(r'<div class="slider-track">(.*?)</div>', html, re.DOTALL)
        if track_match:
            track_html = track_match.group(1)
            slider_imgs = re.findall(r'<img[^>]+class="[^"]*slider-img[^"]*"', track_html)
            all_imgs = re.findall(r'<img[^>]+>', track_html)
            if len(all_imgs) == 0:
                errors.append("Slider vazio: nenhuma imagem encontrada na track.")
            elif len(slider_imgs) == 0:
                errors.append(f"Bug 1/0 detectado! Imagens na track não têm a classe 'slider-img' ({len(all_imgs)} imagens sem classe).")
        else:
            warnings.append("Slider-track não encontrado.")

        # 2. BOTTOM BAR CHECK (Prevenção de quebra no mobile)
        if 'bottom-bar-icons' in html or 'bottom-bar-actions' in html or 'btn-buy-now' in html:
            errors.append("Bottom-bar com classes ad-hoc inválidas (quebra visual mobile).")
        if 'class="bottom-bar"' in html:
            if 'store-chat-image-group' not in html:
                warnings.append("Bottom-bar sem grupo oficial Loja/Chat (store-chat-image-group).")
            if 'btn-buy' not in html or 'btn-line1' not in html:
                errors.append("Botão de compra fora do padrão canônico (btn-buy / btn-line1).")

        # 3. STORE CARD CHECK (Deve haver no máximo 1 no HTML e NUNCA após a descrição)
        store_count = html.count('class="store-widget-section"')
        if store_count > 1:
            errors.append(f"Card da Stone Shop duplicado no HTML ({store_count} ocorrências)!")
        
        pos_store = html.find('class="store-widget-section"')
        pos_desc = html.find('class="about-product-section"')
        if pos_store != -1 and pos_desc != -1 and pos_store > pos_desc:
            errors.append("Card da Stone Shop posicionado após a descrição! Deve ficar antes da descrição.")

        # 4. DUPLICATE VIDEOS & CREATOR AVATARS CHECK EM VIDEOS-CRIADORES.JS
        # Localiza o dataset do produto em vjs
        dataset_m = re.search(rf'const [A-Z0-9_]*{pid}[A-Z0-9_]*_VIDEOS_MAP\s*=\s*\[(.*?)\];', vjs, re.DOTALL)
        if dataset_m:
            block = dataset_m.group(1)
            videos = re.findall(r'video:\s*["\']([^"\']+)["\']', block)
            if len(videos) > 0 and len(videos) != len(set(videos)):
                dups = len(videos) - len(set(videos))
                errors.append(f"Vídeos repetidos detectados no carrossel de criadores: {dups} duplicatas!")
            
            creator_avatars = re.findall(r'avatar:\s*["\']([^"\']+)["\']', block)
            for ca in creator_avatars:
                ca_path = ca.replace('../', '')
                if not os.path.exists(ca_path):
                    errors.append(f"Avatar de criador inexistente: {ca_path}")
                if pid == 124 and ('churras' in ca or 'biscuitt' in ca or 'chinelo' in ca):
                    errors.append(f"Contaminação de nicho no avatar do criador: {ca}!")

        # 5. REVIEW PHOTOS CHECK (Verifica existência das fotos e previne imagens vazias ou banners publicitários)
        review_photos = re.findall(r'src=["\'](\.\./img/reviews/[^"\'?]+)', html)
        for rp in review_photos:
            local_path = rp.replace('../', '')
            if not os.path.exists(local_path):
                errors.append(f"Foto de avaliação inexistente: {local_path}")
            elif check_ocr:
                ocr_issue = check_image_ocr(local_path)
                if ocr_issue:
                    errors.append(ocr_issue)

        # 6. REVIEW AVATAR CHECK (Existência e unicidade de fotos de perfil)
        avatars = list(dict.fromkeys(re.findall(r'src=["\'](\.\./img/reviews-avatars/[^"\'?]+)', html)))
        import hashlib
        seen_hashes = {}
        for av in avatars:
            local_path = av.replace('../', '')
            if not os.path.exists(local_path):
                warnings.append(f"Avatar inexistente: {local_path}")
            else:
                with open(local_path, 'rb') as af:
                    ahash = hashlib.md5(af.read()).hexdigest()
                if ahash in seen_hashes:
                    errors.append(f"Perfil de avaliação repetido detectado! {local_path} tem a mesma foto que {seen_hashes[ahash]}.")
                else:
                    seen_hashes[ahash] = local_path

        # 7. PRODUTO_ATUAL CHECK (Prevenção do bug R$ 0,00 e placeholder 80x80 no modal)
        if 'PRODUTO_ATUAL' not in html:
            errors.append("PRODUTO_ATUAL não declarado no script da página!")
        else:
            if 'price: 0' in html or 'preco: 0' in html or 'preco: 0.0' in html:
                errors.append("Preço zerado (R$ 0,00) detectado no PRODUTO_ATUAL!")
            if 'img:' not in html and 'image:' not in html:
                errors.append("Imagem principal ausente no PRODUTO_ATUAL (causa placeholder 80x80)!")

        status = "OK" if len(errors) == 0 else "ERRO"
        results[path] = {
            "status": status,
            "errors": errors,
            "warnings": warnings
        }
        
        if errors:
            total_errors += len(errors)
            print(f"[FALHA] {os.path.basename(path)} -> {errors}")

    print("\n=== RESUMO DO LINTER ===")
    print(f"Total de Erros Críticos Encontrados: {total_errors}")
    return total_errors == 0

if __name__ == "__main__":
    target = [sys.argv[1]] if len(sys.argv) > 1 else None
    success = run_linter(target)
    sys.exit(0 if success else 1)
