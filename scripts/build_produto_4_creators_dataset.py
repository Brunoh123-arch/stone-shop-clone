import json
import os

def generate_dataset():
    catbox_map_file = 'scripts/catbox_videos_map.json'
    catbox_map = {}
    if os.path.exists(catbox_map_file):
        with open(catbox_map_file, 'r', encoding='utf-8') as f:
            catbox_map = json.load(f)

    v1_url = catbox_map.get('criador-4-1.mp4', 'https://files.catbox.moe/placeholder1.mp4')
    v2_url = catbox_map.get('criador-4-2.mp4', 'https://files.catbox.moe/placeholder2.mp4')
    v3_url = catbox_map.get('criador-4-3.mp4', 'https://files.catbox.moe/placeholder3.mp4')

    videos = [
        {
            "catbox": v1_url,
            "local": "../videosprodutos/criador-4-1.mp4",
            "poster": "../img/poster-criador-4-1.jpg",
            "title": "JBL BOOMBOX 3 - Testando o grave no volume máximo! O subwoofer dedicado faz tremer a casa toda! 🔊🔥 #jbl #boombox3 #sompesado"
        },
        {
            "catbox": v2_url,
            "local": "../videosprodutos/criador-4-2.mp4",
            "poster": "../img/poster-criador-4-2.jpg",
            "title": "Bass Test insano na JBL Boombox 3! Radiadores passivos laterais excursionando muito e áudio cristalino! 💥🎶 #basstest #jblboombox3"
        },
        {
            "catbox": v3_url,
            "local": "../videosprodutos/criador-4-3.mp4",
            "poster": "../img/poster-criador-4-3.jpg",
            "title": "Review sincero da JBL Boombox 3: bateria durou o fim de semana inteiro e a alça de metal é muito firme! 🔋🏆 #review #jblbrasil"
        }
    ]

    creators_meta = [
        ("Thiago Bass & Áudio", "thiagobass.som", "JBL BOOMBOX 3 no volume máximo! O subwoofer dedicado dessa versão de 3 vias faz as janelas vibrarem! Potência absurda! 🔊🔥"),
        ("Rodrigo Tech & Games", "rodrigo.techaudio", "Bass Test com funk e eletrônica na Boombox 3: graves profundos sem distorcer nada. Melhor caixa portátil do mercado! 🎶💥"),
        ("Lucas & Mari Churrasco", "casal.somdechurrasco", "Levamos a JBL Boombox 3 pro sítio e tocou mais de 20 horas direto no churrasco sem pedir tomada! Bateria monstra! 🔋🥩"),
        ("Marcelo Oliveira", "marcelo_somautomotivo", "Comparando a Boombox 3 com som de mala: a fidelidade dos agudos e o peso do grave colocam muito som no bolso! 🚗🔊"),
        ("Camila Ferreira", "camilafitness.treino", "Coloquei no treino ao ar livre na praia: à prova d'água IP67, tomou respingo de mar e chuva e seguiu tocando impecável! 🏖️🌧️"),
        ("Felipe Sonorização", "felipe.proaudio", "Arquitetura acústica de 3 vias (subwoofer + 2 midranges + 2 tweeters) fez toda a diferença no palco sonoro da Boombox 3! 🎛️🎵"),
        ("Larissa Mendes", "larissareviews.lar", "Chegou super rápido, caixa lacrada original JBL! A alça metálica com acabamento em silicone facilita demais carregar! 📦✨"),
        ("Bruno Santos Áudio", "bruno.audiotech", "Testando o modo PartyBoost emparelhando com outra caixa: vira um verdadeiro paredão de som sem delay! 🔊🔗"),
        ("Diego Barreto", "diegobarretocasa", "A pressão sonora da Boombox 3 dentro de casa é surreal! Não precisa de home theater pra ver filme com ela! 🎬🍿"),
        ("Rafael Moreira", "rafaelmoreira_som", "Bateria de 24 horas reais medida no teste contínuo a 60% do volume. Construção blindada que aguenta qualquer rolê! 🔋⚡"),
        ("Amanda Lima", "amandalimadicas", "Achei essa promoção da JBL Boombox 3 no TikTok Shop com desconto surreal e frete grátis! Compra do ano! 🏷️👏"),
        ("Gabriel Souza", "gabriel.bassboost", "Medição com decibelímetro no estúdio: picos impressionantes com resposta linear de frequência a partir de 40Hz! 📊🎶"),
        ("Vanessa Nogueira", "vanessacoisasdelar", "Som impecável pra festinha em família no quintal! Todo mundo elogiou a qualidade e clareza das vozes! 🥳🎤"),
        ("Eduardo Prado", "dudugadgets", "O tecido reforçado à prova d'água e poeira dá uma segurança total pra levar pra represa ou piscina sem medo! 💦🏊‍♂️"),
        ("Patrícia Albuquerque", "paty.viagens", "Nossa companheira de camping e praia! Conecta 2 celulares via Bluetooth ao mesmo tempo, cada um põe sua música! 📱📲"),
        ("Matheus Silva", "matheus.somforte", "O grave bate no peito de verdade! Quem gosta de graves encorpados e definidos vai pirar na JBL Boombox 3! 💥🥁"),
        ("Jéssica Ramos", "dicasdajessica.tech", "Unboxing completo da JBL Boombox 3 preta: cabo AC reforçado, manuais e acabamento fosco impecável! 📦🖤"),
        ("André Carvalho", "andrecarvalhosom", "Conexão Bluetooth 5.3 ultra estável, alcancei mais de 15 metros sem nenhuma falha de sinal! 📶✨"),
        ("Renata Duarte", "renata.lifestyle", "A melhor aquisição pro verão! Bateria infinita, resistente à água e o design icônico da JBL que chama atenção onde chega! ☀️🌴"),
        ("Leandro Pacheco", "leandrotechbr", "Equalização no app JBL Portable permite ajustar grave, médio e agudo do jeito que você preferir! Muito intuitivo! 🎚️📱"),
        ("Sabrina Rocha", "sabrinarochahome", "Presente pro meu marido e ele ficou bobo com a potência! Desligou as caixas antigas da sala pra usar só a Boombox 3! ❤️🎁"),
        ("Alexandre Castro", "alexandre.sompesado", "Testando sub-grave a 35Hz: o radiador passivo lateral pula limpo sem chiar. Engenharia de ponta da JBL! 🔊👌"),
        ("Carolina Peixoto", "carolpeixoto.dicas", "Custo benefício inacreditável com o cupom de desconto! Veio certinho, nota 10 na entrega relâmpago! 🚚⚡"),
        ("Monique Vianna", "monique_vianna", "Usamos na festa da piscina dos amigos: molhou toda e o som continuou cristalino e perfeito sem chiar! 🏊‍♀️🎶"),
        ("Beto & Ju", "casal_aventura", "Caixa de som definitiva pra estrada e acampamento! Estrutura de aço na alça dá muita firmeza pra transportar! 🏕️💪"),
        ("Clayton Achadinhos", "clayton.achadinhos", "Achado de ouro: JBL Boombox 3 original no lote promocional! Aproveitem enquanto tem estoque! 🛒🔥"),
        ("Daniela Prado", "danyprado_musica", "Clareza nos médios e agudos mesmo quando o grave tá no máximo. O som preenche ambientes gigantescos com facilidade! 🎼✨"),
        ("Vitor Guimarães", "vitorg.som", "Testei 48 horas de uso alternado e a bateria ainda marcou 30%! Não existe concorrente com essa autonomia! 🔋🔝"),
        ("Tatiane Siqueira", "tatisiqueiradicas", "Design moderno, base antiderrapante pesada que não sai do lugar mesmo com o som tremendo tudo! 💎🔊"),
        ("Lucas Pinheiro", "lucaspinheirotech", "PartyBoost sincroniza instantâneo com a minha Charge 5! Som estéreo imersivo de altíssimo nível! 🎧💥"),
        ("Nathália Borges", "nathalia_borges", "Embalagem mega protegida, entrega em 3 dias com código de rastreio funcional. Experiência de compra impecável! 📦❤️"),
        ("Gustavo Henrique", "gustavo.audiophile", "Padrão de qualidade sonora internacional! Boombox 3 é a rainha indiscutível das caixas Bluetooth portáteis! 👑🔊")
    ]

    dataset_32 = []
    for idx, (name, user, desc) in enumerate(creators_meta):
        v_idx = idx % 3
        v_obj = videos[v_idx]
        avatar_num = (idx % 28) + 1
        dataset_32.append({
            "name": name,
            "username": user,
            "avatar": f"../img/creators-tech/creator-{avatar_num}.jpg",
            "poster": v_obj["poster"],
            "video": v_obj["catbox"],
            "localVideo": v_obj["local"],
            "startTime": 0.2,
            "likes": 13800 + (idx * 420) % 16500,
            "comments": 78 + (idx * 13) % 150,
            "shares": 45 + (idx * 9) % 90,
            "saves": 1250 + (idx * 110) % 2100,
            "title": desc
        })

    with open('scripts/creators_produto_4_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset_32, f, ensure_ascii=False, indent=2)

    print(f"Dataset de {len(dataset_32)} criadores gerado com sucesso em scripts/creators_produto_4_dataset.json!")
    return dataset_32

if __name__ == '__main__':
    generate_dataset()
