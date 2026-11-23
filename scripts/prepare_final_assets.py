import os
from PIL import Image, ImageOps

def make_square_800(in_path, out_path, bg_color=(255, 255, 255)):
    with Image.open(in_path) as im:
        if im.mode in ('RGBA', 'P'):
            im = im.convert('RGB')
        w, h = im.size
        # We want clean 800x800.
        # Fit image within 800x800 with padding or smart crop
        target_size = (800, 800)
        im.thumbnail(target_size, Image.Resampling.LANCZOS)
        
        # Create square canvas with bg_color (default white)
        new_im = Image.new('RGB', target_size, bg_color)
        paste_x = (800 - im.width) // 2
        paste_y = (800 - im.height) // 2
        new_im.paste(im, (paste_x, paste_y))
        new_im.save(out_path, 'JPEG', quality=95)
        print(f"Processed: {out_path} ({new_im.size})")

def crop_center_square(in_path, out_path):
    with Image.open(in_path) as im:
        if im.mode in ('RGBA', 'P'):
            im = im.convert('RGB')
        w, h = im.size
        min_dim = min(w, h)
        left = (w - min_dim) // 2
        top = (h - min_dim) // 2
        right = left + min_dim
        bottom = top + min_dim
        cropped = im.crop((left, top, right, bottom))
        resized = cropped.resize((800, 800), Image.Resampling.LANCZOS)
        resized.save(out_path, 'JPEG', quality=95)
        print(f"Center Cropped: {out_path} (800x800)")

# 1. Body Modelador 106
# body_1: 3 shapewear bodysuits (cover)
crop_center_square('scripts/temp_images/body_1.jpg', 'img/produto-106-1.jpg')
# body_2: Black variation
crop_center_square('scripts/temp_images/body_2.jpg', 'img/produto-106-2.jpg')
# body_3: Beige variation
crop_center_square('scripts/temp_images/body_3.jpg', 'img/produto-106-3.jpg')
# body_1 top crop for fabric/clasps detail
with Image.open('scripts/temp_images/body_1.jpg') as im:
    w, h = im.size
    # crop bottom hooks and crotch detail
    hooks_crop = im.crop((w*0.3, h*0.5, w*0.9, h*0.95)).resize((800, 800), Image.Resampling.LANCZOS)
    hooks_crop.save('img/produto-106-4.jpg', 'JPEG', quality=95)
    print("Saved img/produto-106-4.jpg")

# body_6 or body_1 upper crop
with Image.open('scripts/temp_images/body_1.jpg') as im:
    w, h = im.size
    upper_crop = im.crop((w*0.05, h*0.05, w*0.8, h*0.65)).resize((800, 800), Image.Resampling.LANCZOS)
    upper_crop.save('img/produto-106-5.jpg', 'JPEG', quality=95)
    print("Saved img/produto-106-5.jpg")

# 2. Mini Aspirador 107
# Cover: Clean shot on pedestal with attachments (img_3.jpg)
crop_center_square('scripts/temp_asp2/img_3.jpg', 'img/produto-107-1.jpg')
# Variation Black: Isolated black vacuum (img_1.jpg in temp_asp2 or real_asp_7.jpg)
make_square_800('scripts/temp_asp/real_asp_7.jpg', 'img/produto-107-2.jpg')
# Variation White: Clean white background shot of vacuum (img_0.jpg in temp_asp2)
crop_center_square('scripts/temp_asp2/img_0.jpg', 'img/produto-107-3.jpg')
# Kit 3 nozzles: real_asp_4.jpg
crop_center_square('scripts/temp_asp/real_asp_4.jpg', 'img/produto-107-4.jpg')
# Turbo motor & HEPA: img_2.jpg
crop_center_square('scripts/temp_asp2/img_2.jpg', 'img/produto-107-5.jpg')

print("All 800x800 square product photos created successfully!")
