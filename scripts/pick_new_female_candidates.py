import glob, os, math
from PIL import Image, ImageDraw

# Vamos listar candidatos em tiktok_real
candidates = glob.glob('img/reviews-avatars/tiktok_real/*.jpg')
print(f"Total candidatos: {len(candidates)}")

# Vamos gerar um grid com 30 candidatos para inspecionarmos
cols = 5
rows = 6
thumb_w, thumb_h = 160, 160
label_h = 30

img = Image.new('RGB', (cols * thumb_w, rows * (thumb_h + label_h)), color=(240, 240, 240))
draw = ImageDraw.Draw(img)

selected_candidates = candidates[100:130] # pegar fatia do meio
for idx, f in enumerate(selected_candidates):
    c = idx % cols
    r = idx // cols
    x = c * thumb_w
    y = r * (thumb_h + label_h)
    
    try:
        im = Image.open(f).convert('RGB')
        im = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        img.paste(im, (x, y))
    except:
        pass
    
    bname = os.path.basename(f)
    draw.rectangle([x, y + thumb_h, x + thumb_w, y + thumb_h + label_h], fill=(20, 20, 20))
    draw.text((x + 5, y + thumb_h + 5), bname[:18], fill=(0, 255, 255))

img.save('scripts/candidates_grid.jpg', quality=90)
print("Salvo scripts/candidates_grid.jpg")
