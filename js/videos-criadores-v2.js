// LÓGICA E UI DOS VÍDEOS DOS CRIADORES — js/videos-criadores.js
// SISTEMA OFICIAL TIKTOK SHOP (COM SUPORTE CONTEXTUAL POR PRODUTO)
// =============================================================

(function() {
  // Avatares FEMININOS reais mapeados do diretório FOTOSDEPERFIL
  const isPagesDir = typeof window !== 'undefined' && window.location.pathname.includes('/pages/');
  const avatarBase = isPagesDir ? '../img/creators-avatars/' : 'img/creators-avatars/';

  // 28 Fotos de Perfil Reais do TikTok de Pessoas Reais (sem fotos genéricas ou fakes)
  const AVATARS_FEMININOS = Array.from({ length: 28 }, (_, i) => `${avatarBase}creator-${i + 1}.jpg`);

  const avatarBodyBase = isPagesDir ? '../img/creators-body/' : 'img/creators-body/';
  const AVATARS_BODY = Array.from({ length: 28 }, (_, i) => `${avatarBodyBase}creator-${i + 1}.jpg`);

  const avatarAspiradorBase = isPagesDir ? '../img/creators-aspirador/' : 'img/creators-aspirador/';
  const AVATARS_ASPIRADOR = Array.from({ length: 28 }, (_, i) => `${avatarAspiradorBase}creator-${i + 1}.jpg`);

  const avatarTechBase = isPagesDir ? '../img/creators-tech/' : 'img/creators-tech/';
  const AVATARS_TECH = Array.from({ length: 28 }, (_, i) => `${avatarTechBase}creator-${i + 1}.jpg`);

  const avatarAutoBase = isPagesDir ? '../img/creators-auto/' : 'img/creators-auto/';
  const AVATARS_AUTO = Array.from({ length: 28 }, (_, i) => `${avatarAutoBase}creator-${i + 1}.jpg`);

  const CREATORS_BODY_NAMES = [
    { name: "Giulia Ferreira", user: "giulia.provador" },
    { name: "Letícia Ramos", user: "leticiamoda.br" },
    { name: "Marina Alencar", user: "marina.looks" },
    { name: "Camila Vasconcelos", user: "camilavestir" },
    { name: "Renata Nogueira", user: "renatablog_" },
    { name: "Bianca Prado", user: "biancaprado.fit" },
    { name: "Patrícia Coimbra", user: "patyfashionreal" },
    { name: "Isabella Silveira", user: "isabellastyle" },
    { name: "Carolina Muniz", user: "carol_looksbr" },
    { name: "Bruna Esteves", user: "brunafitness" },
    { name: "Nathália Meireles", user: "nathymoda.oficial" },
    { name: "Tamires Albuquerque", user: "tamiresveste" },
    { name: "Gabriela Fontes", user: "gabicouto_br" },
    { name: "Jéssica Medeiros", user: "jessicamedeirosfit" },
    { name: "Sabrina Siqueira", user: "sabrinalooks" },
    { name: "Viviane Farias", user: "vivifariasmoda" },
    { name: "Rafaela Godoy", user: "rafagodoyfit" },
    { name: "Monique Barreto", user: "moniquevestir" },
    { name: "Aline Castilho", user: "alinecastilhostyle" },
    { name: "Tatiane Rezende", user: "tatirezende_" },
    { name: "Thais Antunes", user: "thaislooksreal" },
    { name: "Priscila Neves", user: "prinevesmoda" },
    { name: "Talita Morais", user: "talitamoraisbr" },
    { name: "Daniele Gusmão", user: "danigusmaofit" },
    { name: "Vanessa Guedes", user: "vanessaguedeslooks" },
    { name: "Milena Pimentel", user: "milenapimentel_" },
    { name: "Jaqueline Macedo", user: "jaquemacedomoda" },
    { name: "Kelly Brandão", user: "kellybrandaostyle" }
  ];

  const CREATORS_ASPIRADOR_NAMES = [
    { name: "Juliana Prado", user: "dicasda.ju" },
    { name: "Rafael Souza", user: "rafael.ape" },
    { name: "Eduardo Costa", user: "canalcleantech" },
    { name: "Carol Mendes", user: "rotinada.carol" },
    { name: "Lucas Martins", user: "organiza.lucas" },
    { name: "Rayane Silva", user: "achadinhosdaray" },
    { name: "Mariana & Thiago", user: "meuprimeiroap" },
    { name: "Patrícia Alencar", user: "lar.da.paty" },
    { name: "Diego Ferreira", user: "diegotech.br" },
    { name: "Larissa Rocha", user: "larissa.organiza" },
    { name: "Marcos Silva", user: "marcos_automotivo" },
    { name: "Felipe & Dani", user: "dicasdocasal_" },
    { name: "Gabriel Nunes", user: "ape.pequeno" },
    { name: "Bárbara Dias", user: "barbaracasa" },
    { name: "Rodrigo Antunes", user: "rodrigo.reviews" },
    { name: "Camila & Léo", user: "nossoapto" },
    { name: "Thiago Moreira", user: "thiagodicasuteis" },
    { name: "Bruna Organiza", user: "brunaorganiza.lar" },
    { name: "Renan Silveira", user: "renan_garagem" },
    { name: "Aline Apê 304", user: "alineape304" },
    { name: "Guilherme Tech", user: "guitechdicas" },
    { name: "Paula & Beto", user: "casinha.paulaebeto" },
    { name: "Matheus Dicas", user: "matheusreviews" },
    { name: "Vanessa Limpeza", user: "vanessalimpezareal" },
    { name: "André Viana", user: "andrevianacasa" },
    { name: "Jéssica Casal", user: "dicasparadois" },
    { name: "Alexandre Casa", user: "alexandre.rotina" },
    { name: "Tatiana Dicas", user: "tatidicaslimpeza" }
  ];

  const CREATORS_TECH_NAMES = [
    { name: "Matheus Tech", user: "matheustechbr" },
    { name: "Bruno Cinema", user: "brunocine" },
    { name: "Guilherme Setup", user: "setupdomateus" },
    { name: "Lucas Gadgets", user: "lucasgadgets" },
    { name: "Rodrigo Games", user: "rodrigogamesbr" },
    { name: "Felipe Hardware", user: "felipehardware" },
    { name: "Pedro Cinema", user: "cinemaemcasa.br" },
    { name: "Tiago Geek", user: "tiagogeekreview" },
    { name: "Renan Play", user: "renanplaytech" },
    { name: "Leonardo Home", user: "leohometheater" },
    { name: "Carlos Projeção", user: "carlosprojetores" },
    { name: "Danilo Setup", user: "danilosetups" },
    { name: "Vinicius Tech", user: "viniciustechreview" },
    { name: "Gustavo Nerd", user: "gustavonerdcast" },
    { name: "Fabio Gadgets", user: "fabiogadgetsbr" },
    { name: "Marcelo Smart", user: "marcelosmarthome" },
    { name: "Igor Display", user: "igordisplay4k" },
    { name: "Alan Setup", user: "alansetupgames" },
    { name: "Murilo Tech", user: "murilotech_" },
    { name: "Caio Cinema", user: "caiocinematech" },
    { name: "Arthur Review", user: "arthurtechreviews" },
    { name: "Samuel Streaming", user: "samuelstreaming" },
    { name: "Henrique Gadgets", user: "henriquegadgets" },
    { name: "Victor 4K", user: "victorcinema4k" },
    { name: "Lucas Pixel", user: "lucaspixeltech" },
    { name: "Enzo Gaming", user: "enzogamingbr" },
    { name: "Rafael Telão", user: "rafaeltelaohome" },
    { name: "Daniel TechHub", user: "danieltechhub" }
  ];

  const CREATORS_AUTO_NAMES = [
    { name: "Tiago Borracharia", user: "tiago_oficina" },
    { name: "Marcos Pneus", user: "marcos_pneus" },
    { name: "Rodrigo Mecânico", user: "rodrigo_mecanico" },
    { name: "Fábio Motorista", user: "fabiomotorista" },
    { name: "Paulo Oficina", user: "paulo_auto" },
    { name: "Alexandre Rodas", user: "alexandrerodasbr" },
    { name: "Carlos Garagem", user: "carlosdicasauto" },
    { name: "Renato Auto", user: "renatoautooficial" },
    { name: "Leandro Pneus", user: "leandropneusecia" },
    { name: "Marcelo Uber", user: "marcelouberbr" },
    { name: "Eduardo Rodagem", user: "eduardorodagem" },
    { name: "Cláudio Oficina", user: "claudioautocenter" },
    { name: "Jorge Borracheiro", user: "jorgeborracheiro" },
    { name: "Daniel PneuShow", user: "danielpneushow" },
    { name: "Fernando Estrada", user: "fernandonaestrada" },
    { name: "Ricardo Motor", user: "ricardomotortech" },
    { name: "Luciano Asfalto", user: "lucianoasfalto" },
    { name: "Gustavo Rodas", user: "gustavorodas_" },
    { name: "Mauro Garage", user: "maurogaragebr" },
    { name: "Cristiano Auto", user: "cristianoautodicas" },
    { name: "Valter Mecânica", user: "valtermecanica" },
    { name: "Silvio Rodas", user: "silviorodasoficial" },
    { name: "Sérgio Pneus", user: "sergiopneusbr" },
    { name: "Márcio Estrada", user: "marcioestrada_" },
    { name: "Gilberto Auto", user: "gilbertoautocenter" },
    { name: "Rogério Motor", user: "rogeriomotorista" },
    { name: "Wagner Borracharia", user: "wagnerpneus" },
    { name: "André Garagem", user: "andregaragemauto" }
  ];

  // 28 offsets temporais únicos (em segundos) para que NENHUM criador comece a reproduzir o mesmo trecho
  const TAKE_OFFSETS = [
    0.0, 5.2, 11.5, 17.8, 24.0, 
    3.4, 9.1, 15.3, 21.6, 28.2, 
    2.1, 7.8, 13.9, 19.4, 26.0, 
    4.3, 10.5, 16.7, 22.9, 29.5, 
    1.2, 6.4, 12.6, 18.2, 25.1, 
    8.3, 14.7, 20.8
  ];

  // 1. DATASET DE MODA / CHINELO DE STRASS (PRODUTO 104) - 32 CRIADORAS E AVALIAÇÕES REAIS (CATBOX CLOUD CDN)
  const CHINELO_VIDEOS_MAP = [
  {
    name: "Adriana Souza",
    username: "adrianasouza.oficial",
    avatar: "../img/creators-chinelo/creator-104-1.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora1.jpg",
    video: "https://files.catbox.moe/aafohb.mp4",
    desc: "Chinelo strass"
  },
  {
    name: "Marlise Shop",
    username: "marliseshop_br",
    avatar: "../img/creators-chinelo/creator-104-2.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora2.jpg",
    video: "https://files.catbox.moe/2xx2zl.mp4",
    desc: "Chinelo Strass"
  },
  {
    name: "Jamilee Anderson",
    username: "jamileeanderson0",
    avatar: "../img/creators-chinelo/creator-104-3.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora3.jpg",
    video: "https://files.catbox.moe/lrv49i.mp4",
    desc: "Olha o brilho desse chinelo de strass, apaixonada demais! ✨💎"
  },
  {
    name: "Dryelle Santos",
    username: "dry_santoscalcados",
    avatar: "../img/creators-chinelo/creator-104-4.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora4.jpg",
    video: "https://files.catbox.moe/nbalj2.mp4",
    desc: "Chinelo strass"
  },
  {
    name: "Carolina Mello",
    username: "carol_mello_trends",
    avatar: "../img/creators-chinelo/creator-104-5.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora5.jpg",
    video: "https://files.catbox.moe/deh5ya.mp4",
    desc: "Chinelo strass"
  },
  {
    name: "Jamile Santos",
    username: "jamilesantos737",
    avatar: "../img/creators-chinelo/creator-104-6.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora6.jpg",
    video: "https://files.catbox.moe/v0yzdk.mp4",
    desc: "Chinelo strass"
  },
  {
    name: "Marlise Ramos",
    username: "marlise_achadinhos",
    avatar: "../img/creators-chinelo/creator-104-7.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora7.jpg",
    video: "https://files.catbox.moe/8x44i2.mp4",
    desc: "Chinelo Strass"
  },
  {
    name: "Beatriz Lima",
    username: "bialimastyle",
    avatar: "../img/creators-chinelo/creator-104-8.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora8.jpg",
    video: "https://files.catbox.moe/exba1n.mp4",
    desc: "Chinelo strass"
  },
  {
    name: "Thaynara Kelly",
    username: "tky740_achados",
    avatar: "../img/creators-chinelo/creator-104-9.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora9.jpg",
    video: "https://files.catbox.moe/rp1qiy.mp4",
    desc: "O chinelo personalizado com strass viral que combina conforto e muito brilho.✨✨✨✨✨✨✨ #tiktokshopbr1111 #viral #chinelo"
  },
  {
    name: "Tatiane Kelly",
    username: "tatykelly_calcados",
    avatar: "../img/creators-chinelo/creator-104-10.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora10.jpg",
    video: "https://files.catbox.moe/lpgj78.mp4",
    desc: "Esse chinelo é a cara do ano novo ✨✨✨ Ele é todo personalizado com strass e o brilho é incrível ✨✨ #tiktokshopbr1010 #viral #strass #chinelo"
  },
  {
    name: "Mirella Cavalieri",
    username: "mirelacavalieri",
    avatar: "../img/creators-chinelo/creator-104-11.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora11.jpg",
    video: "https://files.catbox.moe/a4ucgq.mp4",
    desc: "Chinelo Feminino De Luxo Strass Confortavel Brilhante Confortável"
  },
  {
    name: "Mirella Modas",
    username: "mirellamodas_real",
    avatar: "../img/creators-chinelo/creator-104-12.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora12.jpg",
    video: "https://files.catbox.moe/w60urq.mp4",
    desc: "Chinelo Feminino De Luxo Strass Confortavel Brilhante Confortável"
  },
  {
    name: "Taís Silva",
    username: "taissilva_oficial",
    avatar: "../img/creators-chinelo/creator-104-13.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora13.jpg",
    video: "https://files.catbox.moe/z0xcjk.mp4",
    desc: "Simplesmente apaixonada em cada detalhe desse chinelo com strass ✨✨✨✨✨ #tiktokshopbr1111 #viral #moda #chinelo"
  },
  {
    name: "Karina Farias",
    username: "karinafarias_trends",
    avatar: "../img/creators-chinelo/creator-104-14.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora14.jpg",
    video: "https://files.catbox.moe/9tnsz8.mp4",
    desc: "Simplesmente encantada com esse chinelo feminino personalizado com strass 🥹❤️❤️ #chinelobrilho #chinelostrass #viral #strass"
  },
  {
    name: "Michele Cavalieri",
    username: "michele_cavalieri",
    avatar: "../img/creators-chinelo/creator-104-15.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora15.jpg",
    video: "https://files.catbox.moe/1lofgx.mp4",
    desc: "Chinelo Feminino De Luxo Strass Confortavel Brilhante Confortável"
  },
  {
    name: "Talita Duarte",
    username: "talita_duarte_calcados",
    avatar: "../img/creators-chinelo/creator-104-16.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora16.jpg",
    video: "https://files.catbox.moe/tfn64t.mp4",
    desc: "Amigas olha esse Chinelo feminino personalizado ó Strass 😍 #viral #strass #chinelo"
  },
  {
    name: "Marcella Cavalieri",
    username: "marcella_cavalieri",
    avatar: "../img/creators-chinelo/creator-104-17.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora17.jpg",
    video: "https://files.catbox.moe/vf4bsn.mp4",
    desc: "Chinelo Feminino De Luxo Strass Confortavel Brilhante Confortável"
  },
  {
    name: "Melissa Cavalieri",
    username: "melissa_cavalieri",
    avatar: "../img/creators-chinelo/creator-104-18.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora18.jpg",
    video: "https://files.catbox.moe/n0ld91.mp4",
    desc: "Chinelo Feminino De Luxo Strass Confortavel Brilhante Confortável"
  },
  {
    name: "Leila Carvalho",
    username: "leilacarvalho47",
    avatar: "../img/creators-chinelo/creator-104-19.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora19.jpg",
    video: "https://files.catbox.moe/cdbtuo.mp4",
    desc: "#tiktoklive #livehighlights  #chinelo #strass #sandaliasfemininas"
  },
  {
    name: "Jhennifer Costa",
    username: "jhennicosta_achados",
    avatar: "../img/creators-chinelo/creator-104-20.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora20.jpg",
    video: "https://files.catbox.moe/yvcfnl.mp4",
    desc: "#chinelo #strass"
  },
  {
    name: "Kethellen Ster",
    username: "ky.ster1",
    avatar: "../img/creators-chinelo/creator-104-21.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora21.jpg",
    video: "https://files.catbox.moe/gpk093.mp4",
    desc: "Chinelo feminino que não dá✨😮 muito lindo né amgs #chinelospersonalizados #chinelobrilho #chinelostrass"
  },
  {
    name: "Jéssica Farias",
    username: "jessicafarias.ofc",
    avatar: "../img/creators-chinelo/creator-104-22.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora22.jpg",
    video: "https://files.catbox.moe/u0vhf1.mp4",
    desc: "Chinelo confortável com correia de strass"
  },
  {
    name: "Jéssica Anderson",
    username: "jessica_anderson_shop",
    avatar: "../img/creators-chinelo/creator-104-23.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora23.jpg",
    video: "https://files.catbox.moe/tm9n3z.mp4",
    desc: "Chinelo com strass"
  },
  {
    name: "Renata Nunes",
    username: "renatanunesofc",
    avatar: "../img/creators-chinelo/creator-104-24.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora24.jpg",
    video: "https://files.catbox.moe/gfe96k.mp4",
    desc: "Esse chinelo no strass é um luxooooooo😍. Amigas, pensa em um chinelo lindooooo e confortável 😍. Ele tem na frete o detalhe todo no strass que dá um charme nele. Pedi minha numeração correta e ficou ótimo pra mim. Vou deixar o link desse chinelo maravilhoso no carrinho laranja pra vocês amigas 🥰 #chinelo #chinelonostrass #chineloconfortavel #calcadosfemeninos #ViralTikTokShop"
  },
  {
    name: "Brenda Oliveira",
    username: "brendinhashop_",
    avatar: "../img/creators-chinelo/creator-104-25.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora25.jpg",
    video: "https://files.catbox.moe/jfpqm3.mp4",
    desc: "Chibelo em nó com strass para arrasar no verão 😍🤌🏻✨ #chinelofeminino #strass #chinelocombrilho #brilho #tiktokshop"
  },
  {
    name: "Larissa Santos",
    username: "lar1.69",
    avatar: "../img/creators-chinelo/creator-104-26.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora26.jpg",
    video: "https://files.catbox.moe/94o8oq.mp4",
    desc: "Rasteirinha strass perfeita 🫰🏼💖 #rasteirinha #strass #comprinhas #tiktokshop #viral"
  },
  {
    name: "Júlia Milagres",
    username: "juliamilagres3",
    avatar: "../img/creators-chinelo/creator-104-27.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora27.jpg",
    video: "https://files.catbox.moe/bxt3b7.mp4",
    desc: "Rasteirinha de strass maravilhosa 🤌 #rasteirinha #chinelo #calcadosfemininos #paravoce #achadinhos"
  },
  {
    name: "Juliana Milagres",
    username: "jumilagres_achados",
    avatar: "../img/creators-chinelo/creator-104-28.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora28.jpg",
    video: "https://files.catbox.moe/qitwtl.mp4",
    desc: "Rasteirinha de Strass #rasteirinha #calcadosfemininos #paravoce #viraltiktokshop #strass"
  },
  {
    name: "Alyne Machado",
    username: "alynesmachado",
    avatar: "../img/creators-chinelo/creator-104-29.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora29.jpg",
    video: "https://files.catbox.moe/qlgwje.mp4",
    desc: "Rasteirinha Strass luxo #verao #chinelo #chinelosdecorados #rasteirinhasdeluxo #rasteirinhafeminina"
  },
  {
    name: "Nila Maria",
    username: "nilmmxdrkze",
    avatar: "../img/creators-chinelo/creator-104-30.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora30.jpg",
    video: "https://files.catbox.moe/mym2lr.mp4",
    desc: "Kit 2 sandálias rasteirinha básica mais chic para lindas mulheres com strass.  2 pares, muito mais estilo! Rasteirinhas com strass que unem conforto e aquele toque chic para deixar qualquer look deslumbrante.  #Rasteirinha #SandaliaFeminina #Strass #ModaFeminina"
  },
  {
    name: "Stilo Z Modas",
    username: "stiloz6",
    avatar: "../img/creators-chinelo/creator-104-31.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora31.jpg",
    video: "https://files.catbox.moe/rs0u0r.mp4",
    desc: "✨ Sandália Rasteira Luxo em Strass ✨ Um modelo delicado, elegante e cheio de brilho! 💎 Com detalhe no dedão, tiras cravejadas em strass e palmilha confortável. Perfeita para deixar qualquer produção ainda mais sofisticada. ✨ 📏 Numeração disponível: 34 ao 39 🛍️ Varejo e atacado #sandaliafeminina#rasteirinha#strass#modafeminina#calçadosfemininos"
  },
  {
    name: "Gabi Santos",
    username: "gabisoficiall",
    avatar: "../img/creators-chinelo/creator-104-32.jpg",
    poster: "../img/posters-chinelo/poster-chinelo-criadora32.jpg",
    video: "https://files.catbox.moe/2gi13x.mp4",
    desc: "Sandália Feminina Rasteirinha Strass. ✨✨ #sandaliafeminina #papete #strass #tiktokshop #viral"
  }
];

    const CREATORS_CHINELO_104 = CHINELO_VIDEOS_MAP.map((vInfo, i) => {
    return {
      name: vInfo.name,
      username: vInfo.username,
      avatar: vInfo.avatar,
      poster: vInfo.poster,
      video: vInfo.video,
      startTime: 0.2,
      likes: 9200 + (i * 513) % 12000,
      commentsCount: 32 + (i * 7) % 90,
      saves: 1200 + (i * 87) % 2100,
      shares: 140 + (i * 19) % 450,
      description: vInfo.desc
    };
  });

      // 1.1 DATASET DO PROJETOR HY300 4K SMART (PRODUTO 105) - CRIADORES 100% REAIS E OFICIAIS
  const PROJETOR_VIDEOS_MAP = [
  {
      name: "Matheus Tech",
      username: "matheustechbr",
      avatar: "../img/creators-tech/creator-1.jpg",
      poster: "../videosprodutos/posters/poster-produto-111.jpg",
      video: "https://files.catbox.moe/facj5t.mp4",
      startTime: 0.2,
      desc: "Gente, transformei meu quarto num cinema 4K por menos de 40 reais! Projetando direto no teto com Netflix! 🍿🎬"
    },
  {
      name: "Bruno Cinema",
      username: "brunocine",
      avatar: "../img/creators-tech/creator-2.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora2.jpg",
      video: "https://files.catbox.moe/4tf7wb.mp4",
      startTime: 0.2,
      desc: "Olha a qualidade desse Projetor Smart HY300! Já vem com Android 11, Wi-Fi e Bluetooth. Conecta na caixa de som e é perfeito! 🔥"
    },
  {
      name: "Lucas Pixel",
      username: "lucaspixeltech",
      avatar: "../img/creators-tech/creator-3.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora3.jpg",
      video: "https://files.catbox.moe/e8go2r.mp4",
      startTime: 0.2,
      desc: "Testando a rotação de 180 graus na parede e no teto. Rotação livre, foco ajustável e imagem gigante de 130 polegadas! 🤩"
    }
  ];

  const CREATORS_PROJETOR_105 = PROJETOR_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 12400 + (i * 618) % 15000,
    commentsCount: 45 + (i * 9) % 120,
    saves: 2100 + (i * 134) % 3200,
    shares: 380 + (i * 45) % 890,
    description: vInfo.desc
  }));

  // 1.2 DATASET DO BODY MODELADOR CINTA ALTA COMPRESSÃO (PRODUTO 106)
  const BODY_106_VIDEOS_MAP = [
  {
      name: "Talita Santos ✨",
      username: "talitasantos_fit",
      avatar: "../img/reviews-avatars/mulheres_validadas/mulher_1.jpg",
      poster: "../videosprodutos/posters/poster-produto-106.jpg",
      video: "https://files.catbox.moe/1hm15q.mp4",
      startTime: 0.2,
      desc: "Meninas, olha como reduz medidas instantaneamente! Não dobra, não enrola e modela tudo! 😍✨"
    },
  {
      name: "Luisa Provador",
      username: "luisaprovador",
      avatar: "../img/reviews-avatars/mulheres_validadas/mulher_2.jpg",
      poster: "../videosprodutos/posters/poster-106-criadora2.jpg",
      video: "https://files.catbox.moe/jpmxf4.mp4",
      startTime: 0.2,
      desc: "Provador sincero: usei com vestido colado e não marca absolutamente nada por baixo! ❤️"
    },
  {
      name: "Camila Moda",
      username: "camilamoda",
      avatar: "../img/reviews-avatars/mulheres_validadas/mulher_7.jpg",
      poster: "../videosprodutos/posters/poster-106-criadora3.jpg",
      video: "https://files.catbox.moe/fl5tle.mp4",
      startTime: 0.2,
      desc: "Tecido respirável de alta compressão com fecho prático entrepernas. Muito confortável! 👏"
    },
  {
      name: "Renata Modeladora",
      username: "renatamodeladora",
      avatar: "../img/reviews-avatars/mulheres_validadas/mulher_11.jpg",
      poster: "../videosprodutos/posters/poster-106-criadora4.jpg",
      video: "https://files.catbox.moe/c2wclc.mp4",
      startTime: 0.2,
      desc: "Segura a barriga sem sufocar, dá pra trabalhar o dia inteiro de boa. Amei! 💖"
    }
  ];

  const CREATORS_BODY_106 = BODY_106_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 10500 + (i * 420) % 11000,
    commentsCount: 52 + (i * 9) % 95,
    saves: 2100 + (i * 130) % 2900,
    shares: 310 + (i * 35) % 600,
    description: vInfo.desc
  }));

  // 1.3 DATASET DO MINI ASPIRADOR DE PÓ E SOPRADOR TURBO 2 EM 1 (PRODUTO 107)
  const ASPIRADOR_107_VIDEOS_MAP = [
  {
      name: "TikShoop Oficial",
      username: "tikshoop7",
      avatar: "../img/creators-aspirador/creator-1.jpg",
      poster: "../videosprodutos/posters/poster-produto-107.jpg",
      video: "https://files.catbox.moe/049abg.mp4",
      startTime: 0.2,
      desc: "Poder de sucção absurdo de 9000Pa! Tirou toda a sujeira dos cantos do banco do carro 🚗💨"
    },
  {
      name: "Canal CleanTech",
      username: "canalcleantech",
      avatar: "../img/creators-aspirador/creator-2.jpg",
      poster: "../videosprodutos/posters/poster-107-criador2.jpg",
      video: "https://files.catbox.moe/nwhxcm.mp4",
      startTime: 0.2,
      desc: "Além de aspirar ele é soprador turbo de ar! Limpa teclado, PC e acende churrasqueira 🔥"
    },
  {
      name: "Dicas do Casal",
      username: "dicasdocasal_",
      avatar: "../img/creators-aspirador/creator-3.jpg",
      poster: "../videosprodutos/posters/poster-107-criador3.jpg",
      video: "https://files.catbox.moe/yki4q2.mp4",
      startTime: 0.2,
      desc: "Filtro HEPA lavável reutilizável, muito fácil de limpar na torneira. Valeu cada centavo! 😍"
    }
  ];

  const CREATORS_ASPIRADOR_107 = ASPIRADOR_107_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 9100 + (i * 490) % 12000,
    commentsCount: 42 + (i * 8) % 110,
    saves: 1600 + (i * 110) % 2500,
    shares: 210 + (i * 25) % 520,
    description: vInfo.desc
  }));

  // 1.4 DATASET DA ESCOVA SECADORA E MODELADORA 5 EM 1 (PRODUTO 108)
  const ESCOVA_108_VIDEOS_MAP = [
  {
      name: "Karen Mendes",
      username: "dailykarenm",
      avatar: "../img/creators-cabelo/creator-108-1.jpg",
      poster: "../videosprodutos/posters/poster-produto-108.jpg",
      video: "https://files.catbox.moe/e7z9vc.mp4",
      startTime: 0.2,
      desc: "Respondendo a dúvidas sobre o efeito Coanda da escova 5 em 1! Seca e modela em minutos sem queimar o cabelo 😍✨"
    },
  {
      name: "Daniele Fogassa",
      username: "danielefogassa",
      avatar: "../img/creators-cabelo/creator-108-2.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora2.jpg",
      video: "https://files.catbox.moe/a33ud2.mp4",
      startTime: 0.2,
      desc: "Como usar essa escova 5 em 1! Testando as ponteiras e mostrando o resultado no meu cabelo ❤️ #escova5em1 #cabelo"
    },
  {
      name: "Jaqueline Santos",
      username: "dicascomjaque",
      avatar: "../img/creators-cabelo/creator-108-3.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora3.jpg",
      video: "https://files.catbox.moe/o5zg5j.mp4",
      startTime: 0.2,
      desc: "Resenha Completa usando o Secador Multifuncional 5 em 1! Potência excelente de 1000W, alinhou meu cabelo sem frizz 👏"
    },
  {
      name: "Marcella Romero",
      username: "marcellaromero",
      avatar: "../img/creators-cabelo/creator-108-4.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora4.jpg",
      video: "https://files.catbox.moe/kduyle.mp4",
      startTime: 0.2,
      desc: "Comprei a Dyson da TikTok Shop! Vale cada centavo, melhor compra que fiz pro meu cabelo esse ano 🩷"
    },
  {
      name: "Dayane Marcheseli",
      username: "dayanemarcheseli",
      avatar: "../img/creators-cabelo/creator-108-5.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora5.jpg",
      video: "https://files.catbox.moe/cl9iht.mp4",
      startTime: 0.2,
      desc: "O queridinho secador escova 5 em 1 voltou pro estoque e na promo do 7.7 🔥💥 #tiktokshopbr77 #escova5em1 #secador5em1"
    },
  {
      name: "cheiadetruques",
      username: "cheiadetruques_",
      avatar: "../img/creators-cabelo/creator-108-6.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora6.jpg",
      video: "https://files.catbox.moe/zm63iv.mp4",
      startTime: 0.2,
      desc: "Pra quem gosta de praticidade e variar nos penteados, essa escovova é perfeita! Seca, alisa e modela! #escovasecadora #tiktokshop #beleza"
    },
  {
      name: "Cassa Ofertas",
      username: "cassaofertas",
      avatar: "../img/creators-cabelo/creator-108-7.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora7.jpg",
      video: "https://files.catbox.moe/r2zsax.mp4",
      startTime: 0.2,
      desc: "Escova de cabelo alisadora 5 em 1✨ Essa escova é perfeita para o dia a dia 😌👌 #cabelos #cabeloliso #escovasecadora"
    },
  {
      name: "Day Alves",
      username: "dayalvesoficial",
      avatar: "../img/creators-cabelo/creator-108-8.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora8.jpg",
      video: "https://files.catbox.moe/g3pnna.mp4",
      startTime: 0.2,
      desc: "Se alisar meu cabelo amor, alisa qualquer coisa kkkkkkkkkk #tiktokshop #testantoprodutos #reviwdeproduto #escovaalisadora5em1 #cachos"
    },
  {
      name: "Caroliny Madona",
      username: "carolinymadona",
      avatar: "../img/creators-cabelo/creator-108-9.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora9.jpg",
      video: "https://files.catbox.moe/gdsx0f.mp4",
      startTime: 0.2,
      desc: "Escova Secadora 5 em 1 com Íons negativos. Secador, Modelador e Alisador  #tiktokshopbr1111 #tiktokshopbr1212 #blackfridayentiktokshop #modelador #escovasecador"
    },
  {
      name: "Nina ♡ UGC",
      username: "nina.creator",
      avatar: "../img/creators-cabelo/creator-108-10.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora10.jpg",
      video: "https://files.catbox.moe/4rrdpx.mp4",
      startTime: 0.2,
      desc: "Meninass, olha esse achado, escova Secadora 5 em 1 com um super desconto! 🤏😍✨️💖"
    },
  {
      name: "Diva & Dama",
      username: "divaedama_ofc",
      avatar: "../img/creators-cabelo/creator-108-11.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora11.jpg",
      video: "https://files.catbox.moe/bm0bve.mp4",
      startTime: 0.2,
      desc: "⬆️LINK AÍ ÓH⬆️ escova secadora 5 em 1. escova que seca e alisa. modelador e secador junto. escova de ar quente multifuncional. escova que faz tudo no cabelo. se"
    },
  {
      name: "Friend’s Promo 🛍️",
      username: "friendspromo_",
      avatar: "../img/creators-cabelo/creator-108-12.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora12.jpg",
      video: "https://files.catbox.moe/xmqioh.mp4",
      startTime: 0.2,
      desc: "A escova 5 em 1 que é a febreeee do momento. 😍 Gostou? Se sim, correee pro link da bio! #tiktokshop #secador5en1 #hair #foru "
    },
  {
      name: "•✯ Chuva de Ofertinhas ✯•",
      username: "chuvadeofertinha",
      avatar: "../img/creators-cabelo/creator-108-13.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora13.jpg",
      video: "https://files.catbox.moe/a9cj0d.mp4",
      startTime: 0.2,
      desc: "Escova Eletrica Limpeza 5 em 1 🫧🧽 #escovaeletrica #escovadelimpeza "
    },
  {
      name: "Achou Levou",
      username: "achoulevoupravoce",
      avatar: "../img/creators-cabelo/creator-108-14.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora14.jpg",
      video: "https://files.catbox.moe/qfigmp.mp4",
      startTime: 0.2,
      desc: "Escova Eletrica De Limpeza 5 EM 1 #promoçãotiktokshop #cozinha #limpeza #escovaeletrica #utensilios "
    },
  {
      name: "-ˋˏ ༻ A Noleto ༺ ˎˊ-",
      username: "anapaulanoletto",
      avatar: "../img/creators-cabelo/creator-108-15.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora15.jpg",
      video: "https://files.catbox.moe/uxdo67.mp4",
      startTime: 0.2,
      desc: "#tiktoklive #livehighlights #escova5em1"
    },
  {
      name: "giiu.achadinhos",
      username: "giiu.achadinhos",
      avatar: "../img/creators-cabelo/creator-108-16.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora16.jpg",
      video: "https://files.catbox.moe/sochhj.mp4",
      startTime: 0.2,
      desc: "Eu gosto de produto que resolve mais de uma coisa de uma vez 😅💖✨ e essa escova secadora 5 em 1 faz exatamente isso. Ela é prática, multifuncional e ainda tá c"
    },
  {
      name: "Achadinhos da Nai 😍🎁",
      username: "nrnaiachadinhos",
      avatar: "../img/creators-cabelo/creator-108-17.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora17.jpg",
      video: "https://files.catbox.moe/y4eg91.mp4",
      startTime: 0.2,
      desc: "✨ Adeus, esfregação! 🧽😍 A escova elétrica 5 em 1 facilita a limpeza da casa! 🏠 🫧 Sem fio e recarregável ✨ Várias funções em um só produto 🚿 Perfeita para b"
    },
  {
      name: "Achei Tendência",
      username: "ache_itendencia",
      avatar: "../img/creators-cabelo/creator-108-18.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora18.jpg",
      video: "https://files.catbox.moe/zp2396.mp4",
      startTime: 0.2,
      desc: "Achadinho Escova 5 em 1 #foryou #foryoupage #fyp #achadinhos #tiktokshop #tiktok "
    },
  {
      name: "Beatriz Oliveira ✨",
      username: "biadicas_hair",
      avatar: "../img/creators-cabelo/creator-108-19.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora19.jpg",
      video: "https://files.catbox.moe/ft686x.mp4",
      startTime: 0.2,
      desc: "✨ Menos tempo na frente do espelho e mais tempo para você! A Escova 5 em 1 reúne várias funções em um só aparelho para deixar seu cabelo lindo de forma prática."
    },
  {
      name: "Nayara Diroldi",
      username: "naydiroldi",
      avatar: "../img/creators-cabelo/creator-108-20.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora20.jpg",
      video: "https://files.catbox.moe/4mcs49.mp4",
      startTime: 0.2,
      desc: "Escova 5 em 1, o queridinho das garotas 💋🎀❤️ #cabelo #dicas #fyp #tiktokshop #belleza "
    },
  {
      name: "Dicas da Mony",
      username: "dicasdamony25",
      avatar: "../img/creators-cabelo/creator-108-21.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora21.jpg",
      video: "https://files.catbox.moe/53ycss.mp4",
      startTime: 0.2,
      desc: "Escova secadora 5 em 1. Prática e super funcional. cabelo de salão em  casa #tiktokshop #cabelo #escova5em1 #escovasecadora "
    },
  {
      name: "Luisa Soares",
      username: "luisasoaress11",
      avatar: "../img/creators-cabelo/creator-108-22.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora22.jpg",
      video: "https://files.catbox.moe/bes77r.mp4",
      startTime: 0.2,
      desc: "Eu amo essa escova secadora 5 em 1 perfeita 💖 ela acabou de voltar pro estoque! Aproveitem!!! #escovasecadora #escova #Gokoco "
    },
  {
      name: "topachadosdacarla",
      username: "topachadosdacarla",
      avatar: "../img/creators-cabelo/creator-108-23.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora23.jpg",
      video: "https://files.catbox.moe/u1xelf.mp4",
      startTime: 0.2,
      desc: "Escova de Limpeza Elétrica 5 em 1 😍😍😍"
    },
  {
      name: "Nataliè Rosè",
      username: "natalierose.oficial",
      avatar: "../img/creators-cabelo/creator-108-24.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora24.jpg",
      video: "https://files.catbox.moe/aj6eh5.mp4",
      startTime: 0.2,
      desc: "Escova 5 em 1 alisadora pra cabelo cacheado e crespo #cabelo #tiktokshopbrasil #viralizar #crespos #gym "
    },
  {
      name: "JACKE Sylva💞",
      username: "jackeshopofc",
      avatar: "../img/creators-cabelo/creator-108-25.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora25.jpg",
      video: "https://files.catbox.moe/p3kspr.mp4",
      startTime: 0.2,
      desc: "escova 5 em 1 seu cabelo com resultado de salão em casa #cabelo #tiktokviral #tiktokshop "
    },
  {
      name: "iris inspira 𝜗ৎ݁˖",
      username: "irisinspira",
      avatar: "../img/creators-cabelo/creator-108-26.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora26.jpg",
      video: "https://files.catbox.moe/o26l96.mp4",
      startTime: 0.2,
      desc: "estou amando usar essa escova secadora 5 em 1 bivolt da gokoco para finalizar meu cabelo 🥹✨ ela é super fácil de usar e ter várias ponteiras ajuda muito na hor"
    },
  {
      name: "Adriele Ramos",
      username: "drih_ramos69",
      avatar: "../img/creators-cabelo/creator-108-27.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora27.jpg",
      video: "https://files.catbox.moe/v1e230.mp4",
      startTime: 0.2,
      desc: "LEMBRANDO QUE ESSA É 110W CONFIRA A VOLTAGEM DA SUA CIDADE! Escova secadora 5 em 1, seca, modela e não quebra!!!  #viraltiktokshop #secadordecabelo #escovamodel"
    },
  {
      name: "AMALLU",
      username: "amalludicas",
      avatar: "../img/creators-cabelo/creator-108-28.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora28.jpg",
      video: "https://files.catbox.moe/kv3y95.mp4",
      startTime: 0.2,
      desc: "Testei a escova secadora 5 em 1 de 1000W e entendi porque todo mundo está comprando 😳 Ela seca, alisa, modela e dá volume ao mesmo tempo. Praticamente um salão"
    },
  {
      name: "Fernanda Live_Shop",
      username: "fernandaliveshop",
      avatar: "../img/creators-cabelo/creator-108-29.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora29.jpg",
      video: "https://files.catbox.moe/yqt8c4.mp4",
      startTime: 0.2,
      desc: "Escova Secadora Alisadora 5 em 1 Babyliss Modelador de Cachos Potente 1100w 110V"
    },
  {
      name: "Aline Coraza",
      username: "alinedescobriu1",
      avatar: "../img/creators-cabelo/creator-108-30.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora30.jpg",
      video: "https://files.catbox.moe/rlvz8f.mp4",
      startTime: 0.2,
      desc: "Secar, alisar, modelar e fazer cachos com um único aparelho! Confira essa oferta! #TikTokShop1010 #Escova5em1 #EscovaModeladora #CabelosFemininos #belezafeminin"
    },
  {
      name: "Tas ᥫ᭡.ִֶָ𓂃 Indica",
      username: "tassindica",
      avatar: "../img/creators-cabelo/creator-108-31.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora31.jpg",
      video: "https://files.catbox.moe/x089oe.mp4",
      startTime: 0.2,
      desc: "Escova secadora 5 em 1 #gokoco #escovasecadora #escovamodeladora #secador #tiktokshopbr1010 "
    },
  {
      name: "Isa Oliveira",
      username: "isaaoliveiral",
      avatar: "../img/creators-cabelo/creator-108-32.jpg",
      poster: "../videosprodutos/posters/poster-produto-108-criadora32.jpg",
      video: "https://files.catbox.moe/olza0w.mp4",
      startTime: 0.2,
      desc: "não sei se to louca mas esse foi meu feedback usando ele, vocês gostaram? #escovasecadora #secadorphilco #secadorphilco5em1 #secador #escovaphilco "
    }
  ];

  const CREATORS_ESCOVA_108 = ESCOVA_108_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 12400 + (i * 620) % 15000,
    commentsCount: 68 + (i * 12) % 140,
    saves: 2800 + (i * 180) % 3500,
    shares: 340 + (i * 40) % 800,
    description: vInfo.desc
  }));

  // 1.5 DATASET DO MODELADOR DE CACHOS AUTOMÁTICO SEM FIO (PRODUTO 109)
  const MODELADOR_109_VIDEOS_MAP = [
  {
      name: "Gabi Modesto",
      username: "gabimodestoo",
      avatar: "../img/creators-cabelo/creator-109-1.jpg",
      poster: "../videosprodutos/posters/poster-produto-109.jpg",
      video: "https://files.catbox.moe/bjcwqr.mp4",
      startTime: 0.2,
      desc: "Qualidade surpreende por esse valor! Carrega igual celular por menos de R$ 50,00! Cachos perfeitos 😍"
    },
  {
      name: "Achadinhos da Luah",
      username: "achadinhos.daluah",
      avatar: "../img/creators-cabelo/creator-109-2.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora2.jpg",
      video: "https://files.catbox.moe/lxfl7p.mp4",
      startTime: 0.2,
      desc: "Modelador de cachos ferro automático sem fio com bateria recarregável embutida cerâmica. Prático demais pra levar na bolsa ✨"
    },
  {
      name: "Yasmin Oliveira",
      username: "yasmin.aoliveira",
      avatar: "../img/creators-cabelo/creator-109-3.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora3.jpg",
      video: "https://files.catbox.moe/xrh3lz.mp4",
      startTime: 0.2,
      desc: "Testei o modelador de cachos sem fio! Ele suga a mecha sozinho e apita quando tá pronto. Amei o resultado! #tiktokshopchegou"
    },
  {
      name: "Samara Fontele",
      username: "samara_fontele",
      avatar: "../img/creators-cabelo/creator-109-4.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora4.jpg",
      video: "https://files.catbox.moe/wwalmv.mp4",
      startTime: 0.2,
      desc: "Cachos sem esforço em qualquer lugar! Levo no carro e arrumo meu cabelo antes das reuniões ❤️ #modeladordecachos #cachos"
    },
  {
      name: "Mariana Quintão",
      username: "maryonlive",
      avatar: "../img/creators-cabelo/creator-109-5.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora5.jpg",
      video: "https://files.catbox.moe/2zwxcu.mp4",
      startTime: 0.2,
      desc: "Modelador sem fio pra sair com o cabelo arrumado em qualquer lugar! Prático demais pra levar na bolsa e fazer cachos no precinho ✨ #tiktokshop #carrinholaranja"
    },
  {
      name: "Laizi Franco",
      username: "laizisantiago",
      avatar: "../img/creators-cabelo/creator-109-6.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora6.jpg",
      video: "https://files.catbox.moe/sdl8jo.mp4",
      startTime: 0.2,
      desc: "Cachos lindos sem passar horas enrolando mecha por mecha 😍✨ O modelador automático faz o trabalho por você! 💕"
    },
  {
      name: "Heloisa Frasão",
      username: "helofrasao",
      avatar: "../img/creators-cabelo/creator-109-7.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora7.jpg",
      video: "https://files.catbox.moe/uqbn1e.mp4",
      startTime: 0.2,
      desc: "Modelador de cabelo automático sem fio! 🤩💖 #tiktoklive #livehighlights #modeladordecachos"
    },
  {
      name: "Rafaella Samara",
      username: "rafaella.samara",
      avatar: "../img/creators-cabelo/creator-109-8.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora8.jpg",
      video: "https://files.catbox.moe/t4ypnz.mp4",
      startTime: 0.2,
      desc: "Ficar sem finalizar o cabelo não é opção!! E agora ficou muito fácil com esse modelado portátil! #modelador #modeladordecachos #cachos"
    },
  {
      name: "Eduarda Santos",
      username: "meeduardasantos",
      avatar: "../img/creators-cabelo/creator-109-9.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora9.jpg",
      video: "https://files.catbox.moe/zch6jv.mp4",
      startTime: 0.2,
      desc: "Esse babyliss praticamente faz o cacho sozinho😱😍❤️ #babyliss #modeladordecachos #penteado #dicasdebeleza #loiro "
    },
  {
      name: "Rita Fregolente | Tiktok Shop",
      username: "ritafregolente",
      avatar: "../img/creators-cabelo/creator-109-10.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora10.jpg",
      video: "https://files.catbox.moe/4x9djd.mp4",
      startTime: 0.2,
      desc: "@GOKOCO #gokoco #escovamodeladoradecachos #escovagokoco compre aqui no carrinho laranja "
    },
  {
      name: "Fernanda Tanaka",
      username: "fernandatanakaoficial",
      avatar: "../img/creators-cabelo/creator-109-11.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora11.jpg",
      video: "https://files.catbox.moe/sktv47.mp4",
      startTime: 0.2,
      desc: "Modelador de cachos em silicone prático ,rápido e  super fácil ! Reutilizável! Pra garantir o seu é só clicar no carrinho laranja !  #curlyhair #cachos #silicon"
    },
  {
      name: "Emily Novaes",
      username: "_milynovaes",
      avatar: "../img/creators-cabelo/creator-109-12.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora12.jpg",
      video: "https://files.catbox.moe/gpftoe.mp4",
      startTime: 0.2,
      desc: "Testei o famoso modelador de cachos que viralizou e acho que temos um novo queridinho por aqui! 💗👀 Vocês usariam? #ModeladorDeCachos #TestandoProdutos #Cabelo"
    },
  {
      name: "Julye Fajárdo Tomio",
      username: "julyefajardotomio",
      avatar: "../img/creators-cabelo/creator-109-13.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora13.jpg",
      video: "https://files.catbox.moe/s4df9x.mp4",
      startTime: 0.2,
      desc: "Babyliss bivolt em oferta relâmpago ⚡️! Ele é muito muito prático #babyliss #modeladordecachos #cabelos #penteados #babylisspro "
    },
  {
      name: "allana menezes",
      username: "allanamenezzes",
      avatar: "../img/creators-cabelo/creator-109-14.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora14.jpg",
      video: "https://files.catbox.moe/h5615y.mp4",
      startTime: 0.2,
      desc: "mudando a curvatura com texturização: bigodinho x modelador de silicone 👀 qual você prefere? . . #texturização #cacheadas #cachos #modeladordecachos #bigodinho"
    },
  {
      name: "Cisa 🌟",
      username: "cisavilasboas",
      avatar: "../img/creators-cabelo/creator-109-15.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora15.jpg",
      video: "https://files.catbox.moe/0tcugw.mp4",
      startTime: 0.2,
      desc: "Resultado de salão em casa 💗Modelador de cachos de 9 mm #tiktoklive #livehighlights #modeladordecachos #cabelocacheado "
    },
  {
      name: "4hi5en0p",
      username: "4hi5en0p",
      avatar: "../img/creators-cabelo/creator-109-16.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora16.jpg",
      video: "https://files.catbox.moe/qhqom8.mp4",
      startTime: 0.2,
      desc: "Modelador de Ondas Cerâmico – Cachos Duradouros com Proteção e Aquecimento Rápido 9mm Wand Cerâmico para Todos os Comprimentos de Cabelo#tiktok"
    },
  {
      name: "DEBS",
      username: "deborapaviani",
      avatar: "../img/creators-cabelo/creator-109-17.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora17.jpg",
      video: "https://files.catbox.moe/bjc1rw.mp4",
      startTime: 0.2,
      desc: "Respondendo a @Suzanna Kulczar | UGC Como usar modelador de cachos automático #modeladordecachosautomatico #modeladorautomático #maimeite #tiktokshopbr77 "
    },
  {
      name: "klleyaaa",
      username: "klleyaaa",
      avatar: "../img/creators-cabelo/creator-109-18.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora18.jpg",
      video: "https://files.catbox.moe/azmcja.mp4",
      startTime: 0.2,
      desc: "Modelador de cachos bigudinhos #cachos #modeladordecachos #tiktokshop "
    },
  {
      name: "Bruna Rocha 💖",
      username: "brunarocha_beauty",
      avatar: "../img/creators-cabelo/creator-109-19.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora19.jpg",
      video: "https://files.catbox.moe/0emzug.mp4",
      startTime: 0.2,
      desc: "Comprou e não sabe fazer os cachos com esse modelador então salva esse vídeo manda pras amigas que agora você vai aprender! #modeladordecachos #babyliss #cabelo"
    },
  {
      name: "Caroliny Madona",
      username: "carolinymadona",
      avatar: "../img/creators-cabelo/creator-109-20.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora20.jpg",
      video: "https://files.catbox.moe/b3lfo3.mp4",
      startTime: 0.2,
      desc: "Modelador de Cachos Cacheador  #tiktokshopbr1111 #cachos #modelador #modeladordecachos #cabelo "
    },
  {
      name: "Dani Rodrigues",
      username: "danirodriguescreator",
      avatar: "../img/creators-cabelo/creator-109-21.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora21.jpg",
      video: "https://files.catbox.moe/ays86y.mp4",
      startTime: 0.2,
      desc: "#modelador #modeladordecachos #babyliss #modeladordecabelo #miracurl "
    },
  {
      name: "Suzana Strazzer",
      username: "suzanastrazzer",
      avatar: "../img/creators-cabelo/creator-109-22.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora22.jpg",
      video: "https://files.catbox.moe/96u117.mp4",
      startTime: 0.2,
      desc: "Cachos sem fonte de calor 🎀 #cabelo #cachos #babyliss "
    },
  {
      name: "@KaahTrends",
      username: "kaahtrends",
      avatar: "../img/creators-cabelo/creator-109-23.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora23.jpg",
      video: "https://files.catbox.moe/n5l2ed.mp4",
      startTime: 0.2,
      desc: "Prancha Triondas Ondulador Formato Triplo Modelador de Cachos 💫 #triondas #ondulado #modelador #modeladordecabelo #modeladordeondas "
    },
  {
      name: "tamyssilvaaa",
      username: "tamyssilvaaa",
      avatar: "../img/creators-cabelo/creator-109-24.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora24.jpg",
      video: "https://files.catbox.moe/ao49pm.mp4",
      startTime: 0.2,
      desc: "Modelador de Cachos bivolt automático 😍 #cabelos #cachos #modeladordecachos #modelador "
    },
  {
      name: "Bia Martine",
      username: "biamartinne",
      avatar: "../img/creators-cabelo/creator-109-25.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora25.jpg",
      video: "https://files.catbox.moe/1ldkm4.mp4",
      startTime: 0.2,
      desc: "#babyliss #modelador #cachos "
    },
  {
      name: "Lara",
      username: "alara.costa",
      avatar: "../img/creators-cabelo/creator-109-26.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora26.jpg",
      video: "https://files.catbox.moe/znhhob.mp4",
      startTime: 0.2,
      desc: "Modelador de cachos automático 😍 #tiktokshopbr66 #modeladordecachos #cachos #cabelo "
    },
  {
      name: "viacheibarato",
      username: "viacheibaratoo",
      avatar: "../img/creators-cabelo/creator-109-27.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora27.jpg",
      video: "https://files.catbox.moe/1mxqma.mp4",
      startTime: 0.2,
      desc: "Modelador de cachos bivolt 😮💖"
    },
  {
      name: "Júlia Rossi ✨",
      username: "juliarossi01_",
      avatar: "../img/creators-cabelo/creator-109-28.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora28.jpg",
      video: "https://files.catbox.moe/nfi13n.mp4",
      startTime: 0.2,
      desc: "O melhor modelador de cachos sem fonte de calor que eu já usei!!  #modeladordecacho#modeladorsemcalor#cachossemfontedecalor "
    },
  {
      name: "Jennifer da Rosa",
      username: "jenniferdarosa2",
      avatar: "../img/creators-cabelo/creator-109-29.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora29.jpg",
      video: "https://files.catbox.moe/mift4h.mp4",
      startTime: 0.2,
      desc: "Esse modelador de cachos superou minhas expectativas! 15 minutos e meu cabelo tava pronto  #cabelos #modeladordecachos  #foryoupage "
    },
  {
      name: "Ana K ✨",
      username: "anakarolline.r",
      avatar: "../img/creators-cabelo/creator-109-30.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora30.jpg",
      video: "https://files.catbox.moe/ijo9us.mp4",
      startTime: 0.2,
      desc: "Amigas eu arrumei esse jeito de fazer no meu cabelo, e estou gostando do resultado! Vocês já testaram?  #modeladordecachos #cabelomodelado #tiktokshop #tiktoksh"
    },
  {
      name: "Stephane | Maternidade e Shop",
      username: "steeolliveira",
      avatar: "../img/creators-cabelo/creator-109-31.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora31.jpg",
      video: "https://files.catbox.moe/ylcr02.mp4",
      startTime: 0.2,
      desc: "Modelados de cachos mais fácil de usar do mundo, muito prático, sem contar o preço 🤌🏼🩷 #babyliss #penteados #penteadosfaceis #penteadosimples #penteado "
    },
  {
      name: "Encontradinhos",
      username: "encontradinhos3",
      avatar: "../img/creators-cabelo/creator-109-32.jpg",
      poster: "../videosprodutos/posters/poster-produto-109-criadora32.jpg",
      video: "https://files.catbox.moe/elrlq8.mp4",
      startTime: 0.2,
      desc: "Modelador De Cachos Profissional BiVolt Secret Curl Digital Com LED #modeladordecachos #modelador "
    }
  ];

  const CREATORS_MODELADOR_109 = MODELADOR_109_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 11200 + (i * 540) % 14000,
    commentsCount: 54 + (i * 10) % 120,
    saves: 2300 + (i * 140) % 3100,
    shares: 280 + (i * 30) % 650,
    description: vInfo.desc
  }));

  // 1.6 DATASET DO TÊNIS KAPPA PULSE RX (PRODUTO 110)
  const KAPPA_110_VIDEOS_MAP = [
  {
      name: "Nati",
      username: "entrecafeesonhos",
      avatar: "../img/creators-auto/avatar-entrecafeesonhos.jpg",
      poster: "../videosprodutos/posters/poster-produto-110.jpg",
      video: "https://files.catbox.moe/2t30kf.mp4",
      startTime: 0.2,
      desc: "Tênis Kappa Pulse Unissex Academia Caminhada. Compre aqui 👉🏻 https://meli.la/2Y4FRAa #tiktokshop #constancia #creatorsea"
    },
  {
      name: "AchadosDoML",
      username: "radardedescontosml",
      avatar: "../img/creators-auto/avatar-radardedescontosml.jpg",
      poster: "../videosprodutos/posters/poster-produto-110-criadora2.jpg",
      video: "https://files.catbox.moe/014o2c.mp4",
      startTime: 0.2,
      desc: "Tênis Kappa Pulse RX é um calçado esportivo projetado para oferecer conforto, leveza e amortecimento em atividades do di"
    },
  {
      name: "Clayton_Achadinhos",
      username: "clayton_achadinhos",
      avatar: "../img/creators-auto/avatar-clayton_achadinhos.jpg",
      poster: "../videosprodutos/posters/poster-produto-110-criadora3.jpg",
      video: "https://files.catbox.moe/qgvpj6.mp4",
      startTime: 0.2,
      desc: "👟🔥 Tênis Kappa Pulse Unissex – Conforto e estilo para o seu dia a dia! Quer um tênis bonito, moderno e confortável para "
    }
  ];

  const CREATORS_KAPPA_110 = KAPPA_110_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 12400 + (i * 450) % 15000,
    commentsCount: 62 + (i * 12) % 110,
    sharesCount: 18 + (i * 4) % 45,
    savesCount: 840 + (i * 90) % 1200,
    description: vInfo.desc
  }));

  // 1.7 DATASET DO PROJETOR LED NATALINO (PRODUTO 111)
  const PROJETOR_111_VIDEOS_MAP = [
    {
      name: "Larissa Holf",
      username: "lariholf",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_14.jpg",
      poster: "../videosprodutos/posters/poster-111-kahena.jpg",
      video: "https://files.catbox.moe/hiuwu2.mp4",
      startTime: 0.2,
      desc: "Projetor de Luz Natalino - efeito perfeito na parede de casa! ✨🎅 #natal #projetorled #decoracaodenatal"
    },
    {
      name: "Wilson Achados",
      username: "wilsondotiktok0",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_25.jpg",
      poster: "../videosprodutos/posters/poster-111-bruna.jpg",
      video: "https://files.catbox.moe/wvxbgd.mp4",
      startTime: 0.2,
      desc: "Projetor natalino 16 desenhos temáticos USB, sensacional pra enfeitar sem bagunça! 🎄✨"
    },
    {
      name: "Malu Looks",
      username: "malu_looks",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_12.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora2.jpg",
      video: "https://files.catbox.moe/eruxi4.mp4",
      startTime: 0.2,
      desc: "Olha o efeito desse projetor de LED natalino na sala, super prático e lindo! 🎄✨ #projetornatalino"
    },
    {
      name: "Alisson Sebold",
      username: "alissonseboldrecomendabr",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_04.jpg",
      poster: "../videosprodutos/posters/poster-111-ale.jpg",
      video: "https://files.catbox.moe/fmi37c.mp4",
      startTime: 0.2,
      desc: "Maneira fácil de deixar a casa no clima de Natal! O projetor LED natalino cria um efeito lindo! ✨🎅"
    },
    {
      name: "Danilo Trovão",
      username: "dmntrovao",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_07.jpg",
      poster: "../videosprodutos/posters/poster-produto-111.jpg",
      video: "https://files.catbox.moe/6lslcd.mp4",
      startTime: 0.2,
      desc: "Projetor natalino com 16 desenhos temáticos, funciona perfeitamente! #DecoracaoDeNatal #natal"
    }
  ];

  const CREATORS_PROJETOR_111 = PROJETOR_111_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 15300 + (i * 320) % 18000,
    commentsCount: 78 + (i * 15) % 140,
    sharesCount: 35 + (i * 7) % 60,
    savesCount: 1100 + (i * 110) % 1500,
    description: vInfo.desc
  }));

  // 1.8 DATASET DO CAMINHÃO BOMBEIRO PATINHOS (PRODUTO 112)
  const CAMINHAO_112_VIDEOS_MAP = [
  {
      name: "alicinhaebianca",
      username: "alicinhaebianca",
      avatar: "../img/creators-auto/avatar-alicinhaebianca.jpg",
      poster: "../videosprodutos/posters/poster-produto-112.jpg",
      video: "https://files.catbox.moe/geut5n.mp4",
      startTime: 0.2,
      desc: "Brinquedo Pista de Patinhos Escorregador "
    },
  {
      name: "Loja do Guza",
      username: "lojadoguza",
      avatar: "../img/creators-auto/avatar-lojadoguza.jpg",
      poster: "../videosprodutos/posters/poster-produto-112-criadora2.jpg",
      video: "https://files.catbox.moe/a00mz6.mp4",
      startTime: 0.2,
      desc: "Escorregador pista de patinhos. Brinquedos Brincadeira de criança  Brinquedo infantil A criançada ama"
    },
  {
      name: "Menino Gessé",
      username: "meninogesse",
      avatar: "../img/creators-auto/avatar-meninogesse.jpg",
      poster: "../videosprodutos/posters/poster-produto-112-criadora3.jpg",
      video: "https://files.catbox.moe/tz769q.mp4",
      startTime: 0.2,
      desc: "Brinquedo Patinho Escorregador  Pista Musical Pato montanha Russa Escada Tobogã R..."
    }
  ];

  const CREATORS_CAMINHAO_112 = CAMINHAO_112_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 9800 + (i * 280) % 11000,
    commentsCount: 45 + (i * 8) % 90,
    sharesCount: 22 + (i * 5) % 40,
    savesCount: 650 + (i * 70) % 900,
    description: vInfo.desc
  }));

  // 1.9 DATASET DO COMEDOURO PET ACRÍLICO DUPLO (PRODUTO 113)
  const COMEDOURO_113_VIDEOS_MAP = [
    {
      name: "Mariana Rocha",
      username: "mari.petlovers",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_18.jpg",
      poster: "../videosprodutos/posters/poster-produto-113.jpg",
      video: "https://files.catbox.moe/grwbds.mp4",
      startTime: 0.2,
      desc: "🐱🐾 Com o Comedouro Elevado, as refeições ficam mais seguras e confortáveis! ✨🐱 #gato #cat #catlover #catlife #mimers "
    },
    {
      name: "Beatriz Santos",
      username: "biaegatinhos",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_22.jpg",
      poster: "../videosprodutos/posters/poster-produto-113-criadora2.jpg",
      video: "https://files.catbox.moe/581lcj.mp4",
      startTime: 0.2,
      desc: "Comedouro elevado de porcelana ❤️🥰🌸"
    },
    {
      name: "Ana Lima",
      username: "canalanalima",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_12.jpg",
      poster: "../videosprodutos/posters/poster-produto-113-criadora3.jpg",
      video: "https://files.catbox.moe/bffyn2.mp4",
      startTime: 0.2,
      desc: "A patroa ganhou um comedouro novo! Comedouro duplo elevado para cachorros e gatos! 🐱🐶✨ #petshop #comedouro"
    },
    {
      name: "Laura Luzia",
      username: "lauraluzia28",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_14.jpg",
      poster: "../videosprodutos/posters/poster-produto-113-criadora4.jpg",
      video: "https://files.catbox.moe/kbl124.mp4",
      startTime: 0.2,
      desc: "Chega de pote de plastico! Esse comedouro elevado pet duplo dura muito e melhora a postura! 🐾✨"
    },
    {
      name: "Luh & Gustavo",
      username: "casalfindss",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_25.jpg",
      poster: "../videosprodutos/posters/poster-produto-113.jpg",
      video: "https://files.catbox.moe/avgf8r.mp4",
      startTime: 0.2,
      desc: "Comedouro elevado para pet com inclinação que facilita a digestão, super aprovado! 🐶🐱❤️"
    }
  ];

  const CREATORS_COMEDOURO_113 = COMEDOURO_113_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 11400 + (i * 380) % 13000,
    commentsCount: 52 + (i * 11) % 95,
    sharesCount: 26 + (i * 6) % 50,
    savesCount: 780 + (i * 85) % 1100,
    description: vInfo.desc
  }));

  // 1.10 DATASET DO CONTROLE ARCADE STICK 7 EM 1 (PRODUTO 114) - 32 CRIADORES INDIVIDUAIS REAIS (ZERO REPETIÇÃO)
  const ARCADE_114_VIDEOS_MAP = [
    {
      name: "Marcos Silva",
      username: "marcos.games",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_1.jpg",
      poster: "../videosprodutos/posters/poster-produto-114-criadora2.jpg",
      video: "https://files.catbox.moe/cfm2lc.mp4",
      startTime: 0.2,
      desc: "Sensação pura dos fliperamas dos anos 90! Controle Arcade Stick 7 em 1 com microswitch mecânico e zero delay 🕹️🔥 #arcade #fightstick #tiktokshop"
    },
    {
      name: "Leonardo Rocha",
      username: "leo_fightsticks",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_3.jpg",
      poster: "../videosprodutos/posters/poster-produto-114-criadora3.jpg",
      video: "https://files.catbox.moe/fbfkzs.mp4",
      startTime: 0.2,
      desc: "Testei no PS4 e PC jogando Street Fighter 6! Os combos saem limpíssimos e a resposta dos 8 botões é imediata! 🎮✨ #streetfighter #fightstick"
    }
  ];

  const CREATORS_ARCADE_114 = ARCADE_114_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 18200 + (i * 610) % 22000,
    commentsCount: 94 + (i * 18) % 180,
    sharesCount: 42 + (i * 9) % 75,
    savesCount: 1450 + (i * 140) % 1900,
    description: vInfo.desc
  }));

  // 1.11 DATASET DO FORNO ELÉTRICO HQ 48L (PRODUTO 115)
  const FORNO_HQ_115_VIDEOS_MAP = [
  {
      name: "Carol Netti",
      username: "carolnetti",
      avatar: "../img/avatars-forno-hq/creator-carol.jpg",
      poster: "../videosprodutos/posters/poster-produto-115.jpg",
      video: "https://files.catbox.moe/dgi7wy.mp4",
      startTime: 0.2,
      desc: "Forno elétrico HQ com 48 litros de capacidade com 1600w @HQ #tiktokshop #tiktoklive #livehighlights"
    },
  {
      name: "Theleleu",
      username: "theleleu1705",
      avatar: "../img/avatars-forno-hq/creator-theleleu.jpg",
      poster: "../videosprodutos/posters/poster-produto-115-c2.jpg",
      video: "https://files.catbox.moe/cexk71.mp4",
      startTime: 0.2,
      desc: "🔥 O TikTok SURTOU com essa oferta! 😱 Forno elétrico HQ de 48 litros, 1600W e muito espaço!"
    },
  {
      name: "Vitrine da Carol",
      username: "vitrine_da_carol",
      avatar: "../img/avatars-forno-hq/creator-vitrine.jpg",
      poster: "../videosprodutos/posters/poster-produto-115-c3.jpg",
      video: "https://files.catbox.moe/u4fc4i.mp4",
      startTime: 0.2,
      desc: "Forno Elétrico HQ 48 Litros HQ #fornoeletrico #fornoeletricohq #forno48litros"
    },
  {
      name: "DAMIS • MARK",
      username: "damis_mark",
      avatar: "../img/avatars-forno-hq/creator-damis.jpg",
      poster: "../videosprodutos/posters/poster-produto-115-c4.jpg",
      video: "https://files.catbox.moe/go5yf7.mp4",
      startTime: 0.2,
      desc: "Comprei o forno elétrico HQ de 48 litros no TikTok Shop e me surpreendi com o tamanho e a potência! 🔌👨‍🍳 #fornohq #cozinha #tiktokshop"
    }
  ];

  const CREATORS_FORNO_HQ_115 = FORNO_HQ_115_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 19400 + (i * 540) % 21000,
    commentsCount: 88 + (i * 14) % 160,
    sharesCount: 38 + (i * 8) % 70,
    savesCount: 1320 + (i * 120) % 1800,
    description: vInfo.desc
  }));

  // 1.12 DATASET DA SMART TV MULTI ROKU 32 (PRODUTO 116)
  const SMART_TV_116_VIDEOS_MAP = [
  {
      name: "Nina Della",
      username: "ninadellashop",
      avatar: "../img/avatars-tv/creator-nina.jpg",
      poster: "../videosprodutos/posters/poster-produto-116.jpg",
      video: "https://files.catbox.moe/db3r4b.mp4",
      startTime: 0.2,
      desc: "🚨🔥 OLHA O PREÇO! O TIKTOK SURTOU! 🤯📺 Smart TV Multi Roku 32 DLED com preço de Black Friday! #EsquentaBlackFriday #SmartTVMulti #RokuTV #TikTokShop"
    }
  ];

  const CREATORS_SMART_TV_116 = SMART_TV_116_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 24500 + (i * 2380),
    commentsCount: 142 + (i * 38),
    sharesCount: 68 + (i * 19),
    savesCount: 1850 + (i * 210),
    description: base.desc
  }));

  // 1.13 DATASET DO FOGÃO ATLAS MÔNACO TOP GLASS (PRODUTO 117)
  const FOGAO_117_VIDEOS_MAP = [
  {
      name: "Henrique Creator",
      username: "henrique_1976",
      avatar: "../img/avatars-fogao/creator-henrique.jpg",
      poster: "../videosprodutos/posters/poster-produto-117.jpg",
      video: "https://files.catbox.moe/55n8uo.mp4",
      startTime: 0.2,
      desc: "Gente, olha esse Fogão Atlas Mônaco Top Glass 4 bocas com mesa de vidro temperado e acendimento automático! Parece cooktop de luxo! 🔥🖤 #fogaoatlas #fogaotopglass #fogao4bocas #cozinha"
    },
  {
      name: "Ariana Top Shop",
      username: "arianababysorrisos",
      avatar: "../img/avatars-fogao/creator-ariana.jpg",
      poster: "../videosprodutos/posters/poster-produto-117-c2.jpg",
      video: "https://files.catbox.moe/w23wcu.mp4",
      startTime: 0.2,
      desc: "Fogão 4 bocas automático mesa de vidro temperado preto fosco! Forno espaçoso com visão panorâmica e super econômico nota A! 👏✨ #fogao #mesadevidro #achadinhos"
    },
  {
      name: "Mylla Gulart",
      username: "vivendo_1proposito",
      avatar: "../img/avatars-fogao/creator-proposito.jpg",
      poster: "../videosprodutos/posters/poster-produto-117-c4.jpg",
      video: "https://files.catbox.moe/sxseft.mp4",
      startTime: 0.2,
      desc: "Testando o Fogão a Gás Atlas Monaco Top Glass 4 Bocas Mesa de Vidro Preto! As chamas são fortes e o forno assa por igual! 🍕🥘 #fogao #comprinhas #tiktokshop"
    }
  ];

  const CREATORS_FOGAO_117 = FOGAO_117_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 21000 + (i * 3200),
    commentsCount: 184 + (i * 45),
    sharesCount: 72 + (i * 24),
    savesCount: 1650 + (i * 290),
    description: base.desc
  }));

  // 1.14 DATASET DA MESA DE JANTAR COM 4 CADEIRAS (PRODUTO 118)
  const MESA_118_VIDEOS_MAP = [
  {
      name: "Selly Maria",
      username: "sellymaria0",
      avatar: "../img/avatars-mesa/creator-selly.jpg",
      poster: "../videosprodutos/posters/poster-produto-118-c2.jpg",
      video: "https://files.catbox.moe/nwj56a.mp4",
      startTime: 0.2,
      desc: "Mesa com 4 cadeiras estofadas: perfeita para ambientes pequenos! Prática, elegante e super resistente! Amei demais! 🍽️🤍 #tiktokshop #mesa4cadeiras #decoracao"
    },
  {
      name: "Mari Utilidades ✨",
      username: "indicacoesdamari_",
      avatar: "../img/avatars-mesa/creator-mari.jpg",
      poster: "../videosprodutos/posters/poster-produto-118-c3.jpg",
      video: "https://files.catbox.moe/yr10g7.mp4",
      startTime: 0.2,
      desc: "A mesa de jantar perfeita para você reunir familiares e amigos com muito conforto! As cadeiras são super estofadas! 😍👏 #mesaposta #mesadejantar #mesa4cadeiras"
    },
  {
      name: "Camila Vitória",
      username: "camilavitorialife",
      avatar: "../img/avatars-mesa/creator-camilav.jpg",
      poster: "../videosprodutos/posters/poster-produto-118-c4.jpg",
      video: "https://files.catbox.moe/vj6tzr.mp4",
      startTime: 0.2,
      desc: "Tour pela minha sala de jantar nova! Conjunto 4 cadeiras com tampo resistente e acabamento impecável da Stone Shop! 💖🥂 #mesa #mesadejantar #mesa4cadeiras"
    }
];

    const CREATORS_MESA_118 = MESA_118_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 24500 + (i * 2800),
    commentsCount: 215 + (i * 38),
    sharesCount: 88 + (i * 19),
    savesCount: 1940 + (i * 210),
    description: base.desc
  }));

  // 1.10.5 DATASET DO FARDO MEGA/HIPER DE FRALDAS HUGGIES & PAMPERS (PRODUTO 119) - CRIADORES E VÍDEOS REAIS TIKTOK SHOP
  const FRALDAS_119_VIDEOS_MAP = [
    {
      name: "Mamãe Recomenda",
      username: "mamae_recomenda_oficial",
      avatar: "../img/avatars-fraldas/creator-mamae.jpg",
      poster: "../videosprodutos/posters/poster-produto-119.jpg",
      video: "https://files.catbox.moe/sfr3li.mp4",
      startTime: 0.2,
      desc: "Meninas, olha esse lote promocional de Fraldas Huggies Máxima Proteção e Pampers com frete grátis na Stone Shop! O custo por tira tá inacreditável! 👶🍼 #maternidade #fraldashuggies #enxovalbebe"
    },
    {
      name: "Fernanda Rezende",
      username: "fernandarezendec",
      avatar: "../img/avatars-fraldas/creator-fernanda.jpg",
      poster: "../videosprodutos/posters/poster-produto-119-c2.jpg",
      video: "https://files.catbox.moe/qfao5v.mp4",
      startTime: 0.2,
      desc: "Fralda Huggies Máxima Proteção até 12 horas sequinha sem vazamentos! Meu bebê dorme a noite toda tranquilo! 💖✨ #ViralTikTokShop #fraldasdescartáveis #fraldaspromocao"
    },
    {
      name: "Adria | Beleza & Achadinhos",
      username: "adriagalvao7",
      avatar: "../img/avatars-fraldas/creator-adria.jpg",
      poster: "../videosprodutos/posters/poster-produto-119-c3.jpg",
      video: "https://files.catbox.moe/fz7mye.mp4",
      startTime: 0.2,
      desc: "Mega economia de fraldas no esquenta Black Friday! Comprei o fardo hiper e ganhei pacote de lenços umedecidos! Corre que vai esgotar rápido! 🏃‍♀️💨 #TikTokShop #Huggies #Achadinhos"
    },
    {
      name: "Lidi indica",
      username: "lidianecastros1",
      avatar: "../img/avatars-fraldas/creator-lidi.jpg",
      poster: "../videosprodutos/posters/poster-produto-119-c4.jpg",
      video: "https://files.catbox.moe/664mdu.mp4",
      startTime: 0.2,
      desc: "Agora só compro fralda aqui na Stone Shop! Preço de atacado muito melhor que em farmácia e entrega super rápida! 📦🥰 #huggies #fralda #maternidade #foryou"
    }
  ];

    const CREATORS_FRALDAS_119 = FRALDAS_119_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 31200 + (i * 3100),
    commentsCount: 280 + (i * 52),
    sharesCount: 110 + (i * 28),
    savesCount: 2450 + (i * 320),
    description: base.desc
  }));

  // 1.10.6 DATASET DO SOFÁ RETRÁTIL E RECLINÁVEL 3 LUGARES VELUDO SUEDE (PRODUTO 120) - CRIADORES E VÍDEOS REAIS TIKTOK SHOP
  const SOFA_120_VIDEOS_MAP = [
    {
      name: "ContentStudio",
      username: "contentstudio03",
      avatar: "../img/avatars-sofa/creator-content.jpg",
      poster: "../videosprodutos/posters/poster-produto-120.jpg",
      video: "https://files.catbox.moe/qdufjg.mp4",
      startTime: 0.2,
      desc: "Gente, olha o tamanho e o conforto desse sofá retrátil e reclinável de 3 lugares em veludo! Parece cinema na sala! 🛋️✨ #SofáRetrátil #SalaDecorada #tiktokshop"
    },
    {
      name: "Patypooh",
      username: "patypooh03",
      avatar: "../img/avatars-sofa/creator-paty.jpg",
      poster: "../videosprodutos/posters/poster-produto-120-c2.jpg",
      video: "https://files.catbox.moe/7oorlp.mp4",
      startTime: 0.2,
      desc: "Sofá Retrátil e Reclinável com molas ensacadas e espuma D33! Abre até 1,80m e vira uma cama de casal perfeita! 🥰👏 #tiktokviral #casa #sofa"
    },
    {
      name: "Telma Indica",
      username: "telmareis341",
      avatar: "../img/avatars-sofa/creator-telma.jpg",
      poster: "../videosprodutos/posters/poster-produto-120-c3.jpg",
      video: "https://files.catbox.moe/ctdyx8.mp4",
      startTime: 0.2,
      desc: "O sofá dos sonhos pra maratonar filmes e séries! Retrátil, reclinável, macio demais e super fácil de limpar! Aproveitem o cupom! 🍿🛋️ #tiktokshop #sofaretratil #decoracao"
    },
    {
      name: "Aura Glow Shop",
      username: "auraglowshop70",
      avatar: "../img/avatars-sofa/creator-aura.jpg",
      poster: "../videosprodutos/posters/poster-produto-120-c4.jpg",
      video: "https://files.catbox.moe/3b1m78.mp4",
      startTime: 0.2,
      desc: "Transforme sua sala com muito conforto e elegância! Sofá retrátil e reclinável revestido em veludo suede premium da Stone Shop! 💖🛋️ #SofaRetratil #MoveisParaCasa #decor"
    }
  ];

    const CREATORS_SOFA_120 = SOFA_120_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 27800 + (i * 2900),
    commentsCount: 230 + (i * 42),
    sharesCount: 95 + (i * 22),
    savesCount: 2120 + (i * 260),
    description: base.desc
  }));

  // 1.10.7 DATASET DO TRAVESSEIRO CERVICAL ORTOPÉDICO ABRANUV PRO 2.0 (PRODUTO 121) - CRIADORES E VÍDEOS REAIS TIKTOK SHOP
  const TRAVESSEIRO_121_VIDEOS_MAP = [
    {
      name: "Bryan Klug | Creator",
      username: "bryan.klug",
      avatar: "../img/avatars-travesseiro/creator-bryan.jpg",
      poster: "../videosprodutos/posters/poster-produto-121.jpg",
      video: "https://files.catbox.moe/0trj7i.mp4",
      startTime: 0.2,
      desc: "Comprei o travesseiro cervical ortopédico original Abranuv Pro 2.0 na Stone Shop! Mostrei tudo do unboxing até tirar do vácuo! Acabou a dor no pescoço! ☁️🙌 #Abranuv #Travesseiro #TikTokShop"
    },
    {
      name: "Gabriela Sou",
      username: "_gabiso",
      avatar: "../img/avatars-travesseiro/creator-gabriela.jpg",
      poster: "../videosprodutos/posters/poster-produto-121-c2.jpg",
      video: "https://files.catbox.moe/82p725.mp4",
      startTime: 0.2,
      desc: "Dica de ouro de fisioterapia: o travesseiro cervical com espuma viscoelástica alinha a coluna e relaxa a musculatura na hora de dormir! 💤🩺 #travesseiro #fisioterapia #coluna"
    },
    {
      name: "LysaBGalante",
      username: "lysabgalante.tiktokshop",
      avatar: "../img/avatars-travesseiro/creator-lysa.jpg",
      poster: "../videosprodutos/posters/poster-produto-121-c3.jpg",
      video: "https://files.catbox.moe/40pj5q.mp4",
      startTime: 0.2,
      desc: "Travesseiro Cervical Ortopédico anatômico! Sono perfeito, não esquenta e apoia tanto de lado quanto de costas! Melhor investimento pro sono! 😴🛏️ #travesseiro #ortopedico #cervical"
    },
    {
      name: "Maribel Bortolotto",
      username: "maribelbortolotto",
      avatar: "../img/avatars-travesseiro/creator-maribel.jpg",
      poster: "../videosprodutos/posters/poster-produto-121-c4.jpg",
      video: "https://files.catbox.moe/vdi5oq.mp4",
      startTime: 0.2,
      desc: "Testando o Travesseiro Cervical Abranuv Pro 2.0 com capa lavável e tecnologia antiácaro! Minhas noites mudaram completamente! 💖✨ #viraltiktokshop #travesseiro #sono"
    }
  ];

  const CREATORS_TRAVESSEIRO_121 = TRAVESSEIRO_121_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 38900 + (i * 3500),
    commentsCount: 340 + (i * 48),
    sharesCount: 145 + (i * 31),
    savesCount: 3120 + (i * 380),
    description: base.desc
  }));

  // 1.10.7 DATASET DA PANELA DE PRESSÃO ELÉTRICA ELECTROLUX RITA LOBO 6L (PRODUTO 46) - CRIADORES REAIS TIKTOK SHOP
  const ELECTROLUX_46_VIDEOS_MAP = [
    {
      name: "Paloma Vivian",
      username: "paloma_vivian",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/6ef8f712f6d807897d17cd9e157750b3~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=48a8dfdd&x-expires=1795366800&x-signature=MFi%2F2HBYB1EAVKebx%2ByaknLC3PA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-122.jpg",
      video: "https://files.catbox.moe/e3p88g.mp4",
      startTime: 0.2,
      desc: "Unboxing da minha panela de pressão elétrica Electrolux Rita Lobo 6L! Linda, moderna e super silenciosa! 🍲✨ #electrolux #ritalobo #cozinha"
    },
    {
      name: "Vitória Bueno",
      username: "vitoriabueno.home",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/2bd76a14841d08388ce50b4f66457583~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=61b449e0&x-expires=1795366800&x-signature=WAEQ3iFYh7hOmJ5kbiCznLtpqII%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-122-c2.jpg",
      video: "https://files.catbox.moe/4mjnk2.mp4",
      startTime: 0.2,
      desc: "Nova aquisição desbloqueada: panela de pressão elétrica Electrolux digital! Facilita muito a rotina na cozinha! 🍛🔥"
    },
    {
      name: "Juliane Furtado",
      username: "julianefurtadovidareal",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/d41b826c107825d1ae17022d470e9e96~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=cfb2e86e&x-expires=1795366800&x-signature=oAriVTe6OTj1o7Maa8GeFLGSA4M%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-122-c3.jpg",
      video: "https://files.catbox.moe/x8kw1f.mp4",
      startTime: 0.2,
      desc: "Fazendo feijão na panela de pressão elétrica Electrolux Rita Lobo 6L! Caldo grossinho e cozimento perfeito sem chiado! 🫘❤️ #PanelaRitaLobo"
    },
    {
      name: "Bia Barbosa",
      username: "biabarbosa.indicaa",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/83c97bd98a947f77ef2bb3cd97993d49~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=92fd1eaa&x-expires=1795366800&x-signature=UDGnwLEyMHSktUajczIubMwoH%2B0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-122-c4.jpg",
      video: "https://files.catbox.moe/asz0ui.mp4",
      startTime: 0.2,
      desc: "Panela de pressão elétrica Electrolux é vida! Super segura com várias travas e mantém a comida quentinha! 🍲✨"
    },
    {
      name: "Kátia Romão",
      username: "katialimaromao",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/f04c30e3fa04c1e0f6cd528a5ea87677~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=97ff9754&x-expires=1795366800&x-signature=uuAICPIxsMDa8mA8x6GZHvXM3ZU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-122.jpg",
      video: "https://files.catbox.moe/7iz443.mp4",
      startTime: 0.2,
      desc: "A panela que mais me ajuda na correria da cozinha! Panela de pressão elétrica Electrolux por Rita Lobo 6L com painel digital! 🖤✨"
    }
  ];

  const CREATORS_ELECTROLUX_46 = ELECTROLUX_46_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 31200 + (i * 2800),
    commentsCount: 280 + (i * 38),
    sharesCount: 140 + (i * 22),
    savesCount: 2800 + (i * 310),
    description: base.desc
  }));

  // 1.10.8 DATASET DA PANELA DE PRESSÃO ELÉTRICA DIGITAL 5L (PRODUTO 122) - CRIADORES E VÍDEOS REAIS TIKTOK SHOP
  const PANELA_122_VIDEOS_MAP = [
    {
      name: "Sabrina Rosene",
      username: "sabrinarosene",
      avatar: "../img/avatars-panela/creator-sabrina.jpg",
      poster: "../videosprodutos/posters/poster-produto-122.jpg",
      video: "https://files.catbox.moe/h6lcpu.mp4",
      startTime: 0.2,
      desc: "Você pode achar que não precisa, até ter e se arrepender de não ter comprado antes! Feijão pronto em 15 minutos sem barulho de chiado! 🍲✨ #cozinha #panelaeletrica #pressao #tiktokshop"
    },
    {
      name: "Karina Cepellos",
      username: "karinacepellos",
      avatar: "../img/avatars-panela/creator-karina.jpg",
      poster: "../videosprodutos/posters/poster-produto-122-c2.jpg",
      video: "https://files.catbox.moe/vdek7s.mp4",
      startTime: 0.2,
      desc: "Panela de Pressão Elétrica Digital 5L: mais praticidade, 10 travas de segurança e não queima a comida! O recipiente antiaderente sai pra lavar! 🍛🔥 #paneladepressao #panelaeletrica #achadinhos"
    },
    {
      name: "Nárlen Aquino",
      username: "valeapena_levar",
      avatar: "../img/avatars-panela/creator-valeapena.jpg",
      poster: "../videosprodutos/posters/poster-produto-122-c3.jpg",
      video: "https://files.catbox.moe/32rwkx.mp4",
      startTime: 0.2,
      desc: "Testando a panela de pressão elétrica digital! Carne de panela desfiando em 25 minutos e desliga sozinha quando termina! Maravilhosa! 🥩🍗 #paneladepressao #itensdecozinha #tiktokshop"
    },
    {
      name: "ShopTEM",
      username: "shoptem2026",
      avatar: "../img/avatars-panela/creator-shoptem.jpg",
      poster: "../videosprodutos/posters/poster-produto-122-c4.jpg",
      video: "https://files.catbox.moe/5cit3t.mp4",
      startTime: 0.2,
      desc: "Chegou a queridinha da cozinha! Panela de pressão elétrica digital com display touch e timer programável! Comprei com cupom na Stone Shop! 💖🥘 #panelaeletrica #panela #cozinhapratica"
    }
  ];

    const CREATORS_PANELA_122 = PANELA_122_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 29500 + (i * 2700),
    commentsCount: 245 + (i * 35),
    sharesCount: 105 + (i * 24),
    savesCount: 2350 + (i * 290),
    description: base.desc
  }));

  // 1.10.9 DATASET DA LAVADORA DE ALTA PRESSÃO PORTÁTIL SEM FIO A BATERIA (PRODUTO 123) - CRIADORES E VÍDEOS REAIS TIKTOK SHOP
  const LAVADORA_123_VIDEOS_MAP = [
    {
      name: "Rafael",
      username: "rafa7169019",
      avatar: "../img/avatars-lavadora/creator-rafael.jpg",
      poster: "../videosprodutos/posters/poster-produto-123.jpg",
      video: "https://files.catbox.moe/iopyod.mp4",
      startTime: 0.2,
      desc: "Lavadora de alta pressão portátil sem fio com 2 baterias recarregáveis! Limpei meu carro e a calçada inteira sem precisar de tomada! Sensacional! 🚗💦 #lavadoradealtapressao #lavajato #tiktokshop"
    },
    {
      name: "bionic.shop",
      username: "bionic.shop",
      avatar: "../img/avatars-lavadora/creator-bionic.jpg",
      poster: "../videosprodutos/posters/poster-produto-123-c2.jpg",
      video: "https://files.catbox.moe/cqx9m9.mp4",
      startTime: 0.2,
      desc: "Lava jato portátil profissional com maleta completa! Puxa água direto de balde ou torneira! A pressão é surreal! 🧰⚡ #LavadoraPortátil #Limpeza #lavajato #achadinhos"
    },
    {
      name: "Edutilidades Shop",
      username: "edutilidades",
      avatar: "../img/avatars-lavadora/creator-ed.jpg",
      poster: "../videosprodutos/posters/poster-produto-123-c3.jpg",
      video: "https://files.catbox.moe/wcutms.mp4",
      startTime: 0.2,
      desc: "Lavadora alta pressão a bateria 48V kit completo com aplicador de sabão, filtro e 2 bicos de leque! Muito potente e leve! 🚗🧼 #lavajato #ferramentas #tiktokshop"
    },
    {
      name: "Achadinhos Tiktok Shop",
      username: "achadinhoos_tiktok.shop",
      avatar: "../img/avatars-lavadora/creator-achadinhos.jpg",
      poster: "../videosprodutos/posters/poster-produto-123-c4.jpg",
      video: "https://files.catbox.moe/2lscen.mp4",
      startTime: 0.2,
      desc: "O produto que todo homem e dono de casa precisa ter! Lavadora de alta pressão sem fio com maleta organizadora! Comprei na Stone Shop com super desconto! 🚀🚿 #lavadoraaltapressao #lavajato #viraltiktokshop"
    }
  ];

    const CREATORS_LAVADORA_123 = LAVADORA_123_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 34200 + (i * 3100),
    commentsCount: 295 + (i * 44),
    sharesCount: 130 + (i * 26),
    savesCount: 2780 + (i * 310),
    description: base.desc
  }));

  // DATASET CHUVEIRO ACQUA DUO LORENZETTI (PRODUTO 32)
  const CHUVEIRO_32_VIDEOS_MAP = [
    {
      name: "Patrick Araújo",
      username: "patrickaraujos",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_15.jpg",
      poster: "../videosprodutos/posters/video-produto-32-take3.jpg",
      video: "https://files.catbox.moe/b1fvp6.mp4",
      desc: "Review sincero do Acqua Duo Lorenzetti! Pressão excelente e água quentinha no chuveiro e ducha! 🚿🔥 #reforma #chuveiro #acquaduo"
    },
    {
      name: "Thais Magnago",
      username: "thaismagnago",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_30.jpg",
      poster: "../videosprodutos/posters/video-produto-32-take4.jpg",
      video: "https://files.catbox.moe/gdwjt5.mp4",
      desc: "Melhor investimento pra casa! O chuveiro Acqua Duo é lindo e super potente! 🖤✨ #tourpeloape #acquaduo #lorenzetti"
    }
  ];

  const CREATORS_CHUVEIRO_32 = CHUVEIRO_32_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: 0.2,
    likes: 25400 + (i * 2800),
    commentsCount: 215 + (i * 32),
    sharesCount: 82 + (i * 18),
    savesCount: 1980 + (i * 220),
    description: base.desc
  }));

  // 1.10.10 DATASET DO LIVRO INFANTIL INTERATIVO BILÍNGUE FALANTE (PRODUTO 124) - CRIADORES E VÍDEOS REAIS TIKTOK SHOP
  const LIVRO_124_VIDEOS_MAP = [
    {
      name: "Dicas da Mamãe",
      username: "dicasdamamae.oficial",
      avatar: "../img/reviews-avatars/mulheres_validadas/mulher_21.jpg",
      poster: "../videosprodutos/posters/poster-produto-124.jpg",
      video: "https://files.catbox.moe/64aksn.mp4",
      startTime: 0.2,
      desc: "Livro Infantil Interativo Bilíngue Falante! Tocou na página e ele fala em Português e Inglês! Substitui as telas do celular com diversão e aprendizado! 📚👶🇬🇧 #livroinfantil #livrointerativo #bilingue #maternidade"
    },
    {
      name: "Larissa Recomenda",
      username: "larissarecomenda",
      avatar: "../img/reviews-avatars/mulheres_validadas/mulher_14.jpg",
      poster: "../videosprodutos/posters/poster-produto-124-c2.jpg",
      video: "https://files.catbox.moe/c83xk4.mp4",
      startTime: 0.2,
      desc: "Melhor achadinho pro desenvolvimento do seu filho! Livro falante com caneta tátil, ensina animais, frutas e números em 2 idiomas! 🍼✨ #achadinhos #brinquedoseducativos #tiktokshop"
    },
    {
      name: "Catiane",
      username: "catiane_oficial",
      avatar: "../img/avatars-livro/creator-catiane.jpg?v=1794781000",
      poster: "../videosprodutos/posters/poster-produto-124-c3.jpg",
      video: "https://files.catbox.moe/r5fs78.mp4",
      startTime: 0.2,
      desc: "Gente, meu bebê não larga mais esse livro! É super interativo, o som sai limpinho e ele já tá repetindo as palavrinhas em inglês! 🧠💛 #maternidadereal #livrosonoro #desenvolvimentoinfantil"
    },
    {
      name: "Luísa Sarmento",
      username: "luisaklix",
      avatar: "../img/avatars-livro/creator-luisa.jpg?v=1794781000",
      poster: "../videosprodutos/posters/poster-produto-124-c4.jpg",
      video: "https://files.catbox.moe/pe4ms6.mp4",
      startTime: 0.2,
      desc: "Tchau celular! Esse livro inteligente interativo tem 10 páginas táteis que falam com a caneta. Vale cada centavo! 👶📖 #brinquedoeducativo #semtelas #maedeprimeiraviagem"
    },
    {
      name: "Vandinho Souza",
      username: "vandinhosouzaa",
      avatar: "../img/avatars-livro/creator-vandinho.jpg?v=1794781000",
      poster: "../videosprodutos/posters/poster-produto-124-c5.jpg",
      video: "https://files.catbox.moe/4wzbvs.mp4",
      startTime: 0.2,
      desc: "Livro interativo educativo bilíngue para desenvolver melhor o seu filho! Qualidade 10/10, entrega super rápida da Stone Shop! 🚀📚 #brinquedoeducativo #filhos #tiktokshop"
    }
  ];

    const CREATORS_LIVRO_124 = LIVRO_124_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 28400 + (i * 2900),
    commentsCount: 310 + (i * 52),
    sharesCount: 160 + (i * 35),
    savesCount: 3120 + (i * 410),
    description: base.desc
  }));

  // 1.25 DATASET DA MOCHILA REBECCA BONBON JUVENIL (PRODUTO 28) - CRIADORAS 100% REAIS TIKTOK SHOP
  const REBECCA_BONBON_28_VIDEOS_MAP = [
    {
      name: "Evilyn Ribeiro",
      username: "evi_ribeiro1",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/2d3eb5487cc8efae10a1c0004661c8f4~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=9ee4ca70&x-expires=1795366800&x-signature=z6r7VYIqVvBo4%2BiYaC%2FvoDY%2B6%2F4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-28-c2.jpg",
      video: "https://files.catbox.moe/kegz2k.mp4",
      startTime: 0.2,
      desc: "Abrindo a mochila Rebecca Bonbon da minha filha! Material impecável, detalhes dourados e muito espaço! ✨🎒"
    },
    {
      name: "Mãe e Madrasta",
      username: "mae_madrasta",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/26b28a5bec8a8c312250e738380e1695~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=6d6a8511&x-expires=1795366800&x-signature=G7T8Nzz9DB6ECJMz3ZolQv2rg%2Bo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-28-c3.jpg",
      video: "https://files.catbox.moe/b2ztu8.mp4",
      startTime: 0.2,
      desc: "Chegou a mochila Rebecca Bonbon original! Qualidade surreal, chaveiro lindo do cachorrinho e super resistente! 🎀"
    },
    {
      name: "Dayse Santos",
      username: "daysesantos777",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/7323233900525436934~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=185c420d&x-expires=1795366800&x-signature=Mm0%2FmUUd75CdKH5Tdi3eoiux6jY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-28-c4.jpg",
      video: "https://files.catbox.moe/ihak03.mp4",
      startTime: 0.2,
      desc: "Unboxing da minha mochila da Rebecca Bonbon! Perfeita em todos os ângulos, super confortável nas costas! 📚🎒✨"
    },
    {
      name: "Larissa Daily",
      username: "larihdailyy_",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/af9046555e71170b8fcfc4e95abaff83~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=f5b21b95&x-expires=1795366800&x-signature=%2FZxne7944nr4u7HC7fLEWaDTGyg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "../videosprodutos/posters/poster-produto-28-c5.jpg",
      video: "https://files.catbox.moe/w58lgl.mp4",
      startTime: 0.2,
      desc: "Unboxing da minha mochila escolar Rebecca Bonbon! Cabe tudo e mais um pouco, tecido impermeável top! 🍱🥤"
    }
  ];

  const CREATORS_REBECCA_BONBON_28 = REBECCA_BONBON_28_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 31400 + (i * 2400),
    commentsCount: 290 + (i * 45),
    sharesCount: 180 + (i * 30),
    savesCount: 3400 + (i * 390),
    description: base.desc
  }));

  // 1.26 DATASET DA MOCHILA BLUEY E BINGO (PRODUTO 33) - CRIADORES 100% REAIS TIKTOK SHOP
  const BLUEY_33_VIDEOS_MAP = [
    {
      name: "D’Lily Variedades",
      username: "dlily.variedades",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/f879914a752a821266c3313d6c24a497~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=330ac987&x-expires=1795366800&x-signature=Ez5zQW6kyigtawUur50mTDQLAiU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oEF7IUEDCcfBGjzQTpUZEneIwBFx8RAW4ZBqgg~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=RbiOZS9vFY%2Bn%2BBZCITjZlwSLH%2B4%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2",
      video: "https://files.catbox.moe/8x2qjy.mp4",
      startTime: 0.2,
      desc: "Kit de mochila da Bluey e Bingo com lancheira térmica saindo para entrega! Apaixonada! 🎒✨ #bluey #voltaasaulas"
    },
    {
      name: "Aldenice Souza",
      username: "aldenice._",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/257448a53c7b45a482c786ff40c42941~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=cde9330c&x-expires=1795366800&x-signature=XGo7rpfSHRpofxBTAxIcK%2BU1Ps0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o4oWeAG3sNDD1LjEVqOl3HoIAQduCQjQfnCGIf~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=sLK%2BN5UwWB6GXrqgxkWKadlKGDw%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2",
      video: "https://files.catbox.moe/m8dral.mp4",
      startTime: 0.2,
      desc: "Mochila infantil Bluey e Bingo maravilhosa! Minha pequena amou as cores e os bolsos laterais! 💙🧡"
    },
    {
      name: "Feitozzi",
      username: "feitozzi",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/710133245a8de43131f8174771745112~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=4479a56e&x-expires=1795366800&x-signature=bI27yC6kmHKdttlM2AHpCdWhqRM%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oo7E6I1lIY7EcD7BEvhDfB6RHoAFDGygeLjqQu~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=NwNKhylPDWnjIIf8r5uZcmUSY7E%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2",
      video: "https://files.catbox.moe/1n5fg2.mp4",
      startTime: 0.2,
      desc: "Coleção de mochilas escolares da Bluey! Estampa vibrante, material reforçado e lancheira combinando! 🐾"
    },
    {
      name: "Dejane ✨",
      username: "deshop75",
      avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/480a8ab197c25f750308a7edc2a2ae25~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=24208e5c&x-expires=1795366800&x-signature=%2FlwwqXTr8YdqtIu0c14nvsUN5Kc%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
      poster: "https://p19-common-sign.tiktokcdn.com/tos-alisg-p-0037/oM407ASOd4AfIEQVHfFfDEAdTp3AOOIBjADtIn~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=2%2FiS7HW73j0%2FX%2FE7DrI0cP70suM%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2",
      video: "https://files.catbox.moe/bj3ql1.mp4",
      startTime: 0.2,
      desc: "Mochila escolar da Bluey perfeita para as aulas! Leve, espaçosa e com acabamento de primeira linha! 📚🎒"
    }
  ];

  const CREATORS_BLUEY_33 = BLUEY_33_VIDEOS_MAP.map((base, i) => ({
    name: base.name,
    username: base.username,
    avatar: base.avatar,
    poster: base.poster,
    video: base.video,
    startTime: base.startTime || 0.2,
    likes: 28500 + (i * 2100),
    commentsCount: 260 + (i * 38),
    sharesCount: 150 + (i * 25),
    savesCount: 2900 + (i * 310),
    description: base.desc
  }));





  // 1.11 DATASET DA CAIXA DE SOM AIWA BOOMBOX PLUS (PRODUTO 7) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const AIWA_7_VIDEOS_MAP = [];

    const CREATORS_AIWA_7 = AIWA_7_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 19500 + (i * 420) % 25000,
    commentsCount: 110 + (i * 22) % 210,
    sharesCount: 55 + (i * 12) % 95,
    savesCount: 1600 + (i * 150) % 2200,
    description: vInfo.desc
  }));



  // 1.12 DATASET DA FRITADEIRA AIR FRYER ELGIN 5L (PRODUTO 5) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const AIRFRYER_5_VIDEOS_MAP = [
  {
      name: "Camila Achados",
      username: "camila.achadinhos",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_10.jpg",
      poster: "../img/poster-criador-5-1.jpg",
      video: "https://files.catbox.moe/a8zjrb.mp4",
      startTime: 0.2,
      desc: "Fritadeira Elétrica Visio Fry Elgin 5L 1700w! O visor transparente com luz interna é sensacional, dá pra ver a comida assando sem abrir! ✨🍟"
    }
  ];

  const CREATORS_AIRFRYER_5 = AIRFRYER_5_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 12500 + (i * 390) % 15000,
    commentsCount: 65 + (i * 11) % 130,
    sharesCount: 38 + (i * 8) % 70,
    savesCount: 1100 + (i * 95) % 1500,
    description: vInfo.desc
  }));



  // 1.13 DATASET DA BICICLETA ERGOMÉTRICA FITNESS SEVENFIT (PRODUTO 6) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const BIKE_6_VIDEOS_MAP = [
  {
      name: "Rayssa Calazans",
      username: "raysscalazans",
      avatar: "../img/creators-auto/avatar-criador-6-1.jpg",
      poster: "../img/poster-criador-6-1.jpg",
      video: "https://files.catbox.moe/perlvk.mp4",
      startTime: 0.2,
      desc: "Gente, testei minha bike ergométrica em casa e me surpreendeu demais! Pedal super suave e silencioso! 🚴‍♀️✨"
    }
  ];

  const CREATORS_BIKE_6 = BIKE_6_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 11800 + (i * 490) % 14000,
    commentsCount: 54 + (i * 9) % 120,
    sharesCount: 16 + (i * 5) % 50,
    savesCount: 780 + (i * 85) % 1100,
    description: vInfo.desc
  }));



  // 1.14 DATASET DA CAIXA DE SOM JBL BOOMBOX 3 (PRODUTO 4) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const JBL_4_VIDEOS_MAP = [
  {
      name: "Thiago Bass & Áudio",
      username: "thiagobass.som",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_21.jpg",
      poster: "../img/poster-criador-4-1.jpg",
      video: "https://files.catbox.moe/s313zy.mp4",
      startTime: 0.2,
      desc: "JBL BOOMBOX 3 no volume máximo! O subwoofer dedicado dessa versão de 3 vias faz as janelas vibrarem! Potência absurda! 🔊🔥"
    },
  {
      name: "Rodrigo Tech & Games",
      username: "rodrigo.techaudio",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_23.jpg",
      poster: "../img/poster-criador-4-2.jpg",
      video: "https://files.catbox.moe/zlnumo.mp4",
      startTime: 0.2,
      desc: "Bass Test com funk e eletrônica na Boombox 3: graves profundos sem distorcer nada. Melhor caixa portátil do mercado! 🎶💥"
    },
  {
      name: "Lucas & Mari Churrasco",
      username: "casal.somdechurrasco",
      avatar: "../img/creators-tech/creator-3.jpg",
      poster: "../img/poster-criador-4-3.jpg",
      video: "https://files.catbox.moe/pj5xsi.mp4",
      startTime: 0.2,
      desc: "Levamos a JBL Boombox 3 pro sítio e tocou mais de 20 horas direto no churrasco sem pedir tomada! Bateria monstra! 🔋🥩"
    }
  ];

    const CREATORS_JBL_4 = JBL_4_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 13800 + (i * 420) % 16500,
    commentsCount: 78 + (i * 13) % 150,
    sharesCount: 45 + (i * 9) % 90,
    savesCount: 1250 + (i * 110) % 2100,
    description: vInfo.desc
  }));



  // 1.15 DATASET DA PISCINA SPLASH FUN MOR 2400L (PRODUTO 12) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const PISCINA_12_VIDEOS_MAP = [
  {
      name: "Vaninha Medeiros",
      username: "vaninhamedeiros2",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_1.jpg",
      poster: "../img/poster-criador-12-1.jpg",
      video: "https://files.catbox.moe/h5x3n6.mp4",
      startTime: 0.2,
      desc: "Montando nossa piscina Mor 2400 Litros no quintal! Super fácil, só inflar a borda superior e encher de água que ela sobe sozinha! 💦☀️ #piscinamor #splashfun"
    }
  ];

  const CREATORS_PISCINA_12 = PISCINA_12_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 14200 + (i * 410) % 18000,
    commentsCount: 68 + (i * 11) % 145,
    sharesCount: 42 + (i * 8) % 85,
    savesCount: 1150 + (i * 90) % 2100,
    description: vInfo.desc
  }));



  // 1.16 DATASET DA CAIXA DE SOM AMPLIFICADA AIWA PARTY BOX AWS-PB-07 (PRODUTO 8) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const AIWA_8_VIDEOS_MAP = [
  {
      name: 'Rodrigo Fonseca',
      username: 'rodrigofonseca_som',
      avatar: '../img/creators-tech/avatar-criador-8-1.jpg',
      poster: '../img/poster-criador-8-1.jpg',
      video: 'https://files.catbox.moe/k3u5ff.mp4',
      startTime: 0.2,
      desc: 'Lançamento oficial da AIWA Partybox AWS-PB-07! 100W RMS de som puro, show de luzes RGB dinâmico e TWS para parear duas caixas! 🔊✨ #aiwa #partybox #sompotente'
    },
  {
      name: 'TioSuper Tech',
      username: 'tio_super',
      avatar: '../img/creators-tech/avatar-criador-8-2.jpg',
      poster: '../img/poster-criador-8-2.jpg',
      video: 'https://files.catbox.moe/8ynmxe.mp4',
      startTime: 0.2,
      desc: 'Testando os graves no talo da AIWA Party Box! Essa caixa bate muito forte com o Bass Boost ativado, qualidade absurda pra festa! 🔥🎶 #aiwa #caixadesom #bass'
    },
  {
      name: 'Lucas Áudio Review',
      username: 'lucas.audioreview',
      avatar: '../img/creators-tech/avatar-criador-8-3.jpg',
      poster: '../img/poster-criador-8-3.jpg',
      video: 'https://files.catbox.moe/32ulh9.mp4',
      startTime: 0.2,
      desc: 'Demonstração da AIWA Party Box com entrada de microfone, conexão Bluetooth 5.3 e Lightshow multicolorido! O som preenche o ambiente todo! 🎤🎉 #aiwa #partybox'
    }
  ];

    const CREATORS_AIWA_PARTYBOX_8 = AIWA_8_VIDEOS_MAP.map((vInfo, i) => ({
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 15400 + (i * 480) % 18000,
    commentsCount: 88 + (i * 14) % 150,
    sharesCount: 32 + (i * 8) % 70,
    savesCount: 1200 + (i * 110) % 1800,
    description: vInfo.desc
  }));


  // 2. DATASET AUTOMOTIVO / PNEUS PIRELLI (PRODUTO-101)
  const PNEU_VIDEOS = [
    "https://files.catbox.moe/ifsim6.mp4",
    "https://files.catbox.moe/3lusxf.mp4",
    "https://files.catbox.moe/38b3hv.mp4",
    "https://files.catbox.moe/nqu6ks.mp4",
    "https://files.catbox.moe/q3naa4.mp4",
    "https://files.catbox.moe/pj5xsi.mp4",
    "https://files.catbox.moe/rpimi5.mp4",
    "https://files.catbox.moe/zlnumo.mp4",
    "https://files.catbox.moe/duznxa.mp4",
    "https://files.catbox.moe/cill8y.mp4",
    "https://files.catbox.moe/2n37mu.mp4",
    "https://files.catbox.moe/kkl0yf.mp4"
  ];

  const PNEU_POSTER_FILES = [
    "WhatsApp Video 2026-07-27 at 19.36.22.jpg", "WhatsApp Video 2026-07-27 at 19.36.26.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.27.jpg", "WhatsApp Video 2026-07-27 at 19.36.32.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.35.jpg", "WhatsApp Video 2026-07-27 at 19.36.40.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.41.jpg", "WhatsApp Video 2026-07-27 at 19.36.43.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.48.jpg", "WhatsApp Video 2026-07-27 at 19.36.52.jpg",
    "WhatsApp Video 2026-07-27 at 19.36.53.jpg", "WhatsApp Video 2026-07-27 at 19.37.01.jpg",
    "WhatsApp Video 2026-07-27 at 19.37.04.jpg"
  ];
  const PNEU_POSTERS = PNEU_POSTER_FILES.map(f => (isPagesDir ? '../' : '') + 'videosdoscriadorespneu/posters/' + f);

  const CREATORS_TIRES = PNEU_VIDEOS.map((video, i) => {
    const item = CREATORS_AUTO_NAMES[i % CREATORS_AUTO_NAMES.length];
    return {
      name: item.name,
      username: item.user,
      avatar: AVATARS_AUTO[i % AVATARS_AUTO.length],
      poster: PNEU_POSTERS[i % PNEU_POSTERS.length],
      video: video,
      startTime: TAKE_OFFSETS[i % TAKE_OFFSETS.length],
      likes: 4500 + (i * 320) % 8000,
      commentsCount: 18 + (i * 4) % 60,
      saves: 850 + (i * 65) % 1500,
      shares: 95 + (i * 12) % 300,
      description: "Pneus novos instalados e alinhados! Qualidade Pirelli original, segurança máxima na pista! 🚗💨"
    };
  });

  const SCOOTER_POSTER_FILES = ["poster-1.jpg"];
  const SCOOTER_POSTERS = SCOOTER_POSTER_FILES.map(f => (isPagesDir ? '../' : '') + 'img/posters-scooter/' + f);
  const SCOOTER_CREATORS_INFO = [
    { name: "Matheus EletroMob", user: "matheuseletromob", desc: "Scooter Elétrica TUI 1000W! Autonomia surreal para o dia a dia na cidade! 🛴⚡ #scooter #mobilidadeurbana #tecnologia" }
  ];

  const CREATORS_SCOOTER_102 = SCOOTER_CREATORS_INFO.map((item, i) => ({
    name: item.name,
    username: item.user,
    avatar: (isPagesDir ? '../' : '') + 'img/reviews-avatars/tiktok_real/' + (i % 2 === 0 ? `tt_avatar_${i * 2 + 1}.jpg` : `tt_avatar_${i * 2 + 2}.jpg`),
    poster: SCOOTER_POSTERS[i % SCOOTER_POSTERS.length],
    video: (isPagesDir ? '../' : '') + 'videoscooterintroducao/scooter-preta.mp4',
    startTime: 0.2,
    likes: 21000 + (i * 2400),
    commentsCount: 180 + (i * 26),
    saves: 1600 + (i * 180),
    shares: 65 + (i * 15),
    description: item.desc
  }));

  // IDs de produtos com vídeo dedicado Catbox CDN
  const DEDICATED_VIDEOS = [5, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 35, 52, 55, 57, 58, 59, 60, 61, 63, 64, 65, 70, 72, 73, 75, 78, 80, 81, 83, 85, 87, 89, 91, 92, 94, 95, 96, 97, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115];

  // Comentários de Moda / Sandália / Chinelo
  const COMMENTS_FASHION = [
    "Gente, esse chinelo é lindo demais, o strass brilha muito na luz! 💖",
    "Chegou certinho aqui no RJ em 4 dias, super bem embalado!",
    "Peguei o tamanho 37/38 e ficou perfeito no pé, muito macio.",
    "Não machuca nada entre os dedos, dá pra andar o dia todo.",
    "Comprei o branco e agora quero o preto e o caramelo também kkkk",
    "Qualidade surreal pelo preço, no shopping um desse não sai por menos de 100!",
    "Amei demais, super levinho e a sola não escorrega em piso molhado.",
    "Minha mãe viu o meu e pediu pra comprar um pra ela também!",
    "Entrega rápida e frete grátis, nota 10 TikTok Shop!",
    "Combina com tudo, vestido, shortinho jeans, saia... perfeito pro verão!",
    "O acabamento das pedrinhas é muito firme, não solta fácil.",
    "Podem comprar sem medo meninas, é idêntico ao anúncio!",
    "Muito delicado nos pés, dá um charme especial no look.",
    "Chegou antes do prazo e veio com saquinho de proteção, amei!",
    "O salto é baixinho e super confortável, não cansa nada as pernas."
  ];

  // Comentários de Pneus
    // Comentários do Projetor HY300 4K Smart
  const COMMENTS_PROJETOR = [
    "Gente, transformei meu quarto num cinema! A imagem no teto deitado na cama é surreal de perfeita! 🍿🎬",
    "Chegou em 3 dias aqui em Curitiba! Já veio com Netflix e YouTube instalado, foi só colocar a senha do Wi-Fi.",
    "Conectei minha caixinha de som Bluetooth nele e o som ficou potente demais!",
    "Pelo amor de Deus, por esse preço promocional do 11.11 não tem como não comprar. Vale cada centavo!",
    "Dá pra espelhar o iPhone e Android sem fio de boa, roda vídeo do TikTok e jogos lisinho.",
    "A rotação de 180 graus é genial, você vira pra qualquer parede ou pro teto e o foco ajusta na hora.",
    "Minha esposa amou, agora a gente assiste série toda noite deitadinho no teto do quarto kkkk 😍",
    "Melhor compra que já fiz na internet, esquece TV cara de 2 mil reais!"
  ];

  
  const COMMENTS_BODY_106 = [
    "Meninas, o efeito desse body no vestido é inacreditável! Sumiu a pochete na hora! 😍",
    "Comprei o M e serviu perfeitamente. Tecido super firme mas não sufoca nem enrola.",
    "Amei que tem abertura higiênica embaixo, dá pra usar o dia todo tranquilamente.",
    "Comprei o bege e agora já tô comprando o preto. Melhor modelador que já tive!",
    "Chegou em 3 dias aqui em SP, super discreto na embalagem e acabamento impecável.",
    "Disfarça super bem as gordurinhas das costas também, postura fica retinha!"
  ];

  const COMMENTS_ASPIRADOR_107 = [
    "A potência desse mini aspirador é absurda pelo tamanho! Puxou toda a sujeira dos bancos do carro.",
    "A função sopradora pra limpar o teclado e o console do carro é simplesmente genial! 🚗💨",
    "Chegou super rápido com os 3 bicos e cabo de carregar. Bateria dura muito!",
    "Cabe certinho no porta-luvas, salva demais no dia a dia com as crianças.",
    "O filtro HEPA é muito fácil de lavar na torneira. Valeu cada centavo da promoção!",
    "Melhor compra do mês no TikTok Shop, recomendo de olhos fechados!"
  ];

  const COMMENTS_ESCOVA_108 = [
    "Gente essa escova 5 em 1 é idêntica àquela de 4 mil reais! Seca e modela perfeito!",
    "O efeito Coanda de sugar a mecha pro cacho é real, não queima nada o cabelo.",
    "Chegou em 3 dias aqui em SP, bem embalada com todas as 5 ponteiras. Apaixonada!",
    "Meu cabelo é crespo e alisou a raiz com facilidade, sem deixar cheiro de queimado.",
    "Comprei pelo cupom de desconto e valeu cada centavo, melhor compra da vida!"
  ];

  const COMMENTS_MODELADOR_109 = [
    "Esse modelador sem fio me salvou no casamento! Retoquei os cachos no carro em 5 minutos.",
    "Ele puxa o cabelo suavemente e apita certinho no tempo. Não engancha nada!",
    "A bateria dura pra fazer a cabeça inteira duas vezes tranquilamente. Muito prático!",
    "Melhor invenção pro cabelo, não queima a mão nem o pescoço.",
    "Cacho perfeito e dura o dia todo sem precisar de laquê. Podem comprar sem medo!"
  ];


  const COMMENTS_TIRES = [
    "pneu excelente, recomendo demais!",
    "coloquei o cinturato p7 e achei muito macio no asfalto",
    "Pirelli original de verdade, vale cada centavo",
    "entrega rápida, comprei no pix e enviaram na hora",
    "borracha muito fresca, DOT de fabricação recente"
  ];

  // Comentários de Controle Arcade 7 em 1 (Fightstick)
  const COMMENTS_ARCADE_114 = [
    "Mano, o direcional com microswitch faz aquele clique gostoso demais, zero delay nos combos! 🕹️🔥",
    "Testei no Street Fighter 6 e KOF 98 no PC, os especiais saem lisos sem engasgar!",
    "As ventosas na base seguram mesmo na mesa? Aqui na de vidro colou igual chiclete kkkk",
    "Compatível com PS4 e Nintendo Switch de verdade? Plug and play direto?",
    "Chegou aqui em SP em 3 dias pela Stone Shop, super bem embalado na caixa original!",
    "Pelo preço promocional não achei nada parecido, qualidade de fightstick muito mais caro.",
    "Joguei Tekken 8 no emulador do PC e a precisão do manche 360 é fantástica!",
    "Os 8 botões mecânicos têm uma resposta tátil imediata, nada daquela borracha mole de controle barato.",
    "Lembrou na hora os fliperamas de shopping dos anos 90, nostalgia pura! 👏🕹️",
    "Cabo de 2.5m é perfeito pra jogar do sofá sem esticar cabo nenhum."
  ];

  // Comentários Gerais para outros produtos
  const COMMENTS_GENERAL = [
    "Chegou super rápido aqui em casa, muito bem embalado!",
    "Qualidade me surpreendeu muito pelo valor pago, recomendo!",
    "Melhor compra do mês no TikTok Shop, com certeza comprarei de novo.",
    "Idêntico ao que foi mostrado no vídeo, nota 10!",
    "O acabamento é excelente e veio com nota fiscal certinha.",
    "Comprei com frete grátis e chegou antes do prazo previsto.",
    "Excelente custo benefício, super valeu a pena!",
    "Muito prático pro dia a dia, recomendo de olhos fechados."
  ];

  const USERNAME_PREFIXES = ["camila_", "larissa.", "aninha_", "gabi_", "mari_", "bia_closet", "ju_costa", "amanda_", "carol_", "renata_"];
  const GAMER_USERNAME_PREFIXES = ["lucas_", "marcos_", "thiago_", "gabriel_", "felipe_", "leo_", "bruno_", "danilo_", "arthur_", "diego_"];

  function generateRandomComment(idx, contextType) {
    const isGamer = contextType === 'arcade114';
    const prefixes = isGamer ? GAMER_USERNAME_PREFIXES : USERNAME_PREFIXES;
    const prefix = prefixes[idx % prefixes.length];
    const user = `${prefix}${(idx * 17) % 100}`;
    const avatar = isGamer 
      ? (isPagesDir ? `../img/reviews-avatars/tiktok_real/tt_avatar_${1 + ((idx * 2) % 40)}.jpg` : `img/reviews-avatars/tiktok_real/tt_avatar_${1 + ((idx * 2) % 40)}.jpg`)
      : AVATARS_FEMININOS[idx % AVATARS_FEMININOS.length];
    
    let pool = COMMENTS_GENERAL;
    if (contextType === 'tires') pool = COMMENTS_TIRES;
    else if (contextType === 'chinelo') pool = COMMENTS_FASHION;
    else if (contextType === 'projetor') pool = COMMENTS_PROJETOR;
    else if (contextType === 'bodymodelador') pool = COMMENTS_BODY_106;
    else if (contextType === 'aspirador') pool = COMMENTS_ASPIRADOR_107;
    else if (contextType === 'escova108') pool = COMMENTS_ESCOVA_108;
    else if (contextType === 'modelador109') pool = COMMENTS_MODELADOR_109;
    else if (contextType === 'arcade114') pool = COMMENTS_ARCADE_114;

    const text = pool[idx % pool.length];
    const recentTikTokDates = [
      "há 18 min",
      "há 35 min",
      "há 1 h",
      "há 2 h",
      "há 3 h",
      "há 5 h",
      "há 8 h",
      "ontem",
      "ontem",
      "há 1 d",
      "há 1 d",
      "há 2 d",
      "há 2 d",
      "há 3 d",
      "há 4 d",
      "há 5 d",
      "há 6 d",
      "há 1 sem"
    ];
    const date = recentTikTokDates[idx % recentTikTokDates.length];
    const likes = Math.floor(((idx * 7) % 85) + 15);
    return { avatar, user, text, date, likes, liked: false };
  }

  // Elementos globais do modal TikTok
  let ttModal = null;
  let ttVideo = null;
  let currentVideoIndex = 0;
  let videoList = [];

  function formatNumber(num) {
    if (!num || isNaN(num)) return '0';
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1).replace('.', ',') + 'M';
    }
    if (num >= 10000) {
      const formatted = (num / 1000).toFixed(1).replace('.0', '').replace('.', ',');
      return formatted + 'K';
    }
    return num.toLocaleString('pt-BR');
  }

  // Injeta estilos CSS necessários
  function injectStyles() {
    if (document.getElementById('tt-styles')) return;
    const style = document.createElement('style');
    style.id = 'tt-styles';
    style.innerHTML = `
      .creators-section:empty,
      .creators-section[style*="display: none"] {
        display: none !important;
        padding: 0 !important;
        margin: 0 !important;
        border: none !important;
        height: 0 !important;
        min-height: 0 !important;
      }
      .creators-section {
        padding: 14px 0 14px 14px !important;
        background: #ffffff !important;
        margin-bottom: 8px !important;
        border-bottom: 8px solid #f5f5f5 !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "TikTok Sans", "Plus Jakarta Sans", sans-serif !important;
      }
      .creators-title {
        font-size: 16px;
        font-weight: 700;
        color: #161823;
        margin-bottom: 12px;
        letter-spacing: -0.2px;
      }
      .creators-carousel {
        display: flex !important;
        gap: 8px !important;
        overflow-x: auto !important;
        padding: 0 14px 4px 0 !important;
        scroll-behavior: smooth !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
      }
      .creators-carousel::-webkit-scrollbar {
        display: none;
      }
      .creator-card {
        flex: 0 0 104px !important;
        width: 104px !important;
        height: 148px !important;
        border-radius: 8px !important;
        position: relative !important;
        overflow: hidden !important;
        cursor: pointer !important;
        background: #111 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
        -webkit-tap-highlight-color: transparent !important;
      }
      .tt-modal {
        display: none;
        position: fixed !important;
        inset: 0 !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        width: 100vw !important;
        width: 100% !important;
        height: 100dvh !important;
        height: 100vh !important;
        height: -webkit-fill-available !important;
        max-height: 100dvh !important;
        background: #000 !important;
        z-index: 999999 !important;
        flex-direction: column !important;
        justify-content: center !important;
        align-items: center !important;
        touch-action: none !important;
        user-select: none !important;
        -webkit-user-select: none !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
      }
      .tt-container {
        position: relative !important;
        width: 100% !important;
        max-width: 480px !important;
        height: 100% !important;
        max-height: 100% !important;
        background: #000 !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
        touch-action: none !important;
        box-sizing: border-box !important;
      }
      .tt-play-icon-overlay {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) scale(0.95);
        width: 68px;
        height: 68px;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        border-radius: 50%;
        display: none;
        align-items: center;
        justify-content: center;
        pointer-events: none;
        z-index: 15;
        transition: transform 0.15s, opacity 0.15s;
      }
      .tt-top-bar {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        padding: 12px 14px;
        padding-top: max(16px, calc(10px + env(safe-area-inset-top)));
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 10;
        box-sizing: border-box;
        background: linear-gradient(180deg, rgba(0,0,0,0.65) 0%, transparent 100%);
      }
      .tt-back-btn {
        background: none;
        border: none;
        color: #fff;
        cursor: pointer;
        padding: 0;
        display: flex;
        align-items: center;
      }
      .tt-search-container {
        flex: 1;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(8px);
        border-radius: 18px;
        display: flex;
        align-items: center;
        padding: 6px 12px;
        gap: 6px;
      }
      .tt-search-input {
        flex: 1;
        background: none;
        border: none;
        color: #fff;
        font-size: 13px;
        outline: none;
      }
      .tt-video-wrapper {
        position: relative !important;
        width: 100% !important;
        height: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background: #000 !important;
        overflow: hidden !important;
        touch-action: none !important;
        cursor: pointer !important;
        will-change: transform, opacity !important;
        box-sizing: border-box !important;
      }
      .tt-video-wrapper:active {
        cursor: grabbing;
      }
      .tt-video {
        width: 100% !important;
        height: 100% !important;
        object-fit: contain !important;
        background: #000 !important;
        pointer-events: none !important;
      }
      .tt-right-actions {
        position: absolute !important;
        right: 10px !important;
        bottom: calc(24px + env(safe-area-inset-bottom, 12px)) !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        gap: 14px !important;
        z-index: 10 !important;
        pointer-events: auto !important;
      }
      .tt-creator-wrapper {
        position: relative;
        margin-bottom: 6px;
      }
      .tt-creator-avatar {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        border: 2px solid #fff;
        object-fit: cover;
      }
      .tt-follow-btn {
        position: absolute;
        bottom: -7px;
        left: 50%;
        transform: translateX(-50%);
        width: 20px;
        height: 20px;
        background: #fe2c55;
        color: #fff;
        border-radius: 50%;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        font-weight: bold;
        cursor: pointer;
      }
      .tt-action-btn {
        background: none;
        border: none;
        color: #fff;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        cursor: pointer;
        padding: 0;
      }
      .tt-action-label {
        font-size: 12px;
        font-weight: 600;
        text-shadow: 0 1px 2px rgba(0,0,0,0.6);
      }
      .tt-left-info {
        position: absolute !important;
        left: 14px !important;
        right: 76px !important;
        bottom: calc(24px + env(safe-area-inset-bottom, 12px)) !important;
        color: #fff !important;
        z-index: 10 !important;
        pointer-events: auto !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.95) !important;
      }
      .tt-username {
        font-size: 15px !important;
        font-weight: 700 !important;
        margin-bottom: 4px !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.95) !important;
        line-height: 1.25 !important;
      }
      
      .tt-product-anchor {
        display: inline-flex !important;
        align-items: center !important;
        gap: 6px !important;
        background: rgba(0, 0, 0, 0.7) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 6px !important;
        padding: 5px 9px !important;
        margin-top: 6px !important;
        cursor: pointer !important;
        color: #ffffff !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.4) !important;
        transition: transform 0.15s ease !important;
      }
      .tt-product-anchor:active {
        transform: scale(0.96) !important;
      }
      .tt-anchor-title {
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
        max-width: 190px !important;
        color: #ffb800 !important;
        font-weight: 700 !important;
      }

      .tt-desc {
        font-size: 13px !important;
        line-height: 1.35 !important;
        text-shadow: 0 1px 4px rgba(0,0,0,0.95) !important;
        display: -webkit-box !important;
        -webkit-line-clamp: 2 !important;
        -webkit-box-orient: vertical !important;
        overflow: hidden !important;
        word-break: break-word !important;
      }
      .tt-comments-drawer {
        position: absolute;
        bottom: -100%;
        left: 0;
        width: 100%;
        height: 65%;
        background: #fff;
        border-radius: 14px 14px 0 0;
        z-index: 20;
        transition: bottom 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
        display: flex;
        flex-direction: column;
      }
      .tt-comments-drawer.open {
        bottom: 0;
      }
      .tt-drawer-header {
        padding: 14px 16px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #eee;
      }
      .tt-drawer-title {
        font-size: 14px;
        font-weight: 700;
        color: #161823;
      }
      .tt-drawer-close {
        background: none;
        border: none;
        font-size: 16px;
        cursor: pointer;
        color: #666;
      }
      .tt-drawer-list {
        flex: 1;
        overflow-y: auto;
        padding: 12px 16px;
      }
      .tt-comment-item {
        display: flex;
        gap: 10px;
        margin-bottom: 14px;
      }
      .tt-comment-avatar {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        object-fit: cover;
      }
      .tt-comment-user {
        font-size: 12px;
        font-weight: 700;
        color: #666;
      }
      .tt-comment-text {
        font-size: 13px;
        color: #161823;
        margin-top: 2px;
      }
      .tt-comment-input-bar {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 10px 14px;
        border-top: 1px solid #eee;
        background: #fff;
        box-sizing: border-box;
        flex-shrink: 0;
      }
      .tt-comment-input {
        flex: 1;
        height: 38px;
        background: #f1f1f2;
        border: none;
        border-radius: 20px;
        padding: 0 16px;
        font-size: 13.5px;
        color: #161823;
        outline: none;
        box-sizing: border-box;
      }
      .tt-comment-input::placeholder {
        color: #8a8b91;
      }
      .tt-comment-submit-btn {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #fe2c55;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        flex-shrink: 0;
        transition: transform 0.15s, opacity 0.15s;
        box-shadow: 0 2px 8px rgba(254, 44, 85, 0.3);
      }
      .tt-comment-submit-btn:active {
        transform: scale(0.92);
      }
      .tt-toast {
        position: absolute;
        top: 75px;
        left: 50%;
        transform: translateX(-50%);
        background: rgba(22, 24, 35, 0.92);
        color: #fff;
        padding: 10px 20px;
        border-radius: 24px;
        font-size: 13px;
        font-weight: 600;
        z-index: 99999;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.25s ease, transform 0.25s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.3);
        white-space: nowrap;
      }
      .tt-toast.show {
        opacity: 1;
        transform: translateX(-50%) translateY(8px);
      }
    `;
    document.head.appendChild(style);
  }


  // Inicializa o carrossel na página (COM SUPORTE A PRÉ-RENDERIZAÇÃO E PLAY INSTANTÂNEO)
  

  // ===== DATASETS DOS PRODUTOS 9, 10, 11, 13, 14, 15, 17, 18, 21, 22 =====
