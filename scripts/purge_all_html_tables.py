import os, glob, re

ds_dir = r"C:\Users\Dell\Downloads\ds"
clone_dir = r"C:\Users\Dell\Downloads\stone_shop_clone"

img_block_104 = """        <!-- SUBSEÇÃO 3: GUIA DE TAMANHOS OFICIAL DO VENDEDOR (IMAGEM REAL) -->
        <div class="size-guide-block">
          <h3 class="about-subtitle">Guia de tamanhos</h3>
          <div class="size-guide-image-card" style="background: #fafafc; border-radius: 8px; padding: 12px; text-align: center; border: 1px solid #f0f0f2; margin-top: 6px;">
            <img src="../img/guia-tamanhos-104.png" alt="Tabela de Medidas - Calçados" style="max-width: 100%; height: auto; border-radius: 6px; display: block; margin: 0 auto;">
          </div>
        </div>"""

def process_repo(base_dir):
    pages = sorted(glob.glob(os.path.join(base_dir, "pages", "produto-*.html")))
    print(f"Processing {len(pages)} pages in {base_dir}...")
    
    table_pattern = re.compile(r'\s*<!--\s*SUBSE[^\n]*?3:[^\n]*?-->\s*<div class="size-guide-block">[\s\S]*?</div>\s*</div>', re.IGNORECASE)
    
    modified_count = 0
    errors = []
    
    for p in pages:
        fname = os.path.basename(p)
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            c = f.read()
            
        orig = c
        
        if fname == "produto-104.html":
            # Replace HTML table with real image block
            c, count = table_pattern.subn("\n" + img_block_104 + "\n", c)
            if count > 0:
                print(f"Replaced HTML table with real image in: {fname}")
        else:
            # Remove HTML table block completely
            c, count = table_pattern.subn("", c)
            if count > 0:
                modified_count += 1
                
        # Check tag balance
        open_divs = len(re.findall(r'<div\b', c, re.I))
        close_divs = len(re.findall(r'</div>', c, re.I))
        if open_divs != close_divs:
            errors.append(f"{fname}: open={open_divs}, close={close_divs}, diff={open_divs - close_divs}")
            
        if c != orig:
            with open(p, "w", encoding="utf-8") as f:
                f.write(c)
                
    print(f"Finished {base_dir}: modified {modified_count} files, errors: {len(errors)}")
    if errors:
        for err in errors[:10]:
            print("  ERROR:", err)

process_repo(ds_dir)
process_repo(clone_dir)
print("ALL DONE!")
