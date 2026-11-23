import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    index_html = f.read()

# Dados mapeados
products_to_add = [
    (6, "Bicicleta Ergométrica Fitness Cardio Sevenfit", "https://http2.mlstatic.com/D_NQ_NP_2X_679526-MLA100501405537_122025-F.webp", "147,00", "499,00", "-70%", "1.4K vendido(s)", "Fitness e Musculação"),
    (9, "Ar Condicionado Portátil HQ 8.500 BTU/h Frio", "img/produtos/p09/slide_1.jpg", "92,80", "1.299,00", "-92%", "3.8K vendido(s)", "Climatização e Ar"),
    (20, "Bicicleta Aro 29 GT Sprint MX7 24V MTB Freio Disco", "https://down-br.img.susercontent.com/file/br-11134207-81z1k-me910y70d7nmf6", "147,00", "599,00", "-75%", "2.1K vendido(s)", "Ciclismo"),
    (25, "Bicicleta Aro 20 Bmx Infantil GottBikes", "https://down-br.img.susercontent.com/file/br-11134207-81z1k-mer4ub5zgb9c1b", "109,00", "399,00", "-72%", "890 vendido(s)", "Ciclismo Infantil"),
    (36, "Celular Xiaomi Poco X7 Pro 5G 512GB Amarelo 12RAM", "img/produtos/p36/slide_1.jpg", "92,80", "2.499,00", "-96%", "9.5K vendido(s)", "Smartphones"),
    (50, "Lava e Seca Midea Master Clean Smart 11kg Titanium", "https://down-br.img.susercontent.com/file/sg-11134201-7rd5t-lvyp165360qj66", "247,90", "3.499,00", "-92%", "4.3K vendido(s)", "Eletrodomésticos"),
    (53, "Starlink V4 Internet Satélite Wi-Fi 6 Padrão Anatel", "https://down-br.img.susercontent.com/file/br-11134207-81z1k-me8xwns12tqb8f", "94,90", "2.199,00", "-95%", "6.7K vendido(s)", "Conectividade"),
    (55, "Nintendo Switch Desbloqueado + 10 Jogos MicroSD 128GB", "https://down-br.img.susercontent.com/file/br-11134207-7r98o-m024asxqvazr6b", "64,90", "1.899,00", "-96%", "8.2K vendido(s)", "Games e Consoles"),
    (56, "Esteira Elétrica Ergométrica Dobrável Heroi Sports", "esteirafotos/esteiraprimeirafoto.PNG", "69,90", "1.199,00", "-94%", "1.9K vendido(s)", "Fitness e Corrida"),
    (59, "Mini Internet Rápida Via Satélite Antena Original", "https://down-br.img.susercontent.com/file/br-11134207-7r98o-md1zj59a435t8d", "94,90", "1.799,00", "-94%", "2.5K vendido(s)", "Conectividade"),
    (65, "Sofá 3 Lugares Retrátil e Reclinável Cama inBox 2,00m", "https://down-br.img.susercontent.com/file/sg-11134201-7rdxn-lzou0oyl6coa73", "147,90", "1.599,00", "-90%", "3.1K vendido(s)", "Móveis e Sala"),
    (82, "Lava e Seca 11kg Hisense 11 Programas Titanium", "https://down-br.img.susercontent.com/file/br-11134207-7r98o-man0mifag5bt63", "257,90", "3.299,00", "-92%", "1.6K vendido(s)", "Eletrodomésticos"),
    (89, "Kit Conjunto de Panelas de Ferro Esmaltadas Luxo 18 Peças", "https://down-br.img.susercontent.com/file/br-11134207-81ztc-mj765kpbq3nla8", "79,90", "699,00", "-88%", "4.7K vendido(s)", "Utilidades Domésticas"),
    (94, "Bicicleta Bike Ergométrica Spinning Academia 120kg", "https://down-br.img.susercontent.com/file/br-11134207-7r98o-m78dqlbsalos96", "147,00", "999,00", "-85%", "2.8K vendido(s)", "Fitness e Musculação"),
    (96, "Aparelho de Jantar Oxford Ryo Maresia 30 Peças", "https://down-br.img.susercontent.com/file/sg-11134201-7rd5p-m7uwvu85tnp9ae", "69,90", "499,00", "-86%", "3.4K vendido(s)", "Mesa Posta"),
    (97, "Jogo de Jantar Canyon Porcelana Decorada 20 Peças", "https://down-br.img.susercontent.com/file/sg-11134201-81zwa-mimr7kh9srno54", "69,90", "399,00", "-82%", "1.8K vendido(s)", "Mesa Posta"),
    (100, "Apple iPhone 15 / 15 Plus / 15 Pro / 15 Pro Max", "img/iphones/15/preto/1.png", "108,90", "4.899,00", "-97%", "14.2K vendido(s)", "Smartphones"),
    (101, "Pneus Pirelli Original - Alta Durabilidade e Segurança", "https://tyre24.pirelli.com/dynamic_engine/assets/visori/cake/p7cnt.png", "599,00", "899,00", "-33%", "5.6K vendido(s)", "Automotivo"),
    (102, "Scooter Elétrica TUI 1000W 2 Lugares Sem CNH", "imagemscooterpreta/D_NQ_NP_2X_712059-MLA99509048862_112025-F.webp", "99,90", "3.999,00", "-97%", "7.1K vendido(s)", "Mobilidade Urbana"),
    (106, "Body Modelador Cinta Alta Compressão Efeito Lipo", "img/produto-106-1.jpg", "29,90", "129,00", "-76%", "11.8K vendido(s)", "Moda Feminina"),
    (107, "Mini Aspirador de Pó Sem Fio Portátil e Soprador Turbo", "img/produto-107-1.jpg", "34,90", "149,00", "-76%", "9.4K vendido(s)", "Acessórios Automotivos"),
    (118, "Conjunto Sala de Jantar Mesa Tampo Chanfrado com 4 Cadeiras", "img/mesa-jantar-slide-1.webp", "589,00", "1.299,00", "-54%", "890 vendido(s)", "Móveis e Sala"),
    (119, "Combo Fardo Mega Fraldas Huggies Supreme Care & Pampers", "img/fraldas-slide-1.webp", "589,00", "899,00", "-34%", "1.5K vendido(s)", "Bebês e Crianças"),
    (120, "Sofá Retrátil e Reclinável 3 Lugares 2,10m Suede Premium", "img/sofa-slide-1.webp", "589,00", "1.799,00", "-67%", "2.2K vendido(s)", "Móveis e Sala"),
    (121, "Travesseiro Cervical Ortopédico Espuma Viscoelástica", "img/travesseiro-slide-1.webp", "219,00", "399,00", "-45%", "4.1K vendido(s)", "Cama e Banho"),
    (122, "Panela de Pressão Elétrica Digital 5L Painel Touch Inox", "img/panela-pressao-slide-1.webp", "589,00", "999,00", "-41%", "3.7K vendido(s)", "Eletroportáteis"),
    (123, "Lavadora de Alta Pressão Portátil Sem Fio 48V com Maleta", "img/lavadora-slide-1.webp", "589,00", "899,00", "-34%", "5.3K vendido(s)", "Ferramentas"),
    (124, "Livro Infantil Interativo Bilíngue Falante Inglês/Português", "img/livro-interativo-slide-1.webp", "97,90", "199,00", "-50%", "6.2K vendido(s)", "Brinquedos")
]

