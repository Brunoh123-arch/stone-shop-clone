import json
import re

videos = [
    {
        "catbox": "https://files.catbox.moe/nz8c17.mp4",
        "local": "../videosprodutos/criador-12-1.mp4",
        "poster": "../img/poster-criador-12-1.jpg",
        "title": "Montando nossa piscina Mor 2400 Litros no quintal! Super fácil, só inflar a borda superior e encher de água que ela sobe sozinha! 💦☀️ #piscinamor #splashfun"
    },
    {
        "catbox": "https://files.catbox.moe/xqo3s2.mp4",
        "local": "../videosprodutos/criador-12-2.mp4",
        "poster": "../img/poster-criador-12-2.jpg",
        "title": "O verão em casa ficou muito mais divertido! Piscina Splash Fun Mor 2400L, lona grossa reforçada e sem nenhuma quina pontuda pras crianças! 😎🏊‍♂️"
    },
    {
        "catbox": "https://files.catbox.moe/34jgf7.mp4",
        "local": "../videosprodutos/criador-12-3.mp4",
        "poster": "../img/poster-criador-12-3.jpg",
        "title": "Unboxing e tour completo da Piscina Splash Fun Redonda Mor 2400 Litros! Cabe a família toda e refresca demais no calor! 🌊❤️"
    }
]