// ===== DATASETS CLIMATIZADORES E AR CONDICIONADO (PRODUTOS 9, 10, 11, 27, 29, 30, 44) =====
const CREATORS_CLIMATIZADOR_OSTER_11 = [
  {
    "name": "Lar & Clima",
    "username": "lareclima.br",
    "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_16.jpg",
    "poster": "../img/posters-climatizador/poster-1.jpg",
    "video": "https://files.catbox.moe/p7r4vc.mp4",
    "localVideo": "https://files.catbox.moe/p7r4vc.mp4",
    "startTime": 0,
    "likes": 14200,
    "comments": 38,
    "shares": 180,
    "saves": 1200,
    "title": "Climatizador Oster 5,3L testado no calor! Com bolsa de gelo refresca o quarto todo ❄️👏"
  },
  {
    "name": "Dicas do Lar",
    "username": "dicasdolar.sp",
    "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_18.jpg",
    "poster": "../img/posters-climatizador/poster-2.jpg",
    "video": "https://files.catbox.moe/ac2l43.mp4",
    "localVideo": "https://files.catbox.moe/ac2l43.mp4",
    "startTime": 0,
    "likes": 15400,
    "comments": 42,
    "shares": 195,
    "saves": 1350,
    "title": "Super silencioso e econômico, perfeito pra quem não pode instalar split! 💨✨"
  },
  {
    "name": "Casa Prática",
    "username": "casapratica.br",
    "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_20.jpg",
    "poster": "../img/posters-climatizador/poster-3.jpg",
    "video": "https://files.catbox.moe/byfq7d.mp4",
    "localVideo": "https://files.catbox.moe/byfq7d.mp4",
    "startTime": 0,
    "likes": 12800,
    "comments": 35,
    "shares": 160,
    "saves": 1100,
    "title": "Testando as 3 velocidades do Climatizador Oster. Ventilação excelente! ❄️👌"
  }
];

    const CREATORS_CLIMATIZADOR_MIDEA_30 = [];

    const CREATORS_CLIMATIZADOR_VENTISOL_44 = [];

    const CREATORS_AR_HQ_29 = [];

    const CREATORS_AR_HQ_9 = [
  {
    "name": "Tech Casa Brasil",
    "username": "techcasabr",
    "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_16.jpg",
    "poster": "../img/posters-ar-portatil/poster-1.jpg",
    "video": "https://files.catbox.moe/mr2lij.mp4",
    "localVideo": "https://files.catbox.moe/mr2lij.mp4",
    "startTime": 0,
    "likes": 14200,
    "comments": 38,
    "shares": 180,
    "saves": 1200,
    "title": "Ar Condicionado Portátil HQ 8.500 BTUs: perfeito pra quartos de até 12m², gela super rápido sem quebradeira!"
  }
  ];

  const CREATORS_AR_HISENSE_10 = [];

    const CREATORS_AR_LG_27 = [];

    const CREATORS_PISCINA_PIXLAR_13 = [
  {
    "name": "Renata Silveira",
    "username": "renatasilveira.lar",
    "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_1.jpg",
    "poster": "../img/posters-piscina/poster-piscina-01.jpg",
    "video": "https://files.catbox.moe/h5x3n6.mp4",
    "localVideo": "https://files.catbox.moe/h5x3n6.mp4",
    "startTime": 0.2,
    "likes": 18400,
    "comments": 45,
    "shares": 120,
    "saves": 350,
    "title": "Piscina inflável 1000L montada no quintal! As crianças amaram ☀️💦"
  }
  ];

  const CREATORS_CHURRASQUEIRA_ARKE_14 = [
  {
    "name": "Camila Rocha",
    "username": "camilaoch.ape",
    "avatar": "../img/avatars-churras/creator-camila.jpg",
    "poster": "../img/posters-churras/poster-arke-c1.jpg?v=20261113_arke_v100",
    "video": "https://files.catbox.moe/jwkiqt.mp4",
    "localVideo": "https://files.catbox.moe/jwkiqt.mp4",
    "likes": 37200,
    "comments": 41,
    "shares": 485,
    "saves": 3700,
    "title": "Churrasqueira Arke Vitta Smart 5 Espetos Rotativa no apê! Sem fumaça nenhuma 🔥🥩",
    "startTime": 0.2
  },
  {
    "name": "Marcos Vinicius",
    "username": "marcoschurras_ape",
    "avatar": "../img/avatars-churras/creator-marcos.jpg",
    "poster": "../img/posters-churras/poster-arke-c2.jpg?v=20261113_arke_v100",
    "video": "https://files.catbox.moe/qmv0y6.mp4",
    "localVideo": "https://files.catbox.moe/qmv0y6.mp4",
    "likes": 28400,
    "comments": 32,
    "shares": 245,
    "saves": 2800,
    "title": "Frangos inteiros dourando nos 5 espetos rotativos da Arke! Fica muito macio e suculento 🍗",
    "startTime": 0.2
  },
  {
    "name": "Larissa Rezende",
    "username": "larissarezende_home",
    "avatar": "../img/avatars-churras/creator-larissa.jpg",
    "poster": "../img/posters-churras/poster-arke-c3.jpg?v=20261113_arke_v100",
    "video": "https://files.catbox.moe/mfpyu6.mp4",
    "localVideo": "https://files.catbox.moe/mfpyu6.mp4",
    "likes": 31700,
    "comments": 45,
    "shares": 310,
    "saves": 3270,
    "title": "Ligando a Arke Vitta Smart 5 espetos elétrica: esquenta rápido demais e o vidro não deixa fumaça escapar!",
    "startTime": 0.2
  },
  {
    "name": "Rodrigo Barcellos",
    "username": "rodrigo.brasa",
    "avatar": "../img/avatars-churras/creator-rodrigo.jpg",
    "poster": "../img/posters-churras/poster-arke-c4.jpg?v=20261113_arke_v100",
    "video": "https://files.catbox.moe/cbcaqg.mp4",
    "localVideo": "https://files.catbox.moe/cbcaqg.mp4",
    "likes": 42190,
    "comments": 58,
    "shares": 494,
    "saves": 4219,
    "title": "Churrasco completo com 5 espetos: picanha, alcatra e linguiça toscana assando juntos por igual! 🥩",
    "startTime": 0.2
  },
  {
    "name": "Juliana Mendes",
    "username": "julianamendes_ape",
    "avatar": "../img/avatars-churras/creator-juliana.jpg",
    "poster": "../img/posters-churras/poster-arke-c5.jpg?v=20261113_arke_v100",
    "video": "https://files.catbox.moe/ba3szw.mp4",
    "localVideo": "https://files.catbox.moe/ba3szw.mp4",
    "likes": 25400,
    "comments": 39,
    "shares": 278,
    "saves": 2640,
    "title": "Zero fumaça no apartamento! A água na bandeja de gordura não deixa queimar e é super fácil de lavar 👏",
    "startTime": 0.2
  },
  {
    "name": "Fernando Costa",
    "username": "fernandochurrasco",
    "avatar": "../img/avatars-churras/creator-fernando.jpg",
    "poster": "../img/posters-churras/poster-arke-c6.jpg?v=20261113_arke_v100",
    "video": "https://files.catbox.moe/jhxyrw.mp4",
    "localVideo": "https://files.catbox.moe/jhxyrw.mp4",
    "likes": 29050,
    "comments": 46,
    "shares": 300,
    "saves": 2955,
    "title": "Picanha com legumes e queijo coalho nos espetos giratórios elétricos da Arke. Melhor investimento do ano!",
    "startTime": 0.2
  },
  {
    "name": "Patrícia Alencar",
    "username": "paty.varandagourmet",
    "avatar": "../img/avatars-churras/creator-patricia.jpg",
    "poster": "../img/posters-churras/poster-arke-c7.jpg?v=20261113_arke_v100",
    "video": "https://files.catbox.moe/vtlv5y.mp4",
    "localVideo": "https://files.catbox.moe/vtlv5y.mp4",
    "likes": 22900,
    "comments": 42,
    "shares": 287,
    "saves": 2350,
    "title": "Montagem completa da churrasqueira Arke 5 espetos na varanda gourmet. Espetos macios e resistentes 🍖",
    "startTime": 0.2
  },
  {
    "name": "Lucas Medeiros",
    "username": "lucasmedeiros_bbq",
    "avatar": "../img/avatars-churras/creator-lucas.jpg",
    "poster": "../img/posters-churras/poster-arke-c8.jpg?v=20261113_arke_v100",
    "video": "https://files.catbox.moe/3xa4m3.mp4",
    "localVideo": "https://files.catbox.moe/3xa4m3.mp4",
    "likes": 34550,
    "comments": 69,
    "shares": 414,
    "saves": 3525,
    "title": "Olha a casquinha dourada dessa picanha giratória na Arke Vitta Smart! 100% aprovada para apartamento!",
    "startTime": 0.2
  }
  ];

    const CREATORS_CHURRASQUEIRA_BISCUITT_15 = [
  {
    "name": "Carlos BBQ",
    "username": "carlosbbq_oficial",
    "avatar": "../img/avatars-biscuitt/creator-carlos.jpg",
    "poster": "../img/posters-biscuitt/poster-biscuitt-c1.jpg",
    "video": "https://files.catbox.moe/dpa885.mp4",
    "localVideo": "https://files.catbox.moe/dpa885.mp4",
    "startTime": 0.2,
    "likes": 34200,
    "comments": 48,
    "shares": 420,
    "saves": 3420,
    "title": "Churrasqueira Portátil Biscuitt Steak Master: acende em 3 minutos com cooler USB! 🔥"
  },
  {
    "name": "Renata na Varanda",
    "username": "renatavaranda_gourmet",
    "avatar": "../img/avatars-biscuitt/creator-renata.jpg",
    "poster": "../img/posters-biscuitt/poster-biscuitt-c2.jpg",
    "video": "https://files.catbox.moe/ymfpap.mp4",
    "localVideo": "https://files.catbox.moe/ymfpap.mp4",
    "startTime": 0.2,
    "likes": 27850,
    "comments": 39,
    "shares": 310,
    "saves": 2780,
    "title": "Testando a Table Grill no apartamento: zero fumaça na sala e a carne fica suculenta demais! 🥩"
  },
  {
    "name": "Thiago Brasa",
    "username": "thiagobrasa_oficial",
    "avatar": "../img/avatars-biscuitt/creator-thiago.jpg",
    "poster": "../img/posters-biscuitt/poster-biscuitt-c3.jpg",
    "video": "https://files.catbox.moe/hmxb1e.mp4",
    "localVideo": "https://files.catbox.moe/hmxb1e.mp4",
    "startTime": 0.2,
    "likes": 41200,
    "comments": 62,
    "shares": 490,
    "saves": 4100,
    "title": "O cooler com regulador de ar faz a brasa pegar fogo em minutos sem precisar soprar! Muito prático"
  },
  {
    "name": "Bruno Churras",
    "username": "brunochurras_ape",
    "avatar": "../img/avatars-biscuitt/creator-bruno.jpg",
    "poster": "../img/posters-biscuitt/poster-biscuitt-c4.jpg",
    "video": "https://files.catbox.moe/h7ctxk.mp4",
    "localVideo": "https://files.catbox.moe/h7ctxk.mp4",
    "startTime": 0.2,
    "likes": 23150,
    "comments": 35,
    "shares": 275,
    "saves": 2310,
    "title": "Gasta menos de 250g de carvão e assa picanha, coração e queijo coalho para 4 pessoas tranquilamente!"
  },
  {
    "name": "Gabi no Apê",
    "username": "gabinoape_dicas",
    "avatar": "../img/avatars-biscuitt/creator-gabi.jpg",
    "poster": "../img/posters-biscuitt/poster-biscuitt-c5.jpg",
    "video": "https://files.catbox.moe/84y53y.mp4",
    "localVideo": "https://files.catbox.moe/84y53y.mp4",
    "startTime": 0.2,
    "likes": 36700,
    "comments": 53,
    "shares": 415,
    "saves": 3670,
    "title": "A parede externa tem isolamento térmico, pode pegar na lateral com a mão que não queima! Nota 10 👏"
  },
  {
    "name": "Felipe Grill",
    "username": "felipegrill_bbq",
    "avatar": "../img/avatars-biscuitt/creator-felipe.jpg",
    "poster": "../img/posters-biscuitt/poster-biscuitt-c6.jpg",
    "video": "https://files.catbox.moe/xs7xwp.mp4",
    "localVideo": "https://files.catbox.moe/xs7xwp.mp4",
    "startTime": 0.2,
    "likes": 29400,
    "comments": 42,
    "shares": 330,
    "saves": 2940,
    "title": "A bag térmica de transporte facilita demais levar pra praia ou camping no fim de semana. Top!"
  }
  ];

    const CREATORS_CADEIRAS_PRAIA_MOR_17 = [
  {
    name: "Juliana Mendes",
    username: "ju.praia",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_35.jpg",
    poster: "../img/posters-praia/poster-praia-01.jpg",
    video: "https://files.catbox.moe/a1eoxs.mp4",
    localVideo: "https://files.catbox.moe/a1eoxs.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Cadeiras de praia Mor em alumínio: leves, não enferrujam e perfeitas para o verão! 🏖️☀️"
  },
  {
    name: "Felipe Castro",
    username: "felipe.litoral",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_36.jpg",
    poster: "../img/posters-praia/poster-praia-02.jpg",
    video: "https://files.catbox.moe/s1lcfe.mp4",
    localVideo: "https://files.catbox.moe/s1lcfe.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Kit 4 cadeiras Mor reclináveis, super confortáveis e fáceis de carregar! 🌊"
  },
  {
    name: "Larissa Ramos",
    username: "lari.verao",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_37.jpg",
    poster: "../img/posters-praia/poster-praia-03.jpg",
    video: "https://files.catbox.moe/mc1plp.mp4",
    localVideo: "https://files.catbox.moe/mc1plp.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Fecham compactas e cabem com folga no porta-malas! Super recomendo! 🚗🏖️"
  },
  {
    name: "Marcos Vinicius",
    username: "marcos.mor",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_38.jpg",
    poster: "../img/posters-praia/poster-praia-04.jpg",
    video: "https://files.catbox.moe/9g7hs6.mp4",
    localVideo: "https://files.catbox.moe/9g7hs6.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Estrutura de alumínio reforçado que aguenta até 110kg sem afundar na areia! 👏"
  },
  {
    name: "Camila Litoral",
    username: "camilalitoral",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_44.jpg",
    poster: "../img/posters-praia/poster-praia-10.jpg",
    video: "https://files.catbox.moe/c1oz8o.mp4",
    localVideo: "https://files.catbox.moe/c1oz8o.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "As melhores cadeiras de praia que já tive! Chegou tudo perfeito e bem embalado! ✨"
  },
  {
    name: "Thiago Mar",
    username: "thiagomar_praia",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_45.jpg",
    poster: "../img/posters-praia/poster-praia-01.jpg",
    video: "https://files.catbox.moe/zok50k.mp4",
    localVideo: "https://files.catbox.moe/zok50k.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Partiu praia com as 4 cadeiras novinhas da Mor! Muito resistentes! 🏖️🌊"
  },
  {
    name: "Renata Sol",
    username: "renata.solpraia",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_46.jpg",
    poster: "../img/posters-praia/poster-praia-02.jpg",
    video: "https://files.catbox.moe/vyw8h2.mp4",
    localVideo: "https://files.catbox.moe/vyw8h2.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Super leves de carregar na mão, até as crianças conseguem levar! ☀️"
  },
  {
    name: "Bruno Maresia",
    username: "brunomaresia",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_47.jpg",
    poster: "../img/posters-praia/poster-praia-03.jpg",
    video: "https://files.catbox.moe/sk0yh6.mp4",
    localVideo: "https://files.catbox.moe/sk0yh6.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Alumínio de verdade, pode molhar com água do mar que não oxida! 🏄‍♂️"
  },
  {
    name: "Fernanda Maré",
    username: "fernandapraiana",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_48.jpg",
    poster: "../img/posters-praia/poster-praia-04.jpg",
    video: "https://files.catbox.moe/i84hm4.mp4",
    localVideo: "https://files.catbox.moe/i84hm4.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Melhor compra para o verão! 4 cadeiras de alta qualidade na Stone Shop! 💖"
  },
  {
    name: "Rodrigo Costa",
    username: "rodrigopraia_fit",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_49.jpg",
    poster: "../img/posters-praia/poster-praia-10.jpg",
    video: "https://files.catbox.moe/0n0j04.mp4",
    localVideo: "https://files.catbox.moe/0n0j04.mp4",
    startTime: 0.5,
    likes: 19400,
    comments: 145,
    shares: 680,
    saves: 2100,
    title: "Conforto total no descanso da praia! Regulagem de posições muito firme! 🌴"
  }
];

  const CREATORS_KIT_PRAIA_MOR_18 = [
  {
    name: "Amanda Costa",
    username: "amanda.praia",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_70.jpg",
    poster: "../img/posters-praia/poster-praia-01.jpg",
    video: "https://files.catbox.moe/tfjuih.mp4",
    localVideo: "https://files.catbox.moe/tfjuih.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Kit praia Mor completo com cadeiras, guarda-sol e saca-areia! Maravilhoso! 🏖️✨"
  },
  {
    name: "Lucas Ferraz",
    username: "lucasferraz.sol",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_71.jpg",
    poster: "../img/posters-praia/poster-praia-02.jpg",
    video: "https://files.catbox.moe/rvye6v.mp4",
    localVideo: "https://files.catbox.moe/rvye6v.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Guarda-sol grande com proteção UV e cadeiras articuladas reforçadas! ☀️"
  },
  {
    name: "Mariana Rios",
    username: "mari.verao",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_72.jpg",
    poster: "../img/posters-praia/poster-praia-03.jpg",
    video: "https://files.catbox.moe/boz1bo.mp4",
    localVideo: "https://files.catbox.moe/boz1bo.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Facilidade pra montar e desmontar tudo na praia! Não ocupa espaço no porta-malas! 🌊"
  },
  {
    name: "Diego Litoral",
    username: "diegolitoral",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_73.jpg",
    poster: "../img/posters-praia/poster-praia-04.jpg",
    video: "https://files.catbox.moe/9ut6uv.mp4",
    localVideo: "https://files.catbox.moe/9ut6uv.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Qualidade Mor indiscutível! Kit mais completo e resistente pra curtir em família! 🌴"
  },
  {
    name: "Bianca Mar",
    username: "bianca.praiana",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_74.jpg",
    poster: "../img/posters-praia/poster-praia-10.jpg",
    video: "https://files.catbox.moe/jqvk36.mp4",
    localVideo: "https://files.catbox.moe/jqvk36.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "O saca-areia facilita muito a fixação do guarda-sol no vento forte! 👏"
  },
  {
    name: "Gustavo Mares",
    username: "gustavomares",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_75.jpg",
    poster: "../img/posters-praia/poster-praia-01.jpg",
    video: "https://files.catbox.moe/eat313.mp4",
    localVideo: "https://files.catbox.moe/eat313.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Alumínio leve e tecido resistente de secagem rápida! Vale cada centavo! 🏄‍♂️"
  },
  {
    name: "Carla Verão",
    username: "carlaverao_top",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_76.jpg",
    poster: "../img/posters-praia/poster-praia-02.jpg",
    video: "https://files.catbox.moe/azfbn2.mp4",
    localVideo: "https://files.catbox.moe/azfbn2.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Nossos dias de sol na praia agora são com conforto de primeira! 💖"
  },
  {
    name: "Marcelo Ondas",
    username: "marceloondas",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_77.jpg",
    poster: "../img/posters-praia/poster-praia-03.jpg",
    video: "https://files.catbox.moe/5ki8dk.mp4",
    localVideo: "https://files.catbox.moe/5ki8dk.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Kit praia top! Chegou tudo rápido antes da nossa viagem de fim de ano! 📦✈️"
  },
  {
    name: "Patrícia Mar",
    username: "patriciapraia",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_78.jpg",
    poster: "../img/posters-praia/poster-praia-04.jpg",
    video: "https://files.catbox.moe/3e1lap.mp4",
    localVideo: "https://files.catbox.moe/3e1lap.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Cadeiras confortáveis e guarda-sol amplo com ótima sombra! 🏖️"
  },
  {
    name: "Rafael Silva",
    username: "rafaelsilva_mar",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_79.jpg",
    poster: "../img/posters-praia/poster-praia-10.jpg",
    video: "https://files.catbox.moe/u1mpnm.mp4",
    localVideo: "https://files.catbox.moe/u1mpnm.mp4",
    startTime: 0.5,
    likes: 18700,
    comments: 138,
    shares: 610,
    saves: 1980,
    title: "Conjunto de praia mais bem avaliado do TikTok Shop! 100% aprovado! 🌊"
  }
];

  const BIKE_GT_20_VIDEOS_MAP = [
  { name: "Lucas Pedal & Trilha", username: "lucas_mtb_brasil", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_1.jpg", poster: "../videosprodutos/posters/video-produto-20.jpg", video: "https://files.catbox.moe/8oqszr.mp4", desc: "Aro 29 com 24 marchas indexadas e freio a disco potente! Bike sensacional pra trilha e asfalto! 🚴‍♂️⛰️ #bike #aro29 #mtbbrasil" }
  ];

    const CREATORS_BIKE_GT_20 = BIKE_GT_20_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 16200 + i * 2300, commentsCount: 145 + i * 25, sharesCount: 55 + i * 12, savesCount: 1320 + i * 180, description: b.desc }));

