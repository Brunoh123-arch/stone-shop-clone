import sys
sys.stdout.reconfigure(encoding='utf-8')

for p in ['pages/produto-104.html', 'pages/produto-4.html']:
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        c = f.read()
    pos_rel = c.find('class="related-section"')
    print(f"=== {p} a partir de related-section ===")
    print(c[pos_rel:pos_rel+1500])
    pos_fim = c.find('fim product-info')
    print(c[pos_fim-100:pos_fim+400])
