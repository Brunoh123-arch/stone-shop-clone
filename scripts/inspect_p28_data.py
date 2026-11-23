import re, json

with open('pages/produto-28.html', 'r', encoding='utf-8') as f:
    content = f.read()

m_img = re.search(r'imagens:\s*(\[.*?\]),', content)
if m_img:
    imgs = json.loads(m_img.group(1))
    print(f"Total de imagens no catalogo: {len(imgs)}")
    for i, img in enumerate(imgs):
        print(f"  Slide {i+1}: {img}")

m_var = re.search(r'variacoes:\s*(\{.*?\})\s*\n\s*\};', content)
if m_var:
    var_data = json.loads(m_var.group(1))
    opcoes = var_data.get('cor', {}).get('opcoes', [])
    print(f"\nTotal de opcoes brutas: {len(opcoes)}")
    for i, op in enumerate(opcoes):
        print(f"  Opcao {i+1}: {op['nome']} -> {op['imagem']}")

