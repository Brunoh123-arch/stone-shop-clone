from PIL import Image, ImageDraw
import glob
import os

files = [f'img/review-8-c{i}-1.jpg' for i in range(1, 16) if os.path.exists(f'img/review-8-c{i}-1.jpg')]
print(f'P8 review images found: {len(files)}')

cols = 5
rows = (len(files) + cols - 1) // cols
w, h = 150, 150
grid = Image.new('RGB', (cols * w, rows * (h + 25)), (255, 255, 255))
draw = ImageDraw.Draw(grid)

for idx, p in enumerate(files):
    c = idx % cols
    r = idx // cols
    x = c * w
    y = r * (h + 25)
    try:
        im = Image.open(p).convert('RGB').resize((w, h))
        grid.paste(im, (x, y))
        draw.text((x + 5, y + h + 5), os.path.basename(p), fill=(0, 0, 0))
    except Exception as e:
        draw.text((x + 5, y + 20), 'ERR', fill=(255, 0, 0))

grid.save('scripts/grid_p8_reviews.jpg')
print('Saved scripts/grid_p8_reviews.jpg')
