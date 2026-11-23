import json

videos = [
    {
        "catbox": "https://files.catbox.moe/vq69a8.mp4",
        "local": "../videosprodutos/criador-5-1.mp4",
        "poster": "../img/poster-criador-5-1.jpg",
        "title": "Fritadeira Elétrica Visio Fry Elgin 5L 1700w Air Fryer Digital Cinza! O visor com iluminação interna é perfeito pra ver o ponto do alimento! 🍟✨ #airfryer #elgin"
    },
    {
        "catbox": "https://files.catbox.moe/xifi6d.mp4",
        "local": "../videosprodutos/criador-5-2.mp4",
        "poster": "../img/poster-criador-5-2.jpg",
        "title": "Air Fryer Visio Fry Elgin 5L vale a pena? Testei o painel digital touch e a potência de 1700W! Batata frita sequinha e super crocante em minutos! 🤤"
    },
    {
        "catbox": "https://files.catbox.moe/guv4tj.mp4",
        "local": "../videosprodutos/criador-5-3.mp4",
        "poster": "../img/poster-criador-5-3.jpg",
        "title": "Unboxing completo da Air Fryer Elgin Visio Fry 5L! Cesto quadrado gigante que cabe um frango inteiro e antiaderente Black Resist top demais! 🍗🔥"
    }
]

