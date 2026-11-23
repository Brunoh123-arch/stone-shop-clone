import glob, re, os
from PIL import Image

print("=== VARREDURA DE CAPTURAS DE VÍDEO FATIADAS EM SLIDERS E REVIEWS ===")

# Vamos checar imagens de review e de slider
review_imgs = glob.glob('img/review-*.jpg') + glob.glob('img/review-*.png') + glob.glob('img/review-*.webp')
slider_imgs = glob.glob('img/produto-*.jpg') + glob.glob('img/produto-*.webp')

print(f"Total fotos de review no disco: {len(review_imgs)}")
print(f"Total fotos de slider/produto no disco: {len(slider_imgs)}")

# Fatias de video tipicas tem resolucoes 720x1280, 540x960, 1080x1920 (aspect ratio 9:16)
suspicious_slices = []
for f in review_imgs:
    try:
        with Image.open(f) as im:
            w, h = im.size
            ratio = h / w if w > 0 else 0
            # Se for formato 9:16 vertical de video (aprox 1.77)
            if 1.70 <= ratio <= 1.85 and (w in [720, 1080, 540, 480] or h in [1280, 1920, 960, 854]):
                suspicious_slices.append((f, im.size, ratio))
    except:
        pass

print(f"\nImagens suspeitas de serem capturas fatiadas de vídeo (9:16 exato de celular/vídeo): {len(suspicious_slices)}")
for f, sz, r in suspicious_slices[:20]:
    print(f"  {f} -> {sz} (ratio {r:.2f})")
