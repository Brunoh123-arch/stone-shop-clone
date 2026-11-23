from PIL import Image, ImageDraw
import glob
import os

files = []
for pid in [117, 118, 120, 122, 123]:
    files.extend(glob.glob(f'img/reviews/review-{pid}-*.webp'))

print(f'Total review images in 117-123: {len(files)}')

cols = 5
rows = (len(files) + cols - 1) // cols
w, h = 160, 160
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

grid.save('scripts/grid_117_123.jpg')
print(f'Saved scripts/grid_117_123.jpg')
