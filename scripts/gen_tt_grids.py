import glob, os, math
from PIL import Image, ImageDraw

candidates = glob.glob('img/reviews-avatars/tiktok_real/*.jpg')

def make_grid(files, out_path):
    cols = 6
    rows = math.ceil(len(files) / cols)
    thumb_w, thumb_h = 140, 140
    label_h = 24
    
    img = Image.new('RGB', (cols * thumb_w, rows * (thumb_h + label_h)), color=(240, 240, 240))
    draw = ImageDraw.Draw(img)
    
    for idx, f in enumerate(files):
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
        draw.text((x + 2, y + thumb_h + 3), bname[:16], fill=(255, 255, 0))
    img.save(out_path, quality=90)
    print(f"Salvo {out_path}")

make_grid(candidates[0:36], 'scripts/tt_grid_0_36.jpg')
make_grid(candidates[36:72], 'scripts/tt_grid_36_72.jpg')
