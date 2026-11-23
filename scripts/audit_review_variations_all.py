import glob
import re

pages = sorted(glob.glob('pages/produto-*.html'))
mismatches = []

# Palavras-chave suspeitas que indicam clonagem de celular
phone_keywords = ['titânio', 'titanio', '256gb', '128gb', '512gb', '64gb', 'promax', 'pro max']
shoe_keywords = ['tamanho 3', 'tamanho 4', 'numeração 3', 'numeração 4', '35/36', '37/38', '39/40']
voltage_keywords = ['110v', '220v', 'bivolt']

for p in pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    if 'window.location.replace' in html:
        continue
        
    t = re.search(r'<title>(.*?)</title>', html)
    title = t.group(1) if t else ''
    
    rev_vars = re.findall(r'data-author-variation=["\']([^"\']+)["\']', html)
    if not rev_vars:
        continue
        
    bad_in_this_page = []
    # Se o produto NÃO é celular nem tablet, mas tem variações de celular
    is_phone_or_tablet = any(w in title.lower() for w in ['iphone', 'galaxy', 'celular', 'smartphone', 'tablet', 'pad'])
    is_footwear = any(w in title.lower() for w in ['chinelo', 'tenis', 'tênis', 'sandalia', 'sandália', 'bota', 'sapato'])
    is_electric = any(w in title.lower() for w in ['eletric', 'elétric', 'fryer', 'panela', 'micro-ondas', 'secador', 'ventilador', 'aspirador', 'chuveiro', 'lavadora'])
    
    for v in rev_vars:
        vl = v.lower()
        if not is_phone_or_tablet and any(k in vl for k in phone_keywords):
            bad_in_this_page.append(f"Phone var in non-phone: '{v}'")
        if not is_footwear and any(k in vl for k in shoe_keywords):
            bad_in_this_page.append(f"Shoe var in non-shoe: '{v}'")
        if not is_electric and any(k in vl for k in voltage_keywords):
            bad_in_this_page.append(f"Voltage var in non-electric: '{v}'")
            
    # Checagem específica: tablet do Stitch com titânio
    if 'stitch' in title.lower():
        for v in rev_vars:
            if 'titânio' in v.lower() or 'preto' in v.lower() and 'stitch' not in v.lower():
                bad_in_this_page.append(f"Stitch tablet with iPhone var: '{v}'")
                
    if bad_in_this_page:
        mismatches.append((p, title[:45], set(bad_in_this_page)))

print(f"Total de produtos com contaminação detectada nas variações de reviews: {len(mismatches)}")
for p, t, b in mismatches[:15]:
    print(f"\n{p} ({t}):")
    for item in list(b)[:3]:
        print(f"   - {item}")
