import glob
import re

M_AVATARS = [f"../img/reviews-avatars/unique/m_{i}.jpg" for i in range(1, 58)]
W_AVATARS = [f"../img/reviews-avatars/unique/w_{i}.jpg" for i in range(1, 83)]

def process_catalog():
    files = sorted(glob.glob("pages/produto-*.html"), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))
    total_updated = 0

    for fpath in files:
        pid = int(re.search(r'produto-(\d+)', fpath).group(1))
        with open(fpath, "r", encoding="utf-8") as f:
            html = f.read()

        changed = False
        m_idx = (pid * 7) % len(M_AVATARS)
        w_idx = (pid * 11) % len(W_AVATARS)
        
        # 1. Substituir tags <div class="review-avatar-placeholder">X</div> diretas
        def rep_placeholder(m):
            nonlocal m_idx, w_idx, changed
            changed = True
            if (m_idx + w_idx) % 2 == 0:
                av = M_AVATARS[m_idx % len(M_AVATARS)]
                m_idx += 1
            else:
                av = W_AVATARS[w_idx % len(W_AVATARS)]
                w_idx += 1
            return f'<img loading="lazy" decoding="async" class="review-avatar" src="{av}" alt="Cliente">'

        html_new = re.sub(r'<div class="review-avatar-placeholder">[^<]+</div>', rep_placeholder, html)
        if html_new != html:
            html = html_new
            changed = True

        # 2. Substituir qualquer <img> que aponte para susercontent.com dentro de review-avatar
        def rep_shopee_img(m):
            nonlocal m_idx, w_idx, changed
            changed = True
            alt_match = re.search(r'alt="([^"]*)"', m.group(0))
            alt_val = alt_match.group(1) if alt_match else "Cliente"
            
            is_female = any(x in alt_val.lower() for x in ['maria', 'ana', 'silva', 'laura', 'carol', 'julia', 'camila', 'bruna', 'patricia', 'vanessa', 'ednalva', 'claudia'])
            if is_female:
                av = W_AVATARS[w_idx % len(W_AVATARS)]
                w_idx += 1
            else:
                if (m_idx + w_idx) % 2 == 0:
                    av = M_AVATARS[m_idx % len(M_AVATARS)]
                    m_idx += 1
                else:
                    av = W_AVATARS[w_idx % len(W_AVATARS)]
                    w_idx += 1
                    
            return f'<img loading="lazy" decoding="async" class="review-avatar" src="{av}" alt="{alt_val}">'

        html_new = re.sub(r'<img [^>]*src="https://down-br\.img\.susercontent\.com[^"]*"[^>]*>', rep_shopee_img, html)
        if html_new != html:
            html = html_new
            changed = True

        # 3. Limpar qualquer onerror remanescente que faça referência a review-avatar-placeholder
        html_new = re.sub(r'\s*onerror="this\.outerHTML=\'<div class=\\\'review-avatar-placeholder\\\'[^"]*"', '', html)
        if html_new != html:
            html = html_new
            changed = True

        # 4. Checar DOM antes de salvar
        div_o = len(re.findall(r'<div\b', html))
        div_c = len(re.findall(r'</div>', html))
        if div_o != div_c:
            print(f"ALERTA: P{pid} ficou com DOM desbalanceado (Diff: {div_o - div_c})! Abortando alteração neste arquivo.")
            continue

        if changed:
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(html)
            total_updated += 1

    print(f"Total de produtos atualizados com sucesso: {total_updated}")

if __name__ == "__main__":
    process_catalog()
