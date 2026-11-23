# -*- coding: utf-8 -*-
"""
Auditoria Total de Sliders e Variacoes de Produtos da Stone Shop
Detecta:
1. Produtos com apenas 1 imagem no slider principal do topo.
2. Produtos com variacoes de cores/modelos desconectadas ou sem imagens reais.
"""
import glob
import re
import os

html_files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))

single_slide_products = []
variation_issues = []

for hf in html_files:
    pid = int(re.search(r'produto-(\d+)', hf).group(1))
    with open(hf, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Checagem do Slider Principal (topo)
    # Procura slides do carrossel principal
    slider_match = re.search(r'class=["\'](?:product-slider|main-slider|carousel|swiper-wrapper|slider-track)["\'][^>]*>(.*?)(?=</div>\s*</div>|\s*<div class="product-info|\s*<div class="price-section)', html, re.DOTALL)
    
    # Procura tags de imagem de produto
    prod_imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*class=["\'](?:slide-img|product-img|carousel-img|slider-img)[^"\']*["\']', html)
    if not prod_imgs:
        # Busca alternativa por img com produto-XX no src
        prod_imgs = re.findall(rf'<img[^>]+src=["\']([^"\']*produto-{pid}[^"\']*)["\']', html)

    # Remove duplicatas
    unique_imgs = list(set(prod_imgs))
    
    # Conta slides
    slide_count = len(unique_imgs)
    if slide_count <= 1:
        single_slide_products.append((pid, hf, unique_imgs))

    # 2. Checagem de Variacoes (SKUs)
    # Procura botoes de variacao
    var_options = re.findall(r'class=["\'](?:variation-option|sku-item|option-btn|var-btn)[^"\']*["\'][^>]*>(.*?)</div>', html, re.DOTALL)
    if var_options:
        var_imgs = [re.findall(r'src=["\']([^"\']+)["\']', opt) for opt in var_options]
        # Se tem variacao com nomes de cores diferentes mas todas usam a mesma imagem
        flat_imgs = [img[0] for img in var_imgs if img]
        if len(flat_imgs) > 1 and len(set(flat_imgs)) == 1:
            variation_issues.append((pid, "Todas as variacoes usam a mesma imagem!", flat_imgs[0]))

print("=" * 75)
print("   RELATÓRIO DE AUDITORIA DE SLIDERS E VARIAÇÕES (BRUNO CTO)")
print("=" * 75)
print(f"[*] Total de produtos auditados: {len(html_files)}")
print(f"[*] Produtos com apenas 1 imagem no slider: {len(single_slide_products)}")
for pid, fpath, imgs in single_slide_products[:20]:
    print(f"  [-] P{pid}: {fpath} (Imagens detectadas: {imgs})")

print(f"\n[*] Produtos com problemas de variacao/mesma imagem para cores diferentes: {len(variation_issues)}")
for pid, msg, sample in variation_issues[:15]:
    print(f"  [-] P{pid}: {msg} (Exemplo: {sample})")
