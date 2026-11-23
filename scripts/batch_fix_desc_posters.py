import os
import glob
import re
import subprocess

os.makedirs('img/posters-desc', exist_ok=True)

pages = sorted(glob.glob('pages/produto-*.html'))
fixed = 0

for p in pages:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
        
    if 'window.location.replace' in html:
        continue
        
    m = re.search(r'<video[^>]+id=["\']tt-product-video["\'][^>]*>', html)
    if not m:
        continue
        
    tag = m.group(0)
    if 'poster=' in tag:
        continue
        
    # Extrair id do produto do nome do arquivo
    pid_m = re.search(r'produto-(\d+)\.html', p)
    if not pid_m:
        continue
    pid = pid_m.group(1)
    
    # Extrair src do video
    src_m = re.search(r'src=["\']([^"\']+)["\']', tag)
    if not src_m:
        continue
    src = src_m.group(1)
    
    poster_filename = f"poster-desc-{pid}.jpg"
    poster_rel_path = f"img/posters-desc/{poster_filename}"
    poster_attr_path = f"../img/posters-desc/{poster_filename}"
    
    # Se o poster ainda não foi gerado, gerar via ffmpeg ou fallback
    if not os.path.exists(poster_rel_path) or os.path.getsize(poster_rel_path) == 0:
        # Tentar ffmpeg
        real_src = src
        if not src.startswith(('http://', 'https://')):
            real_src = os.path.normpath(os.path.join('pages', src))
            
        print(f"[{pid}] Gerando poster a partir de: {real_src[:60]}...")
        cmd = [
            'ffmpeg', '-y', '-ss', '00:00:01', '-i', real_src,
            '-vframes', '1', '-q:v', '2', poster_rel_path
        ]
        res = subprocess.run(cmd, capture_output=True, timeout=15)
        
        # Se ffmpeg falhou, usar fallback da primeira imagem do slider
        if not os.path.exists(poster_rel_path) or os.path.getsize(poster_rel_path) == 0:
            first_img = re.search(r'<img[^>]+class=["\'][^"\']*slider-img[^"\']*["\'][^>]+src=["\']([^"\']+)["\']', html)
            if first_img:
                fallback_src = first_img.group(1)
                print(f"[{pid}] Fallback para primeira imagem do slider: {fallback_src[:50]}")
                poster_attr_path = fallback_src

    # Injetar o poster na tag <video ...>
    new_tag = tag.replace('id="tt-product-video"', f'id="tt-product-video" poster="{poster_attr_path}"')
    if new_tag != tag:
        new_html = html.replace(tag, new_tag)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(new_html)
        fixed += 1
        print(f"[{pid}] OK -> Poster injetado: {poster_attr_path}")

print(f"\nTotal de vídeos de descrição corrigidos com poster: {fixed}")
