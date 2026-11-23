from PIL import Image, ImageDraw
import os

imgs = [
    'img/reviews-unboxing/sabala_31/unboxing_2.jpg',
    'img/reviews-unboxing/sabala_31/unboxing_3.jpg',
    'img/reviews-unboxing/sabala_31/unboxing_5.jpg',
    'img/reviews-unboxing/p35/jbl_1.jpg',
    'img/reviews-unboxing/p35/jbl_2.jpg',
    'img/reviews-unboxing/p35/jbl_5.jpg',
    'img/reviews-unboxing/p35/jbl_6.jpg',
    'img/review-61-real-1.jpg',
    'img/review-61-real-3.jpg',
    'img/review-83-real-1.jpg',
    'img/review-83-real-3.jpg'
]

valid = [p for p in imgs if os.path.exists(p)]
cols = 4
rows = (len(valid) + cols - 1) // cols
w, h = 180, 180
grid = Image.new('RGB', (cols * w, rows * (h + 30)), (255, 255, 255))
draw = ImageDraw.Draw(grid)

for idx, p in enumerate(valid):
    c = idx % cols
    r = idx // cols
    x = c * w
    y = r * (h + 30)
    try:
        im = Image.open(p).convert('RGB').resize((w, h))
        grid.paste(im, (x, y))
        draw.text((x + 5, y + h + 5), os.path.basename(p), fill=(0, 0, 0))
    except Exception as e:
        draw.text((x + 5, y + 20), 'ERR', fill=(255, 0, 0))

grid.save('scripts/grid_audio_reviews.jpg')
print(f'Saved scripts/grid_audio_reviews.jpg ({len(valid)} images)')
