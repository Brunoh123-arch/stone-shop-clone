import os
import glob
import re

base_dir = r'C:\Users\Dell\Downloads\stone_shop_clone'

# 1. Fix double </div> in produto-100.html and produto-102.html
for fname in ['produto-100.html', 'produto-102.html']:
    fpath = os.path.join(base_dir, 'pages', fname)
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            c = f.read()
        target = '10.0K vendidos</div>\n      </div>\n      </div>\n<!-- Frete'
        rep = '10.0K vendidos</div>\n      </div>\n<!-- Frete'
        if target in c:
            c = c.replace(target, rep)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Fixed double </div> in {fname}")
        else:
            # Check CRLF
            target_crlf = target.replace('\n', '\r\n')
            rep_crlf = rep.replace('\n', '\r\n')
            if target_crlf in c:
                c = c.replace(target_crlf, rep_crlf)
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(c)
                print(f"Fixed double </div> in {fname} (CRLF)")
            else:
                print(f"Target not found in {fname}")

# 2. Check div balance for all product pages
product_files = glob.glob(os.path.join(base_dir, 'pages', 'produto-*.html'))
unbalanced = []
for pf in product_files:
    with open(pf, 'r', encoding='utf-8') as f:
        txt = f.read()
    o = len(re.findall(r'<div[\s>]', txt))
    c = len(re.findall(r'</div>', txt))
    if o != c:
        unbalanced.append((os.path.basename(pf), o, c, o - c))

print(f"Total product pages: {len(product_files)}. Unbalanced count: {len(unbalanced)}")
if unbalanced:
    for u in unbalanced:
        print(f"  {u[0]}: Open {u[1]}, Close {u[2]}, Diff {u[3]}")
else:
    print("ALL PRODUCT PAGES ARE 100% BALANCED IN DIVS!")
