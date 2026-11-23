from PIL import Image

im1 = Image.open(r'C:/Users/Dell/.gemini/antigravity/brain/626aa811-f9a0-4dad-af48-4ab6e56722e5/.user_uploaded/media_1794376338312_f677364a.jpg')
im2 = Image.open(r'C:/Users/Dell/.gemini/antigravity/brain/626aa811-f9a0-4dad-af48-4ab6e56722e5/.user_uploaded/media_1794376339266_99fb1cd7.jpg')
w, h = im1.size

im1.crop((0, 110, w, 300)).save('scripts/header_im1.png')
im2.crop((0, 110, w, 300)).save('scripts/header_im2.png')

print("Saved header crops!")
