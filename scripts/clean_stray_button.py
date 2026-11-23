import re
import glob

files = glob.glob('pages/produto-*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    # Pattern of stray button before <section class="about-product-section"
    pattern = r'(\s*</div>\s*<button[^>]*Visitar</button>\s*</div>\s*)<section class="about-product-section"'
    if re.search(pattern, c):
        print(f"Cleaning stray button in {f}")
        c = re.sub(pattern, r'\n<section class="about-product-section"', c)
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(c)
