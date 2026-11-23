# -*- coding: utf-8 -*-
import glob
import re

html_files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'produto-(\d+)', x).group(1)))

report = []

for hf in html_files:
    pid = int(re.search(r'produto-(\d+)', hf).group(1))
    with open(hf, 'r', encoding='utf-8') as f:
        html = f.read()

    # Pega slider-track
    track_m = re.search(r'<div class="slider-track"[^>]*>(.*?)</div>\s*(?:<div class="slider-counter"|<div class="slider-dots")', html, re.DOTALL)
    if track_m:
        imgs = re.findall(r'<img[^>]+class="slider-img"[^>]*>', track_m.group(1))
        # Pega o counter se existir
        counter_m = re.search(r'<div class="slider-counter">([^<]+)</div>', html)
        counter_txt = counter_m.group(1).strip() if counter_m else "Sem counter"
        report.append({
            "pid": pid,
            "file": hf,
            "img_count": len(imgs),
            "counter": counter_txt
        })
    else:
        # Tenta pegar qualquer img com class slider-img
        imgs = re.findall(r'<img[^>]+class="slider-img"[^>]*>', html)
        report.append({
            "pid": pid,
            "file": hf,
            "img_count": len(imgs),
            "counter": "Track nao encontrada"
        })

print("=" * 75)
print("   RELATÓRIO COMPLETO DE SLIDERS DE PRODUTO (BRUNO CTO)")
print("=" * 75)

one_image = [r for r in report if r["img_count"] <= 1]
two_to_three = [r for r in report if 2 <= r["img_count"] <= 3]
four_plus = [r for r in report if r["img_count"] >= 4]

print(f"[*] Total de produtos auditados: {len(report)}")
print(f"[*] Produtos com APENAS 1 imagem no slider: {len(one_image)}")
for r in one_image:
    print(f"  [-] P{r['pid']}: {r['img_count']} imagem | Counter: {r['counter']} | {r['file']}")

print(f"\n[*] Produtos com 2 a 3 imagens no slider: {len(two_to_three)}")
for r in two_to_three:
    print(f"  [-] P{r['pid']}: {r['img_count']} imagens | Counter: {r['counter']}")

print(f"\n[*] Produtos com 4+ imagens no slider (padrão saudável): {len(four_plus)}")