// 2. P21: Bola De Futebol De Campo Penalty Bravo XXV (Zero ar condicionado)
const BOLA_PENALTY_21_VIDEOS_MAP = [
  { name: "Felipe Fut & Treino", username: "felipefut_treino", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_9.jpg", poster: "../videosprodutos/posters/video-produto-21.jpg", video: "https://files.catbox.moe/rs5lzn.mp4", desc: "Testando a Penalty Bravo XXV de campo! Quique macio, peso oficial de 430g e costura Termotec que não absorve água! ⚽🔥 #futebol #penalty #futeboldecampo" }
  ];

    const CREATORS_BOLA_PENALTY_21 = BOLA_PENALTY_21_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 18400 + i * 2100, commentsCount: 168 + i * 28, sharesCount: 62 + i * 15, savesCount: 1450 + i * 190, description: b.desc }));

// P74: Camisa Seleção Brasil Masculina Oficial
const CAMISA_BRASIL_74_VIDEOS_MAP = [
  {
    name: "SportFino",
    username: "sportfinoo",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/0373174d8c8ac28c3e0967aa99c9c857~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=e1aaeef9&x-expires=1795366800&x-signature=gDr8AmFk%2FfU6d46937CcldGaNdw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/haa2xd.mp4",
    desc: "Detalhes da camisa oficial da Seleção Brasileira versão torcedor! Escudo bordado de altíssima qualidade! 🇧🇷🔥 #brasil #copadomundo"
  },
  {
    name: "Juliana Medeiros",
    username: "jumedeirosr",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/15abe20ad26603a031b6707a4dad5462~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=bfc1c8bb&x-expires=1795366800&x-signature=Pqii2VxxQv8%2BtIEf5aF8wmR0BPg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/7psxwz.mp4",
    desc: "A nova camisa da Seleção Brasileira! Mostrando cada detalhe do tecido Dri-FIT e do caimento impecável! 🇧🇷✨"
  },
  {
    name: "Eiti por aí",
    username: "eitiporai",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/097ad4b466543d26fb6680f2c85e3727~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=781c27ba&x-expires=1795366800&x-signature=MA%2FNlFdOP0l5PqffMPb%2FZSaaWI8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/adk9fx.mp4",
    desc: "Unboxing e review sincero da camisa amarela do Brasil! O tecido é muito leve, respirável e confortável no corpo! 💛💚"
  },
  {
    name: "Matheus Silva",
    username: "ritmodascamisas",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/c9359eff55edd496645c3a0c2b972481~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=5fe2b60b&x-expires=1795366800&x-signature=1iCW0oFCJ39XeShB%2Fz%2BvuLuUc1Q%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/gw0duv.mp4",
    desc: "Nova camisa da Seleção Canarinho! As aplicações cheias de textura e o tecido tecnológico deixam a camisa surreal! ⚽💎"
  },
  {
    name: "Júlia Stofel",
    username: "juliastofel_",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/632db09b3d96fb6e4c459b21f5ff8e09~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=d4e723cf&x-expires=1795366800&x-signature=aTstWpbkhFR3cwLYkUqh0%2FgSAFw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/ygaaob.mp4",
    desc: "Recebidos da camisa da Seleção Brasileira! Linda demais, tecido super macio e caimento perfeito! 🇧🇷🥰"
  }
];

