import re
import os

STAR_SVG = '<svg viewBox="0 0 24 24" width="12" height="12" fill="#ffb800"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>'

def generate_stars(count):
    return '\n                '.join([STAR_SVG for _ in range(count)])

# Avatar pools: Even = Female, Odd = Male
FEMALE_AVATARS = [f"../img/reviews-avatars/tiktok_real/tt_avatar_{i}.jpg" for i in range(2, 221, 2)]
MALE_AVATARS = [f"../img/reviews-avatars/tiktok_real/tt_avatar_{i}.jpg" for i in range(1, 221, 2)]

# Define additions for each of the 8 products
ADDITIONS = {
    14: [
        {"name": "M**a S**a", "gender": "F", "stars": 5, "var": "220V · Preto", "date": "14/02", "comment": "Churrasqueira maravilhosa! Muito silenciosa girando e a carne assa por igual sem fazer fumaça. Minha família aprovou no domingo!"},
        {"name": "R**o S**a", "gender": "M", "stars": 5, "var": "110V · Preto", "date": "12/02", "comment": "Surpreendeu demais na economia de gás. Os 5 espetos giram macio e o vidro curvo é excelente para acompanhar o ponto da carne."},
        {"name": "C**a P**o", "gender": "F", "stars": 5, "var": "Inox · 220V", "date": "10/02", "comment": "Acabamento em inox impecável, muito fácil de limpar a bandeja coletora de gordura. Chegou em 3 dias aqui em Curitiba."},
        {"name": "T**o A**o", "gender": "M", "stars": 5, "var": "Inox 110V", "date": "08/02", "comment": "Excelente aquisição. Assa picanha e frango com perfeição. O motor bivolt é super prático pra levar pro rancho."},
        {"name": "J**e F**s", "gender": "F", "stars": 4, "var": "220V · Preto", "date": "05/02", "comment": "Produto muito bom e robusto! Só demorou um dia a mais que o previsto por causa dos correios daqui, mas a loja Stone Shop atendeu super bem."},
        {"name": "G**a R**s", "gender": "M", "stars": 5, "var": "110V · Preto", "date": "02/02", "comment": "Zero fumaça no apartamento! Usamos na sacada e não incomodou ninguém. Vale cada centavo investido."},
        {"name": "A**a N**a", "gender": "F", "stars": 5, "var": "Inox · 220V", "date": "29/01", "comment": "Comprei de presente pro meu marido e ele ficou apaixonado. A carne fica muito suculenta e assa bem rápido."},
        {"name": "H**o C**a", "gender": "M", "stars": 5, "var": "220V · Preto", "date": "26/01", "comment": "Sensacional, espetos firmes e cabos que não esquentam. A qualidade da Arke é incomparável."}
    ],
    114: [
        {"name": "K**s M**o", "gender": "M", "stars": 5, "var": "Arcade Stick Retrô 7 em 1 · Cabo USB 2.5m Plug & Play", "date": "15/02", "comment": "Sensibilidade do manche absurda de boa! Conectei no PC e no PS4 de primeira, sem input lag nenhum nos jogos de luta."},
        {"name": "V**r H**o", "gender": "M", "stars": 5, "var": "Arcade Stick Retrô 7 em 1 · Cabo USB 2.5m Plug & Play", "date": "11/02", "comment": "Base pesada e muito estável na mesa, os botões têm aquele clique nostálgico de fliperama dos anos 90. Recomendo forte!"},
        {"name": "F**a B**a", "gender": "F", "stars": 4, "var": "Arcade Stick Retrô 7 em 1 · Cabo USB 2.5m Plug & Play", "date": "07/02", "comment": "Comprei pro meu filho e ele adorou. Funciona perfeitamente no Switch e no computador. Cabo bem longo e resistente."}
    ],
    118: [
        {"name": "M**a S**a", "gender": "F", "stars": 5, "var": "Freijó / Assento Bege Off-White", "date": "14/02", "comment": "A mesa é um espetáculo! O tampo chanfrado dá um ar super moderno na sala e o tecido das cadeiras é um veludo muito gostoso.", "photo": "../img/reviews/review-118-1.webp"},
        {"name": "R**o S**a", "gender": "M", "stars": 5, "var": "Freijó / Assento Cinza Grafite", "date": "12/02", "comment": "Montagem simples e rápida com as ferramentas que vem junto. Cadeiras aguentam peso com muita firmeza e não balançam.", "photo": "../img/reviews/review-118-2.webp"},
        {"name": "C**a P**o", "gender": "F", "stars": 5, "var": "Freijó / Assento Bege Off-White", "date": "10/02", "comment": "Ficou linda demais na minha copa! Chegou tudo super bem embalado sem nenhum arranhão. Recomendo muito!"},
        {"name": "D**o M**s", "gender": "M", "stars": 5, "var": "Preto Fosco / Assento Linho", "date": "08/02", "comment": "Qualidade acima do que eu esperava pelo preço promocional. A madeira é pesada e o acabamento UV é bem brilhoso."},
        {"name": "J**e F**s", "gender": "F", "stars": 4, "var": "Freijó / Assento Cinza Grafite", "date": "06/02", "comment": "Conjunto lindo e confortável! Apenas a caixa das cadeiras estava um pouco amassada na ponta, mas os móveis estavam intactos dentro."},
        {"name": "G**a R**s", "gender": "M", "stars": 5, "var": "Freijó / Assento Bege Off-White", "date": "04/02", "comment": "Entrega relâmpago da Stone Shop, chegou em 4 dias no interior de SP. Cadeiras super fofas e fáceis de montar."},
        {"name": "A**a N**a", "gender": "F", "stars": 5, "var": "Freijó / Assento Cinza Grafite", "date": "01/02", "comment": "Melhor compra que fiz para meu apartamento novo. Tamanho de 1,20m é perfeito, cabe certinho sem apertar o espaço."},
        {"name": "W**r P**a", "gender": "M", "stars": 5, "var": "Freijó / Assento Bege Off-White", "date": "29/01", "comment": "Estrutura reforçada e parafusos de boa qualidade. Já estamos usando todos os dias no almoço em família."},
        {"name": "L**a M**s", "gender": "F", "stars": 5, "var": "Preto Fosco / Assento Linho", "date": "27/01", "comment": "O tom da madeira combinou perfeitamente com os armários da minha cozinha. Estofado muito macio!"},
        {"name": "M**o B**o", "gender": "M", "stars": 5, "var": "Freijó / Assento Cinza Grafite", "date": "24/01", "comment": "Recomendo a todos, acabamento de primeira linha e excelente custo-benefício. Nota 10!"},
        {"name": "B**z L**a", "gender": "F", "stars": 5, "var": "Freijó / Assento Bege Off-White", "date": "21/01", "comment": "Todo mundo que vem em casa elogia a mesa. Valeu muito a pena aproveitar a promoção do TikTok Shop."},
        {"name": "Y**a C**o", "gender": "M", "stars": 4, "var": "Freijó / Assento Bege Off-White", "date": "18/01", "comment": "Muito bonita e resistente. A montagem exige um pouco de paciência, mas seguindo o manual fica perfeita."},
        {"name": "P**a S**s", "gender": "F", "stars": 5, "var": "Freijó / Assento Cinza Grafite", "date": "15/01", "comment": "Perfeição define! Mesa espaçosa e cadeiras que abraçam as costas com a espuma D-23."}
    ],
    119: [
        {"name": "M**a S**a", "gender": "F", "stars": 5, "var": "Tamanho M (5,5 a 9,5kg)", "date": "15/02", "comment": "Fralda maravilhosa! Segura a noite todinha sem vazar e os lenços são super cheirosos e grossinhos.", "photo": "../img/reviews/review-119-4.webp"},
        {"name": "C**a P**o", "gender": "F", "stars": 5, "var": "Tamanho G", "date": "13/02", "comment": "O fardo mega vale muito a pena pelo valor promocional. Huggies Supreme Care é a melhor para pele sensível."},
        {"name": "R**o S**a", "gender": "M", "stars": 5, "var": "Tamanho M (5,5 a 9,5kg)", "date": "11/02", "comment": "Comprei pro meu filho, economia surreal comparado com farmácia de rua. Chegou rápido e bem lacrado."},
        {"name": "J**e F**s", "gender": "F", "stars": 5, "var": "Tamanho XG", "date": "09/02", "comment": "Cintura elástica perfeita que não aperta a barriguinha do bebê. Os lenços vêm com tampa flip-top que não resseca."},
        {"name": "L**a M**s", "gender": "F", "stars": 4, "var": "Tamanho G", "date": "07/02", "comment": "Excelente kit para abastecer o mês! Super recomendo para todas as mamães."},
        {"name": "F**a B**a", "gender": "F", "stars": 5, "var": "Tamanho M (5,5 a 9,5kg)", "date": "04/02", "comment": "Zero assaduras aqui em casa desde que comecei a usar essa linha Supreme Care. Stone Shop de parabéns!"},
        {"name": "G**a R**s", "gender": "M", "stars": 5, "var": "Tamanho G", "date": "02/02", "comment": "Entrega excelente, fardo original de fábrica. Já comprei mais dois kits para garantir estoque."},
        {"name": "A**a N**a", "gender": "F", "stars": 5, "var": "Tamanho XG", "date": "30/01", "comment": "Lenços umedecidos sem álcool e com cheirinho suave. Fraldas com absorção incrível de até 12h."},
        {"name": "B**z L**a", "gender": "F", "stars": 5, "var": "Tamanho M (5,5 a 9,5kg)", "date": "27/01", "comment": "Muito satisfeita! Minha bebê acorda sequinha todas as manhãs. Recomendo de olhos fechados."},
        {"name": "T**o A**o", "gender": "M", "stars": 5, "var": "Tamanho G", "date": "24/01", "comment": "Melhor custo benefício da internet. Preço imbatível e qualidade indiscutível."},
        {"name": "P**a S**s", "gender": "F", "stars": 4, "var": "Tamanho XG", "date": "21/01", "comment": "Ótimo produto, fardo bem volumoso. Entrega dentro do prazo anunciado."},
        {"name": "E**a S**a", "gender": "F", "stars": 5, "var": "Tamanho M (5,5 a 9,5kg)", "date": "18/01", "comment": "Salvou meu orçamento do mês! Fraldas excelentes e lenços de primeira qualidade."},
        {"name": "S**a M**s", "gender": "F", "stars": 5, "var": "Tamanho G", "date": "15/01", "comment": "Tudo original e com validade longa para 2027. Recomendo a compra!"}
    ],
    120: [
        {"name": "M**a S**a", "gender": "F", "stars": 5, "var": "Cinza Chumbo", "date": "14/02", "comment": "Sofá gigante e extremamente aconchegante! O veludo suede é uma delícia ao toque e a espuma D-28 sustenta muito bem.", "photo": "../img/review-120-real-1.jpg"},
        {"name": "R**o S**a", "gender": "M", "stars": 5, "var": "Bege Claro", "date": "12/02", "comment": "Abertura retrátil corre macia e o encosto reclinável tem vários níveis de ajuste. Ficou perfeito na sala de TV.", "photo": "../img/review-120-real-2.jpg"},
        {"name": "C**a P**o", "gender": "F", "stars": 5, "var": "Cinza Chumbo", "date": "10/02", "comment": "Deitei nele e não queria mais levantar de tão macio. Os 2,10m cabem a família toda confortavelmente."},
        {"name": "D**o M**s", "gender": "M", "stars": 5, "var": "Marrom Chocolate", "date": "08/02", "comment": "Estrutura reforçada de eucalipto tratado, não faz nenhum barulho ao sentar. Entrega super ágil."},
        {"name": "J**e F**s", "gender": "F", "stars": 4, "var": "Bege Claro", "date": "06/02", "comment": "Lindo demais! A cor bege é elegante e combina com tudo. Entrega foi feita direto na minha sala pelos entregadores."},
        {"name": "G**a R**s", "gender": "M", "stars": 5, "var": "Cinza Chumbo", "date": "03/02", "comment": "Melhor sofá que já comprei na vida. Vale o dobro do valor cobrado pela qualidade do estofamento."},
        {"name": "A**a N**a", "gender": "F", "stars": 5, "var": "Cinza Chumbo", "date": "31/01", "comment": "Assento tipo pillow top bem fofinho e costura muito bem reforçada. Recomendo fortemente!"},
        {"name": "W**r P**a", "gender": "M", "stars": 5, "var": "Marrom Chocolate", "date": "28/01", "comment": "Rodízios de silicone não riscam o porcelanato ao puxar o assento retrátil. Excelente acabamento."},
        {"name": "L**a M**s", "gender": "F", "stars": 5, "var": "Bege Claro", "date": "25/01", "comment": "Amei o tecido que é fácil de limpar com aspirador ou paninho úmido. Meu marido e filhos amaram."},
        {"name": "T**o A**o", "gender": "M", "stars": 5, "var": "Cinza Chumbo", "date": "22/01", "comment": "Chegou antes da data combinada e em perfeito estado. Muito confortável para maratonar séries."},
        {"name": "B**z L**a", "gender": "F", "stars": 4, "var": "Cinza Chumbo", "date": "19/01", "comment": "Sofá super espaçoso e macio. Apenas um detalhe de costura na lateral inferior mas nada aparente."},
        {"name": "H**o C**a", "gender": "M", "stars": 5, "var": "Bege Claro", "date": "16/01", "comment": "Espuma firme que não afunda. Acabamento de loja de shopping de alto padrão."},
        {"name": "P**a S**s", "gender": "F", "stars": 5, "var": "Marrom Chocolate", "date": "13/01", "comment": "Transformou a minha sala! O suede aveludado dá uma sensação térmica muito agradável."}
    ],
    121: [
        {"name": "M**a S**a", "gender": "F", "stars": 5, "var": "Combo 2 Unidades", "date": "14/02", "comment": "Adeus dor no pescoço! O formato anatômico cervical encaixa perfeitamente na coluna, durmo a noite toda sem acordar."},
        {"name": "R**o S**a", "gender": "M", "stars": 5, "var": "1 Unidade - Travesseiro Abranuv Pro 2.0", "date": "11/02", "comment": "Espuma de memória viscoelástica de verdade, não deforma e volta pra forma original na hora. Excelente densidade."},
        {"name": "C**a P**o", "gender": "F", "stars": 5, "var": "Combo 2 Unidades", "date": "08/02", "comment": "Comprei o combo pra mim e pro meu marido e nós dois sentimos alívio imediato no ombro e pescoço."},
        {"name": "D**o M**s", "gender": "M", "stars": 4, "var": "1 Unidade - Travesseiro Abranuv Pro 2.0", "date": "04/02", "comment": "Demorei uns 2 dias para me acostumar com o formato ergonômico, mas depois disso o sono melhorou 100%."},
        {"name": "J**e F**s", "gender": "F", "stars": 5, "var": "Combo 2 Unidades", "date": "01/02", "comment": "Fronha lavável com zíper super macia e respirável, não esquenta nada a cabeça. Recomendo demais!"}
    ],
    122: [
        {"name": "M**a S**a", "gender": "F", "stars": 5, "var": "110V (127V)", "date": "14/02", "comment": "Panela fantástica! Feijão fica pronto e derretendo em 20 minutos com total silêncio e segurança.", "photo": "../img/reviews/review-122-1.webp"},
        {"name": "R**o S**a", "gender": "M", "stars": 5, "var": "220V", "date": "12/02", "comment": "O painel digital touch tem funções pré-programadas para carne, arroz, feijão e sopa. Muito intuitiva de usar.", "photo": "../img/reviews/review-122-2.webp"},
        {"name": "C**a P**o", "gender": "F", "stars": 5, "var": "110V (127V)", "date": "10/02", "comment": "Capacidade de 5 litros é perfeita para cozinhar para a família inteira. A cuba antiaderente limpa com muita facilidade."},
        {"name": "D**o M**s", "gender": "M", "stars": 5, "var": "220V", "date": "08/02", "comment": "Trava de segurança dupla excelente, sem aquele chiado ou medo das panelas de pressão antigas."},
        {"name": "J**e F**s", "gender": "F", "stars": 4, "var": "110V (127V)", "date": "06/02", "comment": "Adorei a função manter aquecido automática após o término do preparo. Chegou bem rápido e protegida."},
        {"name": "G**a R**s", "gender": "M", "stars": 5, "var": "220V", "date": "04/02", "comment": "Cozinha carne de panela que desfia com garfo. Acabamento em inox escovado combina com toda cozinha moderna."},
        {"name": "A**a N**a", "gender": "F", "stars": 5, "var": "110V (127V)", "date": "01/02", "comment": "A melhor compra de eletroportátil do ano! Prática, silenciosa e muito rápida."},
        {"name": "W**r P**a", "gender": "M", "stars": 5, "var": "220V", "date": "29/01", "comment": "Vem com copo medidor, colher e cabo destacável. Padrão de segurança excelente."},
        {"name": "L**a M**s", "gender": "F", "stars": 5, "var": "110V (127V)", "date": "26/01", "comment": "Faço até sobremesas e pudim nela. Economiza muito gás e tempo na cozinha."},
        {"name": "T**o A**o", "gender": "M", "stars": 5, "var": "220V", "date": "23/01", "comment": "Testei no feijão e na costela gaúcha, ficou sensacional. Entrega da Stone Shop 100% aprovada."},
        {"name": "B**z L**a", "gender": "F", "stars": 4, "var": "110V (127V)", "date": "20/01", "comment": "Panela linda e muito eficiente. O manual explica todas as receitas passo a passo."},
        {"name": "H**o C**a", "gender": "M", "stars": 5, "var": "220V", "date": "17/01", "comment": "Display luminoso com contagem regressiva precisa. Produto de extrema qualidade."},
        {"name": "P**a S**s", "gender": "F", "stars": 5, "var": "110V (127V)", "date": "14/01", "comment": "Super recomendo para quem tem medo de panela tradicional. Essa não tem perigo nenhum e desliga sozinha!"}
    ],
    123: [
        {"name": "M**a S**a", "gender": "F", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "14/02", "comment": "Pressão excelente para lavar o carro e calçadas! O bico snow foam faz aquela espuma densa de lava-rápido profissional.", "photo": "../img/reviews/review-123-3.webp"},
        {"name": "R**o S**a", "gender": "M", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "12/02", "comment": "As duas baterias duram bastante, deu pra lavar dois carros com folga sem precisar recarregar.", "photo": "../img/reviews/review-123-4.webp"},
        {"name": "D**o M**s", "gender": "M", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "10/02", "comment": "A praticidade de puxar água direto de um balde sem precisar de torneira por perto é sensacional."},
        {"name": "C**a P**o", "gender": "F", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "08/02", "comment": "Maleta bem organizada e compacta para guardar no porta-malas. Ótima para limpar janelas e fachadas."},
        {"name": "J**e F**s", "gender": "F", "stars": 4, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "06/02", "comment": "Muito leve e fácil de manusear, não cansa o braço. A pressão do jato ajustável remove limo e sujeira pesada."},
        {"name": "G**a R**s", "gender": "M", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "04/02", "comment": "Excelente custo-benefício. Bateria 48V tem bastante torque e o bocal rotativo multiplica a força da água."},
        {"name": "A**a N**a", "gender": "F", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "01/02", "comment": "Chegou antes do prazo e com todos os acessórios descritos. Funciona muito bem no quintal."},
        {"name": "W**r P**a", "gender": "M", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "29/01", "comment": "O filtro de sucção da mangueira evita que entre pedrinhas no motor. Muito bem projetada."},
        {"name": "L**a M**s", "gender": "F", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "26/01", "comment": "Lavou a varanda todinha sem fios atrapalhando. Liberdade total de movimento!"},
        {"name": "T**o A**o", "gender": "M", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "23/01", "comment": "Potente e prática. Excelente aquisição para quem gosta de cuidar do carro aos finais de semana."},
        {"name": "B**z L**a", "gender": "F", "stars": 4, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "20/01", "comment": "Mangueira de 5 metros dá um bom raio de ação. Recomendo para limpeza residencial."},
        {"name": "H**o C**a", "gender": "M", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "17/01", "comment": "Bateria de longa duração e recarga rápida bivolt. Stone Shop enviou super rápido."},
        {"name": "P**a S**s", "gender": "F", "stars": 5, "var": "Kit Completo 48V (2 Baterias + Maleta + Bico Snow Foam)", "date": "14/01", "comment": "Nota dez! Tira até sujeira de grelha e calçadas encardidas com tranquilidade."}
    ]
}

