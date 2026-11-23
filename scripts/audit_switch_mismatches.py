import re, os, glob

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Mapear títulos de todos os 103 produtos
titles = {}
for h in glob.glob('pages/produto-*.html'):
    num = int(re.search(r'\d+', os.path.basename(h)).group())
    with open(h, 'r', encoding='utf-8', errors='ignore') as fp:
        m = re.search(r'<title>([^<]+)</title>', fp.read())
        t = m.group(1).strip() if m else 'N/A'
        # Limpar titulo
        t = re.sub(r'\s*-\s*Stone\s*Shop.*$', '', t, flags=re.I)
        titles[num] = t

# Analisar switch(prodId)
idx_s = c.find('switch (prodId)')
idx_e = c.find('default:', idx_s)
switch_block = c[idx_s:idx_e]

cases = re.findall(r'case\s+(\d+):\s*activeDataset\s*=\s*([^;]+);', switch_block)

print("=== AUDITORIA COMPLETA DE CONTAMINAÇÃO NOS 103 PRODUTOS ===")
mismatches = []
for p_str, dataset in cases:
    p_num = int(p_str)
    p_title = titles.get(p_num, f'Produto {p_num}')
    ds_clean = dataset.replace('buildNichePool(', '').split(',')[0].strip()
    
    print(f"P#{p_num:03d} | Titulo: {p_title[:45]:<45} | Dataset: {ds_clean}")
    
    # Heurística simples de flag de contaminação
    t_low = p_title.lower()
    ds_low = ds_clean.lower()
    
    flag = False
    if ('mochila' in t_low or 'rebecca' in t_low) and 'ar_' in ds_low: flag = True
    if ('carrinho' in t_low or 'bebe' in t_low or 'bebê' in t_low) and 'ar_' in ds_low: flag = True
    if ('prancha' in t_low or 'cabelo' in t_low) and 'wap' in ds_low: flag = True
    if ('panificadora' in t_low or 'pão' in t_low) and 'secadora' in ds_low: flag = True
    if ('bateria' in t_low or 'partida' in t_low) and 'sofa' in ds_low: flag = True
    if ('alfaiataria' in t_low or 'vestido' in t_low or 'roupa' in t_low) and 'panela' in ds_low: flag = True
    if ('caixa' in t_low or 'som' in t_low or 'jbl' in t_low or 'sabala' in t_low) and ('bike' in ds_low or 'secadora' in ds_low or 'climatizador' in ds_low): flag = True
    if ('piscina' in t_low) and ('churrasqueira' in ds_low): flag = True
    
    if flag:
        mismatches.append((p_num, p_title, ds_clean))
        print(f"  >>> ALERTA VERMELHO CONTAMINAÇÃO EM P#{p_num} <<<")

print(f"\nTotal produtos no switch: {len(cases)}")
print(f"Total contaminações absurdas detectadas: {len(mismatches)}")