creators_meta = [
    ("Vaninha Medeiros", "vaninhamedeiros2", "Montando nossa piscina Mor 2400 Litros no quintal! Super fácil, só inflar a borda superior e encher de água que ela sobe sozinha! 💦☀️ #piscinamor #splashfun"),
    ("Júnior Alves", "junior.a.alves", "O verão em casa ficou muito mais divertido! Piscina Splash Fun Mor 2400L, lona grossa reforçada e sem nenhuma quina pontuda pras crianças! 😎🏊‍♂️"),
    ("Luciana Fortes", "lucianafortes", "Unboxing e tour completo da Piscina Splash Fun Redonda Mor 2400 Litros! Cabe a família toda e refresca demais no calor! 🌊❤️"),
    ("Matheus & Bia", "matheusebia.casa", "Melhor compra pro calor! Enchemos a borda com bomba de bicicleta em 3 minutos. A lona tripla é super resistente! 🚲✨"),
    ("Família Oliveira", "familia.oliveira.lar", "Domingo de sol com a piscina montada! 2,40m de diâmetro é enorme, coube nós dois e as duas crianças com sobra! 👨‍👩‍👧‍👦☀️"),
    ("Rodrigo Silva", "rodrigo.dicascasa", "Dica de ouro: nivelar bem o chão com uma lona antes de encher. A válvula de escoamento facilita muito pra trocar a água depois! 🚿👌"),
    ("Camila Santos", "camilasantos.home", "Chegou super rápido, caixa lacrada com o kit reparo e o manual. Muito mais prática do que aquelas antigas de ferro que enferrujam! 📦😍"),
    ("Amanda & Pedro", "casal.ap202", "As crianças não saem mais da água! Sem ferragem perigosa, a sustentação é toda feita pela borda inflável e a própria água. Segurança 10/10! 🧒💦"),
    ("Larissa Casa & Jardim", "larissajardim.diy", "Transformamos o quintal numa área de lazer com essa piscina Splash Fun da Mor! Custo benefício surreal de bom! 🏡🏖️"),
    ("Felipe Barreto", "felipebarreto.reviews", "Material de PVC reforçado com trama interna de poliéster. Dá pra sentir a qualidade e firmeza da lona logo ao tirar da caixa! 💪🔥"),
    ("Carol Dicas de Mãe", "caroldicasdemae", "Para as mães que têm medo de quinas duras: essa piscina não tem peças rígidas! As crianças pulam na borda e é super macio! 🛟👶"),
    ("Thiago Ramos", "thiagoramos.verao", "Testando a capacidade real de 2400 litros: altura de 63cm é perfeita pra sentar e relaxar com uma bebida gelada no fim de semana! 🍻🧊"),
    ("Juliana Prado", "ju.achadinhoslar", "Comprei na promoção relâmpago com frete grátis e chegou em 3 dias! Super recomendo, a marca Mor é pioneira e nunca decepciona! ⚡🚚"),
    ("Vanessa Rocha", "vanessarocha.casa", "A água fica limpinha com a entrada pro filtro. A tampa de deságue na parte de baixo esvazia rápido sem precisar de balde! 🧼👍"),
    ("Diego & Mari", "casaldiegomari", "Nosso refúgio pro calor de 38 graus! A piscina Splash Fun 2400L é perfeita pra quem não quer reforma no quintal. Montou, curtiu, guardou! 🌴☀️"),
    ("Bruna Vasconcelos", "bruna.organiza", "Super prática de dobrar e guardar no armário quando não estiver usando. O kit reparo vem junto pra qualquer emergência! 🎒✨"),
    ("Lucas Martins", "lucasmartins.oficial", "Enchi a borda com secador no modo ar frio, foi menos de 2 minutos! A piscina foi subindo perfeitamente conforme a mangueira enchia. ⏱️👏"),
    ("Jéssica & Gabriel", "ape.jessicagabriel", "Olha a transparência da água e a resistência do fundo azul! Já é o segundo verão que usamos Mor e continua intacta! 🏊‍♀️💙"),
    ("André Rezende", "andrerezende.lar", "Valeu cada centavo investido. No calor que tá fazendo, essa piscina salvou as férias escolares dos meus filhos! ☀️🎉"),
    ("Aline Mendes", "alinemendes.home", "Muito espaçosa! Comprei achando que seria pequena, mas cabem 4 a 5 pessoas sentadas tranquilamente. Super indico! 🌊👏"),
    ("Rafael Costa", "rafaelcosta.dicas", "A válvula de saída de água tem encaixe pra mangueira, então dá pra aproveitar a água pra regar o jardim na hora de esvaziar! 🌱💧"),
    ("Monique & Tiago", "moniqueetiago.vlog", "Churrasco no quintal com a piscina Splash Fun Mor cheia! O anel inflável serve até de encosto macio pra cabeça. Conforto total! 🥩🏖️"),
    ("Patrícia Alencar", "patriciaalencar.sp", "Chegou antes do prazo em São Paulo. Montagem sem dor de cabeça nenhuma, meus sobrinhos amaram! 😍🎈"),
    ("Daniel Moreira", "danielmoreira.reviews", "A qualidade da lona Mor é indiscutível. Laminado duplo com malha entre as folhas de PVC, aguenta a bagunça dos cachorros e crianças! 🐕👧"),
    ("Renata Nogueira", "renatanogueira.blog", "Melhor investimento do ano pro nosso quintal! Água geladinha e diversão garantida pro fim de semana inteiro! 🍹🌞"),
    ("Bruno Tech Home", "brunotech.home", "Review sincero da Piscina Mor Splash Fun 2400L: montagem em 5 min, material espesso, excelente retenção e custo-benefício imbatível! ⭐⭐⭐⭐⭐"),
    ("Tatiana Viana", "tatianaviana.dicas", "Fizemos uma surpresa pro aniversário do meu filho no quintal com a piscina inflável. A alegria dele não tem preço! 🎂💦"),
    ("Gustavo Lima", "gustavolima.lazer", "Fácil de cuidar e tratar com cloro para piscina de plástico. A água dura a semana toda cristalina! 🧪👌"),
    ("Sabrina & Leo", "sabrinaeleo.casa", "Nosso mini resort em casa! Dá pra colocar boias, colchão inflável e relaxar o dia todo debaixo do sol! ⛱️🕶️"),
    ("Eduardo Santos", "eduardosantos.br", "Produto original de fábrica Mor. Acompanha selo do Inmetro e garantia. Não comprem imitações finas, a original é Mor! 🛡️💯"),
    ("Nathália Faria", "nathaliafaria.lar", "Super rápida pra encher e pra desinflar. Quando o tempo esfria, seca rapidinho ao sol e cabe numa caixa pequena! 📦☀️"),
    ("Clayton Promoções", "clayton_achadinhos", "Achado supremo pro calor: Piscina Splash Fun Mor 2400 Litros com desconto insano! Garanta no carrinho antes que esgote o lote de verão! 🛒🔥")
]

dataset_32 = []
for idx, (name, user, desc) in enumerate(creators_meta):
    v_idx = idx % 3
    v_obj = videos[v_idx]
    avatar_num = (idx % 28) + 1
    dataset_32.append({
        "name": name,
        "username": user,
        "avatar": f"../img/creators-aspirador/creator-{avatar_num}.jpg",
        "poster": v_obj["poster"],
        "video": v_obj["catbox"],
        "localVideo": v_obj["local"],
        "startTime": 0.2,
        "likes": 14200 + (idx * 410) % 18000,
        "comments": 68 + (idx * 11) % 145,
        "shares": 420 + (idx * 38) % 780,
        "saves": 1150 + (idx * 90) % 2100,
        "title": desc
    })

with open('scripts/creators_produto_12_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(dataset_32, f, ensure_ascii=False, indent=2)

print(f"Dataset de {len(dataset_32)} criadores gerado com sucesso!")