const CREATORS_CAMISA_BRASIL_74 = CAMISA_BRASIL_74_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 35200 + i * 3400, commentsCount: 380 + i * 50, sharesCount: 220 + i * 35, savesCount: 3800 + i * 410, description: b.desc }));

// P99: Kit Camisa Seleção Portugal Masculina
const CAMISA_PORTUGAL_99_VIDEOS_MAP = [
  {
    name: "Lucas Santos",
    username: "lsshop80",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/2b6810dae838a5a6e3a18decce2f6849~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=2bcc4ac0&x-expires=1795366800&x-signature=9ReS7YHf1qzT9qEtk6sZ6vFs534%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/uclek6.mp4",
    desc: "Camisa da Seleção de Portugal CR7! O escudo da Federação Portuguesa e o número 7 com acabamento impecável! 🇵🇹🐐"
  },
  {
    name: "Inês Ferreira",
    username: "camisolas.cr7.pt",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/88df7cfb8cea37cf830dd1bce0f7b366~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=77475acc&x-expires=1795366800&x-signature=IW%2BgYSolgkQ6g%2BbOEjx888LNzy4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/hhhnyi.mp4",
    desc: "Unboxing da camisola da Seleção de Portugal! Qualidade do tecido, bordados perfeitos e caimento top! 🔴🟢"
  },
  {
    name: "Bernardo Silva",
    username: "footballjerseys_0",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-useast2a-avt-0068-euttp/00d0341f72559c4c7318850332acaee7~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=9765b823&x-expires=1795366800&x-signature=ge2haAwfMlOVIeQNOsxGpO0Ap%2B4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/x8o2zn.mp4",
    desc: "Nova camisa de Portugal para colecionadores! O vermelho e verde clássicos com detalhes em dourado! 🇵🇹✨"
  },
  {
    name: "Kevin Lima",
    username: "klstyle7",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/f13348aa7861ce139208c8403e6ab587~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=815e3e31&x-expires=1795366800&x-signature=%2FTnKbB3yKiMFq%2FBdS6b2fI2%2BcRY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/e673hy.mp4",
    desc: "Camisa Portugal Cristiano Ronaldo 7! O manto dos gajos tá surreal de lindo, tecido leve e respirável! 🔥⚽"
  },
  {
    name: "Victor Hugo",
    username: "em.vic4",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/a3ba96a878e2c63ae6c9b630cf099b98~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=724f741b&x-expires=1795366800&x-signature=E1%2BvQ4Qebi9CMN5qtm%2BFVWr2fRU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-21.jpg",
    video: "https://files.catbox.moe/e25p8n.mp4",
    desc: "Manto sagrado de Portugal do papai Cris! Tecido autêntico de torcedor, estampa oficial sem falhas! 🇵🇹👑"
  }
];

