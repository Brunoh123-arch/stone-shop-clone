import re, json, os

def get_product_slides(html_text):
    # pega as URLs de imagens válidas de PRODUTO_ATUAL.imagens ou de swiper-slide
    m_imgs = re.search(r'imagens:\s*(\[[^\]]+\])', html_text)
    if m_imgs:
        try:
            imgs = json.loads(m_imgs.group(1).replace("'", '"'))
            valid_imgs = [i for i in imgs if not re.search(r'\.(mp4|webm|ogg|mov)$', i, re.I)]
            if valid_imgs:
                return valid_imgs
        except:
            pass
    
    # fallback para tags img no slider
    slide_imgs = re.findall(r'<div class="swiper-slide"[^>]*>\s*<img[^>]+src=[\'"]([^\'"]+)[\'"]', html_text)
    if slide_imgs:
        return slide_imgs
    
    # fallback para p.img
    m_img = re.search(r'img:\s*[\'"]([^\'"]+)[\'"]', html_text)
    if m_img:
        return [m_img.group(1)]
    return ["../logo.png"]

def aplicar_variacoes_em_produto(pid, label_grupo, lista_opcoes_nomes):
    filepath = f"pages/produto-{pid}.html"
    if not os.path.exists(filepath):
        print(f"[!] Arquivo {filepath} não existe!")
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    slides = get_product_slides(html)
    
    # Monta as opções com imagens dos slides se tiver
    opcoes = []
    for idx, nome_opt in enumerate(lista_opcoes_nomes):
        img_opt = slides[idx % len(slides)]
        opcoes.append({
            "nome": nome_opt,
            "imagem": img_opt
        })
    
    novo_bloco_variacoes = {
        "modelo": {
            "com_imagem": True,
            "label": label_grupo,
            "opcoes": opcoes
        }
    }
    
    bloco_json_str = json.dumps(novo_bloco_variacoes, ensure_ascii=False, indent=4)
    # ajusta identação para o bloco JS
    bloco_js = ",\n  variacoes: " + bloco_json_str.replace('\n', '\n  ')
    
    # 1. Injeta ou substitui variacoes dentro de PRODUTO_ATUAL
    if re.search(r'PRODUTO_ATUAL\s*=\s*\{', html):
        # se já tem variacoes, substitui
        if re.search(r'variacoes:\s*\{.*?\n\s*\}', html, re.DOTALL):
            html = re.sub(r',\s*variacoes:\s*\{.*?\n\s*\}', bloco_js, html, count=1, flags=re.DOTALL)
        elif re.search(r'["\']variacoes["\']:\s*\{.*?\n\s*\}', html, re.DOTALL):
            html = re.sub(r',\s*["\']variacoes["\']:\s*\{.*?\n\s*\}', bloco_js, html, count=1, flags=re.DOTALL)
        else:
            # injeta antes do fechamento }; de PRODUTO_ATUAL
            m_end = re.search(r'(PRODUTO_ATUAL\s*=\s*\{.*?)(\n\s*\};)', html, re.DOTALL)
            if m_end:
                html = html[:m_end.end(1)] + bloco_js + html[m_end.start(2):]
    
    # 2. Alinha 100% das avaliações para baterem com lista_opcoes_nomes
    counter = 0
    def replace_var_attr(m):
        nonlocal counter
        opt = lista_opcoes_nomes[counter % len(lista_opcoes_nomes)]
        counter += 1
        return f'data-author-variation="{opt}"'
    
    html = re.sub(r'data-author-variation="[^"]*"', replace_var_attr, html)
    
    counter_date = 0
    def replace_date_text(m):
        nonlocal counter_date
        opt = lista_opcoes_nomes[counter_date % len(lista_opcoes_nomes)]
        counter_date += 1
        txt = m.group(0)
        if ' · ' in txt:
            data_part = txt.split(' · ')[0]
            return f'{data_part} · {opt}</div>'
        return txt
    
    html = re.sub(r'<div class="review-date">.*?</div>', replace_date_text, html)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"[+] P{pid}: Injetadas {len(lista_opcoes_nomes)} opções ('{label_grupo}') e alinhadas {counter} reviews 1:1.")
    return True

if __name__ == '__main__':
    print("Módulo de injeção carregado com sucesso.")