def format_card(review, avatar_idx, pid):
    is_female = review["gender"] == "F"
    avatar = FEMALE_AVATARS[avatar_idx % len(FEMALE_AVATARS)] if is_female else MALE_AVATARS[avatar_idx % len(MALE_AVATARS)]
    
    photo_html = ""
    if "photo" in review:
        photo_html = f'''
          <div class="review-photos" style="display: flex; gap: 8px; margin-top: 8px; margin-bottom: 4px; flex-wrap: wrap;">
            <img alt="Foto da avaliação" decoding="async" loading="lazy" src="{review['photo']}" style="width: 72px; height: 72px; object-fit: cover; border-radius: 6px; cursor: pointer;" onclick="openReviewModal(this.src)">
          </div>'''
    
    stars_html = generate_stars(review["stars"])
    
    # Check card structure format (standard p118/p104 style)
    return f'''
        <div class="review-card" data-author-name="{review['name']}" data-author-avatar="{avatar}" data-author-stars="{review['stars']}" data-author-variation="{review['var']}" data-author-date="{review['date']}" data-author-comment="{review['comment']}">
          <div class="review-header"><div class="review-user">
            <div class="review-avatar"><img src="{avatar}" alt="{review['name']}" width="32" height="32" style="border-radius:50%;object-fit:cover;" onerror="this.src='../img/reviews-avatars/review-user-1.jpg'"></div>
            <div class="review-user-info">
              <div class="review-user-name">{review['name']}</div>
              <div class="review-user-stars">
                {stars_html}
              </div>
              <div class="review-date">{review['date']} · {review['var']}</div>
            </div>
          </div></div>
          <p class="review-comment">{review['comment']}</p>{photo_html}
        </div>'''