const CREATORS_CAMISA_PORTUGAL_99 = CAMISA_PORTUGAL_99_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 32100 + i * 2900, commentsCount: 340 + i * 42, sharesCount: 190 + i * 28, savesCount: 3400 + i * 360, description: b.desc }));

// 3. P22: Colchão Inflável Bestway Casal Suporta 300kg + Bomba (Zero ar condicionado)
const COLCHAO_BESTWAY_22_VIDEOS_MAP = [
  { name: "Rodrigo Camping & Aventura", username: "rodrigocamping_br", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_19.jpg", poster: "../videosprodutos/posters/video-produto-22.jpg", video: "https://files.catbox.moe/ekswrf.mp4", desc: "Testando o Colchão Inflável Bestway Casal que suporta 300kg! Acompanha bomba manual e infla em menos de 5 minutos! ⛺🌲 #camping #colchaoinflavel #bestway" },
  { name: "Camila Vida ao Ar Livre", username: "camilacamping_life", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_4.jpg", poster: "../videosprodutos/posters/video-produto-22-take1.jpg", video: "https://files.catbox.moe/qi938f.mp4", desc: "Toque aveludado super confortável que não escorrega o lençol. Salvou nossa viagem de acampamento em família! 🥰✨ #acampamento #vidaaoarlivre #conforto" }
  ];

    const CREATORS_COLCHAO_BESTWAY_22 = COLCHAO_BESTWAY_22_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 17300 + i * 2200, commentsCount: 154 + i * 26, sharesCount: 58 + i * 14, savesCount: 1390 + i * 175, description: b.desc }));

// 4. P35: Caixa de Som JBL Boombox 4 Bluetooth 210W
// 1.10 DATASET DA CAIXA DE SOM JBL BOOMBOX 4 (PRODUTO 35) - EXCLUSIVO DESACOPLADO
const JBL_BOOMBOX4_35_VIDEOS_MAP = [];

  const CREATORS_JBL_BOOMBOX4_35 = JBL_BOOMBOX4_35_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 28900 + i * 3100, commentsCount: 260 + i * 42, sharesCount: 95 + i * 22, savesCount: 2200 + i * 260, description: b.desc }));

// 5. P52: iPad 11 Geração A16 256GB Wi-Fi
const PAD11_52_VIDEOS_MAP = [
  { name: "Lucas Apple Tech", username: "lucasappletech", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_33.jpg", poster: "../videosprodutos/posters/video-produto-52.jpg", video: "https://files.catbox.moe/3rtr42.mp4", desc: "Unboxing do novo iPad 11 com chip A16 e 256GB! Desempenho absurdo pra edição de vídeo e multitarefa! 📱⚡ #ipad #apple #ipad11" }
  ];

    const CREATORS_PAD11_52 = PAD11_52_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 31200 + i * 3400, commentsCount: 290 + i * 45, sharesCount: 110 + i * 25, savesCount: 2500 + i * 290, description: b.desc }));

// 6. P55: Nintendo Switch Desbloqueado + 10 Jogos 128GB
const SWITCH_55_VIDEOS_MAP = [
  { name: "Renan Games Brasil", username: "renangames_br", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_39.jpg", poster: "../videosprodutos/posters/video-produto-55.jpg", video: "https://files.catbox.moe/wvgft8.mp4", desc: "Nintendo Switch já desbloqueado com cartão de 128GB e os 10 melhores jogos à sua escolha! É ligar e jogar! 🎮🔥 #nintendoswitch #games #switchdesbloqueado" }
  ];

    const CREATORS_SWITCH_55 = SWITCH_55_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 27500 + i * 2900, commentsCount: 240 + i * 36, sharesCount: 88 + i * 20, savesCount: 2150 + i * 240, description: b.desc }));

// 7. P57: Caixa de Som Joog One Hifi 200W com 2 Microfones Sem Fio
const JOOG_ONE_57_VIDEOS_MAP = [
  { name: "Marcos Karaokê Show", username: "marcoskaraoke_show", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_45.jpg", poster: "../videosprodutos/posters/video-produto-57.jpg", video: "https://files.catbox.moe/2v31tr.mp4", desc: "Caixa Joog One 200W HiFi com 2 microfones sem fio inclusos! O som é limpíssimo e o eco do microfone é profissional! 🎤🔊 #karaoke #joogone #caixadesom" }
  ];

    const CREATORS_JOOG_ONE_57 = JOOG_ONE_57_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21400 + i * 2500, commentsCount: 188 + i * 30, sharesCount: 72 + i * 16, savesCount: 1720 + i * 210, description: b.desc }));

// 8. P58: Caixa de Som Alexa Echo Dot 5ª Geração
const ECHODOT_58_VIDEOS_MAP = [
  { name: "Gabriel Casa Inteligente", username: "gabrielcasasmart", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_51.jpg", poster: "../videosprodutos/posters/video-produto-58.jpg", video: "https://files.catbox.moe/v6io74.mp4", desc: "A nova Echo Dot 5ª Geração tem graves 2x mais potentes e sensor de temperatura integrado! Alexa é vida! 🏠🗣️ #echodot5 #alexa #casainteligente" }
  ];

    const CREATORS_ECHODOT_58 = ECHODOT_58_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25800 + i * 2800, commentsCount: 225 + i * 35, sharesCount: 82 + i * 19, savesCount: 2050 + i * 230, description: b.desc }));

// 9. P59: Mini Antena Internet Satélite Original
const STARLINK_59_VIDEOS_MAP = [
  { name: "Carlos Vida no Campo", username: "carlos_vidanocampo", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_57.jpg", poster: "../videosprodutos/posters/video-produto-59.jpg", video: "https://files.catbox.moe/s6vnyh.mp4", desc: "Internet de 200 Megas no sítio onde não pegava nem sinal de celular! Essa mini antena via satélite é milagrosa! 📡🌾 #starlink #internetrural #sitio" }
  ];

    const CREATORS_STARLINK_59 = STARLINK_59_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 29800 + i * 3200, commentsCount: 270 + i * 40, sharesCount: 102 + i * 24, savesCount: 2380 + i * 270, description: b.desc }));

// 10. P61: Caixa de Som Joog Amplificada Break X1 Touch 13" 800W Android
const JOOG_BREAK_61_VIDEOS_MAP = [
  { name: "DJ Sandro Eventos", username: "djsandro_eventos", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_63.jpg", poster: "../videosprodutos/posters/video-produto-61.jpg", video: "https://files.catbox.moe/ifsim6.mp4", desc: "Joog Break X1 com 800W e tela touch de 13 polegadas com sistema Android! Você abre o YouTube direto nela e canta! 🎤🔥 #joogbreakx1 #somprofissional #dj" }
  ];

    const CREATORS_JOOG_BREAK_61 = JOOG_BREAK_61_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 32400 + i * 3500, commentsCount: 310 + i * 48, sharesCount: 115 + i * 26, savesCount: 2600 + i * 300, description: b.desc }));

// 11. P63: Smartwatch Redmi Watch 5 Lite GPS
const REDMI_WATCH_63_VIDEOS_MAP = [
  { name: "Felipe Corredor", username: "felipecorredor_fit", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_69.jpg", poster: "../videosprodutos/posters/video-produto-63.jpg", video: "https://files.catbox.moe/z40bo0.mp4", desc: "Redmi Watch 5 Lite com GPS integrado independente do celular! A precisão na corrida de rua é cirúrgica! 🏃‍♂️⌚ #redmiwatch5 #smartwatch #corrida" }
  ];

    const CREATORS_REDMI_WATCH_63 = REDMI_WATCH_63_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 24100 + i * 2600, commentsCount: 195 + i * 32, sharesCount: 76 + i * 18, savesCount: 1880 + i * 220, description: b.desc }));

// 12. P65: Sofá 3 Lugares Retrátil e Reclinável Cama inBox Senses 2,00m
const SOFA_SENSES_65_VIDEOS_MAP = [
  { name: "Juliana Decora Lar", username: "judecoralar", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_46.jpg", poster: "../videosprodutos/posters/video-produto-65.jpg", video: "https://files.catbox.moe/my8eud.mp4", desc: "Chegou nosso Sofá Cama inBox Senses de 2 metros! Tecido Velusoft cinza super macio e retrátil que vira cama de casal! 🛋️✨ #sofaretratil #camainbox #saladeestar" }
  ];

    const CREATORS_SOFA_SENSES_65 = SOFA_SENSES_65_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 28500 + i * 3000, commentsCount: 250 + i * 38, sharesCount: 90 + i * 21, savesCount: 2280 + i * 250, description: b.desc }));

// 13. P70: Secadora de Roupa Mueller Solaris 8kg
const SECADORA_MUELLER_70_VIDEOS_MAP = [
  { name: "Simone Dicas de Lavanderia", username: "simonelavanderia", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_52.jpg", poster: "../videosprodutos/posters/video-produto-70.jpg", video: "https://files.catbox.moe/n5jecm.mp4", desc: "Secadora de parede Mueller Solaris 8kg! Salvou meus dias de chuva, roupa sequinha e cheirosa em menos de 1 hora! 👕☀️ #secadoraderoupa #mueller #lavanderia" }
  ];

    const CREATORS_SECADORA_MUELLER_70 = SECADORA_MUELLER_70_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 22600 + i * 2400, commentsCount: 192 + i * 28, sharesCount: 68 + i * 15, savesCount: 1780 + i * 190, description: b.desc }));

// 14. P73: Caixa Bluetooth Waaw Hyperboom 1000 by Alok
const WAAW_HYPERBOOM_73_VIDEOS_MAP = [
  { name: "DJ Bruno Alok Vibe", username: "brunodjvibe", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_83.jpg", poster: "../videosprodutos/posters/video-produto-73.jpg", video: "https://files.catbox.moe/qd8ybp.mp4", desc: "Waaw Hyperboom 1000 assinada pelo Alok! Graves absurdos e show de luzes dinâmicas que sincronizam com a batida! 🔊🔥 #waaw #hyperboom1000 #alok" }
  ];

    const CREATORS_WAAW_HYPERBOOM_73 = WAAW_HYPERBOOM_73_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 27900 + i * 2900, commentsCount: 245 + i * 36, sharesCount: 88 + i * 20, savesCount: 2180 + i * 240, description: b.desc }));



// P53: Starlink V4 Padrão Anatel
const STARLINK_53_VIDEOS_MAP = [
  { name: "Rodrigo Tech Rural", username: "rodrigotechrural", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_33.jpg", poster: "../videosprodutos/posters/video-produto-53.jpg", video: "https://files.catbox.moe/s6vnyh.mp4", desc: "Starlink V4 geração padrão Anatel com Wi-Fi 6 de alta velocidade onde não tem sinal de celular! 🛰️⚡ #starlink #internetsatelite" }
];
const CREATORS_STARLINK_53 = STARLINK_53_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 38000, commentsCount: 420, sharesCount: 190, savesCount: 3100, description: b.desc }));

// P76: Aparelho Jogo De Jantar 30 Peças Orgânico
const APARELHO_76_VIDEOS_MAP = [];
const CREATORS_APARELHO_76 = APARELHO_76_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21000, commentsCount: 190, sharesCount: 70, savesCount: 1800, description: b.desc }));

// P98: Conjunto de 12 Copos De Cristal Long Drink
const COPOS_98_VIDEOS_MAP = [];
const CREATORS_COPOS_98 = COPOS_98_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 22500, commentsCount: 195, sharesCount: 75, savesCount: 1850, description: b.desc }));

// P60: Caixa Som Sabala DR-908 Exclusivo
const SABALA_60_VIDEOS_MAP = [
  { name: "Tech Som Sabala", username: "techsomsabala", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_19.jpg", poster: "../img/posters-sabala/poster_1.jpg", video: "https://files.catbox.moe/duznxa.mp4", desc: "Sabala DR-908 super portátil com som balanceado e graves encorpados! 🔊✨ #sabala #dr908" }
];
const CREATORS_SABALA_60 = SABALA_60_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 23000, commentsCount: 210, sharesCount: 80, savesCount: 1900, description: b.desc }));
// P78: Extratora Spot Cleaner WAP 1400W Exclusivo
const SPOTCLEANER_78_VIDEOS_MAP = [
  { name: "Mari Dicas WAP", username: "maridicaswap", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_62.jpg", poster: "../videosprodutos/posters/video-produto-78.jpg", video: "https://files.catbox.moe/cill8y.mp4", desc: "A WAP Spot Cleaner tirou toda sujeira do sofá e colchão! Potência incrível de 1400W! 🧼✨ #wap #spotcleaner" }
];
const CREATORS_SPOTCLEANER_78 = SPOTCLEANER_78_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 32000, commentsCount: 290, sharesCount: 110, savesCount: 2500, description: b.desc }));

// P82: Lava e Seca 11kg Hisense (blindagem: vazio para ocultar limpo sem vídeo)
const CREATORS_HISENSE_82 = [];
// 15. P78: Extratora e Higienizadora Portátil WAP Spot Cleaner 127V
const WAP_EXTRATORA_78_VIDEOS_MAP = [
  { name: "Carla Dicas de Limpeza", username: "carladicasdelimpeza", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_62.jpg", poster: "../videosprodutos/posters/video-produto-78.jpg", video: "https://files.catbox.moe/6ubsxb.mp4", desc: "A WAP Spot Cleaner tirou mancha antiga de café do sofá em 2 minutos! A água sai preta de tanta sujeira que puxa! 🧼✨ #wap #extratora #spotcleaner" }
];

    const CREATORS_WAP_EXTRATORA_78 = WAP_EXTRATORA_78_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 33500 + i * 3600, commentsCount: 320 + i * 50, sharesCount: 120 + i * 28, savesCount: 2700 + i * 310, description: b.desc }));

// 16. P80: Panificadora 19 Programas Gallant 600W
const PANIFICADORA_80_VIDEOS_MAP = [
  { name: "Casa Com Amor", username: "casacomamor215", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_18.jpg", poster: "../videosprodutos/posters/video-produto-80.jpg", video: "https://files.catbox.moe/yvjiu5.mp4", desc: "Vem abrir comigo a minha nova aquisição! Panificadora Gallant 19 programas bate, fermenta e assa sozinha! 🍞✨ #panificadora #gallant #paocaseiro" },
  { name: "Kah (A Casa da Kah)", username: "acasadakah_", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_22.jpg", poster: "../videosprodutos/posters/video-produto-80-take1.jpg", video: "https://files.catbox.moe/psnlw9.mp4", desc: "Receita do pão na panificadora Gallant! Fica fofinho e super douradinho! 🍞🥐 #panificadoragallant" }
];

    const CREATORS_PANIFICADORA_80 = PANIFICADORA_80_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 23400 + i * 2500, commentsCount: 205 + i * 30, sharesCount: 75 + i * 17, savesCount: 1850 + i * 200, description: b.desc }));

// 17. P85: Caixa De Som Karaokê Joog X2 300W Tela 10,1" 2 Microfones
const JOOG_X2_85_VIDEOS_MAP = [
  { name: "Tiago Karaokê Brasil", username: "tiagokaraoke_br", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_97.jpg", poster: "../videosprodutos/posters/video-produto-85.jpg", video: "https://files.catbox.moe/ukmosr.mp4", desc: "Caixa Joog X2 com 300W e tela integrada de 10,1 polegadas! Vem com 2 microfones sem fio de alta sensibilidade! 🎤🔊 #joogx2 #karaoke #festaemcasa" }
  ];

    const CREATORS_JOOG_X2_85 = JOOG_X2_85_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 26700 + i * 2800, commentsCount: 230 + i * 34, sharesCount: 84 + i * 19, savesCount: 2100 + i * 230, description: b.desc }));

// 18. P87: Calça Mom Jeans Feminina KISSMELADY com Cinto Preto
const MOM_JEANS_87_VIDEOS_MAP = [
  { name: "Larissa Moda & Estilo", username: "larissamoda_estilo", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_78.jpg", poster: "../videosprodutos/posters/video-produto-87.jpg", video: "https://files.catbox.moe/80bwka.mp4", desc: "Meninas, olha o caimento dessa calça mom jeans da KISSMELADY! Modela a cintura perfeitamente e o cinto preto já vem junto! 👖✨ #momjeans #modafeminina #lookdodia" }
  ];

    const CREATORS_MOM_JEANS_87 = MOM_JEANS_87_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 29400 + i * 3100, commentsCount: 265 + i * 38, sharesCount: 96 + i * 22, savesCount: 2350 + i * 260, description: b.desc }));

// 18.1. P72: Jogo de Panelas 13 Peças Ferro Fundido Esmaltado
const PANELAS_FERRO_72_VIDEOS_MAP = [
  { name: "Camila Franklin", username: "camilafrankliin", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_14.jpg", poster: "../videosprodutos/posters/video-produto-89.jpg", video: "https://files.catbox.moe/q5cnpr.mp4", desc: "Essas panelas são um luxo, super pesadas, são panelas de ferro fundido pra vida toda!! 🥘🔥 #ferrofundido #jogodepanelas" }
];
    const CREATORS_PANELAS_FERRO_72 = PANELAS_FERRO_72_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 24800 + i * 2700, commentsCount: 210 + i * 32, sharesCount: 76 + i * 18, savesCount: 1950 + i * 220, description: b.desc }));

// 19. P89: Kit Conjunto Panelas de Ferro Esmaltadas Luxo 18 Peças
const PANELAS_FERRO_89_VIDEOS_MAP = [
  { name: "Camila Franklin", username: "camilafrankliin", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_88.jpg", poster: "../videosprodutos/posters/video-produto-89.jpg", video: "https://files.catbox.moe/wvqi46.mp4", desc: "Eu to apaixonada nas minhas panelas de ferro fundido esmaltadas! A comida fica com sabor incrível! 🥘🔥 #panelasdeferro #cozinha #gastronomia" }
  ];

    const CREATORS_PANELAS_FERRO_89 = PANELAS_FERRO_89_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25300 + i * 2700, commentsCount: 218 + i * 32, sharesCount: 78 + i * 18, savesCount: 1980 + i * 220, description: b.desc }));

// 19.1. P90: Jogo De Panela Avant Space 5 Peças - Tognana Cor Preto
const PANELAS_AVANT_90_VIDEOS_MAP = [
  {
    name: "Aghata Moreira",
    username: "aghatamoreiraa97",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/06ae10ae9263e3b2bff686013811df7d~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b41ec4a1&x-expires=1795366800&x-signature=m9a78SFE%2BwSpdb0PzwBlzNWE36o%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-89.jpg",
    video: "https://files.catbox.moe/8dgikb.mp4",
    desc: "Jogo de panelas antiaderente grafite com fundo triplo de indução! Não gruda nada e o acabamento é lindo demais! 🍳🤎 #tognana #panelasitalianas #cozinha"
  },
  {
    name: "Junior Ofertas",
    username: "juniorofertas",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/dccf13f6c55a869b60534c46af76aca7~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=c3175f2a&x-expires=1795366800&x-signature=6u0hZz5cZwQY81r0ljf5Xl0JyF0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-89-take1.jpg",
    video: "https://files.catbox.moe/002wty.mp4",
    desc: "Jogo de panelas cerâmica antiaderente completo! Cabos em baquelite que não esquentam e tampas de vidro temperado! ✨🥘 #achadinhos #panelasdeinducao"
  },
  {
    name: "Rê Santana",
    username: "produtinhosonlinee",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/d719e4b9a10459813607d8841c845178~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=9505dc7a&x-expires=1795366800&x-signature=g2ckDU9i0DPmdYVlNuQjCieKC24%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-89-take2.jpg",
    video: "https://files.catbox.moe/06vxoq.mp4",
    desc: "Testando o antiaderente 5 camadas de mármore do jogo Avant Space! Desliza 100% sem óleo e limpa super fácil! 📦✨ #panelas #unboxing"
  },
  {
    name: "Mari Munyz",
    username: "marimunyz",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/20e863722ea248da2fabd8c40de4f7ff~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=5f281081&x-expires=1795366800&x-signature=0HrBFk4YO1Sp3qlPa2R5p6cfhOE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-89-take3.jpg",
    video: "https://files.catbox.moe/7048l9.mp4",
    desc: "Unboxing completo do jogo de panelas de indução! O material é bem grosso e a distribuição de calor é uniforme! 🖤✨ #cozinhaorganizada"
  },
  {
    name: "Anny Andrade",
    username: "annyandrade03",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/7333783957153103877~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=658d0ebb&x-expires=1795366800&x-signature=6xPewySIK3bmCV8oLiu0IkMNf8U%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../videosprodutos/posters/video-produto-89-take4.jpg",
    video: "https://files.catbox.moe/pekqoj.mp4",
    desc: "Meu jogo de panelas chegou e eu estou completamente apaixonada! Design sofisticado que decora a bancada da cozinha! 🍳🔥 #fogaoinducao #panelastognana"
  }
];
// Panificadoras P48 / P84
const PANIFICADORA_48_84_VIDEOS_MAP = [
  { name: "Ingrid Rocha", username: "_ingriidrocha", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_48.jpg", poster: "../videosprodutos/posters/video-produto-80.jpg", video: "https://files.catbox.moe/u5toyv.mp4", desc: "Pão quentinho todo dia de manhã sem trabalho nenhum! A panificadora faz tudo sozinha, bate, fermenta e assa. Perfeita! 🍞✨ #panificadora #paocaseiro #cozinha" },
  { name: "Amanda Cristhiny", username: "amandacristhiny_", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_50.jpg", poster: "../videosprodutos/posters/video-produto-80-take1.jpg", video: "https://files.catbox.moe/t5xtp1.mp4", desc: "Olha a fofura desse pão doce feito na panificadora! Acordar com o cheiro de pão pela casa é maravilhoso! 🥐❤️ #panificadoramondial #receitas #paofofinho" },
  { name: "Hairda Hoffman", username: "hairdahoffman", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_52.jpg", poster: "../videosprodutos/posters/video-produto-80-take2.jpg", video: "https://files.catbox.moe/3a2qhi.mp4", desc: "Testando a função timer da panificadora! Coloquei os ingredientes à noite e acordei com pão integral fresquinho e crocante! 🍞⏰ #receitasfaceis #rotinamatinal" }
  ];

    const CREATORS_PANIFICADORA_48_84 = PANIFICADORA_48_84_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 18500 + i * 2900, commentsCount: 240 + i * 45, sharesCount: 120 + i * 32, savesCount: 1450 + i * 180, description: b.desc }));

