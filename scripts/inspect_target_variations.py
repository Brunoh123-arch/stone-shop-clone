import re

pids = [14, 114, 118, 119, 120, 121, 122, 123]

for pid in pids:
    path = f"pages/produto-{pid}.html"
    txt = open(path, encoding='utf-8').read()
    print(f"\n--- PRODUTO {pid} ---")
    # find variation options
    opts = re.findall(r'<button[^>]*class="[^"]*variation-option[^"]*"[^>]*>([\s\S]*?)</button>', txt)
    clean_opts = [re.sub(r'<[^>]+>', '', o).strip() for o in opts]
    print(f"Variation buttons: {clean_opts}")
    # find PRODUTO_ATUAL variacoes
    m = re.search(r'variacoes:\s*(\{[\s\S]*?\n\s*\}),', txt)
    if m:
        print(f"PRODUTO_ATUAL variacoes snippet: {m.group(1)[:200]}")