creators_meta = [
    ("Camila Achados", "camila.achadinhos", "Fritadeira Elétrica Visio Fry Elgin 5L 1700w! O visor transparente com luz interna é sensacional, dá pra ver a comida assando sem abrir! ✨🍟"),
    ("Rodrigo Reviews", "rodrigo.techhome", "Air Fryer Visio Fry Elgin 5L é boa? Testando o painel digital de 12 funções e a potência de 1700W! Super silenciosa e rápida!"),
    ("Mariana & Lucas Cozinha", "casal.receitas", "Unboxing da nossa Air Fryer Elgin 5L Visio Fry! O cesto quadrado cabe muito mais comida do que as redondas, nota 10! 🍗"),
    ("Larissa Santos", "larissa.lardocelar", "Gente, apaixonada nessa fritadeira da Elgin! O acabamento cinza digital é muito elegante e não engordura a cozinha toda! 😍"),
    ("Felipe Gastronomia", "felipe.chefemcasa", "Fizemos pão de queijo e coxinha na Visio Fry Elgin 5L. Em 12 minutos ficou douradinho por fora e macio por dentro! 🧀"),
    ("Bárbara Oliveira", "dicasda_barbara", "Cesto quadrado de 5 litros antiaderente Black Resist: limpa super fácil, nada gruda e pode lavar na máquina! 🧽✨"),
    ("Rafael Cozinha Prática", "rafael.praticidade", "A melhor compra pra cozinha em 2026! 1700W de potência real, esquenta muito rápido e economiza gás! 🔥"),
    ("Carol Mendes", "rotinada.carol", "Mostrando de pertinho como funciona a luz interna da Visio Fry Elgin! Aperta o botão e acende na hora sem perder calor! 💡"),
    ("Juliana Prado", "dicasda.ju", "Chegou minha Air Fryer Elgin 5L digital! Veio super bem embalada e já estreei fazendo batata rústica com alecrim! 🍟"),
    ("Thiago Moreira", "thiago.reviews", "Testei a temperatura real com termômetro: chega fácil nos 200°C com circulação de ar 360 perfeita. Recomendo demais!"),
    ("Aline Apê 304", "alineape304", "Essa fritadeira elétrica da Elgin é perfeita pra família! Cabe almoço inteiro de uma vez só no cesto de 5 litros! 🍽️"),
    ("Diego Ferreira", "diegotech.casa", "Painel touch screen responde rápido, comandos intuitivos e aviso sonoro quando o prato está pronto. 10/10!"),
    ("Patrícia Alencar", "lar.da.paty", "Olha o frango a passarinho dourado sem uma gota de óleo! Crocante por fora e suculento por dentro! 🍗❤️"),
    ("Lucas Martins", "organiza.lucas", "Substituiu meu forno convencional. Faz bolo, assados, grelhados e legumes no ponto certo com timer automático!"),
    ("Rayane Silva", "achadinhosdaray", "Achei essa promoção da Elgin Visio Fry 5L e não pensei duas vezes! Custo benefício imbatível pelo tamanho e acabamento! 🏷️"),
    ("Renata Nogueira", "renatablog_casa", "Muito linda na bancada da cozinha! O visor de vidro dá um charme todo especial e moderno! ✨"),
    ("Alexandre Casa", "alexandre.rotina", "Praticidade pura pro dia a dia! Coloco as refeições e acompanho pelo vidro temperado, sem cheiro de gordura!"),
    ("Tatiana Dicas", "tatidicaslimpeza", "Dica de ouro: o cesto não gruda gordura porque o revestimento é duplo. Uma passada de esponja macia e tá limpo! 🧼"),
    ("Felipe & Dani", "dicasdocasal_", "Receita de nugget e batata na Elgin Visio Fry 5L pro lanche da tarde! Ficou crocante em 10 minutos! 🍔🍟"),
    ("Vanessa Guedes", "vanessaguedeshome", "Espaço interno generoso, acabamento fosco premium e visor iluminado. Superou todas as minhas expectativas!"),
    ("Gabriel Nunes", "ape.pequeno", "Perfeita pra quem mora em apartamento! Não solta fumaça e o design quadrado otimiza espaço no armário. 👌"),
    ("Bruna Organiza", "brunaorganiza.lar", "Testando o modo pré-aquecimento e as 12 receitas programadas da Visio Fry. Muito simples de usar!"),
    ("Paula & Beto", "casinha.paulaebeto", "Nossa primeira Air Fryer digital e acertamos em cheio na Elgin 5L! Comida saudável e gostosa todo dia! 🥗"),
    ("Matheus Dicas", "matheusreviews", "Review sincero da Air Fryer Elgin Visio Fry 5L: potência de sobra, visor super útil e ruído baixo do motor. Aprovada!"),
    ("Jéssica Casal", "dicasparadois", "Fizemos salmão com legumes na nossa Elgin 5L! Ficou perfeito, suculento e pronto em 15 minutos! 🐟🥕"),
    ("Sabrina Siqueira", "sabrinalooks.casa", "Mostrando como ela fica ligada à noite: a iluminação interna é linda e muito funcional! 💡✨"),
    ("André Viana", "andrevianacasa", "Chegou em 2 dias pelo frete grátis! Caixa lacrada de fábrica com manual e garantia oficial Elgin. 📦"),
    ("Monique Barreto", "moniquereceitas", "Bolo de caneca e mini tortinhas na Air Fryer Elgin 5L! Assa por igual graças ao fluxo 360 de ar quente! 🥧"),
    ("Eduardo Costa", "canalcleantech", "Consumo elétrico medido: muito econômica pro padrão de 1700W! Vale cada centavo! ⚡"),
    ("Nathália Meireles", "nathymoda.lar", "Comprei de presente pra minha mãe e ela amou! Não precisa ficar abrindo toda hora pra ver se queimou! ❤️"),
    ("Tamires Albuquerque", "tamires_cozinha", "Costelinha com barbecue na Air Fryer Visio Fry 5L! Desmanchando na boca, perfeita demais! 🍖"),
    ("Clayton Achadinhos", "clayton_achadinhos", "Achado supremo pro lar: Air Fryer Elgin 5L Visio Fry! Garanta no link antes que esgote o lote promocional! 🛒🔥")
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
        "likes": 11200 + (idx * 370) % 13500,
        "comments": 54 + (idx * 9) % 120,
        "shares": 310 + (idx * 35) % 650,
        "saves": 920 + (idx * 85) % 1800,
        "title": desc
    })

with open('scripts/creators_produto_5_dataset.json', 'w', encoding='utf-8') as f:
    json.dump(dataset_32, f, ensure_ascii=False, indent=2)

print(f"Dataset de {len(dataset_32)} criadores gerado com sucesso!")