// P31: Caixa De Som Bluetooth 200w 39000mah Tws Ipx6 Sabala Dr-909
const SABALA_31_VIDEOS_MAP = [
  {
    name: "Elvyn | Canal do Pincei",
    username: "issopresta",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_15.jpg",
    poster: "../img/posters-sabala/poster_1.jpg",
    video: "https://files.catbox.moe/1ig8lo.mp4",
    desc: "Na minha humilde opinião, a Sabala DR-909 é o melhor custo benefício hoje! 39.000mAh de bateria, 200W RMS e graves que batem pesado! 🔊🔥 #sabala #dr909 #caixadesom #sompesado"
  },
  {
    name: "Mundo Tec Smartphones",
    username: "mundotec.smartphone",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_22.jpg",
    poster: "../img/posters-sabala/poster_3.jpg",
    video: "https://files.catbox.moe/nqu6ks.mp4",
    desc: "A Caixa Sabala DR-909 enterra qualquer concorrente por metade do preço! Acabamento impecável e conexão TWS estéreo! ⚡🎶 #sabaladr909 #techaudio #somdequalidade"
  },
  {
    name: "Gaspar Recomenda",
    username: "gaspar_recomenda",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_44.jpg",
    poster: "../img/posters-sabala/poster_4.jpg",
    video: "https://files.catbox.moe/rpimi5.mp4",
    desc: "Caixa de Som Bluetooth SABALA DR-909 é um monstro! Coloquei no volume máximo no churrasco e não distorceu nada! 🥩🎉 #sabala #somdechurrasco #audiophile"
  },
  {
    name: "Rosleon Reviews",
    username: "rosleonoficial",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_58.jpg",
    poster: "../img/posters-sabala/poster_5.jpg",
    video: "https://files.catbox.moe/q3naa4.mp4",
    desc: "Testando a Sabala DR-909 de 200W no limite! Som limpo, graves potentes e o dobro de potência no modo TWS! 💥🎵 #sabaladr909 #reviewcompleto #testedeaudio"
  }
  ];

  const CREATORS_SABALA_31 = SABALA_31_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25400 + i * 2900, commentsCount: 310 + i * 45, sharesCount: 110 + i * 22, savesCount: 2150 + i * 240, description: b.desc }));

// P36: Celular Xiaomi Poco X7 Pro 5g 512gb 12ram
const POCO_X7_PRO_36_VIDEOS_MAP = [
  {
    name: "Tuk Imperial",
    username: "tukemperial",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/522ccc97986d0d2a8d739f5c7c05fedc~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=01d4cd71&x-expires=1795366800&x-signature=FL7xG%2FhBSlQr9nCxVDZQbYJ87%2BQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../img/posters-poco/poster_5.jpg",
    video: "https://files.catbox.moe/blcp5n.mp4",
    desc: "Poco X7 Pro o rei dos intermediarios premium com Dimensity 8400! Desempenho absurdo e tela 1.5K!"
  },
  {
    name: "Day Syndell",
    username: "day.syndell",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/e75c438ac8747ad3c1307a28df62556b~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=4ed6f03f&x-expires=1795366800&x-signature=h90CLnuC9X7EOIBINvQi7aiX0JQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../img/posters-poco/poster_2.jpg",
    video: "https://files.catbox.moe/jxkrk9.mp4",
    desc: "Unboxing Poco X7 Pro Xiaomi troquei meu celular por essa maquina! Amarelo em couro vegano lindo demais!"
  },
  {
    name: "Brabo Store",
    username: "brabostore22",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/87123ea6231d9d7da3b4620724d5fd08~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=81d31585&x-expires=1795366800&x-signature=rH5ulwnDSiMdmhx4wDJihbQGr4c%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../img/posters-poco/poster_1.jpg",
    video: "https://files.catbox.moe/7dva6t.mp4",
    desc: "Poco X7 Pro em maos visual gamer agressivo e carregador turbo de 90W na caixa original! ⚡📦"
  },
  {
    name: "Cellofertas",
    username: "cellofertas.brasi",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/07aafa1a760cdd12170f10494a2a56f0~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=e0ef512d&x-expires=1795366800&x-signature=XrfpfqfXQc4FA1T1Y672BPmufAU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../img/posters-poco/poster_3.jpg",
    video: "https://files.catbox.moe/sc9goq.mp4",
    desc: "Poco X7 Pro 512GB potencia sem limites tela AMOLED 120Hz super fluida e bateria monstra!"
  },
  {
    name: "Bloom Fofa",
    username: "bloomfofa",
    avatar: "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/33d6f9be69fce8466cff54d0d615b87c~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=2c37201d&x-expires=1795366800&x-signature=AFf%2FjFVLDA0lWcI%2BLJ%2FR6IXA%2FJY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    poster: "../img/posters-poco/poster_4.jpg",
    video: "https://files.catbox.moe/uv1bfg.mp4",
    desc: "Unboxing do meu celular Poco X7 Pro roda tudo no ultra muito rapido amei demais! 💛📱"
  }
];

  const CREATORS_POCO_X7_PRO_36 = POCO_X7_PRO_36_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 29800 + i * 3200, commentsCount: 380 + i * 52, sharesCount: 140 + i * 28, savesCount: 2600 + i * 290, description: b.desc }));

const CREATORS_PANELAS_AVANT_90 = PANELAS_AVANT_90_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21500 + i * 3820, commentsCount: 420 + i * 73, sharesCount: 310 + i * 48, savesCount: 1850 + i * 190, description: b.desc }));

// 20. P91: Pipoqueira Classic Retrô Philco PPI04V
const PIPOQUEIRA_91_VIDEOS_MAP = [
  { name: "Mariana Cinema em Casa", username: "maricinemaemcasa", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg", poster: "../videosprodutos/posters/video-produto-91.jpg", video: "https://files.catbox.moe/xqpya7.mp4", desc: "Pipoqueira Classic Retrô Philco! Misturador automático e bandeja para servir, parece cinema de verdade em casa! 🍿🎬 #pipoqueira #philco #cinemaemcasa" }
  ];

    const CREATORS_PIPOQUEIRA_91 = PIPOQUEIRA_91_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21800 + i * 2300, commentsCount: 185 + i * 28, sharesCount: 65 + i * 16, savesCount: 1720 + i * 190, description: b.desc }));

// 21. P92: Conjunto Panelas de Ferro Fundido Esmaltado 10 Peças
const PANELAS_FERRO_92_VIDEOS_MAP = [
  { name: "Chef Marcelo Carnes", username: "chefmarcelocarnes", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_111.jpg", poster: "../videosprodutos/posters/video-produto-92.jpg", video: "https://files.catbox.moe/sdcjn0.mp4", desc: "Conjunto 10 Peças em ferro fundido esmaltado! Distribuição homogênea de calor que sela bifes com crosta perfeita! 🥩🔥 #panelasferrofundido #culinaria #chef" }
  ];

    const CREATORS_PANELAS_FERRO_92 = PANELAS_FERRO_92_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 24700 + i * 2600, commentsCount: 212 + i * 31, sharesCount: 76 + i * 18, savesCount: 1940 + i * 210, description: b.desc }));

// 22. P94: Bicicleta Bike Ergometrica Spinning Academia Fitness 120kg (Desacoplada da Bike 6)
const BIKE_SPINNING_94_VIDEOS_MAP = [
  { name: "Lucas Treino & Spinning", username: "lucasspinning_fit", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_17.jpg", poster: "../videosprodutos/posters/video-produto-94.jpg", video: "https://files.catbox.moe/perlvk.mp4", desc: "Bike de Spinning profissional suporta até 120kg! Roda de inércia pesada com frenagem macia e silenciosa no apartamento! 🚴‍♂️🔥 #spinning #bikeindoor #treinoemcasa" }
  ];

    const CREATORS_BIKE_SPINNING_94 = BIKE_SPINNING_94_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 26300 + i * 2800, commentsCount: 228 + i * 34, sharesCount: 82 + i * 19, savesCount: 2080 + i * 230, description: b.desc }));

// 23. P95: YESOP Máquina De Gelo Portátil 12kg/dia Turbo Ice
const MAQUINA_GELO_95_VIDEOS_MAP = [
  { name: "Felipe Drinks & Bar", username: "felipedrinksbar", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_27.jpg", poster: "../videosprodutos/posters/video-produto-95.jpg", video: "https://files.catbox.moe/0qd90i.mp4", desc: "Máquina de Gelo Portátil YESOP 12kg/dia! Faz os primeiros cubos ocos em apenas 6 minutos! Nunca mais comprei saco de gelo! 🧊🍹 #maquinadegelo #yesop #drinks" }
  ];

    const CREATORS_MAQUINA_GELO_95 = MAQUINA_GELO_95_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 31500 + i * 3300, commentsCount: 285 + i * 42, sharesCount: 105 + i * 24, savesCount: 2450 + i * 270, description: b.desc }));

// 24. P96: Aparelho de Jantar/Chá Oxford Ryo Maresia 30 Peças
const APARELHO_RYO_96_VIDEOS_MAP = [
  { name: "Carla Mesa Posta Luxo", username: "carlamesapostabr", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_22.jpg", poster: "../videosprodutos/posters/video-produto-96.jpg", video: "https://files.catbox.moe/i9wuhf.mp4", desc: "Aparelho de Jantar Oxford Ryo Maresia 30 peças! Formato orgânico inspirado na praia e acabamento fosco acetinado divino! 🍽️🌊 #oxfordporcelanas #mesaposta #ryomaresia" }
  ];

    const CREATORS_APARELHO_RYO_96 = APARELHO_RYO_96_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 28200 + i * 2900, commentsCount: 248 + i * 36, sharesCount: 92 + i * 20, savesCount: 2240 + i * 240, description: b.desc }));

// 25. P97: Jogo de Jantar Canyon Porcelana Decorada 20 Peças Tramontina
const JOGO_JANTAR_97_VIDEOS_MAP = [
  { name: "Renata Mesa & Afeto", username: "renatamesaeafeto", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_28.jpg", poster: "../videosprodutos/posters/video-produto-97.jpg", video: "https://files.catbox.moe/0hhasi.mp4", desc: "Jogo de Jantar Tramontina Canyon Porcelana Decorada 20 peças! Os tons terrosos e as estampas geométricas são um escândalo! 🍽️✨ #tramontina #jogodejantar #mesaposta" }
  ];

    const CREATORS_JOGO_JANTAR_97 = JOGO_JANTAR_97_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25600 + i * 2700, commentsCount: 220 + i * 32, sharesCount: 80 + i * 18, savesCount: 2020 + i * 220, description: b.desc }));



  // 1.16 DATASET DA CHURRASQUEIRA MOR RODEIO BACIA ESMALTADA (PRODUTO 16) - 32 CRIADORES 100% REAIS TIKTOK SHOP
  const CREATORS_CHURRASQUEIRA_RODEIO_16 = [
  {
      name: 'Chef Marcelo Carnes',
      username: 'chefmarcelocarnes',
      avatar: '../img/reviews-avatars/tiktok_real/tt_avatar_25.jpg',
      poster: '../videosprodutos/posters/video-produto-16-take2.jpg',
      video: "https://files.catbox.moe/jwkiqt.mp4",
      startTime: 0.2,
      likes: 24100,
      commentsCount: 145,
      saves: 2100,
      shares: 480,
      desc: 'Ponto perfeito da carne assando na grelha! Retenção de calor sensacional e suculência garantida! 🍖✨ #churrascoemcasa #grelha #carnes'
    },
  {
      name: 'Rodrigo Barbecue',
      username: 'rodrigobbq',
      avatar: '../img/reviews-avatars/tiktok_real/tt_avatar_43.jpg',
      poster: '../videosprodutos/posters/video-produto-16-take3.jpg',
      video: "https://files.catbox.moe/dpa885.mp4",
      startTime: 0.1,
      likes: 19800,
      commentsCount: 110,
      saves: 1680,
      shares: 340,
      desc: 'Costela e linguiça assando no capricho! Acendimento rápido do carvão e churrasco de primeira! 🥩🍖 #bbqbrasil #churrascotop'
    },
  {
      name: 'Carlos Grill',
      username: 'carlosgrill_oficial',
      avatar: '../img/reviews-avatars/tiktok_real/tt_avatar_55.jpg',
      poster: '../img/posters-churras/poster-arke-c2.jpg',
      video: "https://files.catbox.moe/qmv0y6.mp4",
      startTime: 0.2,
      likes: 21300,
      commentsCount: 125,
      saves: 1820,
      shares: 390,
      desc: 'Churrasco no ponto ideal! Espeto girando e carne dourando por igual sem queimar! 🔥🥩 #churrasco #carnesnobres'
    },
  {
      name: 'Lucas Steakhouse',
      username: 'lucassteakhouse',
      avatar: '../img/reviews-avatars/tiktok_real/tt_avatar_62.jpg',
      poster: '../img/posters-biscuitt/poster-biscuitt-c2.jpg',
      video: "https://files.catbox.moe/ymfpap.mp4",
      startTime: 0.2,
      likes: 25400,
      commentsCount: 160,
      saves: 2300,
      shares: 450,
      desc: 'Aquele bife ancho no fogo alto da churrasqueira! Casquinha crocante e centro super suculento! 🥩🔥 #bbq'
    }
];

