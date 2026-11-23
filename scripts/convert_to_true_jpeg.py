from PIL import Image
import os, glob

folders = ['img/produtos/p31', 'img/produtos/p36', 'img/reviews-unboxing/sabala_31', 'img/reviews-unboxing/poco_36']

for fld in folders:
    for f in os.listdir(fld):
        p = os.path.join(fld, f)
        if os.path.isfile(p):
            try:
                im = Image.open(p)
                rgb_im = im.convert('RGB')
                rgb_im.save(p, 'JPEG', quality=92)
                print(f"Converted {p} to true JPEG ({rgb_im.size})")
            except Exception as e:
                print(f"Error converting {p}: {e}")