cards_html = []
for pid, title, img, cur, old, disc, sales, cat in products_to_add:
    card = f"""              <!-- Produto {pid}: {title} -->
              <a href="pages/produto-{pid}.html" data-cat="{cat}" data-nome="{title.lower()}" data-vendas="{sales.split()[0]}" data-id="{pid}" style="text-decoration: none; color: inherit;">
                <div class="card-inner-box">
                  <img src="{img}" alt="{title}" loading="lazy" class="card-thumb-img" referrerpolicy="no-referrer">
                  <div class="card-details-col">
                    <div class="card-top-info">
                      <h3 class="prod-card-title">{title}</h3>
                      <div class="prod-badge-row">
                        <span class="badge-frete-gratis">Frete grátis</span>
                      </div>
                    </div>
                    <div class="prod-bottom-info">
                      <div class="price-stack-col">
                        <div class="price-cur-row"><span class="currency">R$</span> {cur}</div>
                        <div class="price-old-row">
                          <div class="price-old-val">R$ {old}</div>
                          <span class="discount-pill">{disc}</span>
                        </div>
                      </div>
                      <div class="sales-count-txt">{sales}</div>
                    </div>
                  </div>
                </div>
              </a>"""
    cards_html.append(card)

new_cards_str = "\n\n" + "\n\n".join(cards_html) + "\n"

# Injetar logo apos o card 23
pos_23 = index_html.find('href="pages/produto-23.html"')
end_23 = index_html.find('</a>', pos_23) + 4

new_index_html = index_html[:end_23] + new_cards_str + index_html[end_23:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_index_html)

print("index.html ATUALIZADO COM OS 28 PRODUTOS RESTANTES! VITRINE 100% COMPLETA (103 PRODUTOS)!")