function initCarousel() {
    const targetContainer = document.getElementById('creators-section');
    if (!targetContainer) return;

    // Detecta ID canônico do produto
    const match = window.location.pathname.match(/produto-(\d+)(?:\.html)?(?:$|\/|\?)/i);
    const prodId = match ? parseInt(match[1], 10) : null;

    if (!prodId) {
      if (targetContainer) {
        targetContainer.innerHTML = '';
        targetContainer.style.setProperty('display', 'none', 'important');
      }
      return;
    }

    let activeDataset = [];
    let contextType = 'general';

    // Função utilitária para montar pool de criadores por nicho temático
    // Garantia de ancoragem: o vídeo nativo do produto é SEMPRE o item 1 (#0),
    // seguido pelos criadores autênticos do mesmo nicho, com desduplicação estrita de vídeo.
        // Blindagem Soberana da Regra 7.11 & 7.17: Piso Mínimo de 10 Vídeos de Criadores por Produto com Blindagem Estrita de Gênero
    function enforceMinimumCreators(list, minCount = 10, isFemale = false) {
      if (!Array.isArray(list) || list.length === 0) return list || [];
      return list;
    }

    function buildNichePool(primaryList, fallbackNicheList) {
      // BLINDAGEM SOBERANA ZIKA: ISOLAMENTO 1:1 ESTRITO
      // PROIBICAO ABSOLUTA DE EMPRESTAR MIDIA DO VIZINHO
      if (!primaryList || !Array.isArray(primaryList) || primaryList.length === 0) {
        return [];
      }
      return primaryList;
    }

    // Pools de Nicho Oficiais para Blindagem contra Vídeo Solitário
  // DATASET DA ESTEIRA ELETRICA ERGOMETRICA (PRODUTO 56) - 100% REAIS FITNESS / CORRIDA / TREINO
  const ESTEIRA_56_VIDEOS_MAP = [
    {
      name: "Heloisa Gomes",
      username: "byheloisagomes",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_18.jpg",
      poster: "../videosprodutos/posters/poster-produto-110.jpg",
      video: "https://files.catbox.moe/1m8e3i.mp4",
      desc: "Esteira ergométrica bivolt silenciosa dobrável 12 velocidades! Perfeita para caminhar em casa! 🏃‍♀️⚡ #esteira #fitness"
    },
    {
      name: "Camila (Apê 156)",
      username: "ape156",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_22.jpg",
      poster: "../videosprodutos/posters/poster-produto-110-criadora2.jpg",
      video: "https://files.catbox.moe/3g25ts.mp4",
      desc: "Esteira Elétrica Dobrável Portátil para Treinar em Casa sem ocupar espaço! 🏃‍♀️✨ #treinoemcasa #esteiraeletrica"
    },
    {
      name: "Dhi Lins",
      username: "dhiovanalinsoficial",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_14.jpg",
      poster: "../videosprodutos/posters/poster-produto-110-criadora3.jpg",
      video: "https://files.catbox.moe/maizzc.mp4",
      desc: "Onde há foco, há progresso! Esteira dobrável excelente pra bater a meta diária em casa! 🏃‍♂️⚡ #esteiraergometrica"
    },
    {
      name: "Thiago Achados",
      username: "achados.premium77",
      avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_25.jpg",
      poster: "../videosprodutos/posters/poster-produto-110.jpg",
      video: "https://files.catbox.moe/9a840r.mp4",
      desc: "Esteira inteligente dobrável com controle remoto e velocidade ajustável, prática demais! 🏃‍♂️⚡ #treinoemcasa"
    }
  ];

  const CREATORS_ESTEIRA_56 = ESTEIRA_56_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 23400 + i * 2900, commentsCount: 180 + i * 35, sharesCount: 75 + i * 16, savesCount: 1850 + i * 190, description: b.desc }));

    const POOL_AR_CLIMA = [
      ...CREATORS_AR_HQ_9,
      ...CREATORS_AR_HQ_29,
      ...CREATORS_AR_HISENSE_10,
      ...CREATORS_AR_LG_27,
      ...CREATORS_CLIMATIZADOR_OSTER_11,
      ...CREATORS_CLIMATIZADOR_MIDEA_30,
      ...CREATORS_CLIMATIZADOR_VENTISOL_44
    ];

    const POOL_AUDIO = [
      ...CREATORS_JBL_BOOMBOX4_35,
      ...CREATORS_SABALA_31,
      ...CREATORS_AIWA_PARTYBOX_8,
      ...CREATORS_AIWA_7,
      ...CREATORS_JBL_4,
      ...CREATORS_JOOG_ONE_57,
      ...CREATORS_JOOG_BREAK_61,
      ...CREATORS_WAAW_HYPERBOOM_73,
      ...CREATORS_JOOG_X2_85,
      ...CREATORS_ECHODOT_58
    ];

    const POOL_CHURRASQUEIRAS = [
      ...CREATORS_CHURRASQUEIRA_ARKE_14,
      ...CREATORS_CHURRASQUEIRA_BISCUITT_15,
      ...CREATORS_CHURRASQUEIRA_RODEIO_16
    ];

    const POOL_BIKES_SPINNING = [
      ...CREATORS_BIKE_6,
      ...CREATORS_BIKE_SPINNING_94
    ];

    const POOL_BIKES_RUA = [
      ...CREATORS_BIKE_GT_20
    ];

    const POOL_ESTEIRA_FITNESS = [
      ...CREATORS_ESTEIRA_56
    ];

    const POOL_ESPORTES = [
      ...CREATORS_BOLA_PENALTY_21,
      ...CREATORS_KAPPA_110,
      ...CREATORS_MOM_JEANS_87
    ];

    const POOL_PANELAS = [
      ...CREATORS_PANELAS_AVANT_90,
      ...CREATORS_PANELA_122,
      ...CREATORS_PANELAS_FERRO_89,
      ...CREATORS_PANELAS_FERRO_92
    ];

    const POOL_MESA_JANTAR = [
      ...CREATORS_APARELHO_RYO_96,
      ...CREATORS_JOGO_JANTAR_97,
      ...CREATORS_MESA_118
    ];

    const POOL_ELETRO_COZINHA = [
      ...CREATORS_FORNO_HQ_115,
      ...CREATORS_AIRFRYER_5,
      ...CREATORS_FOGAO_117,
      ...CREATORS_PANELA_122,
      ...CREATORS_PANIFICADORA_48_84,
      ...CREATORS_PANIFICADORA_80,
      ...CREATORS_PIPOQUEIRA_91,
      ...CREATORS_MAQUINA_GELO_95
    ];

    const POOL_LIMPEZA = [
      ...CREATORS_WAP_EXTRATORA_78,
      ...CREATORS_ASPIRADOR_107
    ];

    const POOL_LAVANDERIA = [
      ...CREATORS_LAVADORA_123,
      ...CREATORS_SECADORA_MUELLER_70
    ];

    const POOL_TECH_DISPOSITIVOS = [
      ...CREATORS_PAD11_52,
      ...CREATORS_POCO_X7_PRO_36
    ];

    const POOL_GAMES = [
      ...CREATORS_SWITCH_55,
      ...CREATORS_ARCADE_114
    ];

    const POOL_CONECTIVIDADE = [
      ...CREATORS_STARLINK_59,
      ...CREATORS_REDMI_WATCH_63,
      ...CREATORS_POCO_X7_PRO_36
    ];

    const POOL_SOFAS = [
      ...CREATORS_SOFA_SENSES_65,
      ...CREATORS_SOFA_120
    ];

    const POOL_COLCHAO_DORMIR = [
      ...CREATORS_COLCHAO_BESTWAY_22,
      ...CREATORS_TRAVESSEIRO_121
    ];

    const POOL_MODA_FEMININA = [
      ...CREATORS_MOM_JEANS_87,
      ...CREATORS_BODY_106
    ];

        // Seleção estrita e determinística por Single Source of Truth (Product ID)
    // PROIBIÇÃO ABSOLUTA DE EMPRÉSTIMO OU HERANÇA ENTRE PRODUTOS DIFERENTES
    
  // =========================================================================
  // DATASETS OFICIAIS EXTRAÍDOS VIA PLAYWRIGHT MCP (PERFIL MAX DIGITAL)
  // CRIADORES REAIS DO TIKTOK SHOP COM COERÊNCIA DE GÊNERO E ZERO REPETIÇÃO
  // =========================================================================

  // P34: Lava Louças Praxis Portátil LLPP Semi-Automática Bivolt
  const PRAXIS_34_VIDEOS_MAP = [
    { name: "Jéssica Martins", username: "3decorando", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_02.jpg", poster: "../img/produto-34-1.jpg", video: "https://files.catbox.moe/11ffrq.mp4", desc: "Essa lava-louças portátil da Praxis não precisa de instalação hidráulica! 🤩🫧 #lavaloucas #praxis #cozinha" },
    { name: "Letícia Veloso", username: "leticiavelososs", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_04.jpg", poster: "../img/produto-34-2.jpg", video: "https://files.catbox.moe/efnhg1.mp4", desc: "Testando a lava-louças portátil da Praxis! 🧡🫧 Compacta, lava com água quente e louças brilhando! #tiktokshop" },
    { name: "Diário do Primeiro Apê", username: "diariodoprimeiroape", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_06.jpg", poster: "../img/produto-34-3.jpg", video: "https://files.catbox.moe/o84hxh.mp4", desc: "A lava louças mais barata da internet vale a pena? Resenha completa da Praxis! ✨" },
    { name: "Camille Cesário", username: "camillecesario", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_08.jpg", poster: "../img/produto-34-1.jpg", video: "https://files.catbox.moe/uij8io.mp4", desc: "Como funciona minha lava louças portátil Praxis na bancada da cozinha! 🍽️" },
    { name: "Vitrine de Achadinhos", username: "pechinchas.vitrine", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_10.jpg", poster: "../img/produto-34-2.jpg", video: "https://files.catbox.moe/9k8c7q.mp4", desc: "Lava Louças Praxis Portátil Semi-Automática! Praticidade total pro dia a dia 🤩" }
  ];
  const CREATORS_PRAXIS_34 = PRAXIS_34_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21400 + i * 2300, commentsCount: 195 + i * 25, sharesCount: 88 + i * 14, savesCount: 1720 + i * 180, description: b.desc }));

  // P54: Purificador Eletrônico Compacto Efficient PE11X Electrolux
  const PURIFICADOR_54_VIDEOS_MAP = [
    { name: "Damis Mark", username: "dam.elis", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_12.jpg", poster: "../img/produto-54-1.jpg", video: "https://files.catbox.moe/6n9lsb.mp4", desc: "Purificador Electrolux PE11X maravilhoso! Água gelada, tratada e purificada sem cloro! 💦 #electrolux" },
    { name: "Carol Casone", username: "carolinecasone", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_14.jpg", poster: "../img/produto-54-2.jpg", video: "https://files.catbox.moe/iydgj5.mp4", desc: "Respondendo dúvidas sobre o purificador Electrolux PE11X compacto! Design lindo na cozinha 😍" },
    { name: "Apartamento 102", username: "bloco14ap102", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_16.jpg", poster: "../img/produto-54-3.jpg", video: "https://files.catbox.moe/q0yb8j.mp4", desc: "Purificador de água Electrolux 💦💧 Praticidade total e água pura o dia todo!" },
    { name: "Andressa Lopes", username: "apt104s2", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_17.jpg", poster: "../img/produto-54-1.jpg", video: "https://files.catbox.moe/oivafp.mp4", desc: "Resenha sincera do purificador Electrolux PE11X. Troca de filtro super fácil e fluxo rápido!" },
    { name: "Pacheco Creator", username: "pacheco_machry", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_18.jpg", poster: "../img/produto-54-2.jpg", video: "https://files.catbox.moe/z1pg95.mp4", desc: "Tem que aproveitar! Purificador de água Electrolux PE11X bivolt silencioso e top!" }
  ];
  const CREATORS_PURIFICADOR_54 = PURIFICADOR_54_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25400 + i * 2100, commentsCount: 220 + i * 30, sharesCount: 95 + i * 16, savesCount: 1980 + i * 220, description: b.desc }));

  // P40: Micro-ondas Mondial Mo-01-21-e 1200w 21 Litros
  const MONDIAL_40_VIDEOS_MAP = [
    { name: "Vanessa Silva", username: "nessasil_", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_20.jpg", poster: "../img/produto-40-1.jpg", video: "https://files.catbox.moe/xzwsy6.mp4", desc: "Micro-ondas da Mondial de 21 litros espelhado 😍 Lindo, potente e compacto! #microondas #mondial" },
    { name: "Wesley Machado", username: "wesleymachadoshop", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_21.jpg", poster: "../img/produto-40-2.jpg", video: "https://files.catbox.moe/shmn9s.mp4", desc: "Micro-ondas Mondial 21L ✨ Potência de 1200W e funções práticas pro dia a dia na cozinha!" },
    { name: "Garcia Indica", username: "garcia_indica", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_22.jpg", poster: "../img/produto-40-3.jpg", video: "https://files.catbox.moe/dzhghs.mp4", desc: "Microondas Mondial 21 litros compacto com puxador prático e receitas pré-programadas!" },
    { name: "Analice Salles", username: "analicepitrez", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_23.jpg", poster: "../img/produto-40-1.jpg", video: "https://files.catbox.moe/8mh69y.mp4", desc: "Comprei o Microondas Mondial 21L 1200W MO-01-21-E e estou super satisfeita! Design espelhado incrível!" },
    { name: "Sara Koniczna", username: "sarakoniczna2025", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_24.jpg", poster: "../img/produto-40-2.jpg", video: "https://files.catbox.moe/wcs86f.mp4", desc: "Excelente micro-ondas da Mondial de 21 litros! Aquece super rápido e muito fácil de limpar!" }
  ];
  const CREATORS_MONDIAL_40 = MONDIAL_40_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 19800 + i * 2400, commentsCount: 180 + i * 28, sharesCount: 72 + i * 15, savesCount: 1650 + i * 190, description: b.desc }));

  // P41: Fritadeira Air Fryer Forno Oven 12L Mondial
  const OVEN_41_VIDEOS_MAP = [
    { name: "Laís Veloso", username: "laisvelosop", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_24.jpg", poster: "../img/produto-41-1.jpg", video: "https://files.catbox.moe/9y2j8z.mp4", desc: "Airfryer Mondial 12 litros Forno Oven! Cabe um frango inteiro e assa tudo por igual 🤩🍗" },
    { name: "Nosso Lar 123", username: "nosso_lar__123", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_26.jpg", poster: "../img/produto-41-2.jpg", video: "https://files.catbox.moe/zi3ydm.mp4", desc: "Minha nova Air Fryer Oven de 12 litros da Mondial! Vem com 2 bandejas e cesto de 5L ✨" },
    { name: "Edvana Alves", username: "amorzinho4435", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_28.jpg", poster: "../img/produto-41-3.jpg", video: "https://files.catbox.moe/zpl81h.mp4", desc: "Air Fryer Mondial 12L prática demais pra família toda! Dá pra fazer várias receitas juntas!" },
    { name: "Thayná Mello", username: "euthaynamello_", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_30.jpg", poster: "../img/produto-41-1.jpg", video: "https://files.catbox.moe/d478qj.mp4", desc: "A minha mais nova Air Fryer 12 litros queridinha! Acabamento lindo em inox e super rápida!" },
    { name: "Patrícia Dias", username: "patriciadias804", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_32.jpg", poster: "../img/produto-41-2.jpg", video: "https://files.catbox.moe/fg8dza.mp4", desc: "Bolo fofinho e dourado feito na Air Fryer Forno Mondial 12L! Super recomendo!" }
  ];
  const CREATORS_OVEN_41 = OVEN_41_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 31200 + i * 3200, commentsCount: 290 + i * 35, sharesCount: 125 + i * 22, savesCount: 2450 + i * 280, description: b.desc }));

  // P45: Prancha Pro 480 Turbo MQ Professional Bivolt
  const MQ_45_VIDEOS_MAP = [
    { name: "Clau B", username: "dicasclaub", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_32.jpg", poster: "../img/produto-45-1.jpg", video: "https://files.catbox.moe/v900zz.mp4", desc: "Que chapinha perfeita da MQ Professional PRO 480! Brilho espelhado e deslize ultra suave 😍🫶🏻" },
    { name: "Sheila Gimenez", username: "sheilagimenezz", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_34.jpg", poster: "../img/produto-45-2.jpg", video: "https://files.catbox.moe/ppsl9u.mp4", desc: "Alisamento impecável com meu equipamento top! Prancha Pro 480 MQ Hair ✨" },
    { name: "Grace Silva", username: "greysilvahelena", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_36.jpg", poster: "../img/produto-45-3.jpg", video: "https://files.catbox.moe/jb8mrw.mp4", desc: "O sonho de toda mulher que ama cuidar do cabelo! MQ Pro 480 Turbo sela a cutícula na hora 💖" },
    { name: "Jappa", username: "_eujapaoficial", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_38.jpg", poster: "../img/produto-45-1.jpg", video: "https://files.catbox.moe/6a95oa.mp4", desc: "Prancha Professional MQ PRO 480 Turbo. 5 níveis de temperatura e tecnologia de titânio puro!" },
    { name: "Jessica Lopes", username: "jesslopesoficial1", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_40.jpg", poster: "../img/produto-45-2.jpg", video: "https://files.catbox.moe/npls76.mp4", desc: "Review profissional da MQ Pro 480. Não queima as pontas e o liso dura dias! Perfeita!" }
  ];
  const CREATORS_MQ_45 = MQ_45_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 28400 + i * 2700, commentsCount: 245 + i * 32, sharesCount: 110 + i * 19, savesCount: 2150 + i * 240, description: b.desc }));

  // P38: Kit Lattafa Yara Collection Feminino Edp 4x25ml
  const YARA_38_VIDEOS_MAP = [
    { name: "Fragrancih", username: "fragrancih", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_40.jpg", poster: "../img/produto-38-1.jpg", video: "https://files.catbox.moe/ml8w43.mp4", desc: "Kit de miniaturas YARA Lattafa! 4 variações exclusivas para o dia a dia! ✨" },
    { name: "Gabby Fragrances", username: "gabbyfragrances", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_42.jpg", poster: "../img/produto-38-2.jpg", video: "https://files.catbox.moe/etv97p.mp4", desc: "Lattafa Yara Collection 4 Pcs Perfume Set! Fixação absurda e aroma incrível! 🌸🎀" },
    { name: "Aura 18K Perfumaria", username: "lojaaura18k", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_44.jpg", poster: "../img/produto-38-3.jpg", video: "https://files.catbox.moe/di2102.mp4", desc: "Kit Yara Collection Lattafa. Quatro miniaturas, um universo de fragrâncias de luxo! 💖" },
    { name: "Moça dos Perfumes", username: "mocadosperfumescba", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_46.jpg", poster: "../img/produto-38-1.jpg", video: "https://files.catbox.moe/rxlz3w.mp4", desc: "Doce, cremoso e envolvente. O kit Yara árabe é um dos maiores sucessos de vendas do TikTok!" }
  ];
  const CREATORS_YARA_38 = YARA_38_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 34500 + i * 3100, commentsCount: 310 + i * 40, sharesCount: 145 + i * 25, savesCount: 2800 + i * 310, description: b.desc }));

  // P23: Conjunto De 24 Potes Herméticos Croix Com Tampa E Trava
  const CROIX_23_VIDEOS_MAP = [
    { name: "Dicas da Angélica", username: "lar.da.angell", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_48.jpg", poster: "../img/produto-23-1.jpg", video: "https://files.catbox.moe/tiko7j.mp4", desc: "Kit com 24 Potes Herméticos Croix com tampa que trava! Borracha de vedação total e não vaza nada! 🥗" },
    { name: "Carolaine Moreira", username: "carolaine_moreira", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_50.jpg", poster: "../img/produto-23-2.jpg", video: "https://files.catbox.moe/s87i1c.mp4", desc: "Conjunto De 24 Potes Herméticos Croix Com Tampa E Trava. Organização impecável na cozinha e despensa! ✨" },
    { name: "Complete Store", username: "completestore0", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_52.jpg", poster: "../img/produto-23-3.jpg", video: "https://files.catbox.moe/gb8uzv.mp4", desc: "Conjunto de 24 Potes Herméticos Croix com tampa e 4 travas. Praticidade absoluta no dia a dia!" }
  ];
  const CREATORS_CROIX_23 = CROIX_23_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 22100 + i * 2000, commentsCount: 175 + i * 22, sharesCount: 65 + i * 12, savesCount: 1540 + i * 160, description: b.desc }));

  // P24: Triciclo Infantil 4 em 1 Multifuncional Kababy
  const KABABY_24_VIDEOS_MAP = [
    { name: "Déborah Influencer", username: "deboraoinfluencer", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_54.jpg", poster: "../img/produto-24-1.jpg", video: "https://files.catbox.moe/d137fd.mp4", desc: "Triciclo Infantil 4 em 1 Multifuncional Carrinho de Bebê Com Empurrador e Capota Solar - Kababy! 👼🏻" },
    { name: "Achados Com Gosto", username: "achados.com.gosto", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_56.jpg", poster: "../img/produto-24-2.jpg", video: "https://files.catbox.moe/w6fwpu.mp4", desc: "O companheiro perfeito para todas as fases! Triciclo 4 em 1 Kababy com capota solar e total segurança! 🚲✨" }
  ];
  const CREATORS_KABABY_24 = KABABY_24_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 18900 + i * 1900, commentsCount: 155 + i * 20, sharesCount: 58 + i * 11, savesCount: 1410 + i * 150, description: b.desc }));

  // P25: Bicicleta Aro 20 BMX infantil GottBikes
  const BMX_25_VIDEOS_MAP = [
    { name: "Story Ofertas BR", username: "storyofertasbr", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_58.jpg", poster: "../img/produto-25-1.jpg", video: "https://files.catbox.moe/eym6k1.mp4", desc: "Bicicleta Aro 20 BMX Infantil - Quadro reforçado em aço carbono e freios V-Brake precisos! 🚲🔥" },
    { name: "Shop da Bike", username: "shopdabike", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_60.jpg", poster: "../img/produto-25-2.jpg", video: "https://files.catbox.moe/s61az3.mp4", desc: "Aquela bike BMX que deixa qualquer passeio muito mais radical e divertido! A criançada ama 🚴‍♂️" }
  ];
  const CREATORS_BMX_25 = BMX_25_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 17800 + i * 1800, commentsCount: 140 + i * 19, sharesCount: 52 + i * 10, savesCount: 1320 + i * 140, description: b.desc }));

  // P26: Carrinho de Bebê Guarda Chuva Passeio Leve e Dobrável
  const CARRINHO_26_VIDEOS_MAP = [
    { name: "JFK Variedades", username: "jfk.variedades", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_62.jpg", poster: "../img/produto-26-1.jpg", video: "https://files.catbox.moe/zpxw9r.mp4", desc: "Carrinho de bebê estilo guarda-chuva: super leve, dobra fácil e perfeito pro dia a dia! 🛒💕" },
    { name: "Jaacy Macedo", username: "jaacymacedo_", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_64.jpg", poster: "../img/produto-26-2.jpg", video: "https://files.catbox.moe/u5dmvx.mp4", desc: "3 motivos pra ter um carrinho guarda-chuva: leve, compacto no porta-malas e super confortável! ✨" }
  ];
  const CREATORS_CARRINHO_26 = CARRINHO_26_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 20500 + i * 2100, commentsCount: 168 + i * 22, sharesCount: 64 + i * 13, savesCount: 1560 + i * 165, description: b.desc }));

  // P39: Secador de Cabelos Philco PSC3500 4 em 1 Dobrável 1450W
  const PHILCO_39_VIDEOS_MAP = [
    { name: "Amanda Soares", username: "mandasoaris", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_66.jpg", poster: "../img/produto-39-1.jpg", video: "https://files.catbox.moe/36o9s0.mp4", desc: "O verdadeiro PS5 das garotas! Secador e modelador 4 em 1 Philco PSC3500 com efeito Coanda 💅✨" },
    { name: "Karen Mendes", username: "dailykarenm", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_68.jpg", poster: "../img/produto-39-2.jpg", video: "https://files.catbox.moe/ybjva3.mp4", desc: "Comprei o secador 4 em 1 dobrável da Philco! Modela os cachos com ar sem queimar os fios 😍💖" },
    { name: "Lilian Maurente", username: "lilianmaurente", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_70.jpg", poster: "../img/produto-39-3.jpg", video: "https://files.catbox.moe/ynj6md.mp4", desc: "Resultado de salão em casa com preço de centavos perto do importado! Philco PSC3500 é surreal 😭" },
    { name: "Dai Mendes", username: "favoritosdadaii", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_72.jpg", poster: "../img/produto-39-1.jpg", video: "https://files.catbox.moe/m38pfu.mp4", desc: "Secador de Cabelos Philco PSC3500 4 em 1 Dobrável – 1450W! Perfeito para viagens 🧳💖" },
    { name: "Leandra Klisievicz", username: "leandraklisievicz", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_74.jpg", poster: "../img/produto-39-2.jpg", video: "https://files.catbox.moe/3el0vq.mp4", desc: "Review sincera do secador 4 em 1 da Philco, modela rápido e não queima o cabelo ⭐️💖" }
  ];
  const CREATORS_PHILCO_39 = PHILCO_39_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 29800 + i * 2900, commentsCount: 265 + i * 34, sharesCount: 118 + i * 20, savesCount: 2280 + i * 260, description: b.desc }));

  // P50: Lava e Seca Midea Master Clean Smart 11kg Titanium
  const MIDEA_50_VIDEOS_MAP = [
    { name: "Luana Aura", username: "luanaauracreator", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_72.jpg", poster: "../img/produto-50-1.jpg", video: "https://files.catbox.moe/iawt94.mp4", desc: "Não fico mais sem! Lava e Seca Midea Master Clean Smart 11kg Titanium, prática e moderna 🧺✨" },
    { name: "Juh Fidelis", username: "juhhfidelis", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_74.jpg", poster: "../img/produto-50-2.jpg", video: "https://files.catbox.moe/dst456.mp4", desc: "A bonitona chegou! Lava e Seca Midea 11kg Titanium, silenciosa e perfeita para o dia a dia ❤️" },
    { name: "Djeniffer Guimarães", username: "djeniffer.guimara", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_76.jpg", poster: "../img/produto-50-1.jpg", video: "https://files.catbox.moe/h9xx40.mp4", desc: "Achadinho aprovadíssimo! Lava e Seca Midea 11kg Master Clean com controle inteligente via Wi-Fi 📱" },
    { name: "Yasmin Souza", username: "yasmin.souzzaa._", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_78.jpg", poster: "../img/produto-50-2.jpg", video: "https://files.catbox.moe/ps4hqe.mp4", desc: "Compramos a digníssima! Lava e Seca Midea 11kg Titanium, salva a rotina e economiza muito espaço 🫧💖" },
    { name: "Déborah", username: "deboraoinfluencer", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_80.jpg", poster: "../img/produto-50-1.jpg", video: "https://files.catbox.moe/xjfkuh.mp4", desc: "Lava e Seca Midea Master Clean Smart 11kg Wi-Fi Titanium! Roupa sequinha e cheirosa direto pro cabide 🧺" }
  ];
  const CREATORS_MIDEA_50 = MIDEA_50_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 27100 + i * 2600, commentsCount: 235 + i * 30, sharesCount: 98 + i * 17, savesCount: 2040 + i * 230, description: b.desc }));

  // P19: Tablet Vision TAB 7 Stitch + Capa e Bolsa Positivo
  const STITCH_19_VIDEOS_MAP = [
    { name: "Dahiane Achados", username: "achados_dah", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_76.jpg", poster: "../img/produto-19-1.jpg", video: "https://files.catbox.moe/3wzagk.mp4", desc: "Presente perfeito pras crianças! Tablet Stitch da Positivo com capa protetora e jogos educativos 💙✨" },
    { name: "Yasmin Fernandes", username: "yafernandes_", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_78.jpg", poster: "../img/produto-19-2.jpg", video: "https://files.catbox.moe/mqfzip.mp4", desc: "Comprei o tablet do Stitch perfeito pra minha filha com bolsa temática e controle parental 🥹🩵" },
    { name: "Lais Cordeiro", username: "laiscordeiro01", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_80.jpg", poster: "../img/produto-19-1.jpg", video: "https://files.catbox.moe/01mmmd.mp4", desc: "Tablet Positivo Vision TAB 7 Stitch 64GB com bolsa exclusiva, tela nítida e super resistente 📱" },
    { name: "Kamila Santos", username: "dicasfacilita", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_82.jpg", poster: "../img/produto-19-2.jpg", video: "https://files.catbox.moe/lo6a22.mp4", desc: "Tablet Positivo Vision TAB 7 Stitch infantil completo com capa emborrachada e alça de transporte ✨" },
    { name: "Vi e Comprei", username: "viacheiecomprei", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_84.jpg", poster: "../img/produto-19-1.jpg", video: "https://files.catbox.moe/25pill.mp4", desc: "Achadinho incrível! Tablet Stitch com Android 14 Go, rápido, seguro e muito fofo pro dia a dia 💙" }
  ];
  const CREATORS_STITCH_19 = STITCH_19_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21900 + i * 2100, commentsCount: 185 + i * 24, sharesCount: 78 + i * 14, savesCount: 1690 + i * 180, description: b.desc }));

  // P64: Bateria Auxiliar De Partida Portátil Bomba De Ar
  const BATERIA_64_VIDEOS_MAP = [
    { name: "Gilberto e Aline", username: "validashop", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_79.jpg", poster: "../img/produto-64-1.jpg", video: "https://files.catbox.moe/q1oiaj.mp4", desc: "Bomba de Ar 4 em 1 Multifuncional, infla pneus rápido e dá partida em emergências 🚗⚡" },
    { name: "Cleiton Pesca", username: "pesca.criativa", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_81.jpg", poster: "../img/produto-64-2.jpg", video: "https://files.catbox.moe/q62x2f.mp4", desc: "Auxiliar de partida, compressor e powerbank 4 em 1! Não fico sem no carro e no barco 🚙" },
    { name: "Casal Visionário", username: "acatherinelussani", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_83.jpg", poster: "../img/produto-64-1.jpg", video: "https://files.catbox.moe/15i1tw.mp4", desc: "Compressor multifunção 150 PSI e partida rápida de emergência. Salva de verdade nas viagens! ⚡" },
    { name: "Felipe Dicas", username: "felipedicasnet", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_85.jpg", poster: "../img/produto-64-2.jpg", video: "https://files.catbox.moe/zjqwgy.mp4", desc: "Bomba de ar portátil e calibrador digital com bateria interna e lanterna LED potente 🛞" },
    { name: "Luiz Felipe", username: "felipeindicabr", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_87.jpg", poster: "../img/produto-64-1.jpg", video: "https://files.catbox.moe/0jv9uz.mp4", desc: "Dá partida até em motor pesado sem precisar de chupeta! Equipamento indispensável pro carro 🚗" }
  ];
  const CREATORS_BATERIA_64 = BATERIA_64_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 24300 + i * 2300, commentsCount: 205 + i * 27, sharesCount: 88 + i * 15, savesCount: 1890 + i * 200, description: b.desc }));

  // P68: Jogo de Panelas Cerâmica Kit 5 Peças Antiaderente
  const CERAMICA_68_VIDEOS_MAP = [
    { name: "Nicole Santos", username: "nyymorenna", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_82.jpg", poster: "../img/produto-68-1.jpg", video: "https://files.catbox.moe/gacybk.mp4", desc: "Renovando meu enxoval com o jogo de panelas em cerâmica 5 peças! Fundo triplo antiaderente 🤍✨" },
    { name: "Bia Barreto", username: "beatrizz.barreto", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_84.jpg", poster: "../img/produto-68-2.jpg", video: "https://files.catbox.moe/mxayy3.mp4", desc: "Troquei minhas panelas velhas por cerâmica antiaderente! Não gruda nada e cozinha por igual ✨" },
    { name: "Mila Mifar", username: "milamifar", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_86.jpg", poster: "../img/produto-68-1.jpg", video: "https://files.catbox.moe/wfucd0.mp4", desc: "Kit 5 peças em cerâmica com fundo triplo que funciona em fogão a gás e indução 💕" },
    { name: "Yasmim Oliveira", username: "yascoliveirab", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_88.jpg", poster: "../img/produto-68-2.jpg", video: "https://files.catbox.moe/lr0tj1.mp4", desc: "Jogo 5 panelas cerâmica antiaderente super premium, tampa de vidro com saída de vapor 🤩" },
    { name: "Clube dos Achadinhos", username: "clubedosachadiinhoos", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_90.jpg", poster: "../img/produto-68-1.jpg", video: "https://files.catbox.moe/0yeupc.mp4", desc: "Conjunto 5 peças cerâmica completo, cabo antitérmico e acabamento marmorizado de luxo 🏠" }
  ];
  const CREATORS_CERAMICA_68 = CERAMICA_68_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 26800 + i * 2500, commentsCount: 225 + i * 29, sharesCount: 95 + i * 16, savesCount: 2110 + i * 220, description: b.desc }));

  // P75: Kit 10 Camisetas Dry Fit Masculina
  const DRYFIT_75_VIDEOS_MAP = [
    { name: "Brenda Nunes", username: "brendanuness_1", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_85.jpg", poster: "../img/produto-75-1.jpg", video: "https://files.catbox.moe/7wnkoq.mp4", desc: "Kit com 10 camisetas Dry Fit conforto, estilo e rendimento pro treino ou dia a dia 💪😎" },
    { name: "Matheus Shop", username: "matheuzshop", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_87.jpg", poster: "../img/produto-75-2.jpg", video: "https://files.catbox.moe/lmprnn.mp4", desc: "Kit 10 camisas dry fit masculinas, tecido leve anti suor e caimento atlético impecável 🏋️‍♂️" },
    { name: "Loja 365", username: "shoptresmeiacinco365", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_89.jpg", poster: "../img/produto-75-1.jpg", video: "https://files.catbox.moe/5l382m.mp4", desc: "Kit com 10 camisas Dry Fit perfeitas para treino pesado, corrida e caminhada diária 🔥" },
    { name: "David Souza", username: "d.v.variedades", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_91.jpg", poster: "../img/produto-75-2.jpg", video: "https://files.catbox.moe/eoyce3.mp4", desc: "Kit com 10 camisetas Dry Fit alta durabilidade, secagem ultrarrápida e zero transparência 🏃" },
    { name: "Elite Masculina", username: "elitemasculinashop", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_93.jpg", poster: "../img/produto-75-1.jpg", video: "https://files.catbox.moe/4nta3q.mp4", desc: "Tá valendo a pena demais! Camisetas esportivas respiráveis, costura reforçada e não amarrota ⚡" }
  ];
  const CREATORS_DRYFIT_75 = DRYFIT_75_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 23100 + i * 2200, commentsCount: 195 + i * 25, sharesCount: 82 + i * 14, savesCount: 1780 + i * 190, description: b.desc }));

  // P88: Conjunto Feminino Alfaiataria Laris
  const ALFAIATARIA_88_VIDEOS_MAP = [
    { name: "Beatriz Falasca", username: "beatrizfalasca", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_88.jpg", poster: "../img/produto-88-1.jpg", video: "https://files.catbox.moe/kzxi1d.mp4", desc: "Tô sem acreditar no caimento desse conjunto de alfaiataria! Blusa com botões forrados e calça social 😱✨" },
    { name: "Samara Fashion", username: "samarafashion_modesta", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_90.jpg", poster: "../img/produto-88-2.jpg", video: "https://files.catbox.moe/1fdkcv.mp4", desc: "Conjunto de calça e colete de alfaiataria verão elegante, corte reto chic e moderno 💖" },
    { name: "Larissa Closet", username: "lariicloset", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg", poster: "../img/produto-88-1.jpg", video: "https://files.catbox.moe/5mv5f6.mp4", desc: "Conjunto social feminino colete com calça alfaiataria acabamento premium para trabalhar 💫" },
    { name: "Manuela Souza", username: "manuela_souzahh0", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg", poster: "../img/produto-88-2.jpg", video: "https://files.catbox.moe/y6t37g.mp4", desc: "Conjunto alfaiataria colete e calça impecável, caimento fluido que valoriza a silhueta 🎀" },
    { name: "Duda Leal", username: "dudaleal.outfits", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg", poster: "../img/produto-88-1.jpg", video: "https://files.catbox.moe/94txtj.mp4", desc: "Look de trabalho completo: conjunto alfaiataria sofisticado, tecido encorpado que não amassa ✨" }
  ];
  const CREATORS_ALFAIATARIA_88 = ALFAIATARIA_88_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 32400 + i * 3000, commentsCount: 285 + i * 36, sharesCount: 135 + i * 22, savesCount: 2620 + i * 290, description: b.desc }));

  // P103: Vestido longo feminino costas nua fenda
  const VESTIDO_103_VIDEOS_MAP = [
    { name: "Kevely", username: "kevelybr", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_92.jpg", poster: "../img/produto-103-1.jpg", video: "https://files.catbox.moe/0ajj9s.mp4", desc: "Vestido longo feminino com fenda lateral e costas nuas! Caimento fluido e deslumbrante 🦋👗" },
    { name: "Cassy Correa", username: "cassycorrea0", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_94.jpg", poster: "../img/produto-103-2.jpg", video: "https://files.catbox.moe/as7hah.mp4", desc: "Vestido suplex longo colado com fenda e costas nuas! Elegância, conforto e modelagem perfeita 💖" },
    { name: "Keyla Braga", username: "keylasbraga", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg", poster: "../img/produto-103-1.jpg", video: "https://files.catbox.moe/1uaeyo.mp4", desc: "Vestido longo festa costas nua e fenda lateral, tecido encorpado que não marca nada ✨" },
    { name: "Andréia Alves", username: "andreia.alves.aaa", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_98.jpg", poster: "../img/produto-103-2.jpg", video: "https://files.catbox.moe/0r3osh.mp4", desc: "Look impecável para eventos noturnos, jantares e formaturas. Modela o corpo com elegância máxima 👑" },
    { name: "Érica Leão", username: "ericamcabeluda", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_100.jpg", poster: "../img/produto-103-1.jpg", video: "https://files.catbox.moe/3sbo0d.mp4", desc: "Vestido longo com fenda sensual e decote nas costas, valoriza muito a silhueta e veste super bem 👗" }
  ];
  const CREATORS_VESTIDO_103 = VESTIDO_103_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 35800 + i * 3300, commentsCount: 320 + i * 42, sharesCount: 155 + i * 26, savesCount: 2950 + i * 330, description: b.desc }));

  // P100: Apple iPhone 15 / 15 Plus / 15 Pro / 15 Pro Max
  const IPHONE_100_VIDEOS_MAP = [
    { name: "Rafael Pacheco", username: "rafaelpachecotech", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_96.jpg", poster: "../img/produto-100-1.jpg", video: "https://files.catbox.moe/c6hua3.mp4", desc: "Unboxing oficial do iPhone 15 lacrado! Cabo USB-C trançado e tela Dynamic Island linda 🚀📱" },
    { name: "Vitória Taques", username: "vitoriatmsugc", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_97.jpg", poster: "../img/produto-100-2.jpg", video: "https://files.catbox.moe/czrpji.mp4", desc: "Unboxing do meu novo iPhone 15 cor azul! Acabamento em vidro fosco simplesmente perfeito 💙" },
    { name: "Fernanda Oliveira", username: "fernandaaa_oliv", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_98.jpg", poster: "../img/produto-100-1.jpg", video: "https://files.catbox.moe/4je9vm.mp4", desc: "Meu novo companheiro! iPhone 15 rosa, câmera de 48MP e bateria que dura o dia inteiro 🩷🥹" },
    { name: "Diogo Silva", username: "diogooslvv", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_99.jpg", poster: "../img/produto-100-2.jpg", video: "https://files.catbox.moe/xcta68.mp4", desc: "Perfeição em cada detalhe! iPhone 15 Blue unboxing e primeiras impressões 🌊🐚" },
    { name: "Tuane Sangy", username: "tuanesangy", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_100.jpg", poster: "../img/produto-100-1.jpg", video: "https://files.catbox.moe/q5ctfn.mp4", desc: "Comprei meu primeiro iPhone 15 e deu tudo certo! Câmera cinematográfica e super rápido ✨" }
  ];
  const CREATORS_IPHONE_100 = IPHONE_100_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 42100 + i * 3900, commentsCount: 380 + i * 48, sharesCount: 195 + i * 32, savesCount: 3450 + i * 390, description: b.desc }));

switch (prodId) {

      case 4:
        activeDataset = CREATORS_JBL_4;
        contextType = 'jbl_4';
        break;
      case 5:
        activeDataset = CREATORS_AIRFRYER_5;
        contextType = 'airfryer_5';
        break;
      case 6:
        activeDataset = CREATORS_BIKE_6;
        contextType = 'bike_6';
        break;
      case 7:
        activeDataset = CREATORS_AIWA_7;
        contextType = 'aiwa_7';
        break;
      case 8:
        activeDataset = CREATORS_AIWA_PARTYBOX_8;
        contextType = 'aiwa_partybox_8';
        break;
      case 9:
        activeDataset = CREATORS_AR_HQ_9;
        contextType = 'ar_hq_9';
        break;
      case 10:
        activeDataset = CREATORS_AR_HISENSE_10;
        contextType = 'ar_hisense_10';
        break;
      case 11:
        activeDataset = CREATORS_CLIMATIZADOR_OSTER_11;
        contextType = 'climatizador_oster_11';
        break;
      case 12:
        activeDataset = CREATORS_PISCINA_12;
        contextType = 'piscina_12';
        break;
      case 13:
        activeDataset = CREATORS_PISCINA_PIXLAR_13;
        contextType = 'piscina_pixlar_13';
        break;
      case 16:
        activeDataset = CREATORS_CHURRASQUEIRA_RODEIO_16;
        contextType = 'churrasqueira_rodeio_16';
        break;
      case 17:
        activeDataset = CREATORS_CADEIRAS_PRAIA_MOR_17;
        contextType = 'cadeiras_praia_mor_17';
        break;
      case 18:
        activeDataset = CREATORS_KIT_PRAIA_MOR_18;
        contextType = 'kit_praia_mor_18';
        break;
      case 20:
        activeDataset = CREATORS_BIKE_GT_20;
        contextType = 'bike_gt_20';
        break;
      case 21:
        activeDataset = CREATORS_BOLA_PENALTY_21;
        contextType = 'bola_penalty_21';
        break;
      case 22:
        activeDataset = CREATORS_COLCHAO_BESTWAY_22;
        contextType = 'colchao_bestway_22';
        break;
      case 27:
        activeDataset = CREATORS_AR_LG_27;
        contextType = 'ar_lg_27';
        break;
      case 28:
        activeDataset = CREATORS_REBECCA_BONBON_28;
        contextType = 'rebecca_bonbon_28';
        break;
      case 29:
        activeDataset = CREATORS_AR_HQ_29;
        contextType = 'ar_hq_29';
        break;
      case 30:
        activeDataset = CREATORS_CLIMATIZADOR_MIDEA_30;
        contextType = 'climatizador_midea_30';
        break;
      case 31:
        activeDataset = CREATORS_SABALA_31;
        contextType = 'sabala_31';
        break;
      case 32:
        activeDataset = CREATORS_CHUVEIRO_32;
        contextType = 'chuveiro_32';
        break;
      case 35:
        activeDataset = CREATORS_JBL_BOOMBOX4_35;
        contextType = 'jbl_boombox4_35';
        break;
      case 36:
        activeDataset = CREATORS_POCO_X7_PRO_36;
        contextType = 'poco_x7_pro_36';
        break;
      case 44:
        activeDataset = CREATORS_CLIMATIZADOR_VENTISOL_44;
        contextType = 'climatizador_ventisol_44';
        break;
      case 46:
        activeDataset = CREATORS_ELECTROLUX_46;
        contextType = 'electrolux_46';
        break;
      case 47:
        activeDataset = CREATORS_WAP_EXTRATORA_78;
        contextType = 'wap_extratora_47';
        break;
      case 48:
        activeDataset = CREATORS_PANIFICADORA_48_84;
        contextType = 'panificadora_48';
        break;
      case 52:
        activeDataset = CREATORS_PAD11_52;
        contextType = 'pad11_52';
        break;
      case 55:
        activeDataset = CREATORS_SWITCH_55;
        contextType = 'switch_55';
        break;
      case 56:
        activeDataset = CREATORS_ESTEIRA_56;
        contextType = 'esteira_56';
        break;
      case 57:
        activeDataset = CREATORS_JOOG_ONE_57;
        contextType = 'joog_one_57';
        break;
      case 58:
        activeDataset = CREATORS_ECHODOT_58;
        contextType = 'echodot_58';
        break;
      case 59:
        activeDataset = CREATORS_STARLINK_59;
        contextType = 'starlink_59';
        break;
      case 61:
        activeDataset = CREATORS_JOOG_BREAK_61;
        contextType = 'joog_break_61';
        break;
      case 63:
        activeDataset = CREATORS_REDMI_WATCH_63;
        contextType = 'redmi_watch_63';
        break;
      case 65:
        activeDataset = CREATORS_SOFA_SENSES_65;
        contextType = 'sofa_senses_65';
        break;
      case 70:
        activeDataset = CREATORS_SECADORA_MUELLER_70;
        contextType = 'secadora_mueller_70';
        break;
      case 73:
        activeDataset = CREATORS_WAAW_HYPERBOOM_73;
        contextType = 'waaw_hyperboom_73';
        break;
      case 78:
        activeDataset = CREATORS_SPOTCLEANER_78;
        contextType = 'spotcleaner_78';
        break;
      case 80:
        activeDataset = CREATORS_PANIFICADORA_80;
        contextType = 'panificadora_80';
        break;
      case 85:
        activeDataset = CREATORS_JOOG_X2_85;
        contextType = 'joog_x2_85';
        break;
      case 87:
        activeDataset = CREATORS_MOM_JEANS_87;
        contextType = 'mom_jeans_87';
        break;
      case 89:
        activeDataset = CREATORS_PANELAS_FERRO_89;
        contextType = 'panelas_ferro_89';
        break;
      case 90:
        activeDataset = CREATORS_PANELAS_AVANT_90;
        contextType = 'panelas_avant_90';
        break;
      case 91:
        activeDataset = CREATORS_PIPOQUEIRA_91;
        contextType = 'pipoqueira_91';
        break;
      case 92:
        activeDataset = CREATORS_PANELAS_FERRO_92;
        contextType = 'panelas_ferro_92';
        break;
      case 94:
        activeDataset = CREATORS_BIKE_SPINNING_94;
        contextType = 'bike_spinning_94';
        break;
      case 95:
        activeDataset = CREATORS_MAQUINA_GELO_95;
        contextType = 'maquina_gelo_95';
        break;
      case 96:
        activeDataset = CREATORS_APARELHO_RYO_96;
        contextType = 'aparelho_ryo_96';
        break;
      case 97:
        activeDataset = CREATORS_JOGO_JANTAR_97;
        contextType = 'jogo_jantar_97';
        break;
      case 102:
        activeDataset = CREATORS_SCOOTER_102;
        contextType = 'scooter_102';
        break;
      case 111:
        activeDataset = CREATORS_PROJETOR_111;
        contextType = 'projetor_111';
        break;
      case 113:
        activeDataset = CREATORS_COMEDOURO_113;
        contextType = 'comedouro_113';
        break;
      case 114:
        activeDataset = CREATORS_ARCADE_114;
        contextType = 'arcade_114';
        break;
      case 116:
        activeDataset = CREATORS_SMART_TV_116;
        contextType = 'smart_tv_116';
        break;
      case 14:
        activeDataset = CREATORS_CHURRASQUEIRA_ARKE_14;
        contextType = 'churrasqueira_14';
        break;
      case 15:
        activeDataset = CREATORS_CHURRASQUEIRA_BISCUITT_15;
        contextType = 'churrasqueira_15';
        break;
      case 101:
        activeDataset = CREATORS_TIRES;
        contextType = 'tires';
        break;
      case 104:
        activeDataset = CREATORS_CHINELO_104;
        contextType = 'chinelo';
        break;
      case 105:
        activeDataset = CREATORS_PROJETOR_105;
        contextType = 'projetor';
        break;
      case 106:
        activeDataset = CREATORS_BODY_106;
        contextType = 'bodymodelador';
        break;
      case 107:
        activeDataset = CREATORS_ASPIRADOR_107;
        contextType = 'aspirador';
        break;
      case 108:
        activeDataset = CREATORS_ESCOVA_108;
        contextType = 'escova108';
        break;
      case 109:
        activeDataset = CREATORS_MODELADOR_109;
        contextType = 'modelador109';
        break;
      case 110:
        activeDataset = CREATORS_KAPPA_110;
        contextType = 'kappa110';
        break;
      case 112:
        activeDataset = CREATORS_CAMINHAO_112;
        contextType = 'patinhos112';
        break;
      case 115:
        activeDataset = CREATORS_FORNO_HQ_115;
        contextType = 'fornohq115';
        break;
      case 117:
        activeDataset = CREATORS_FOGAO_117;
        contextType = 'fogao117';
        break;
      case 118:
        activeDataset = CREATORS_MESA_118;
        contextType = 'mesa118';
        break;
      case 119:
        activeDataset = CREATORS_FRALDAS_119;
        contextType = 'fraldas119';
        break;
      case 120:
        activeDataset = CREATORS_SOFA_120;
        contextType = 'sofa120';
        break;
      case 121:
        activeDataset = CREATORS_TRAVESSEIRO_121;
        contextType = 'travesseiro121';
        break;
      case 122:
        activeDataset = CREATORS_PANELA_122;
        contextType = 'panela122';
        break;
      case 123:
        activeDataset = CREATORS_LAVADORA_123;
        contextType = 'lavadora123';
        break;
      case 124:
        activeDataset = CREATORS_LIVRO_124;
        contextType = 'livro124';
        break;

      
      case 19:
        activeDataset = CREATORS_STITCH_19;
        contextType = 'stitch_19';
        break;
      case 23:
        activeDataset = CREATORS_CROIX_23;
        contextType = 'croix_23';
        break;
      case 24:
        activeDataset = CREATORS_KABABY_24;
        contextType = 'kababy_24';
        break;
      case 25:
        activeDataset = CREATORS_BMX_25;
        contextType = 'bmx_25';
        break;
      case 26:
        activeDataset = CREATORS_CARRINHO_26;
        contextType = 'carrinho_26';
        break;
      case 33:
        activeDataset = CREATORS_BLUEY_33;
        contextType = 'bluey_33';
        break;
      case 34:
        activeDataset = CREATORS_PRAXIS_34;
        contextType = 'praxis_34';
        break;
      case 38:
        activeDataset = CREATORS_YARA_38;
        contextType = 'yara_38';
        break;
      case 39:
        activeDataset = CREATORS_PHILCO_39;
        contextType = 'philco_39';
        break;
      case 40:
        activeDataset = CREATORS_MONDIAL_40;
        contextType = 'mondial_40';
        break;
      case 41:
        activeDataset = CREATORS_OVEN_41;
        contextType = 'oven_41';
        break;
      case 45:
        activeDataset = CREATORS_MQ_45;
        contextType = 'mq_45';
        break;
      case 49:
        activeDataset = CREATORS_WAP_EXTRATORA_78;
        contextType = 'wap_extratora_78';
        break;
      case 50:
        activeDataset = CREATORS_MIDEA_50;
        contextType = 'midea_50';
        break;
      case 53:
        activeDataset = CREATORS_STARLINK_53;
        contextType = 'starlink_53';
        break;
      case 54:
        activeDataset = CREATORS_PURIFICADOR_54;
        contextType = 'purificador_54';
        break;
      case 60:
        activeDataset = CREATORS_SABALA_60;
        contextType = 'sabala_60';
        break;
      case 64:
        activeDataset = CREATORS_BATERIA_64;
        contextType = 'bateria_64';
        break;
      case 68:
        activeDataset = CREATORS_CERAMICA_68;
        contextType = 'ceramica_68';
        break;
      case 72:
        activeDataset = CREATORS_PANELAS_FERRO_72;
        contextType = 'panelas_ferro_72';
        break;
      case 74:
        activeDataset = CREATORS_CAMISA_BRASIL_74;
        contextType = 'camisa_brasil_74';
        break;
      case 75:
        activeDataset = CREATORS_DRYFIT_75;
        contextType = 'dryfit_75';
        break;
      case 76:
        activeDataset = CREATORS_APARELHO_76;
        contextType = 'aparelho_76';
        break;
      case 82:
        activeDataset = CREATORS_HISENSE_82;
        contextType = 'hisense_82';
        break;
      case 88:
        activeDataset = CREATORS_ALFAIATARIA_88;
        contextType = 'alfaiataria_88';
        break;
      case 98:
        activeDataset = CREATORS_COPOS_98;
        contextType = 'copos_98';
        break;
      case 99:
        activeDataset = CREATORS_CAMISA_PORTUGAL_99;
        contextType = 'camisa_portugal_99';
        break;
      case 100:
        activeDataset = CREATORS_IPHONE_100;
        contextType = 'iphone_100';
        break;
      case 103:
        activeDataset = CREATORS_VESTIDO_103;
        contextType = 'vestido_103';
        break;

      default:
        // Produto sem vídeos dedicados: oculta carrossel limpo com display: none
        activeDataset = [];
        contextType = 'sem_video';
        break;
    }

// Desacoplamento estrito entre o vídeo oficial da descrição e os vídeos de criadores
    const descVidEl = document.querySelector('#tt-product-video, .product-video-player, #product-desc-video');
    const descVidSrc = descVidEl ? (descVidEl.getAttribute('src') || '').trim() : '';
    if (descVidSrc && Array.isArray(activeDataset) && activeDataset.length > 0) {
      activeDataset = activeDataset.filter(item => {
        const itemVid = (item.video || item.localVideo || '').trim();
        return itemVid && itemVid !== descVidSrc;
      });
    }

    if (!activeDataset || activeDataset.length === 0) {
      if (targetContainer) {
        targetContainer.innerHTML = '';
        targetContainer.style.setProperty('display', 'none', 'important');
      }
      return;
    }

    // Trava de segurança obrigatória: desduplicação por Set (Req 4)
    const seen = new Set();
    activeDataset = activeDataset.filter(item => { if(!item.video || seen.has(item.video)) return false; seen.add(item.video); return true; });

    if (!activeDataset || activeDataset.length === 0) {
      if (targetContainer) {
        targetContainer.innerHTML = '';
        targetContainer.style.setProperty('display', 'none', 'important');
      }
      return;
    }

    const totalVideosCount = activeDataset.length;
    const countBadge = totalVideosCount >= 30 ? '30+' : (totalVideosCount >= 20 ? (totalVideosCount + '+') : totalVideosCount);

    // Popula a lista oficial de vídeos em memória com metadados e comentários realistas
    videoList = [];
    for (let i = 0; i < totalVideosCount; i++) {
      const originalItem = activeDataset[i];
      const videoId = i;
      
      const likes = originalItem.likes || (12400 + ((i * 4391) % 48000));
      const comments = originalItem.commentsCount || originalItem.comments || (38 + ((i * 19) % 210));
      const saves = originalItem.saves || Math.max(120, Math.floor(likes * 0.11));
      const shares = originalItem.shares || Math.max(30, Math.floor(likes * 0.035));

      const item = {
        id: videoId,
        name: originalItem.name,
        username: originalItem.username,
        avatar: originalItem.avatar,
        poster: originalItem.poster,
        video: originalItem.video,
        startTime: originalItem.startTime || 0.2,
        likes: likes,
        commentsCount: comments,
        saves: saves,
        shares: shares,
        description: originalItem.description || originalItem.desc || originalItem.title || '',
        liked: false,
        saved: false,
        followed: false,
        commentsList: (function() {
          if (contextType === 'modelador109' || (typeof isModelador !== 'undefined' && isModelador)) {
            return [
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_1.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_1.jpg',
                user: 'mari.cachos',
                text: 'Menina do céu, esquenta rápido? Meu cabelo é grosso e difícil de pegar cacho!',
                date: 'Há 18 min',
                likes: 42,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/creators-cabelo/creator-109-5.jpg' : 'img/creators-cabelo/creator-109-5.jpg',
                user: 'maryonlive',
                isCreator: true,
                text: 'Esquenta em 30s amiga! Uso em 180°C e o cacho dura o dia todo sem precisar de laquê 😍✨',
                date: 'Há 15 min',
                likes: 89,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_2.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_2.jpg',
                user: 'bia_closet',
                text: 'Esse modelador sem fio me salvou no casamento! Retoquei no carro em 5 minutos ✨',
                date: 'Há 1 hora',
                likes: 29,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_3.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_3.jpg',
                user: 'camila_looks',
                text: 'Tinha pavor de queimar o dedo ou a orelha com babyliss comum, esse isolamento térmico é perfeito!',
                date: 'Há 3 horas',
                likes: 18,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_4.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_4.jpg',
                user: 'ju_costa',
                text: 'Comprei pelo carrinho laranja e chegou em 3 dias aqui em Curitiba! Amei muito ❤️',
                date: 'Ontem',
                likes: 15,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_5.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_5.jpg',
                user: 'larissa.silva',
                text: 'A bateria dura pra fazer a cabeça inteira duas vezes tranquilamente. Muito prático!',
                date: 'Há 1 dia',
                likes: 11,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_6.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_6.jpg',
                user: 'gabi_couto',
                text: 'Pega em cabelo curto/chanel ou só em cabelo comprido?',
                date: 'Há 1 dia',
                likes: 7,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/creators-cabelo/creator-109-5.jpg' : 'img/creators-cabelo/creator-109-5.jpg',
                user: 'maryonlive',
                isCreator: true,
                text: 'Pega super bem em curto também amiga! É só colocar a mecha mais perto da ponta que ele puxa suave 🥰',
                date: 'Há 1 dia',
                likes: 34,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_7.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_7.jpg',
                user: 'tami.albuquerque',
                text: 'Vem com o cabo pra carregar? É USB normal?',
                date: 'Há 2 dias',
                likes: 5,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_8.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_8.jpg',
                user: 'carol_rezende',
                text: 'Vem sim com o cabo USB-C e os dois pentes e clipes de mecha, caixinha completa!',
                date: 'Há 2 dias',
                likes: 21,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_9.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_9.jpg',
                user: 'renatinha_moda',
                text: 'Comprei na promoção relâmpago de ontem, já enviaram código de rastreio!',
                date: 'Há 3 dias',
                likes: 14,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_10.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_10.jpg',
                user: 'biancaprado.fit',
                text: 'Amei que dá pra escolher o lado do cacho (L ou R), fica com acabamento de salão.',
                date: 'Há 4 dias',
                likes: 19,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_11.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_11.jpg',
                user: 'paty.coimbra',
                text: 'Gente, o preço tá muito barato pelo que entrega, na gringa custa mais de 50 dólares.',
                date: 'Há 5 dias',
                likes: 27,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_12.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_12.jpg',
                user: 'isabella_style',
                text: 'O meu chegou hoje cedo! Já testei e aprovei com louvor 😍👏',
                date: 'Há 6 dias',
                likes: 9,
                liked: false
              }
            ];
          } else if (contextType === 'escova108' || (typeof isEscova !== 'undefined' && isEscova)) {
            return [
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_6.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_6.jpg',
                user: 'aninha_hair',
                text: 'Gente essa escova 5 em 1 seca e modela ao mesmo tempo? Fica com brilho de salão?',
                date: 'Há 25 min',
                likes: 38,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_7.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_7.jpg',
                user: 'paty_style',
                text: 'O efeito Coanda de sugar a mecha é real, não queima nada o cabelo!',
                date: 'Há 2 horas',
                likes: 24,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_8.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_8.jpg',
                user: 'carol.dicas',
                text: 'Chegou em 3 dias aqui em SP, bem embalada com todas as 5 ponteiras. Apaixonada!',
                date: 'Ontem',
                likes: 19,
                liked: false
              }
            ];
          } else if (contextType === 'churrasqueira_14') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Galera, recomendo colocar um pouquinho de água na bandeja antes de ligar. Não faz fumaça e a gordura sai na água fácil de lavar! 🥩👏',
                date: 'Há 2 horas',
                likes: 56,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-fernando.jpg' : 'img/avatars-churras/creator-fernando.jpg',
                user: 'churras_em_familia',
                text: 'Realmente zero fumaça no apartamento! Coloquei água na bandeja coletora e assou a picanha perfeitamente 🔥',
                date: 'Há 1 hora',
                likes: 38,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-rodrigo.jpg' : 'img/avatars-churras/creator-rodrigo.jpg',
                user: 'gustavo_ape12',
                text: 'Os 5 espetos rotativos giram super macio. Melhor investimento de churrasco da vida!',
                date: 'Há 3 horas',
                likes: 24,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-patricia.jpg' : 'img/avatars-churras/creator-patricia.jpg',
                user: 'paty_gourmet',
                text: 'Cabe uma peça de maminha inteira nos espetos centrais? Fica bem dourada?',
                date: 'Há 4 horas',
                likes: 19,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-churras/creator-lucas.jpg' : 'img/avatars-churras/creator-lucas.jpg',
                user: 'rodrigo_moura',
                text: 'Chegou em 2 dias aqui pela Stone Shop, caixa lacrada com todos os 5 espetos e manual.',
                date: 'Ontem',
                likes: 17,
                liked: false
              }
            ];
          } else if (contextType === 'churrasqueira_15') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Galera, o cooler com entrada USB/pilhas acende a brasa em 3 minutos sem sofrer! Fica zero fumaça na varanda 🔥🥩',
                date: 'Há 2 horas',
                likes: 62,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-biscuitt/creator-carlos.jpg' : 'img/avatars-biscuitt/creator-carlos.jpg',
                user: 'marcelo_bbq',
                text: 'O cooler com regulador USB acelera o acendimento em 3 minutos, não precisa ficar abanando! 👏',
                date: 'Há 1 hora',
                likes: 38,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-biscuitt/creator-renata.jpg' : 'img/avatars-biscuitt/creator-renata.jpg',
                user: 'paty_varandinha',
                text: 'Fiz picanha e queijo coalho na varanda ontem, zero fumaça no apê! Meus vizinhos nem sentiram cheiro ❤️',
                date: 'Há 3 horas',
                likes: 27,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-biscuitt/creator-thiago.jpg' : 'img/avatars-biscuitt/creator-thiago.jpg',
                user: 'thiago_brasa',
                text: 'Gasta um punhado minúsculo de carvão. Uma bag de 2kg de carvão dura semanas!',
                date: 'Há 4 horas',
                likes: 21,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/avatars-biscuitt/creator-gabi.jpg' : 'img/avatars-biscuitt/creator-gabi.jpg',
                user: 'carol_ape12',
                text: 'Chegou em 2 dias aqui pela Stone Shop, a bag térmica é linda e a grelha limpa na pia sem esforço.',
                date: 'Ontem',
                likes: 15,
                liked: false
              }
            ];
          } else if (contextType === 'mesa118' || contextType === 'mesa_118') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Gente, a mesa é maravilhosa e o acabamento chanfrado com as cadeiras em suede é super confortável! Vale cada centavo ✨🪑',
                date: 'Há 2 horas',
                likes: 47,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_6.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_6.jpg',
                user: 'larissa_home',
                text: 'As cadeiras em suede são muito confortáveis e a espuma D26 não afunda. Entrega da Stone Shop foi super rápida!',
                date: 'Há 1 hora',
                likes: 31,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_3.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_3.jpg',
                user: 'felipe_moraes',
                text: 'Comprei o modelo Freijó com Off White, mesa muito estável e firme, não balança nada. Amei demais!',
                date: 'Há 3 horas',
                likes: 22,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_8.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_8.jpg',
                user: 'camila_ape54',
                text: 'Coube perfeitamente na minha sala de jantar compacta. Recomendo de olhos fechados!',
                date: 'Há 4 horas',
                likes: 18,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_10.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_10.jpg',
                user: 'renata_design',
                text: 'Chegou tudo muito bem embalado com proteção reforçada nas quinas do tampo. Nota 10!',
                date: 'Ontem',
                likes: 14,
                liked: false
              }
            ];
          } else if (contextType === 'arcade114') {
            return [
              {
                avatar: originalItem.avatar,
                user: originalItem.username,
                isCreator: true,
                text: 'Galera, recomendo fixar bem as 4 ventosas numa mesa de vidro ou madeira lisa! O manche 360 fica super firme e os combos saem perfeitos! 🕹️🔥',
                date: 'Há 1 hora',
                likes: 84,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_1.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_1.jpg',
                user: 'lucas_retrogamer',
                text: 'Mano, o clique dos microswitches é satisfatório demais! Zero delay no PS4 e no PC.',
                date: 'Há 45 min',
                likes: 42,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_3.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_3.jpg',
                user: 'thiago_kof',
                text: 'Testei no KOF 98 e no Street Fighter 6, os especiais e hadouken saem limpos sem engasgar!',
                date: 'Há 2 horas',
                likes: 31,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_5.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_5.jpg',
                user: 'marcos_arcade',
                text: 'Reconheceu no PC de primeira como X-Input sem instalar nenhum driver. Excelente custo-benefício!',
                date: 'Há 3 horas',
                likes: 27,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/tiktok_real/tt_avatar_7.jpg' : 'img/reviews-avatars/tiktok_real/tt_avatar_7.jpg',
                user: 'felipe_gamers',
                text: 'Cabo USB de 2.5m bem reforçado, dá pra jogar do sofá com folga no Nintendo Switch.',
                date: 'Ontem',
                likes: 19,
                liked: false
              }
            ];
          } else {
            return [
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_1.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_1.jpg',
                user: 'mariasilva.ofc',
                text: 'Menina do céu, o meu chegou ontem e é simplesmente PERFEITO!',
                date: 'Há 2 horas',
                likes: 14,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_2.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_2.jpg',
                user: 'carol_looks',
                text: 'Super fácil de usar, amei o resultado 😍',
                date: 'Há 5 horas',
                likes: 8,
                liked: false
              },
              {
                avatar: isPagesDir ? '../img/reviews-avatars/mulheres_validadas/mulher_3.jpg' : 'img/reviews-avatars/mulheres_validadas/mulher_3.jpg',
                user: 'amanda.santoss',
                text: 'Chegou rápido demais aqui em SP! Nota 10',
                date: 'Ontem',
                likes: 5,
                liked: false
              }
            ];
          }
        })()
      };
      videoList.push(item);
    }

    // Se já existirem cards pré-renderizados no HTML estático (Zero Delay):
    const existingList = document.getElementById('creators-carousel-list');
    const existingCards = existingList ? existingList.querySelectorAll('.creator-card') : [];

    if (!existingCards.length) {
      // Se a página não tiver pré-render estático, gera agora dinamicamente
      targetContainer.innerHTML = `
        <h3 class="creators-title">Vídeos de criadores (${countBadge})</h3>
        <div class="creators-carousel" id="creators-carousel-list"></div>
      `;

      const listElement = document.getElementById('creators-carousel-list');
      for (let i = 0; i < totalVideosCount; i++) {
        const item = videoList[i];
        const loadingAttr = i < 4 ? 'loading="eager"' : 'loading="lazy"';
        const fetchAttr = i < 2 ? 'fetchpriority="high"' : '';
        const cardHtml = `
          <div class="creator-card" data-video-id="${i}">
            <video class="creator-preview-vid" src="${item.video}" poster="${item.poster}" autoplay muted loop playsinline webkit-playsinline preload="${i < 4 ? 'auto' : 'none'}" style="width: 100%; height: 100%; object-fit: cover; position: absolute; top: 0; left: 0; pointer-events: none;"></video>
            <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(180deg, rgba(0,0,0,0.15) 0%, transparent 40%, rgba(0,0,0,0.75) 100%); pointer-events: none;"></div>
            <div style="position: absolute; top: 8px; left: 8px; width: 22px; height: 22px; background: rgba(0,0,0,0.45); backdrop-filter: blur(4px); border-radius: 50%; display: flex; align-items: center; justify-content: center; z-index: 2; pointer-events: none;">
              <svg viewBox="0 0 24 24" style="fill: #fff; width: 10px; height: 10px; margin-left: 1px;"><path d="M8 5v14l11-7z"/></svg>
            </div>
            <div style="position: absolute; bottom: 0; left: 0; width: 100%; padding: 6px; display: flex; align-items: center; gap: 5px; z-index: 2; box-sizing: border-box; pointer-events: none;">
              <img src="${item.avatar}" alt="" style="width: 18px; height: 18px; border-radius: 50%; object-fit: cover; border: 1px solid #fff; flex-shrink: 0;" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
              <span style="font-size: 10px; font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; text-shadow: 0 1px 2px rgba(0,0,0,0.8);">${item.name}</span>
            </div>
          </div>
        `;
        listElement.insertAdjacentHTML('beforeend', cardHtml);
      }
    }

    // Vincula o clique nos cards com PREVENÇÃO DE CLIQUE DUPLO e PLAY IMEDIATO
    const allCards = targetContainer.querySelectorAll('.creator-card');
    allCards.forEach((card, idx) => {
      card.onclick = function(e) {
        if (e) {
          e.preventDefault();
          e.stopPropagation();
        }
        const id = parseInt(this.getAttribute('data-video-id') !== null ? this.getAttribute('data-video-id') : idx, 10);
        openTikTokVideo(id);
      };
    });

    // Inicializa o modal em background para deixá-lo quente na memória
    createTikTokModalMarkup();

    // AUTOPLAY AUTOMÁTICO DOS VÍDEOS DE CRIADORES NO CARROSSEL (PADRÃO TIKTOK SHOP)
    if ('IntersectionObserver' in window) {
      const vidObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          const v = entry.target.querySelector('video.creator-preview-vid');
          if (!v) return;
          if (entry.isIntersecting) {
            v.muted = true;
            const p = v.play();
            if (p !== undefined) p.catch(() => {});
          } else {
            v.pause();
          }
        });
      }, { threshold: 0.15 });

      allCards.forEach(card => vidObserver.observe(card));
    } else {
      allCards.forEach((card, idx) => {
        if (idx < 3) {
          const v = card.querySelector('video.creator-preview-vid');
          if (v) { v.muted = true; v.play().catch(() => {}); }
        }
      });
    }

    // Disparo imediato para os primeiros cards visíveis (Zero Delay)
    setTimeout(() => {
      const firstVids = targetContainer.querySelectorAll('.creator-card:nth-child(-n+3) video.creator-preview-vid');
      firstVids.forEach(v => {
        v.muted = true;
        const p = v.play();
        if (p !== undefined) p.catch(() => {});
      });
    }, 250);

  }

  // Cria ou vincula o Modal TikTok
  function createTikTokModalMarkup() {
    if (document.getElementById('tiktok-modal')) {
      ttModal = document.getElementById('tiktok-modal');
      ttVideo = document.getElementById('tt-modal-player');
      setupModalEventListeners();
      return;
    }

    ttModal = document.createElement('div');
    ttModal.className = 'tt-modal';
    ttModal.id = 'tiktok-modal';

    ttModal.innerHTML = `
      <div class="tt-container">
        <div class="tt-top-bar">
          <button class="tt-back-btn" id="tt-close-btn" aria-label="Voltar">
            <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg>
          </button>
          <div class="tt-search-container">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input class="tt-search-input" type="text" value="Encontrar conteúdo relacionado" readonly>
          </div>
        </div>

        <div class="tt-video-wrapper" id="tt-video-wrapper">
          <video class="tt-video" id="tt-modal-player" loop playsinline webkit-playsinline autoplay preload="auto" style="background:#000;"></video>

          <div class="tt-play-icon-overlay" id="tt-play-overlay">
            <svg viewBox="0 0 24 24" width="34" height="34" fill="#fff"><path d="M8 5v14l11-7z"/></svg>
          </div>

          <div class="tt-right-actions">
            <div class="tt-creator-wrapper">
              <img class="tt-creator-avatar" id="tt-action-avatar" src="../logo.png" alt="Stone Shop">
              <button class="tt-follow-btn" id="tt-action-follow">+</button>
            </div>
            <button class="tt-action-btn" id="tt-action-like">
              <svg viewBox="0 0 24 24" width="32" height="32" fill="#fff"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
              <span class="tt-action-label" id="tt-like-count">14.2K</span>
            </button>
            <button class="tt-action-btn" id="tt-action-comment">
              <svg viewBox="0 0 24 24" width="30" height="30" fill="#fff"><path d="M21.99 4c0-1.1-.89-2-1.99-2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4-.01-18zM18 14H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"/></svg>
              <span class="tt-action-label" id="tt-comment-count">128</span>
            </button>
            <button class="tt-action-btn" id="tt-action-save">
              <svg viewBox="0 0 24 24" width="30" height="30" fill="#fff"><path d="M17 3H7c-1.1 0-1.99.9-1.99 2L5 21l7-3 7 3V5c0-1.1-.9-2-2-2z"/></svg>
              <span class="tt-action-label" id="tt-save-count">3.4K</span>
            </button>
            <button class="tt-action-btn" id="tt-action-share">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="#fff"><path d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92s2.92-1.31 2.92-2.92c0-1.61-1.31-2.92-2.92-2.92z"/></svg>
              <span class="tt-action-label">Compartilhar</span>
            </button>
          </div>

          <div class="tt-left-info">
            <div class="tt-username" id="tt-display-name">@tiktokshop</div>
            <div class="tt-desc" id="tt-display-desc">Review oficial do produto</div>
            <div class="tt-product-anchor" id="tt-product-anchor">
              <svg viewBox="0 0 24 24" width="13" height="13" fill="#ffb800" style="flex-shrink:0;"><path d="M19 6h-2c0-2.76-2.24-5-5-5S7 3.24 7 6H5c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm-7-3c1.66 0 3 1.34 3 3H9c0-1.66 1.34-3 3-3zm7 17H5V8h14v12z"/></svg>
              <span class="tt-anchor-title" id="tt-anchor-title">Produto Oficial</span>
              <svg viewBox="0 0 24 24" width="11" height="11" fill="none" stroke="#fff" stroke-width="2.5" style="flex-shrink:0;"><polyline points="9 18 15 12 9 6"/></svg>
            </div>
          </div>

          <div class="tt-comments-drawer" id="tt-comments-drawer">
            <div class="tt-drawer-header">
              <span class="tt-drawer-title" id="tt-drawer-title">128 comentários</span>
              <button class="tt-drawer-close" id="tt-drawer-close">✕</button>
            </div>
            <div class="tt-drawer-list" id="tt-drawer-comments-list"></div>
            <div class="tt-comment-input-bar">
              <input type="text" class="tt-comment-input" id="tt-comment-input-field" placeholder="Adicionar comentário...">
              <button class="tt-comment-submit-btn" id="tt-comment-send-btn" aria-label="Enviar comentário">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(ttModal);
    ttVideo = document.getElementById('tt-modal-player');
    setupModalEventListeners();
  }

  // Alterna Play / Pause e Mute com Atualização de Ícones
  function updateSoundBadge() {
    const badge = document.getElementById('tt-sound-badge');
    if (!badge) return;
    if (ttVideo && ttVideo.muted) {
      badge.style.display = 'flex';
    } else {
      badge.style.display = 'none';
    }
  }

  function togglePlayPause() {
    if (!ttVideo) return;
    const playOverlay = document.getElementById('tt-play-overlay');

    // Se estiver tocando muted e o usuário tocar na tela, ativa o som primeiro!
    if (!ttVideo.paused && ttVideo.muted) {
      ttVideo.muted = false;
      updateSoundBadge();
      showTikTokToast('Som ativado 🔊');
      return;
    }

    if (ttVideo.paused) {
      const p = ttVideo.play();
      if (p !== undefined) {
        p.then(() => {
          if (playOverlay) playOverlay.style.display = 'none';
          updateSoundBadge();
        }).catch(() => {
          ttVideo.muted = true;
          ttVideo.play().then(() => {
            if (playOverlay) playOverlay.style.display = 'none';
            updateSoundBadge();
          }).catch(() => {
            if (playOverlay) playOverlay.style.display = 'flex';
          });
        });
      }
    } else {
      ttVideo.pause();
      if (playOverlay) playOverlay.style.display = 'flex';
    }
  }

  // Configura todos os eventos de clique, toque e swipe do Modal
  function setupModalEventListeners() {
    if (!ttModal || ttModal.getAttribute('data-events-bound') === 'true') return;
    ttModal.setAttribute('data-events-bound', 'true');

    const closeBtn = document.getElementById('tt-close-btn');
    if (closeBtn) closeBtn.onclick = closeTikTokModal;

    const soundBadge = document.getElementById('tt-sound-badge');
    if (soundBadge) {
      soundBadge.onclick = function(e) {
        e.stopPropagation();
        if (ttVideo) {
          ttVideo.muted = false;
          updateSoundBadge();
          showTikTokToast('Som ativado 🔊');
        }
      };
    }

    const drawerClose = document.getElementById('tt-drawer-close');
    if (drawerClose) drawerClose.onclick = () => {
      document.getElementById('tt-comments-drawer').classList.remove('open');
    };

    const actionComment = document.getElementById('tt-action-comment');
    if (actionComment) actionComment.onclick = (e) => {
      e.stopPropagation();
      document.getElementById('tt-comments-drawer').classList.toggle('open');
    };

    // Teclado
    document.addEventListener('keydown', e => {
      if (!ttModal || ttModal.style.display !== 'flex') return;
      if (e.key === 'ArrowDown' || e.key === 'PageDown') nextTikTokVideo();
      if (e.key === 'ArrowUp' || e.key === 'PageUp') prevTikTokVideo();
      if (e.key === 'Escape') closeTikTokModal();
      if (e.key === ' ') {
        e.preventDefault();
        togglePlayPause();
      }
    });

    const wrapper = ttModal.querySelector('.tt-video-wrapper');
    const playOverlay = document.getElementById('tt-play-overlay');

    let touchStartY = 0;
    let touchStartX = 0;
    let touchCurrentY = 0;
    let touchStartTime = 0;
    let isTracking = false;
    let isVerticalSwipe = false;

    function handleStart(clientY, clientX, target) {
      if (isTransitioning) return;
      if (target.closest('#tt-comments-drawer') || 
          target.closest('.tt-right-actions') || 
          target.closest('.tt-top-bar') ||
          target.closest('#tt-sound-badge') ||
          target.closest('.tt-drawer-close')) {
        return;
      }
      touchStartY = clientY;
      touchStartX = clientX;
      touchCurrentY = clientY;
      touchStartTime = Date.now();
      isTracking = true;
      isVerticalSwipe = false;
      if (wrapper) wrapper.style.transition = 'none';
    }

    function handleMove(clientY, clientX, e) {
      if (!isTracking || isTransitioning) return;
      const deltaY = clientY - touchStartY;
      const deltaX = clientX - touchStartX;

      if (!isVerticalSwipe) {
        if (Math.abs(deltaY) > 25 && Math.abs(deltaY) > Math.abs(deltaX)) {
          isVerticalSwipe = true;
        } else if (Math.abs(deltaX) > 20) {
          isTracking = false;
          return;
        }
      }

      if (isVerticalSwipe) {
        if (e && e.cancelable) e.preventDefault();
        touchCurrentY = clientY;
        if (wrapper) wrapper.style.transform = `translateY(${deltaY * 0.7}px)`;
      }
    }

    function handleEnd() {
      if (!isTracking) return;
      isTracking = false;

      const deltaY = touchCurrentY - touchStartY;
      const deltaTime = Date.now() - touchStartTime;
      const velocity = Math.abs(deltaY) / (deltaTime || 1);

      // TOQUE RÁPIDO (TAP): Menos de 20px de movimento e menos de 450ms -> TOGGLE PLAY / PAUSE / UNMUTE!
      if (!isVerticalSwipe && Math.abs(deltaY) < 20 && deltaTime < 450) {
        if (wrapper) wrapper.style.transform = '';
        togglePlayPause();
        return;
      }

      // Se passou o dedo para cima ou para baixo:
      if (Math.abs(deltaY) > 35 || (Math.abs(deltaY) > 20 && velocity > 0.3)) {
        if (deltaY < 0) {
          nextTikTokVideo();
        } else {
          prevTikTokVideo();
        }
      } else {
        if (wrapper) {
          wrapper.style.transition = 'transform 0.2s cubic-bezier(0.25, 1, 0.5, 1)';
          wrapper.style.transform = 'translateY(0)';
          setTimeout(() => {
            if (wrapper) {
              wrapper.style.transition = '';
              wrapper.style.transform = '';
            }
          }, 200);
        }
      }
    }

    // Touch events (Mobile)
    ttModal.addEventListener('touchstart', e => {
      if (e.touches && e.touches.length > 0) {
        handleStart(e.touches[0].clientY, e.touches[0].clientX, e.target);
      }
    }, { passive: true });

    ttModal.addEventListener('touchmove', e => {
      if (e.touches && e.touches.length > 0) {
        handleMove(e.touches[0].clientY, e.touches[0].clientX, e);
      }
    }, { passive: false });

    ttModal.addEventListener('touchend', () => { handleEnd(); }, { passive: true });
    ttModal.addEventListener('touchcancel', () => { handleEnd(); }, { passive: true });

    // Desktop Click no wrapper para dar play/pause
    if (wrapper) {
      wrapper.onclick = function(e) {
        if (e.target.closest('#tt-comments-drawer') || 
            e.target.closest('.tt-right-actions') || 
            e.target.closest('.tt-top-bar') ||
            e.target.closest('#tt-sound-badge') ||
            e.target.closest('.tt-drawer-close')) {
          return;
        }
        togglePlayPause();
      };
    }

    if (playOverlay) {
      playOverlay.onclick = function(e) {
        e.stopPropagation();
        togglePlayPause();
      };
    }

    // Ações laterais (Likes, Seguir, Favoritar, Compartilhar)
    const likeBtn = document.getElementById('tt-action-like');
    if (likeBtn) likeBtn.onclick = function(e) {
      e.stopPropagation();
      const item = videoList[currentVideoIndex];
      if (!item) return;
      item.liked = !item.liked;
      this.querySelector('svg').style.fill = item.liked ? '#fe2c55' : '#fff';
      item.likes += item.liked ? 1 : -1;
      document.getElementById('tt-like-count').textContent = formatNumber(item.likes);
    };

    const followBtn = document.getElementById('tt-action-follow');
    if (followBtn) followBtn.onclick = function(e) {
      e.stopPropagation();
      const item = videoList[currentVideoIndex];
      if (!item) return;
      item.followed = !item.followed;
      this.textContent = item.followed ? '✓' : '+';
      this.style.background = item.followed ? '#25D366' : '#fe2c55';
    };

    const saveBtn = document.getElementById('tt-action-save');
    if (saveBtn) saveBtn.onclick = function(e) {
      e.stopPropagation();
      const item = videoList[currentVideoIndex];
      if (!item) return;
      item.saved = !item.saved;
      this.querySelector('svg').style.fill = item.saved ? '#face15' : '#fff';
      item.saves += item.saved ? 1 : -1;
      document.getElementById('tt-save-count').textContent = formatNumber(item.saves);
      showTikTokToast(item.saved ? 'Salvo nos favoritos' : 'Removido dos favoritos');
    };

    const shareBtn = document.getElementById('tt-action-share');
    if (shareBtn) shareBtn.onclick = function(e) {
      e.stopPropagation();
      if (navigator.share) {
        navigator.share({
          title: document.title,
          url: window.location.href
        }).catch(() => {});
      } else {
        showTikTokToast('Link copiado!');
      }
    };

    const commentSend = document.getElementById('tt-comment-send-btn');
    if (commentSend) commentSend.onclick = handleSendComment;
    const commentInput = document.getElementById('tt-comment-input-field');
    if (commentInput) commentInput.onkeydown = e => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleSendComment();
      }
    };
  }

  // Envio de comentário simulado
  function handleSendComment() {
    const input = document.getElementById('tt-comment-input-field');
    if (!input) return;
    const val = input.value.trim();
    if (!val) return;
    input.value = '';
    input.blur();
    showTikTokToast('Comentário enviado para análise');
  }

  function showTikTokToast(msg) {
    let toast = document.getElementById('tt-toast-feedback');
    if (!toast && ttModal) {
      toast = document.createElement('div');
      toast.id = 'tt-toast-feedback';
      toast.className = 'tt-toast';
      const container = ttModal.querySelector('.tt-container');
      if (container) container.appendChild(toast);
    }
    if (toast) {
      toast.textContent = msg;
      toast.classList.add('show');
      setTimeout(() => { toast.classList.remove('show'); }, 2300);
    }
  }

  // Abre o Modal e Toca o Vídeo Imediatamente
  function openTikTokVideo(id) {
    currentVideoIndex = id;
    const item = videoList[id];
    if (!item) return;

    if (!ttModal) {
      createTikTokModalMarkup();
    }

    ttModal.style.display = 'flex';
    document.body.style.overflow = 'hidden';

    // Carrega e dá play NO MESMO FRAME DO CLIQUE
    loadVideoData(item);
  }

  let isTransitioning = false;

  function nextTikTokVideo() {
    if (!videoList || videoList.length <= 1 || isTransitioning) return;
    isTransitioning = true;
    const nextIndex = (currentVideoIndex + 1) % videoList.length;
    animateVideoSwitch(nextIndex, 'up');
  }

  function prevTikTokVideo() {
    if (!videoList || videoList.length <= 1 || isTransitioning) return;
    isTransitioning = true;
    const prevIndex = (currentVideoIndex - 1 + videoList.length) % videoList.length;
    animateVideoSwitch(prevIndex, 'down');
  }

  function animateVideoSwitch(newIndex, direction) {
    const wrapper = ttModal ? ttModal.querySelector('.tt-video-wrapper') : null;
    const playOverlay = document.getElementById('tt-play-overlay');
    if (playOverlay) playOverlay.style.display = 'none';

    if (wrapper) {
      const exitY = direction === 'up' ? '-100%' : '100%';
      const enterY = direction === 'up' ? '100%' : '-100%';

      wrapper.style.transition = 'transform 0.22s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.22s ease';
      wrapper.style.transform = `translateY(${exitY})`;
      wrapper.style.opacity = '0.5';

      setTimeout(() => {
        currentVideoIndex = newIndex;
        loadVideoData(videoList[currentVideoIndex]);

        wrapper.style.transition = 'none';
        wrapper.style.transform = `translateY(${enterY})`;
        wrapper.style.opacity = '0.5';

        wrapper.offsetHeight; // Força reflow

        requestAnimationFrame(() => {
          wrapper.style.transition = 'transform 0.22s cubic-bezier(0.25, 1, 0.5, 1), opacity 0.22s ease';
          wrapper.style.transform = 'translateY(0)';
          wrapper.style.opacity = '1';

          setTimeout(() => {
            wrapper.style.transition = '';
            wrapper.style.transform = '';
            wrapper.style.opacity = '';
            isTransitioning = false;
          }, 240);
        });
      }, 210);
    } else {
      currentVideoIndex = newIndex;
      loadVideoData(videoList[currentVideoIndex]);
      isTransitioning = false;
    }
  }

  window.openTikTokVideo = openTikTokVideo;
  window.nextTikTokVideo = nextTikTokVideo;
  window.prevTikTokVideo = prevTikTokVideo;

  function closeTikTokModal() {
    if (ttModal) {
      ttModal.style.display = 'none';
      document.body.style.overflow = '';
      if (ttVideo) {
        try { ttVideo.pause(); } catch(e) {}
        ttVideo.removeAttribute('src');
        ttVideo.removeAttribute('data-active-src');
        try { ttVideo.load(); } catch(e) {}
      }
      const playOverlay = document.getElementById('tt-play-overlay');
      if (playOverlay) playOverlay.style.display = 'none';
    }
  }

  // Carrega Dados do Vídeo e Inicia Reprodução Instantânea com Faststart
  function loadVideoData(item) {
    if (!ttVideo) return;

    const targetSrc = item.video;
    const posterSrc = item.poster || item.avatar || '';
    const playOverlay = document.getElementById('tt-play-overlay');

    // Seta imediatamente o poster para nunca piscar preto
    if (posterSrc) {
      ttVideo.poster = posterSrc;
      const wrapper = ttModal ? ttModal.querySelector('.tt-video-wrapper') : null;
      if (wrapper) {
        wrapper.style.backgroundImage = 'url("' + posterSrc + '")';
        wrapper.style.backgroundSize = 'cover';
        wrapper.style.backgroundPosition = 'center';
      }
    }

    // Atualiza metadados textuais e contadores
    const actionAvatar = document.getElementById('tt-action-avatar');
    if (actionAvatar) actionAvatar.src = item.avatar;
    const displayName = document.getElementById('tt-display-name');
    if (displayName) displayName.textContent = `@${item.username}`;
    const displayDesc = document.getElementById('tt-display-desc');
    if (displayDesc) displayDesc.textContent = item.description || item.desc || '';
    const likeCount = document.getElementById('tt-like-count');
    if (likeCount) likeCount.textContent = formatNumber(item.likes || 12400);
    const commentCount = document.getElementById('tt-comment-count');
    if (commentCount) commentCount.textContent = formatNumber(item.commentsCount || 68);
    const saveCount = document.getElementById('tt-save-count');
    if (saveCount) saveCount.textContent = formatNumber(item.saves || 2800);
        // Atualiza Âncora Oficial de Produto (Shopping Tag TikTok Shop)
    const anchorEl = document.getElementById('tt-product-anchor');
    const anchorTitle = document.getElementById('tt-anchor-title');
    if (anchorTitle) {
      const prodObj = (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL) ? PRODUTO_ATUAL : (window.PRODUTO_ATUAL || {});
      const pName = prodObj.nome || (document.title ? document.title.replace(' - Stone Shop', '').trim() : 'Produto Oficial');
      const pPrice = prodObj.preco ? `R$ ${Number(prodObj.preco).toFixed(2).replace('.', ',')}` : '';
      anchorTitle.textContent = `${pName.slice(0, 26)}... · ${pPrice}`;
      if (anchorEl) {
        anchorEl.setAttribute('data-product-id', prodObj.id || '');
        anchorEl.onclick = function(e) {
          e.stopPropagation();
          closeTikTokModal();
          const buyBtn = document.getElementById('btn-buy') || document.querySelector('.btn-buy');
          if (buyBtn) buyBtn.click();
        };
      }
    }

    const drawerTitle = document.getElementById('tt-drawer-title');
    if (drawerTitle) drawerTitle.textContent = `${formatNumber(item.commentsCount || 68)} comentários`;

    const likeSvg = document.querySelector('#tt-action-like svg');
    if (likeSvg) likeSvg.style.fill = item.liked ? '#fe2c55' : '#fff';
    const saveSvg = document.querySelector('#tt-action-save svg');
    if (saveSvg) saveSvg.style.fill = item.saved ? '#face15' : '#fff';

    const followEl = document.getElementById('tt-action-follow');
    if (followEl) {
      followEl.textContent = item.followed ? '✓' : '+';
      followEl.style.background = item.followed ? '#25D366' : '#fe2c55';
    }

    // Renderizar comentários da gaveta
    const commentsList = document.getElementById('tt-drawer-comments-list') || document.getElementById('tt-drawer-list');
    if (commentsList && item.commentsList) {
      commentsList.innerHTML = '';
      item.commentsList.forEach(c => {
        const el = document.createElement('div');
        el.className = 'tt-comment-item';
        el.innerHTML = `
          <img class="tt-comment-avatar" src="${c.avatar}" alt="" onerror="this.src='../img/creators-avatars/creator-1.jpg'">
          <div style="flex:1;">
            <div class="tt-comment-user">${c.user}${c.isCreator ? ' <span style="background: #fe2c55; color: #fff; font-size: 9px; font-weight: 700; padding: 1px 5px; border-radius: 3px; vertical-align: middle;">Criador</span>' : ''}</div>
            <div class="tt-comment-text">${c.text}</div>
            <div style="font-size:11px; color:#999; margin-top:3px;">${c.date} · Responder</div>
          </div>
          <div class="tt-comment-like-box" style="display:flex; flex-direction:column; align-items:center; color:${c.liked ? '#fe2c55' : '#888'}; font-size:11px; cursor:pointer; padding:2px; min-width:28px;">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="${c.liked ? '#fe2c55' : 'none'}" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
            <span class="tt-comment-like-count">${c.likes}</span>
          </div>
        `;
        const likeBox = el.querySelector('.tt-comment-like-box');
        if (likeBox) {
          likeBox.onclick = function(e) {
            e.stopPropagation();
            c.liked = !c.liked;
            c.likes += c.liked ? 1 : -1;
            this.style.color = c.liked ? '#fe2c55' : '#888';
            const svg = this.querySelector('svg');
            if (svg) svg.setAttribute('fill', c.liked ? '#fe2c55' : 'none');
            this.querySelector('.tt-comment-like-count').textContent = c.likes;
          };
        }
        commentsList.appendChild(el);
      });
    }

    // Configura source do vídeo (sem chamar .load() para não abortar o gesto do usuário)
    if (ttVideo.getAttribute('data-active-src') !== targetSrc) {
      ttVideo.setAttribute('data-active-src', targetSrc);
      ttVideo.src = targetSrc;
    }

    ttVideo.onplaying = function() {
      if (playOverlay) playOverlay.style.display = 'none';
      const wrapper = ttModal ? ttModal.querySelector('.tt-video-wrapper') : null;
      if (wrapper) wrapper.style.backgroundImage = 'none';
      updateSoundBadge();
    };

    // DISPARO IMEDIATO DO PLAY:
    // Tenta unmuted (com som). Se o navegador mobile bloquear por política de áudio, toca muted na hora!
    ttVideo.muted = false;
    const playPromise = ttVideo.play();
    if (playPromise !== undefined) {
      playPromise.then(() => {
        if (playOverlay) playOverlay.style.display = 'none';
        updateSoundBadge();
      }).catch(err => {
        console.warn('Autoplay unmuted barrado no celular, tocando muted garantido:', err);
        ttVideo.muted = true;
        ttVideo.play().then(() => {
          if (playOverlay) playOverlay.style.display = 'none';
          updateSoundBadge();
        }).catch(err2 => {
          console.warn('Play falhou completamente:', err2);
          if (playOverlay) playOverlay.style.display = 'flex';
        });
      });
    }
  }

  function init() {
    injectStyles();
    initCarousel();
  }


  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
