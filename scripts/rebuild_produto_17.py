import json
import re
import os

def fix_produto_17():
    print("Fixing Produto 17 (Kit 4 Cadeiras Mor)...")
    
    # 1. Update CREATORS_CADEIRAS_PRAIA_MOR_17 in js/videos-criadores.js
    with open('beach_32_catbox_urls.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
        
    creators_meta = [
        ("Juliana Mendes", "ju.praia", "Essas 4 cadeiras de praia da Mor em alumínio são as melhores que já tivemos! Leves demais e não enferrujam 🏖️", 19200, 154, 720, 2100),
        ("Felipe Castro", "felipe.litoral", "Kit 4 cadeiras Mor que comprei na promoção da Stone Shop! Reclinam em 4 posições, dá pra deitar quase reto.", 28400, 340, 980, 3100),
        ("Larissa Ramos", "lari.verao", "Olha a facilidade pra fechar e carregar as 4 cadeiras juntas! Cabem no porta-malas do carro com folga.", 16500, 112, 530, 1800),
        ("Marcos Vinicius", "marcos.mor", "Review sincero das cadeiras Mor: estrutura reforçada de alumínio, suporta até 110kg e não afunda na areia.", 33100, 420, 1350, 4200),
        ("Camila Rocha", "camila.beach", "As cores sortidas vieram lindas! Tecido super fresco e fácil de limpar depois que volta da praia.", 22800, 260, 890, 2750),
        ("Rodrigo Alves", "rodrigo.sol", "Economizamos uma fortuna em aluguel de cadeiras no quiosque! Se pagaram na primeira semana de férias.", 41500, 580, 1900, 5400),
        ("Aline Souza", "aline.costa", "O acabamento nos braços é anatômico e a regulagem das posições é bem macia, sem prender os dedos.", 14900, 98, 440, 1600),
        ("Diego Barbosa", "diego.lazer", "Alumínio de verdade que resiste à maresia pesada! Já tive de ferro que enferrujou, Mor é outro nível.", 27600, 310, 1020, 3300),
        ("Beatriz Lima", "bia.mar", "As cadeiras são bem largas e confortáveis, a gente passa o dia inteiro na praia sem dor nas costas.", 18700, 175, 680, 2250),
        ("Gustavo Santos", "gustavo.praia", "Chegaram super rápido em 3 dias úteis! Tudo novinho, embalado na caixa com nota e garantia.", 13400, 88, 390, 1450),
        ("Patrícia Fernandes", "paty.mor", "Dica de ouro: as 4 cadeiras são tão leves que meus filhos de 8 e 10 anos carregam sem reclamar.", 36200, 510, 1550, 4400),
        ("Danilo Ribeiro", "danilo.verao", "A inclinação máxima deita quase completa pra tomar aquele bronzeado perfeito! Super recomendo.", 24100, 280, 890, 2900),
        ("Fernanda Nogueira", "nanda.litoral", "Comprei o kit com 4 cores diferentes pra família toda, cada um escolheu a sua cor preferida.", 17300, 135, 590, 1950),
        ("Thiago Martins", "thiago.sol", "Qualidade Mor dispensa comentários. Material grosso, costuras reforçadas e tubos sem rebarba.", 31800, 390, 1200, 3700),
        ("Vanessa Cardoso", "vanessa.beach", "Stone Shop foi super rápida no envio! Vieram bem protegidas e o cupom deu um desconto surreal.", 29400, 410, 1300, 3650),
        ("Lucas Moreira", "lucas.mor", "Cadeiras firmes que não balançam quando senta. Aguentam peso de verdade sem entortar a barra.", 15800, 115, 480, 1700),
        ("Carolina Gomes", "carol.lazer", "Muito práticas pra levar pro camping e piscina de condomínio também, dobram facinho.", 21200, 240, 780, 2550),
        ("Renato Peixoto", "renato.costa", "Melhor custo benefício da internet! Em loja física cobram quase 150 em cada uma avulsa.", 44300, 620, 2100, 5800),
        ("Isabela Dias", "isa.praia", "O tecido seca super rápido quando molha na praia, não fica com cheiro de mofo.", 19800, 190, 710, 2350),
        ("Alexandre Moura", "alex.verao", "Testadas e aprovadas no feriado em Ilhabela! Alumínio perfeito, zero sinais de oxidação.", 26500, 290, 940, 3150),
        ("Priscila Teixeira", "pri.mar", "As cadeiras são leves mas muito estáveis, não tombam quando você deita pra trás.", 34700, 470, 1480, 4100),
        ("Marcelo Freitas", "marcelo.mor", "Presente de aniversário pro meu pai! Ele adorou as 4 posições pra pescar e relaxar.", 16100, 120, 490, 1800),
        ("Tatiane Ramos", "tati.sol", "Kit completo com as 4 cadeiras deixou nossa família super bem instalada na praia.", 23500, 270, 860, 2850),
        ("Eduardo Silveira", "edu.beach", "Capacidade de 110kg real. Tenho 102kg e a cadeira fica firme sem estalar nada.", 38900, 540, 1750, 4900),
        ("Mariana Lopes", "mari.litoral", "Design clássico da Mor que todo brasileiro conhece. Confiabilidade pura!", 18200, 145, 620, 2150),
        ("Rafael Fonseca", "rafa.lazer", "Dá pra carregar no banco de trás ou no porta-malas sem riscar nada, são bem compactas.", 27100, 330, 1050, 3400),
        ("Sabrina Castro", "sabrina.mor", "O alumínio não absorve calor como o ferro, então não queima as pernas no sol do meio-dia.", 32400, 430, 1380, 3950),
        ("Leonardo Nunes", "leo.praia", "Kit com 4 cadeiras originais Mor pelo preço de 2! Não pensei duas vezes pra comprar.", 46100, 680, 2250, 6200),
        ("Flávia Martins", "flavia.verao", "Adorei a facilidade de lavar com mangueira de água doce quando chega em casa.", 20400, 180, 730, 2400),
        ("Vitor Henrique", "vitor.sol", "Excelente compra, vieram nas cores azul, vermelha, verde e amarela sortidas.", 15200, 105, 450, 1650),
        ("Daniela Pires", "dani.mar", "Minha mãe idosa achou super fácil de levantar da cadeira porque a altura é perfeita.", 28900, 360, 1150, 3500),
        ("Gabriel Neves", "gabriel.mor", "Recomendo a todos da Stone Shop! Produto original Mor lacrado e entrega pontual.", 39800, 560, 1800, 5100)
    ]
    
    avatar_pool = [
        "../img/reviews-avatars/review-user-104-vanessa.jpg",
        "../img/reviews-avatars/review-user-104-juliana.jpg",
        "../img/reviews-avatars/review-user-1.jpg",
        "../img/reviews-avatars/review-user-2.jpg",
        "../img/reviews-avatars/review-user-3.jpg",
        "../img/reviews-avatars/review-user-4.jpg",
        "../img/reviews-avatars/review-user-5.jpg",
        "../img/reviews-avatars/review-user-6.jpg",
        "../img/reviews-avatars/review-user-7.jpg",
        "../img/reviews-avatars/review-user-8.jpg"
    ]
    
    creators_p17 = []
    for i in range(1, 33):
        k = f"beach_{i:02d}"
        v_url = urls.get(k, f"https://files.catbox.moe/fallback_{i}.mp4")
        p_url = f"../img/posters-praia/poster-praia-{i:02d}.jpg"
        meta = creators_meta[i - 1]
        av = avatar_pool[(i - 1) % len(avatar_pool)]
        creators_p17.append({
            "name": meta[0],
            "username": meta[1],
            "avatar": av,
            "poster": p_url,
            "video": v_url,
            "localVideo": f"../videosprodutos/praia_32/beach_{i:02d}.mp4",
            "startTime": 0.5,
            "likes": meta[3],
            "comments": meta[4],
            "shares": meta[5],
            "saves": meta[6],
            "title": meta[2]
        })
        
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
        
    creators_json_str = json.dumps(creators_p17, indent=2, ensure_ascii=False)
    new_decl = f"const CREATORS_CADEIRAS_PRAIA_MOR_17 = {creators_json_str};"
    
    pattern = r'const CREATORS_CADEIRAS_PRAIA_MOR_17 = \[[\s\S]*?\n\];'
    if re.search(pattern, js_code):
        js_code = re.sub(pattern, new_decl, js_code, count=1)
        print("Replaced CREATORS_CADEIRAS_PRAIA_MOR_17 in js/videos-criadores.js")
    else:
        print("CREATORS_CADEIRAS_PRAIA_MOR_17 pattern not found in js/videos-criadores.js!")
        
    with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
        
    # 2. Rebuild reviews in pages/produto-17.html
    reviews_17_data = [
        {
            "name": "J**a M.",
            "avatar": "../img/reviews-avatars/review-user-104-vanessa.jpg?v=1794225",
            "date": "14/10",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Essas 4 cadeiras da Mor são simplesmente perfeitas! O alumínio é super leve, não cansa nada pra levar até a praia e deitam em 4 posições. Chegou tudo certinho!",
            "photos": ["../img/review-18-c2-1.jpg", "../img/review-18-c2-2.jpg"]
        },
        {
            "name": "F**o C.",
            "avatar": "../img/reviews-avatars/review-user-104-juliana.jpg?v=1794225",
            "date": "10/10",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Muito confortáveis e resistentes! Tenho 95kg e a cadeira não estala nem entorta. O tecido é reforçado e as cores vieram bem vivas.",
            "photos": ["../img/review-18-c6-1.jpg"]
        },
        {
            "name": "L**s R.",
            "avatar": "../img/reviews-avatars/review-user-1.jpg",
            "date": "06/10",
            "variation": "Azul (Kit 4 Cadeiras Reclináveis)",
            "comment": "Chegou antes do prazo em Santos! Embalagem original da Mor com nota fiscal. Recomendo demais a Stone Shop pelo atendimento e agilidade.",
            "photos": ["../img/review-18-c4-1.jpg"]
        },
        {
            "name": "M**a T.",
            "avatar": "../img/reviews-avatars/review-user-2.jpg",
            "date": "01/10",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "As 4 posições fazem toda a diferença! Dá pra ficar sentado tomando uma gelada ou deitar pra descansar. Fecham super fácil.",
            "photos": ["../img/review-18-c5-1.jpg"]
        },
        {
            "name": "R**o P.",
            "avatar": "../img/reviews-avatars/review-user-3.jpg",
            "date": "26/09",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Comprei pras férias de fim de ano com a família e valeu cada centavo. Alumínio não enferruja com maresia, vão durar anos!",
            "photos": ["../img/review-18-c7-1.jpg"]
        },
        {
            "name": "C**a S.",
            "avatar": "../img/reviews-avatars/review-user-4.jpg",
            "date": "20/09",
            "variation": "Verde (Kit 4 Cadeiras Reclináveis)",
            "comment": "Super leves, minhas crianças ajudam a carregar na praia sem esforço. Excelente custo-benefício comparado a comprar avulso.",
            "photos": []
        },
        {
            "name": "A**a B.",
            "avatar": "../img/reviews-avatars/review-user-5.jpg",
            "date": "15/09",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "O braço em plástico anatômico é muito bom e a trava das posições fica bem firme, não corre risco de desarmar sozinha.",
            "photos": []
        },
        {
            "name": "D**o G.",
            "avatar": "../img/reviews-avatars/review-user-6.jpg",
            "date": "10/09",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Melhor compra que fiz pro verão! As 4 cadeiras cabem deitadas no porta-malas do meu carro compacto sem aperto.",
            "photos": []
        },
        {
            "name": "E**a N.",
            "avatar": "../img/reviews-avatars/review-user-7.jpg",
            "date": "04/09",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Material de primeira linha. A lona é bem esticadinha e não cede com o tempo. Nota 10!",
            "photos": []
        },
        {
            "name": "V**a L.",
            "avatar": "../img/reviews-avatars/review-user-8.jpg",
            "date": "29/08",
            "variation": "Azul (Kit 4 Cadeiras Reclináveis)",
            "comment": "Entrega relâmpago! Vieram todas novinhas sem nenhum arranhão. Recomendo de olhos fechados.",
            "photos": []
        },
        {
            "name": "T**o K.",
            "avatar": "../img/reviews-avatars/review-user-104-c13.jpg?v=1794225",
            "date": "23/08",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Alívio não ter que pagar aluguel de cadeira na praia nunca mais! Em duas idas à praia o kit já se pagou.",
            "photos": []
        },
        {
            "name": "P**a F.",
            "avatar": "../img/reviews-avatars/review-user-104-c14.jpg?v=1794225",
            "date": "18/08",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Adorei as cores vibrantes das cadeiras! Todo mundo reunido na beira da água com muito conforto.",
            "photos": []
        },
        {
            "name": "G**o D.",
            "avatar": "../img/reviews-avatars/review-user-1.jpg",
            "date": "12/08",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Estrutura tubular de alumínio muito resistente e soldas bem acabadas. Qualidade Mor comprovada.",
            "photos": []
        },
        {
            "name": "B**a C.",
            "avatar": "../img/reviews-avatars/review-user-2.jpg",
            "date": "06/08",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Sensacional! Fomos pro litoral no final de semana e as cadeiras fizeram o maior sucesso. Super confortáveis.",
            "photos": []
        },
        {
            "name": "K**s R.",
            "avatar": "../img/reviews-avatars/review-user-104-vanessa.jpg?v=1794225",
            "date": "31/07",
            "variation": "Sortidas (Kit 4 Cadeiras Reclináveis)",
            "comment": "Atendimento exemplar da loja e produto original de extrema qualidade. Podem comprar com confiança!",
            "photos": []
        }
    ]
    
    star_svg = '<svg viewBox="0 0 24 24" class="star-icon" fill="#ffb800" width="11" height="11"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>'
    stars_5 = star_svg * 5
    
    cards_html = []
    for r in reviews_17_data:
        photos_html = ""
        if r["photos"]:
            imgs = "".join([f'<img loading="lazy" decoding="async" class="review-photo" src="{p}" alt="Foto da cliente TikTok Shop" onclick="openPhotoModal(this.src)">' for p in r["photos"]])
            photos_html = f'<div class="review-photos">{imgs}</div>'
            
        c_markup = f"""<div class="review-card" data-author-name="{r['name']}" data-author-avatar="{r['avatar']}" data-author-stars="5" data-author-variation="{r['variation']}" data-author-date="{r['date']}" data-author-comment="{r['comment']}">
<div class="review-header">
<div class="review-user">
<div class="review-avatar">
<img loading="lazy" decoding="async" src="{r['avatar']}" alt="{r['name']}">
</div>
<div class="review-user-info">
<div class="review-user-name">{r['name']}</div>
<div class="review-user-stars">{stars_5}</div>
<div class="review-date">{r['date']} · {r['variation']}</div>
</div>
</div>
</div>
<p class="review-comment">{r['comment']}</p>
{photos_html}
</div>"""
        cards_html.append(c_markup)
        
    with open('pages/produto-17.html', 'r', encoding='utf-8') as f:
        p17_html = f.read()
        
    pattern2 = r'(<div class="reviews-list">)[\s\S]*?(</section>)'
    new_reviews_markup = r'\1\n' + "\n".join(cards_html) + r'\n</div>\n\2'
    p17_html = re.sub(pattern2, new_reviews_markup, p17_html, count=1)
    
    with open('pages/produto-17.html', 'w', encoding='utf-8') as f:
        f.write(p17_html)
        
    print("pages/produto-17.html updated successfully with 15 canonical reviews and beach creators!")

if __name__ == '__main__':
    fix_produto_17()
