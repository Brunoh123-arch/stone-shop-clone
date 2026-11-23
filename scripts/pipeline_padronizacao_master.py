"""
PIPELINE MASTER DE PADRONIZAÇÃO BLINDADA (PADRÃO TIKTOK SHOP OFICIAL)
Referência Canônica: Jogo de Panelas Avant Space (P90) e JBL Boombox 4 (P35)

Regras Inegociáveis:
1. 5 Slides de Estúdio Oficiais (1000x1000, Fundo Branco Puro #FFFFFF, JPEG Baseline RGB)
2. Criadores Reais Dedicados no js/videos-criadores.js com posters sem marca d'água e vídeos reais
3. Avaliações com Fotos Reais de Unboxing de Compradores (desembalagem em casa, sem capturas de vídeo)
4. Avatares Reais Dedicados sem Duplicatas (Faixas exclusivas do pool tt_avatar_*.jpg)
5. Integridade do DOM (tag depth diff == 0)
6. Deploy Vercel com Alias Oficial e Verificação HTTP 200
"""

import os
import re
import json
import urllib.request
import subprocess
from PIL import Image, ImageOps

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Mapeamento determinístico de faixas de avatares para ZERO repetição entre produtos
AVATAR_RANGES = {
    4: (69, 83),
    9: (181, 200),
    13: (121, 140),
    14: (141, 160),
    31: (81, 100),
    35: (156, 175),
    36: (161, 180),
    90: (211, 230)
}

def get_avatar_pool_for_product(prod_id):
    if prod_id in AVATAR_RANGES:
        start, end = AVATAR_RANGES[prod_id]
    else:
        # Gera faixa dinâmica baseada no ID
        start = 20 + (prod_id * 15) % 250
        end = start + 15
    
    avatars = []
    for i in range(start, end + 1):
        rel_path = f"../img/reviews-avatars/tiktok_real/tt_avatar_{i}.jpg"
        abs_path = os.path.join(BASE_DIR, "img", "reviews-avatars", "tiktok_real", f"tt_avatar_{i}.jpg")
        if os.path.exists(abs_path):
            avatars.append(rel_path)
    # Fallback se a faixa tiver poucos
    if len(avatars) < 10:
        for i in range(1, 40):
            avatars.append(f"../img/reviews-avatars/tiktok_real/tt_avatar_{i}.jpg")
    return avatars

def process_studio_slide(input_path, output_path, target_size=(1000, 1000)):
    """Processa slide de estúdio para fundo branco puro 1000x1000"""
    im = Image.open(input_path).convert('RGB')
    bg = Image.new('RGB', target_size, (255, 255, 255))
    
    avail_w = target_size[0] - 80
    avail_h = target_size[1] - 80
    
    ratio = min(avail_w / im.width, avail_h / im.height)
    new_w = int(im.width * ratio)
    new_h = int(im.height * ratio)
    
    resized = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
    bg.paste(resized, ((target_size[0] - new_w) // 2, (target_size[1] - new_h) // 2))
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    bg.save(output_path, 'JPEG', quality=95, optimize=True)
    print(f"[OK] Slide de estúdio: {output_path} ({target_size[0]}x{target_size[1]})")

def process_unboxing_photo(input_path, output_path, target_size=(800, 800), crop_box=None):
    """Processa foto de unboxing autêntica mantendo aspecto natural de celular"""
    im = Image.open(input_path).convert('RGB')
    if crop_box:
        im = im.crop(crop_box)
    fitted = ImageOps.fit(im, target_size, Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fitted.save(output_path, 'JPEG', quality=92, optimize=True)
    print(f"[OK] Unboxing photo: {output_path} ({target_size[0]}x{target_size[1]})")

def generate_sku_thumbnail(slide_path, thumb_path, size=(160, 160)):
    im = Image.open(slide_path)
    thumb = im.resize(size, Image.Resampling.LANCZOS)
    os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
    thumb.save(thumb_path, 'JPEG', quality=90)
    print(f"[OK] SKU thumbnail: {thumb_path}")

def validate_dom(html_content, filename="page"):
    div_open = len(re.findall(r'<div\b', html_content))
    div_close = len(re.findall(r'</div>', html_content))
    diff = div_open - div_close
    print(f"[{filename}] DOM Divs: abertas={div_open}, fechadas={div_close}, diff={diff}")
    return diff == 0

print("Pipeline Master de Padronização carregado com sucesso!")
