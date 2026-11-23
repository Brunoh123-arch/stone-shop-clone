import json
import re
import os

def update_kit_praia():
    with open('beach_32_catbox_urls.json', 'r', encoding='utf-8') as f:
        urls = json.load(f)
    
    print(f"Loaded {len(urls)} catbox urls")
    
    creators_data = []
    
    creators_meta = [
        ("Amanda Costa", "amanda.praia", "Carrinho Mor que vira mesinha com porta copos! Melhor invenção pra quem vai à praia com a família 🏖️", 18400, 142, 620, 1950),
        ("Lucas Ferreira", "lucasverao", "Olha a facilidade de levar 4 cadeiras, cooler de 18L e guarda-sol tudo num carrinho só! Não precisa pagar aluguel de barraca nunca mais.", 24100, 310, 890, 2800),
        ("Juliana Paes", "juliana.lazer", "Testando o carrinho mesa de praia da Mor na areia fofa! Puxa super leve e vira suporte perfeito pra bebidas 🍹", 15300, 89, 410, 1340),
        ("Felipe Marinho", "felipe.sol", "Kit praia completo original Mor que chegou da Stone Shop! Qualidade absurda do alumínio, super reforçado.", 9800, 65, 230, 890),
        ("Carolina Dias", "carol.mor", "Chega de carregar peso nos braços na praia! Esse carrinho leva tudo e ainda vira mesa pra petiscos.", 31200, 420, 1200, 3900),
        ("Rodrigo Sol", "rodrigo.beach", "As 4 cadeiras reclináveis da Mor são as mais confortáveis que já usei. 4 posições e não esquentam no sol.", 12400, 94, 380, 1120),
        ("Camila Santos", "camila.ferias", "Unboxing do kit praia da Mor! Veio o carrinho mesa, 4 cadeiras, cooler de 18 litros e o guarda-sol. Apaixonada!", 28500, 380, 950, 3100),
        ("Thiago Lazer", "thiago.costa", "Dica de ouro pra praia: esse kit completo se paga em 2 viagens! Economizamos mais de 300 reais em barraca.", 42100, 560, 1800, 5200),
        ("Beatriz Praia", "bia.napraia", "O cooler de 18L manteve tudo trincando o dia todo no sol de 35 graus! Espaço sobra pras latinhas.", 19600, 180, 710, 2200),
        ("Gustavo Verão", "gustavo.mor", "Review sincero: estrutura em alumínio que não enferruja com maresia. Vale cada centavo!", 14700, 115, 490, 1600),
        ("Patrícia Lima", "paty.litoral", "Muito prático pra guardar no porta-malas! Cabe tudo dobrado sem ocupar espaço nenhum.", 22300, 270, 840, 2600),
        ("Danilo Rocha", "danilo.sol", "Fui pra praia de Ubatuba com o kit completo Mor e fez o maior sucesso. Todo mundo na praia perguntando onde comprei.", 17800, 130, 520, 1900),
        ("Larissa Moraes", "larissa.mar", "As cadeiras reclináveis deitam quase retas pra tomar aquele sol maravilhoso! Tecido super resistente.", 35400, 490, 1400, 4100),
        ("Renato Alves", "renato.viagens", "Carrinho vira mesa com 4 porta copos e porta garrafa! Dá pra jogar baralho e apoiar tudo sem cair areia.", 26900, 340, 1100, 3300),
        ("Fernanda Bahia", "nanda.praia", "Stone Shop entregou em 3 dias aqui na Bahia! Tudo original da Mor, embaladinho com nota e garantia.", 18900, 150, 630, 2100),
        ("Eduardo Costa", "edu.lazer", "Montagem e desmontagem em 30 segundos! O saca areia ajuda muito a fixar o guarda sol sem voar no vento.", 13200, 95, 390, 1400),
        ("Vanessa Ramos", "vanessa.sol", "Cores lindas das cadeiras sortidas! Minha família amou, praia agora é outro nível de conforto.", 29100, 390, 1250, 3600),
        ("Bruno Martins", "bruno.mor", "Cooler de 18L com trava na alça pra não abrir ao transportar. Detalhe que faz toda a diferença!", 16400, 120, 480, 1750),
        ("Priscila Neves", "pri.beach", "Levei 2 crianças pequenas pra praia e esse carrinho foi minha salvação! Leva bolsa, toalha, cadeiras e cooler.", 38700, 520, 1600, 4700),
        ("Marcelo Peixoto", "marcelo.praia", "Melhor compra pro verão! Carrinho resistente, rodas largas que não travam na areia mole.", 21500, 230, 780, 2400),
        ("Mariana Castro", "mari.verao", "As 4 posições da cadeira Mor são perfeitas pra relaxar e ler um livro na beira do mar.", 27300, 310, 920, 3100),
        ("Rafael Nogueira", "rafa.litoral", "Economia pura! Pagar 100 reais por dia em quiosque nunca mais. Kit praia Mor nota 10!", 33800, 460, 1350, 4200),
        ("Sabrina Gomes", "sabrina.mor", "Guarda sol com proteção contra raios solares e saída de ar no topo pra não tombar no vento.", 19100, 160, 670, 2300),
        ("Leonardo Silveira", "leo.viagem", "Alumínio de verdade, leve pra puxar até na areia mais fofa. Recomendo demais!", 14800, 105, 430, 1550),
        ("Isabela Fonseca", "isa.sol", "O cooler de 18L cabe mais de 20 latinhas com gelo! Bebida gelada do início ao fim do dia.", 25600, 320, 1050, 3200),
        ("Diego Menezes", "diego.beach", "Kit sensacional, material reforçado e acabamento perfeito da Mor. Chegou super rápido!", 18200, 140, 580, 2050),
        ("Tatiane Cardoso", "tati.lazer", "O carrinho mesa é tão prático que agora levo até pra piquenique no parque também!", 22900, 260, 810, 2700),
        ("Alexandre Moura", "alex.mar", "Já tive cadeiras de ferro que enferrujaram na primeira ida à praia. Essas de alumínio da Mor duram anos!", 31400, 410, 1280, 3850),
        ("Flávia Ribeiro", "flavia.praia", "Adorei as cores das cadeiras! Todo mundo reunido na praia com conforto de primeira.", 20700, 190, 740, 2450),
        ("Vitor Hugo", "vitor.mor", "Testado e aprovado em Cabo Frio com vento forte. O guarda sol ficou firme com o saca areia!", 16900, 125, 510, 1800),
        ("Aline Teixeira", "aline.sol", "Facilidade pra carregar tudo de uma vez do carro até a beira da água sem cansar.", 28400, 360, 1120, 3400),
        ("Gabriel Souza", "gabriel.lazer", "Kit completo Mor original com cupom da Stone Shop saiu muito barato! Recomendo a todos.", 45200, 610, 1950, 5600)
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
    
    for i in range(1, 33):
        k = f"beach_{i:02d}"
        v_url = urls.get(k, f"https://files.catbox.moe/fallback_{i}.mp4")
        p_url = f"../img/posters-praia/poster-praia-{i:02d}.jpg"
        meta = creators_meta[i - 1]
        av = avatar_pool[(i - 1) % len(avatar_pool)]
        
        creators_data.append({
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
    
    # Update js/videos-criadores.js
    with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
        js_code = f.read()
    
    creators_json_str = json.dumps(creators_data, indent=2, ensure_ascii=False)
    new_dataset_decl = f"const CREATORS_KIT_PRAIA_MOR_18 = {creators_json_str};"
    
    # Replace existing CREATORS_KIT_PRAIA_MOR_18
    pattern = r'const CREATORS_KIT_PRAIA_MOR_18 = \[[\s\S]*?\n\];'
    if re.search(pattern, js_code):
        js_code = re.sub(pattern, new_dataset_decl, js_code, count=1)
        print("Replaced CREATORS_KIT_PRAIA_MOR_18 in js/videos-criadores.js")
    else:
        print("CREATORS_KIT_PRAIA_MOR_18 pattern not found!")
    
    with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
        f.write(js_code)
        
    print("Updated js/videos-criadores.js successfully!")

if __name__ == '__main__':
    update_kit_praia()
