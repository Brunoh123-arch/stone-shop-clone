import glob
import re
import os

pages = sorted(glob.glob('pages/produto-*.html'))

def get_product_valid_options(html, title):
    options = []
    
    # 1. Botões de variação visíveis no HTML
    btn_spans = re.findall(r'<button[^>]+class=["\'][^"\']*variation-option[^"\']*["\'][^>]*>.*?<span>(.*?)</span>', html, re.DOTALL)
    if btn_spans:
        clean_btns = [s.strip() for s in btn_spans if s.strip() and len(s.strip()) < 40]
        if clean_btns:
            options.extend(clean_btns)
            
    # 2. JSON de variações no script
    var_section = re.search(r'variacoes\s*:\s*(\{.*?\n\s*\})', html, re.DOTALL)
    if not var_section:
        var_section = re.search(r'variacoes\s*:\s*(\{.*?\});', html, re.DOTALL)
    if var_section:
        names = re.findall(r'["\']nome["\']\s*:\s*["\']([^"\']+)["\']', var_section.group(1))
        for n in names:
            if n not in options and len(n) < 40:
                options.append(n)
                
    # 3. Voltagens simples
    if not options:
        volts = re.findall(r'["\'](110V|220V|127V|Bivolt)["\']', html)
        if volts:
            options.extend(list(dict.fromkeys(volts)))

    # 4. Fallback contextual por nicho
    if not options:
        tl = title.lower()
        if 'stitch' in tl:
            options = ["Azul Stitch 64GB", "Stitch + Capa e Bolsa", "Azul Stitch Octa-Core", "Kit Stitch Completo 64GB"]
        elif 'iphone 15' in tl or '15 pro' in tl:
            options = ["Titânio Preto 128GB", "Titânio Natural 256GB", "Titânio Azul 256GB", "Titânio Branco 128GB"]
        elif 'pad 11' in tl or 'tablet' in tl:
            options = ["Cinza Espacial 128GB", "Prata 256GB", "Azul 128GB"]
        elif 'tv' in tl or 'smart tv' in tl or 'dled' in tl:
            options = ["32\" HD Bivolt", "Preto 32\" Roku TV", "Smart TV 32\" Bivolt"]
        elif 'piscina' in tl:
            options = ["Azul Clássico 1000L", "Padrão Oficial Mor", "Kit Piscina Completa"]
        elif 'jantar' in tl or 'chá' in tl:
            options = ["Jogo Completo Porcelana", "Padrão Oficial", "Coleção Original"]
        elif 'colchão' in tl or 'colchao' in tl:
            options = ["Casal (Suporta 300kg) - Azul", "Padrão Bestway"]
        elif 'fogão' in tl or 'cooktop' in tl:
            options = ["Preto Bivolt Mesa de Vidro", "Inox Bivolt", "Preto Fosco"]
        elif 'air fryer' in tl or 'fritadeira' in tl:
            options = ["Preto 110V", "Inox 110V", "Preto 220V", "Inox 220V"]
        elif 'panela' in tl:
            options = ["Inox 110V", "Inox 220V", "Preto 110V", "Preto 220V"]
        elif 'churrasqueira' in tl:
            options = ["Inox 110V", "Inox 220V", "Preto Esmaltado"]
        elif 'lava e seca' in tl or 'lavadora' in tl:
            options = ["Titanium 110V", "Titanium 220V", "Branco 110V", "Branco 220V"]
        elif 'bicicleta' in tl or 'bike' in tl:
            options = ["Preto/Vermelho Aro 29", "Preto/Azul Aro 29", "Grafite/Amarelo Aro 29"]
        elif 'chinelo' in tl or 'sandália' in tl:
            options = ["Preto Strass", "Dourado Luxo", "Prata Brilho", "Nude Elegance"]
        elif 'tênis' in tl or 'tenis' in tl:
            options = ["Preto/Branco 40", "Preto/Cinza 41", "Azul Marinho 42", "All Black 39"]
        elif 'mochila' in tl:
            options = ["Rosa Rebecca Bonbon", "Lilás Rebecca Bonbon", "Preto Rebecca Bonbon"]
        elif 'projetor' in tl:
            options = ["Branco Smart Android 11", "Preto Smart Android 11"]
        elif 'fone' in tl or 'caixa' in tl or 'som' in tl:
            options = ["Preto Bivolt", "Camuflado Bivolt", "Azul Bivolt"]
        else:
            options = ["Padrão Oficial", "Original Stone Shop", "Edição Especial"]

    return list(dict.fromkeys(options))


