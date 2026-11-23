from PIL import Image, ImageDraw, ImageFont
import os

# Create a clean official TikTok Shop store avatar fallback (512x512)
img = Image.new('RGBA', (512, 512), color=(255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Circle background in TikTok subtle gray
draw.ellipse([8, 8, 504, 504], fill=(244, 245, 247, 255), outline=(230, 232, 235, 255), width=4)

# Draw a stylish store storefront / bag icon in TikTok red/dark
# Store roof / awning
points = [(128, 220), (384, 220), (352, 160), (160, 160)]
draw.polygon(points, fill=(254, 44, 85, 255))

# Store building body
draw.rectangle([160, 220, 352, 360], fill=(22, 24, 35, 255))
# Door
draw.rectangle([224, 270, 288, 360], fill=(255, 255, 255, 255))
# Windows
draw.rectangle([180, 250, 210, 290], fill=(255, 255, 255, 200))
draw.rectangle([302, 250, 332, 290], fill=(255, 255, 255, 200))

img.save('img/seller-default.png', 'PNG')
print("Created img/seller-default.png successfully!")
