import os, math
from PIL import Image, ImageDraw, ImageFont

def make_page(start, end, filename):
    files = [f'img/reviews-avatars/mulheres_validadas/mulher_{i}.jpg' for i in range(start, end + 1)]
    cols = 5
    rows = math.ceil(len(files) / cols)
    thumb_w, thumb_h = 160, 160
    label_h = 30
    
    img = Image.new('RGB', (cols * thumb_w, rows * (thumb_h + label_h)), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    for idx, f in enumerate(files):
        c = idx % cols
        r = idx // cols
        x = c * thumb_w
        y = r * (thumb_h + label_h)
        num = start + idx
        
        if os.path.exists(f):
            try:
                im = Image.open(f).convert('RGB')
                im = im.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                img.paste(im, (x, y))
            except Exception as e:
                pass
        
        draw.rectangle([x, y + thumb_h, x + thumb_w, y + thumb_h + label_h], fill=(20, 20, 20))
        draw.text((x + 10, y + thumb_h + 5), f'MULHER #{num}', fill=(255, 255, 0))
    
    img.save(filename, quality=90)
    print(f"Salvo {filename}")

make_page(1, 25, 'scripts/page1_1_to_25.jpg')
make_page(26, 50, 'scripts/page2_26_to_50.jpg')
make_page(51, 75, 'scripts/page3_51_to_75.jpg')
