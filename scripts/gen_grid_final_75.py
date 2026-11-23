import os, math
from PIL import Image, ImageDraw

def make_grid():
    files = [f'img/reviews-avatars/mulheres_validadas/mulher_{i}.jpg' for i in range(1, 76)]
    cols = 10
    rows = math.ceil(len(files) / cols)
    thumb_w, thumb_h = 100, 100
    label_h = 20
    
    img = Image.new('RGB', (cols * thumb_w, rows * (thumb_h + label_h)), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    for idx, f in enumerate(files):
        c = idx % cols
        r = idx // cols
        x = c * thumb_w
        y = r * (thumb_h + label_h)
        num = idx + 1
        
        if os.path.exists(f):
            try:
                im = Image.open(f).convert('RGB')
                im = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                img.paste(im, (x, y))
            except:
                pass
        
        draw.rectangle([x, y + thumb_h, x + thumb_w, y + thumb_h + label_h], fill=(0, 0, 0))
        draw.text((x + 5, y + thumb_h + 3), f'#{num}', fill=(0, 255, 0))
    
    img.save('scripts/grid_final_75_mulheres.jpg', quality=90)
    print("Salvo scripts/grid_final_75_mulheres.jpg")

make_grid()
