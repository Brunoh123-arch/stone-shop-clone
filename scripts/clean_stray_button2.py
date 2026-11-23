import re
import glob

files = glob.glob('pages/produto-*.html')
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    # Target exact lines:
    target = '</div>\n<button style="background: #fe2c55; color: #ffffff; font-size: 13px; font-weight: 600; border-radius: 18px; padding: 6px 18px; border: none; cursor: pointer;" type="button">Visitar</button>\n</div>\n<section class="about-product-section"'
    target_crlf = target.replace('\n', '\r\n')
    
    replacement = '<section class="about-product-section"'
    
    if target in c:
        print(f"Cleaned LF in {f}")
        c = c.replace(target, replacement)
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(c)
    elif target_crlf in c:
        print(f"Cleaned CRLF in {f}")
        c = c.replace(target_crlf, replacement)
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(c)