def process_product(pid):
    path = f"pages/produto-{pid}.html"
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    additions = ADDITIONS.get(pid, [])
    if not additions:
        return

    # Find the end of the last review-card
    last_card_idx = html.rfind('class="review-card"')
    if last_card_idx == -1:
        print(f"P{pid}: Could not find review-card!")
        return

    # Find the closing </div> of this last card
    # Usually followed by </div>\n\n</div> or similar
    # Let's locate the next </div> that ends the card
    # Or find the end of reviews list
    end_of_card = html.find('</div>\n\n', last_card_idx)
    if end_of_card == -1:
        end_of_card = html.find('</div>\n        </div>', last_card_idx)
    if end_of_card == -1:
        end_of_card = html.find('</div>', last_card_idx)
        # Advance past </div>
        end_of_card = html.find('</div>', end_of_card + 6) + 6

    # Build new cards
    new_cards_html = ""
    for idx, r in enumerate(additions):
        new_cards_html += format_card(r, (pid * 7 + idx * 3), pid) + "\n"

    # Insert before the reviews section closes
    # Look for </section> or <div class="faq or footer or similar closing
    # More reliable: find the last </div> of review-card and insert right after
    # Let's find regex matching the last review-card
    matches = list(re.finditer(r'<div class="review-card"[\s\S]*?(?:</div>\s*</div>(?:\s*<p class="review-comment">[\s\S]*?</p>)?(?:\s*<div class="review-photos"[\s\S]*?</div>)?\s*</div>)', html))
    if matches:
        last_match = matches[-1]
        insert_pos = last_match.end()
        updated_html = html[:insert_pos] + "\n" + new_cards_html + html[insert_pos:]
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated_html)
        print(f"P{pid}: Successfully added {len(additions)} reviews!")
    else:
        # Fallback: search for reviews container
        print(f"P{pid}: using fallback insertion")
        # Find where review-card starts, insert before the next section
        next_sec = re.search(r'(<div class="faq-section"|<div class="footer"|<footer|<section class="faq)', html)
        if next_sec:
            insert_pos = next_sec.start()
            # find last </div> before next_sec
            rev_end = html.rfind('</div>', 0, insert_pos)
            updated_html = html[:rev_end] + "\n" + new_cards_html + html[rev_end:]
            with open(path, "w", encoding="utf-8") as f:
                f.write(updated_html)
            print(f"P{pid}: Fallback added {len(additions)} reviews!")

for pid in ADDITIONS:
    process_product(pid)
