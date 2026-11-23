from PIL import Image
import os

for f in sorted(os.listdir('img/reviews-unboxing/piscina_13')):
    p = os.path.join('img/reviews-unboxing/piscina_13', f)
    im = Image.open(p)
    # Pegar cores predominantes e características
    print(f"=== {f} ===")
    print("Dimensões:", im.size)