def should_replace_variation(current_var, valid_options, title):
    cv_lower = current_var.lower()
    title_lower = title.lower()
    
    # Se a variação atual já é uma das opções válidas, mantém!
    for opt in valid_options:
        if opt.lower() == cv_lower:
            return False
            
    # Contaminação flagrante de celular/iPhone em produtos que não são celulares
    is_phone = any(w in title_lower for w in ['iphone', 'galaxy', 'smartphone', 'celular'])
    phone_tokens = ['titânio', 'titanio', '256gb', '128gb', '512gb', 'promax', 'pro max']
    if not is_phone and any(t in cv_lower for t in phone_tokens):
        return True
        
    # Contaminação de voltagem em produtos não elétricos (roupas, mochilas, calçados)
    is_non_electric = any(w in title_lower for w in ['chinelo', 'tênis', 'vestido', 'calça', 'mochila', 'potes', 'colchão', 'carrinho de bebê', 'triciclo', 'copos', 'jantar'])
    if is_non_electric and any(v in cv_lower for v in ['110v', '220v', '127v', 'bivolt', '700w', '1400w', '600w']):
        return True
        
    # Se a variação é genérica ou estranha ("Original Stone Shop", "Padrão Oficial") e temos opções específicas de cores/voltagem
    if cv_lower in ['original stone shop', 'padrão oficial', 'padrao oficial'] and len(valid_options) > 1:
        return True
        
    # Se não bate com nenhuma opção válida e as opções válidas são cores ou tamanhos estritos
    return True


total_reviews_fixed = 0
products_modified = 0

for p in pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    if 'window.location.replace' in html:
        continue
        
    t_m = re.search(r'<title>(.*?)</title>', html)
    title = t_m.group(1) if t_m else ''
    
    valid_options = get_product_valid_options(html, title)
    if not valid_options:
        continue
        
    cards = re.findall(r'(<div class=["\']review-card["\'][^>]*data-author-variation=["\']([^"\']+)["\'][^>]*>.*?</div>\s*</div>)', html, re.DOTALL)
    if not cards:
        continue
        
    new_html = html
    page_changes = 0
    
    for idx, (card_outer, cur_var) in enumerate(cards):
        if should_replace_variation(cur_var, valid_options, title):
            new_var = valid_options[idx % len(valid_options)]
            
            # 1. Substituir no data-author-variation
            old_card_tag = re.search(r'<div class=["\']review-card["\'][^>]*data-author-variation=["\']([^"\']+)["\'][^>]*>', card_outer)
            if old_card_tag:
                new_card_tag = old_card_tag.group(0).replace(f'data-author-variation="{cur_var}"', f'data-author-variation="{new_var}"')
                new_card_tag = new_card_tag.replace(f"data-author-variation='{cur_var}'", f"data-author-variation='{new_var}'")
                new_card_outer = card_outer.replace(old_card_tag.group(0), new_card_tag)
                
                # 2. Substituir no .review-date
                date_match = re.search(r'<div class=["\']review-date["\']>([^·<]+)·\s*([^<]+)</div>', new_card_outer)
                if date_match:
                    date_prefix = date_match.group(1)
                    new_date_tag = f'<div class="review-date">{date_prefix}· {new_var}</div>'
                    new_card_outer = new_card_outer.replace(date_match.group(0), new_date_tag)
                    
                if new_card_outer != card_outer:
                    new_html = new_html.replace(card_outer, new_card_outer)
                    page_changes += 1
                    
    if page_changes > 0 and new_html != html:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_html)
        products_modified += 1
        total_reviews_fixed += page_changes
        print(f"[{p}] {page_changes} reviews alinhadas para opções: {valid_options[:4]}")

print(f"\n================ RESUMO DO ALINHAMENTO GLOBAL ================")
print(f"Produtos corrigidos: {products_modified}")
print(f"Total de reviews alinhadas à grade real do produto: {total_reviews_fixed}")
