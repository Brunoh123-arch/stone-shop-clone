import subprocess
import os, shutil

src_root = '.'
dest_root = r'C:\Users\Dell\Downloads\tiktok shop'

# 1. Sync css/style.css
shutil.copy2('css/style.css', os.path.join(dest_root, 'css', 'style.css'))
print("Synced css/style.css")

# 2. Sync js files
for js_file in ['app.js', 'videos-criadores.js', 'catalogo.js']:
    src_p = os.path.join('js', js_file)
    dst_p = os.path.join(dest_root, 'js', js_file)
    if os.path.exists(src_p):
        shutil.copy2(src_p, dst_p)
        print(f"Synced js/{js_file}")

# 3. Sync all pages/*.html
pages_synced = 0
for f in os.listdir('pages'):
    if f.endswith('.html'):
        shutil.copy2(os.path.join('pages', f), os.path.join(dest_root, 'pages', f))
        pages_synced += 1
print(f"Synced {pages_synced} pages")

# 4. Sync index.html, real.html, stone.html
for rf in ['index.html', 'real.html', 'stone.html', 'carrinho.html']:
    if os.path.exists(rf):
        shutil.copy2(rf, os.path.join(dest_root, rf))
        print(f"Synced {rf}")

print("All synced to tiktok shop successfully!")

# 5. Sync img/ folder
src_img = 'img'
dst_img = os.path.join(dest_root, 'img')
if os.path.exists(src_img):
    os.makedirs(dst_img, exist_ok=True)
    subprocess.run(['robocopy', src_img, dst_img, '/E', '/NJH', '/NJS', '/NP'], capture_output=True)
    print('Synced img/ directory')
