import re, json, os

with open('scripts/find_fixable_sliders.py', 'r', encoding='utf-8') as f:
    pass

from find_fixable_sliders import fixable_list

print(f"Total de produtos a serem corrigidos no slider: {len(fixable_list)}")

fixed_count = 0
for pid, cat_len, fpath, cat_imgs, title in fixable_list:
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Build slider track images HTML
    slide_tags = []
    for idx, img_url in enumerate(cat_imgs):
        alt_str = f"{title} - Slide {idx+1}"
        loading_attr = 'fetchpriority="high"' if idx == 0 else 'loading="lazy"'
        slide_tags.append(f'<img alt="{alt_str}" class="slider-img" decoding="async" {loading_attr} src="{img_url}"/>')

    new_track_content = "\n".join(slide_tags)
    new_slider_block = f'<div class="slider-track">\n{new_track_content}\n</div>\n<div class="slider-counter">1 / {len(cat_imgs)}</div>'

    # Pattern to find existing slider track and counter
    old_slider_pattern = r'<div class="slider-track">[\s\S]*?</div>\s*<div class="slider-counter">[^<]+</div>'
    
    if re.search(old_slider_pattern, html):
        html_new = re.sub(old_slider_pattern, new_slider_block, html, count=1)
        
        # Check if info-row-opcoes has "1 opção disponível" and adjust if variacoes has more
        var_m = re.search(r'variacoes:\s*(\{[\s\S]*?\})\s*\n\s*\};', html_new)
        if var_m:
            try:
                vd = json.loads(var_m.group(1))
                cores = vd.get('cor', {}).get('opcoes', [])
                tamanhos = vd.get('tamanho', {}).get('opcoes', [])
                
                parts = []
                if cores:
                    parts.append(f"{len(cores)} opções de cor" if len(cores) > 1 else "1 cor")
                if tamanhos:
                    parts.append(f"{len(tamanhos)} tamanhos" if len(tamanhos) > 1 else "1 tamanho")
                    
                if parts:
                    new_op_text = f"{', '.join(parts)} disponíveis"
                    html_new = re.sub(
                        r'(<div class="info-row-opcoes-content"[^>]*>[\s\S]*?<span class="info-row-title">)[^<]+(</span>)',
                        rf'\g<1>{new_op_text}\g<2>',
                        html_new,
                        count=1
                    )
            except Exception:
                pass

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(html_new)
            
        fixed_count += 1
        print(f"[*] P{pid:02d} ({os.path.basename(fpath)}): Slider expandido de 1 para {len(cat_imgs)} slides!")

print(f"\n[+] Total de produtos atualizados com sucesso: {fixed_count}/{len(fixable_list)}")
