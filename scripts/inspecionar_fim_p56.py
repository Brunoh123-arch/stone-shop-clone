with open("pages/produto-56.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'related-products' in l or 'relacionados' in l.lower():
        print(f"Relacionados na linha {i+1}")
        for j in range(max(0, i-15), i+3):
            print(f"{j+1}: {lines[j].rstrip()[:100]}")
        break
