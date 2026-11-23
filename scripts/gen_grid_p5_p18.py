from PIL import Image, ImageDraw
import os

files = [
    'img/review-5-c1-1.jpg', 'img/review-5-c2-1.jpg', 'img/review-5-c3-1.jpg',
    'img/review-18-c1-1.jpg', 'img/review-18-c2-1.jpg', 'img/review-18-c3-1.jpg',
    'img/review-18-c4-1.jpg', 'img/review-18-c5-1.jpg', 'img/review-18-c6-1.jpg',
    'img/review-18-c7-1.jpg', 'img/review-18-c8-1.jpg'
]

valid = [p for p in files if os.path.exists(p)]
cols = 4
rows = (len(valid) + cols - 1) // cols
w, h = 160, 160
grid = Image.new('RGB', (cols * w, rows * (h + 25)), (255, 255, 255))
draw = ImageDraw.Draw(grid)

for idx, p in enumerate(valid):
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

grid.save('scripts/grid_p5_p18.jpg')
print(f'Saved scripts/grid_p5_p18.jpg')
