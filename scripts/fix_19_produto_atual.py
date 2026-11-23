import re, json

pages_to_fix = [74, 96, 97, 99, 100, 102, 103, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 120, 124]

for pid in pages_to_fix:
    fpath = f'pages/produto-{pid}.html'
    with open(fpath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Title
    m_title = re.search(r'<title>(.*?)</title>', text)
    title = m_title.group(1).split('-')[0].strip() if m_title else f"Produto {pid}"
    
    # Price
    m_p = re.search(r'class="price-current">(\d+)<span class="price-cents">,(\d+)</span>', text)
    price = float(f"{m_p.group(1)}.{m_p.group(2)}") if m_p else 49.90
    
    # Price orig
    m_po = re.search(r'class="price-original">R\$\s*([\d\.,]+)', text)
    if m_po:
        old_price = float(m_po.group(1).replace('.', '').replace(',', '.'))
    else:
        old_price = price * 3.5
    
    # Slides
    slides = re.findall(r'class="slider-img"[^>]+src="(.*?)"', text)
    if not slides:
        slides = ["../img/logo.png"]
    
    # Options row
    idx_opt = text.find('info-row-opcoes-content')
    opt_imgs = []
    opt_text = ""
    if idx_opt != -1:
        chunk = text[idx_opt:idx_opt+1000]
        m_txt = re.search(r'class="info-row-title">(.*?)</span>', chunk)
        if m_txt:
            opt_text = m_txt.group(1)
        opt_imgs = re.findall(r'<img[^>]+src="(.*?)"', chunk)
    
    # Build variations structure
    variacoes = {}
    
    if pid == 106: # Body Modelador
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Preto", "imagem": "../img/sku-106-preto.jpg", "preco": price},
                    {"nome": "Bege", "imagem": "../img/sku-106-bege.jpg", "preco": price}
                ]
            },
            "tamanho": {
                "label": "Tamanho",
                "opcoes": ["P", "M", "G", "GG"]
            }
        }
    elif pid == 107: # Mini Aspirador
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Preto", "imagem": slides[0], "preco": price},
                    {"nome": "Branco", "imagem": slides[1] if len(slides)>1 else slides[0], "preco": price}
                ]
            }
        }
    elif pid == 108: # Escova 5 em 1
        variacoes = {
            "voltagem": {
                "label": "Voltagem",
                "opcoes": ["110V", "220V", "Bivolt"]
            },
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Rosa e Cinza", "imagem": slides[0], "preco": price},
                    {"nome": "Dourado e Preto", "imagem": slides[1] if len(slides)>1 else slides[0], "preco": price}
                ]
            }
        }
    elif pid == 109: # Modelador de Cachos
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Cinza e Roxo", "imagem": slides[0], "preco": price},
                    {"nome": "Branco e Dourado", "imagem": slides[1] if len(slides)>1 else slides[0], "preco": price}
                ]
            }
        }
    elif pid == 110: # Tenis Kappa
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Preto com Grafite", "imagem": slides[0], "preco": price},
                    {"nome": "Branco com Marinho", "imagem": slides[1] if len(slides)>1 else slides[0], "preco": price},
                    {"nome": "All Black", "imagem": slides[2] if len(slides)>2 else slides[0], "preco": price}
                ]
            },
            "tamanho": {
                "label": "Tamanho",
                "opcoes": ["38", "39", "40", "41", "42", "43"]
            }
        }
    elif pid == 111: # Projetor Natalino
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Preto", "imagem": slides[0], "preco": price}
                ]
            }
        }
    elif pid == 112: # Patinhos
        variacoes = {
            "modelo": {
                "label": "Modelo",
                "opcoes": [
                    {"nome": "Pista Escada + 3 Patinhos Amarelos", "imagem": slides[0], "preco": price},
                    {"nome": "Pista Escada + 6 Patinhos Amarelos", "imagem": slides[0], "preco": price + 10.0}
                ]
            }
        }
    elif pid == 113: # Comedouro
        variacoes = {
            "modelo": {
                "label": "Modelo",
                "opcoes": [
                    {"nome": "Tigela Dupla Transparente", "imagem": slides[0], "preco": price}
                ]
            }
        }
    elif pid == 114: # Arcade
        variacoes = {
            "conexao": {
                "label": "Conexão",
                "opcoes": [
                    {"nome": "USB Plug & Play Multiplataforma", "imagem": slides[0], "preco": price}
                ]
            }
        }
    elif pid == 120: # Sofa
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Cinza Chumbo", "imagem": slides[0], "preco": price},
                    {"nome": "Bege Areia", "imagem": slides[1] if len(slides)>1 else slides[0], "preco": price}
                ]
            }
        }
    elif pid == 124: # Livro infantil
        variacoes = {
            "idioma": {
                "label": "Edição",
                "opcoes": [
                    {"nome": "Bilíngue Português / Inglês", "imagem": slides[0], "preco": price}
                ]
            }
        }
    elif pid in [74, 99]: # Camisas de futebol
        variacoes = {
            "tamanho": {
                "label": "Tamanho",
                "opcoes": ["P", "M", "G", "GG"]
            },
            "kit": {
                "label": "Kit 2 Camisas",
                "opcoes": [
                    {"nome": "Home (Titular) + Away (Reserva)", "imagem": slides[0], "preco": price}
                ]
            }
        }
    elif pid in [96, 97]: # Aparelho de jantar
        variacoes = {
            "conjunto": {
                "label": "Conjunto",
                "opcoes": [
                    {"nome": "Jogo Completo de Porcelana", "imagem": slides[0], "preco": price}
                ]
            }
        }
    elif pid == 100: # iPhone
        variacoes = {
            "capacidade": {
                "label": "Capacidade",
                "opcoes": ["128GB", "256GB"]
            },
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Preto", "imagem": slides[0], "preco": price},
                    {"nome": "Azul", "imagem": slides[1] if len(slides)>1 else slides[0], "preco": price}
                ]
            }
        }
    elif pid == 102: # Scooter
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Preta", "imagem": slides[0], "preco": price},
                    {"nome": "Laranja", "imagem": slides[1] if len(slides)>1 else slides[0], "preco": price}
                ]
            }
        }
    elif pid == 103: # Vestido
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Preto", "imagem": slides[0], "preco": price},
                    {"nome": "Vermelho", "imagem": slides[1] if len(slides)>1 else slides[0], "preco": price}
                ]
            },
            "tamanho": {
                "label": "Tamanho",
                "opcoes": ["P", "M", "G"]
            }
        }
    elif pid == 105: # Projetor HY300
        variacoes = {
            "cor": {
                "label": "Cor",
                "opcoes": [
                    {"nome": "Branco Smart Android 11 4K", "imagem": slides[0], "preco": price}
                ]
            }
        }
    else:
        # Generic fallback based on slides
        variacoes = {
            "modelo": {
                "label": "Modelo",
                "opcoes": [
                    {"nome": "Padrão Original", "imagem": slides[0], "preco": price}
                ]
            }
        }
    
    prod_obj = {
        "id": pid,
        "nome": title,
        "preco": price,
        "preco_antigo": old_price,
        "img": slides[0],
        "imagens": slides,
        "variacoes": variacoes
    }
    
    new_script = f"window.PRODUTO_ATUAL = {json.dumps(prod_obj, ensure_ascii=False, indent=2)};"
    
    # Replace window.PRODUTO_ATUAL = { ... };
    pattern = r'window\.PRODUTO_ATUAL\s*=\s*\{.*?\};'
    if re.search(pattern, text, re.DOTALL):
        new_text = re.sub(pattern, new_script, text, count=1, flags=re.DOTALL)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"P-{pid}: SUCCESS! PRODUTO_ATUAL updated with id={pid}, name={title[:30]}")
    else:
        print(f"P-{pid}: Pattern not matched!")

print("All 19 products updated!")
