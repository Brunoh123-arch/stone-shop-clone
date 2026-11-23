import re, json

pids = [87, 88, 103, 106, 110]
for pid in pids:
    with open(f'pages/produto-{pid}.html', 'r', encoding='utf-8') as f:
        c = f.read()
    counter = re.search(r'slider-counter">([^<]+)</div>', c)
    c_txt = counter.group(1).strip() if counter else 'N/A'
    
    op_m = re.search(r'info-row-opcoes-content[\s\S]*?info-row-title">([^<]+)</span>', c)
    op_txt = op_m.group(1).strip() if op_m else 'N/A'
    
    # check images
    img_m = re.search(r'imagens:\s*(\[[\s\S]*?\]),', c)
    img_count = len(json.loads(img_m.group(1))) if img_m else 0
    
    # check variacoes
    var_m = re.search(r'variacoes:\s*(\{[\s\S]*?\})\s*\n\s*\};', c)
    var_keys = []
    if var_m:
        try:
            vd = json.loads(var_m.group(1))
            var_keys = list(vd.keys())
        except Exception:
            var_keys = ['JSON error']
            
    print(f"P{pid}: Slider={c_txt} (Catalogo tem {img_count} fotos) | Linha Opcoes='{op_txt}' | Chaves Variações={var_keys}")
