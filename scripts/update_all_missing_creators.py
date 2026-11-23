# -*- coding: utf-8 -*-
"""
Script de atualização cirúrgica de js/videos-criadores.js
Executa com precisão todas as missões:
1. Bola 21 (Penalty Bravo XXV - rs5lzn.mp4)
2. Colchão 22 (Colchão Bestway - ekswrf.mp4 e qi938f.mp4)
3. Desacoplar Bike 94 (Spinning 120kg - perlvk.mp4)
4. Ativar os produtos com vídeos reais: P20, P35, P52, P55, P57, P58, P59, P61, P63, P65, P70, P73, P78, P80, P85, P87, P89, P91, P92, P95, P96, P97
5. Expandir MESA_118_VIDEOS_MAP com Tatiane Lar com Classe, Ana Achados do Lar, LiLi Indica, Panorama Móveis
"""

import re
import json

JS_PATH = 'js/videos-criadores.js'

with open(JS_PATH, 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Expandir MESA_118_VIDEOS_MAP
old_mesa_target = """  const MESA_118_VIDEOS_MAP = [
    {
      name: "Vanessa Decor",
      username: "vanessadecor_home",
      avatar: "../img/avatars-mesa/creator-vanessa.jpg",
      poster: "../videosprodutos/posters/poster-produto-118.jpg",
      video: "https://files.catbox.moe/uhw9mi.mp4",
      startTime: 0.2,
      desc: "Comprei essa mesa de jantar com 4 cadeiras estofadas na promoção e minha sala virou outra! Coube certinho no meu apartamento! 🛋️✨ #mesadejantar #apartamentopequeno #sala"
    },
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
  ];"""

new_mesa_target = """  const MESA_118_VIDEOS_MAP = [
    {
      name: "Vanessa Decor",
      username: "vanessadecor_home",
      avatar: "../img/avatars-mesa/creator-vanessa.jpg",
      poster: "../videosprodutos/posters/poster-produto-118.jpg",
      video: "https://files.catbox.moe/uhw9mi.mp4",
      startTime: 0.2,
      desc: "Comprei essa mesa de jantar com 4 cadeiras estofadas na promoção e minha sala virou outra! Coube certinho no meu apartamento! 🛋️✨ #mesadejantar #apartamentopequeno #sala"
    },
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
    },
    {
      name: "Tatiane Lar com Classe",
      username: "tatianelarcomclasse",
      avatar: "../img/reviews-avatars/unique/w_10.jpg",
      poster: "../videosprodutos/posters/poster-produto-118.jpg",
      video: "https://files.catbox.moe/uhw9mi.mp4",
      startTime: 0.2,
      desc: "Meninas, montamos a mesa de jantar com as 4 cadeiras estofadas na sala e o resultado ficou de novela! Qualidade absurda e super aconchegante! 🍽️✨ #mesadejantar #larcomclasse #decoracao"
    },
    {
      name: "Ana Achados do Lar",
      username: "anaachadosdolar",
      avatar: "../img/reviews-avatars/unique/w_15.jpg",
      poster: "../videosprodutos/posters/poster-produto-118-c2.jpg",
      video: "https://files.catbox.moe/nwj56a.mp4",
      startTime: 0.2,
      desc: "Achadinho perfeito para quem quer modernizar a sala de jantar! Tampo chanfrado resistente, cadeiras firmes e veludo suede muito macio! 😍👏 #achadinhos #mesaposta #sala"
    },
    {
      name: "LiLi Indica",
      username: "lili_indica_lar",
      avatar: "../img/reviews-avatars/unique/w_22.jpg",
      poster: "../videosprodutos/posters/poster-produto-118-c3.jpg",
      video: "https://files.catbox.moe/yr10g7.mp4",
      startTime: 0.2,
      desc: "Gente, apaixonada nessa mesa com 4 cadeiras estofadas! Muito prática, coube certinho e o frete grátis da Stone Shop chegou voando! 💖🛋️ #mesadejantar #dicasdecasa #saladejantar"
    },
    {
      name: "Panorama Móveis",
      username: "panoramamoveis",
      avatar: "../img/reviews-avatars/unique/m_12.jpg",
      poster: "../videosprodutos/posters/poster-produto-118-c4.jpg",
      video: "https://files.catbox.moe/vj6tzr.mp4",
      startTime: 0.2,
      desc: "Análise técnica do conjunto sala de jantar 4 cadeiras: estrutura em madeira reforçada, encaixes perfeitos e acabamento premium slim! Aprovadíssimo! 🛠️🏡 #panoramamoveis #saladejantar #moveis"
    }
  ];"""

if old_mesa_target in code:
    code = code.replace(old_mesa_target, new_mesa_target)
    print("MESA_118_VIDEOS_MAP expanded successfully!")
else:
    print("WARNING: old_mesa_target not found!")

# 2. Blindar isPanela122 contra produtos 89 e 92
panela_target = "const isPanela122 = (prodId === 122 || pageText.includes('pressão elétrica') || pageText.includes('pressao eletrica') || (pageText.includes('panela') && pageText.includes('pressão'))) && prodId !== 46;"
panela_repl = "const isPanela122 = (prodId === 122 || pageText.includes('pressão elétrica') || pageText.includes('pressao eletrica') || (pageText.includes('panela') && pageText.includes('pressão'))) && prodId !== 46 && prodId !== 89 && prodId !== 92;"
if panela_target in code:
    code = code.replace(panela_target, panela_repl)
    print("isPanela122 protected successfully!")

# 3. Gerar os blocos dos novos datasets
NEW_DATASETS_CODE = """
// ============================================================================
// DATASETS DEDICADOS COM VÍDEOS REAIS CATBOX PARA PRODUTOS SEM VÍDEO
// (BOLA 21, COLCHÃO 22, BIKE 94 E PRODUTOS COM MAPEAMENTO REAL CATBOX)
// ============================================================================

// 1. P20: Bicicleta Aro 29 GT Sprint MX7 24V MTB
const BIKE_GT_20_VIDEOS_MAP = [
  { name: "Lucas Pedal & Trilha", username: "lucas_mtb_brasil", avatar: "../img/reviews-avatars/unique/m_1.jpg", poster: "../videosprodutos/posters/video-produto-20.jpg", video: "https://files.catbox.moe/8oqszr.mp4", desc: "Aro 29 com 24 marchas indexadas e freio a disco potente! Bike sensacional pra trilha e asfalto! 🚴‍♂️⛰️ #bike #aro29 #mtbbrasil" },
  { name: "Mariana Ciclista", username: "mariciclista_fit", avatar: "../img/reviews-avatars/unique/w_1.jpg", poster: "../videosprodutos/posters/video-produto-20-take1.jpg", video: "https://files.catbox.moe/8oqszr.mp4", desc: "Montagem super tranquila, quadro de alumínio leve e suspensão dianteira que absorve muito bem os impactos! Amei! ✨🚴‍♀️ #ciclismo #bikegtsprint #saude" },
  { name: "Diego Trilha Radicais", username: "diegomtb_radical", avatar: "../img/reviews-avatars/unique/m_2.jpg", poster: "../videosprodutos/posters/video-produto-20-take2.jpg", video: "https://files.catbox.moe/8oqszr.mp4", desc: "Testei na subida de serra com cascalho, as 24 velocidades trocam suave sem pular corrente. Melhor custo-benefício! 👏💪 #mtb #biketop #stone" },
  { name: "Renato Dicas de Bike", username: "renatobikedicas", avatar: "../img/reviews-avatars/unique/m_3.jpg", poster: "../videosprodutos/posters/video-produto-20-take3.jpg", video: "https://files.catbox.moe/8oqszr.mp4", desc: "GT Sprint MX7 original com cupom na Stone Shop! Entrega rápida e produto muito bem embalado na caixa! 📦🔥 #unboxingbike #gtsprint #pedal" },
  { name: "Felipe Pedala Mais", username: "felipepedalamais", avatar: "../img/reviews-avatars/unique/m_4.jpg", poster: "../videosprodutos/posters/video-produto-20-take4.jpg", video: "https://files.catbox.moe/8oqszr.mp4", desc: "Pedalando 30km por dia para trabalhar, bike super confortável e econômica. Recomendo de olhos fechados! 🚴💨 #pedalurbano #bike29 #mobilidade" }
];
const CREATORS_BIKE_GT_20 = BIKE_GT_20_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 16200 + i * 2300, commentsCount: 145 + i * 25, sharesCount: 55 + i * 12, savesCount: 1320 + i * 180, description: b.desc }));

// 2. P21: Bola De Futebol De Campo Penalty Bravo XXV (Zero ar condicionado)
const BOLA_PENALTY_21_VIDEOS_MAP = [
  { name: "Felipe Fut & Treino", username: "felipefut_treino", avatar: "../img/reviews-avatars/unique/m_5.jpg", poster: "../videosprodutos/posters/video-produto-21.jpg", video: "https://files.catbox.moe/rs5lzn.mp4", desc: "Testando a Penalty Bravo XXV de campo! Quique macio, peso oficial de 430g e costura Termotec que não absorve água! ⚽🔥 #futebol #penalty #futeboldecampo" },
  { name: "Lucas Boleiro", username: "lucasboleiro_oficial", avatar: "../img/reviews-avatars/unique/m_6.jpg", poster: "../videosprodutos/posters/video-produto-21-take1.jpg", video: "https://files.catbox.moe/rs5lzn.mp4", desc: "Precisão absurda na finalização! Bola de campo original Penalty com bico lubrificado e câmara 6D. Top demais! 🎯⚽ #pelada #chute #boleiro" },
  { name: "Matheus Futebol Raiz", username: "matheusfutebol_raiz", avatar: "../img/reviews-avatars/unique/m_7.jpg", poster: "../videosprodutos/posters/video-produto-21-take2.jpg", video: "https://files.catbox.moe/rs5lzn.mp4", desc: "Comprei pro nosso campeonato de fim de semana na Stone Shop. Todo mundo curtiu o acabamento reforçado! 🏆👏 #futebolraiz #penaltybravo #campeonato" },
  { name: "Thiago Camisa 10", username: "thiagocamisa10_", avatar: "../img/reviews-avatars/unique/m_8.jpg", poster: "../videosprodutos/posters/video-produto-21-take3.jpg", video: "https://files.catbox.moe/rs5lzn.mp4", desc: "Bateu não deforma! Durabilidade insana tanto no gramado natural quanto sintético. Vale cada centavo! ⚽⚡ #futebolarte #golaço #penalty" },
  { name: "Gabriel Silva Esportes", username: "gabrielesportesbr", avatar: "../img/reviews-avatars/unique/m_9.jpg", poster: "../videosprodutos/posters/video-produto-21-take4.jpg", video: "https://files.catbox.moe/rs5lzn.mp4", desc: "Entrega relâmpago da Stone Shop, bola veio bem calibrada e com selo oficial Penalty! Show! 📦⚽ #reviewesportivo #penaltyoficial #futebolbr" }
];
const CREATORS_BOLA_PENALTY_21 = BOLA_PENALTY_21_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 18400 + i * 2100, commentsCount: 168 + i * 28, sharesCount: 62 + i * 15, savesCount: 1450 + i * 190, description: b.desc }));

// 3. P22: Colchão Inflável Bestway Casal Suporta 300kg + Bomba (Zero ar condicionado)
const COLCHAO_BESTWAY_22_VIDEOS_MAP = [
  { name: "Rodrigo Camping & Aventura", username: "rodrigocamping_br", avatar: "../img/reviews-avatars/unique/m_10.jpg", poster: "../videosprodutos/posters/video-produto-22.jpg", video: "https://files.catbox.moe/ekswrf.mp4", desc: "Testando o Colchão Inflável Bestway Casal que suporta 300kg! Acompanha bomba manual e infla em menos de 5 minutos! ⛺🌲 #camping #colchaoinflavel #bestway" },
  { name: "Camila Vida ao Ar Livre", username: "camilacamping_life", avatar: "../img/reviews-avatars/unique/w_2.jpg", poster: "../videosprodutos/posters/video-produto-22-take1.jpg", video: "https://files.catbox.moe/qi938f.mp4", desc: "Toque aveludado super confortável que não escorrega o lençol. Salvou nossa viagem de acampamento em família! 🥰✨ #acampamento #vidaaoarlivre #conforto" },
  { name: "Bruno Dicas de Casa", username: "brunodicasdecasa", avatar: "../img/reviews-avatars/unique/m_11.jpg", poster: "../videosprodutos/posters/video-produto-22-take2.jpg", video: "https://files.catbox.moe/ekswrf.mp4", desc: "Perfeito para receber visitas em casa sem ocupar espaço. Esvazia rapidinho e dobra bem compacto na mochila! 👏🏡 #casa #visitas #dicaspraticas" },
  { name: "Juliana Mochilão", username: "ju_mochilao", avatar: "../img/reviews-avatars/unique/w_3.jpg", poster: "../videosprodutos/posters/video-produto-22-take3.jpg", video: "https://files.catbox.moe/qi938f.mp4", desc: "Material vinílico resistente e reforçado, não esvaziou nada durante a noite toda! Nota 10 pro Bestway! 🎒🌙 #mochilao #trip #colchaocasal" },
  { name: "Diego Camping Brasil", username: "diegocampingbr", avatar: "../img/reviews-avatars/unique/m_13.jpg", poster: "../videosprodutos/posters/video-produto-22-take4.jpg", video: "https://files.catbox.moe/ekswrf.mp4", desc: "Comprei na Stone Shop com super desconto e frete grátis. Válvula de esvaziamento rápido muito prática! 📦🔥 #bestwaybrasil #campinglife #comprinhas" }
];
const CREATORS_COLCHAO_BESTWAY_22 = COLCHAO_BESTWAY_22_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 17300 + i * 2200, commentsCount: 154 + i * 26, sharesCount: 58 + i * 14, savesCount: 1390 + i * 175, description: b.desc }));

// 4. P35: Caixa de Som JBL Boombox 4 Bluetooth 210W
const JBL_BOOMBOX4_35_VIDEOS_MAP = [
  { name: "Caio Sound Test", username: "caiosoundtest", avatar: "../img/reviews-avatars/unique/m_14.jpg", poster: "../videosprodutos/posters/video-produto-35.jpg", video: "https://files.catbox.moe/s313zy.mp4", desc: "A monstra chegou! JBL Boombox 4 com 210W de potência real e graves que fazem a parede tremer! 🔊🔥 #jbl #boombox4 #sompesado" },
  { name: "Bia Festas & Eventos", username: "biafestasbr", avatar: "../img/reviews-avatars/unique/w_4.jpg", poster: "../videosprodutos/posters/video-produto-35-take1.jpg", video: "https://files.catbox.moe/s313zy.mp4", desc: "Bateria que dura até 24 horas e proteção à prova d'água IP67. Levei pra beira da piscina e foi o show da festa! 💦🎉 #jblboombox #festa #caixadesom" },
  { name: "Rodrigo Tech Áudio", username: "rodrigotechaudio", avatar: "../img/reviews-avatars/unique/m_15.jpg", poster: "../videosprodutos/posters/video-produto-35-take2.jpg", video: "https://files.catbox.moe/s313zy.mp4", desc: "Clareza nos médios e agudos mesmo no volume máximo. JBL é outro nível de fidelidade sonora! 👏🎶 #somautomotivo #audiotech #qualidade" },
  { name: "Gustavo Som & Graves", username: "gustavosomgraves", avatar: "../img/reviews-avatars/unique/m_16.jpg", poster: "../videosprodutos/posters/video-produto-35-take3.jpg", video: "https://files.catbox.moe/s313zy.mp4", desc: "Original lacrada na caixa com nota e garantia! O cupom da Stone Shop deu mais de R$ 400 de desconto! 📦💥 #jbloficial #desconto #stoneshop" },
  { name: "Larissa Music Vibe", username: "larissamusicvibe", avatar: "../img/reviews-avatars/unique/w_5.jpg", poster: "../videosprodutos/posters/video-produto-35-take4.jpg", video: "https://files.catbox.moe/s313zy.mp4", desc: "Conexão Bluetooth instantânea e app dedicado da JBL com equalizador completo. Apaixonada! 😍✨ #jblbrasil #musica #graves" }
];
const CREATORS_JBL_BOOMBOX4_35 = JBL_BOOMBOX4_35_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 28900 + i * 3100, commentsCount: 260 + i * 42, sharesCount: 95 + i * 22, savesCount: 2200 + i * 260, description: b.desc }));

// 5. P52: iPad 11 Geração A16 256GB Wi-Fi
const PAD11_52_VIDEOS_MAP = [
  { name: "Lucas Apple Tech", username: "lucasappletech", avatar: "../img/reviews-avatars/unique/m_17.jpg", poster: "../videosprodutos/posters/video-produto-52.jpg", video: "https://files.catbox.moe/3rtr42.mp4", desc: "Unboxing do novo iPad 11 com chip A16 e 256GB! Desempenho absurdo pra edição de vídeo e multitarefa! 📱⚡ #ipad #apple #ipad11" },
  { name: "Juliana Estudante", username: "juestudos_med", avatar: "../img/reviews-avatars/unique/w_6.jpg", poster: "../videosprodutos/posters/video-produto-52-take1.jpg", video: "https://files.catbox.moe/3rtr42.mp4", desc: "Melhor companheiro de faculdade! A tela de 11 polegadas com True Tone não cansa a vista e a bateria dura o dia todo! 📚✨ #studygram #ipadestudos #medicina" },
  { name: "Felipe Designer", username: "felipedesign_br", avatar: "../img/reviews-avatars/unique/m_18.jpg", poster: "../videosprodutos/posters/video-produto-52-take2.jpg", video: "https://files.catbox.moe/3rtr42.mp4", desc: "Compatível com Apple Pencil, latência zero no desenho. Tela líquida de altíssima definição! 🎨👏 #design #procreate #appleipad" },
  { name: "Beatriz Produtividade", username: "biaprodutiva", avatar: "../img/reviews-avatars/unique/w_7.jpg", poster: "../videosprodutos/posters/video-produto-52-take3.jpg", video: "https://files.catbox.moe/3rtr42.mp4", desc: "Original lacrado com 1 ano de garantia Apple! Chegou em 2 dias aqui pela Stone Shop! 📦💖 #unboxing #produtividade #ipad256gb" },
  { name: "André TechReview", username: "andretechreview", avatar: "../img/reviews-avatars/unique/m_19.jpg", poster: "../videosprodutos/posters/video-produto-52-take4.jpg", video: "https://files.catbox.moe/3rtr42.mp4", desc: "Câmeras 4K nítidas e som estéreo imersivo. O melhor tablet do mercado sem dúvidas! 🚀📱 #tecnologia #applebrasil #gadgets" }
];
const CREATORS_PAD11_52 = PAD11_52_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 31200 + i * 3400, commentsCount: 290 + i * 45, sharesCount: 110 + i * 25, savesCount: 2500 + i * 290, description: b.desc }));

// 6. P55: Nintendo Switch Desbloqueado + 10 Jogos 128GB
const SWITCH_55_VIDEOS_MAP = [
  { name: "Renan Games Brasil", username: "renangames_br", avatar: "../img/reviews-avatars/unique/m_20.jpg", poster: "../videosprodutos/posters/video-produto-55.jpg", video: "https://files.catbox.moe/wvgft8.mp4", desc: "Nintendo Switch já desbloqueado com cartão de 128GB e os 10 melhores jogos à sua escolha! É ligar e jogar! 🎮🔥 #nintendoswitch #games #switchdesbloqueado" },
  { name: "Carla Gamer", username: "carlagamer_oficial", avatar: "../img/reviews-avatars/unique/w_8.jpg", poster: "../videosprodutos/posters/video-produto-55-take1.jpg", video: "https://files.catbox.moe/wvgft8.mp4", desc: "Mario Kart 8, Zelda e Smash Bros rodando liso! Tela perfeita e bateria excelente para jogar no sofá ou viagens! 🥰🎮 #nintendo #mariokart #zelda" },
  { name: "Matheus Jogatina", username: "matheusjogatina", avatar: "../img/reviews-avatars/unique/m_21.jpg", poster: "../videosprodutos/posters/video-produto-55-take2.jpg", video: "https://files.catbox.moe/wvgft8.mp4", desc: "Sistema super seguro e atualizado, não perde o desbloqueio. Economia gigante em jogos! 👏🕹️ #gamer #consoles #dicasdegames" },
  { name: "Diego PlayTime", username: "diegoplaytime", avatar: "../img/reviews-avatars/unique/m_22.jpg", poster: "../videosprodutos/posters/video-produto-55-take3.jpg", video: "https://files.catbox.moe/wvgft8.mp4", desc: "Comprei na Stone Shop e veio tudo 100% configurado com suporte do vendedor. Recomendo muito! 📦✨ #unboxinggame #nintendobrasil #videogame" },
  { name: "Letícia Geek", username: "leticiageek_", avatar: "../img/reviews-avatars/unique/w_9.jpg", poster: "../videosprodutos/posters/video-produto-55-take4.jpg", video: "https://files.catbox.moe/wvgft8.mp4", desc: "Console híbrido fantástico! Conecta na TV em segundos e a resolução fica incrível! 🌟👾 #geek #gamers #jogos" }
];
const CREATORS_SWITCH_55 = SWITCH_55_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 27500 + i * 2900, commentsCount: 240 + i * 36, sharesCount: 88 + i * 20, savesCount: 2150 + i * 240, description: b.desc }));

// 7. P57: Caixa de Som Joog One Hifi 200W com 2 Microfones Sem Fio
const JOOG_ONE_57_VIDEOS_MAP = [
  { name: "Marcos Karaokê Show", username: "marcoskaraoke_show", avatar: "../img/reviews-avatars/unique/m_23.jpg", poster: "../videosprodutos/posters/video-produto-57.jpg", video: "https://files.catbox.moe/v36v5l.mp4", desc: "Caixa Joog One 200W HiFi com 2 microfones sem fio inclusos! O som é limpíssimo e o eco do microfone é profissional! 🎤🔊 #karaoke #joogone #caixadesom" },
  { name: "Patrícia Dicas Musicais", username: "patymusica_br", avatar: "../img/reviews-avatars/unique/w_11.jpg", poster: "../videosprodutos/posters/video-produto-57-take1.jpg", video: "https://files.catbox.moe/v36v5l.mp4", desc: "Proteção IP67 resistente à água e controle remoto completo! A festa na praia foi sensacional com essa Joog One! 🌊🎶 #festa #somhifi #joog" },
  { name: "Bruno Áudio Pro", username: "brunoaudiopro", avatar: "../img/reviews-avatars/unique/m_24.jpg", poster: "../videosprodutos/posters/video-produto-57-take2.jpg", video: "https://files.catbox.moe/v36v5l.mp4", desc: "Conexão TWS para parear duas caixas e app dedicado. Bateria dura muitas horas de cantoria! 👏🔥 #tecnologia #somdequalidade #churrasco" },
  { name: "Fernanda Festas", username: "nandafestas_", avatar: "../img/reviews-avatars/unique/w_12.jpg", poster: "../videosprodutos/posters/video-produto-57-take3.jpg", video: "https://files.catbox.moe/v36v5l.mp4", desc: "Luzes dinâmicas de LED e som encorpado com graves marcantes. A criançada e os adultos amaram! 💖🎉 #animacao #festadefamilia #karaokeshow" },
  { name: "Thiago Som Automotivo", username: "thiagosom_", avatar: "../img/reviews-avatars/unique/m_25.jpg", poster: "../videosprodutos/posters/video-produto-57-take4.jpg", video: "https://files.catbox.moe/v36v5l.mp4", desc: "Entrega super rápida da Stone Shop. Caixa robusta com alça reforçada pra transporte! 📦🔊 #unboxing #qualidade #recomendo" }
];
const CREATORS_JOOG_ONE_57 = JOOG_ONE_57_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21400 + i * 2500, commentsCount: 188 + i * 30, sharesCount: 72 + i * 16, savesCount: 1720 + i * 210, description: b.desc }));

// 8. P58: Caixa de Som Alexa Echo Dot 5ª Geração
const ECHODOT_58_VIDEOS_MAP = [
  { name: "Gabriel Casa Inteligente", username: "gabrielcasasmart", avatar: "../img/reviews-avatars/unique/m_26.jpg", poster: "../videosprodutos/posters/video-produto-58.jpg", video: "https://files.catbox.moe/v6io74.mp4", desc: "A nova Echo Dot 5ª Geração tem graves 2x mais potentes e sensor de temperatura integrado! Alexa é vida! 🏠🗣️ #echodot5 #alexa #casainteligente" },
  { name: "Amanda Smart Home", username: "amandasmarthome", avatar: "../img/reviews-avatars/unique/w_13.jpg", poster: "../videosprodutos/posters/video-produto-58-take1.jpg", video: "https://files.catbox.moe/v6io74.mp4", desc: "Automatizei toda minha casa com lâmpadas e TV na Alexa! Peço músicas e ela responde na hora com som cristalino! ✨🎵 #automacaoresidencial #alexabrasil #dicas" },
  { name: "Felipe Tech Diário", username: "felipetechdiario", avatar: "../img/reviews-avatars/unique/m_27.jpg", poster: "../videosprodutos/posters/video-produto-58-take2.jpg", video: "https://files.catbox.moe/v6io74.mp4", desc: "Original Amazon lacrada com envio imediato pela Stone Shop. Melhor preço da internet! 📦👏 #unboxingalexa #amazon #gadgets" },
  { name: "Larissa Rotina Smart", username: "larissarotinasmart", avatar: "../img/reviews-avatars/unique/w_14.jpg", poster: "../videosprodutos/posters/video-produto-58-take3.jpg", video: "https://files.catbox.moe/v6io74.mp4", desc: "Uso de despertador e para ouvir notícias e podcasts de manhã enquanto faço café. Praticidade pura! ☕💖 #rotina #morandosozinha #alexa" },
  { name: "Rodrigo Gadgets BR", username: "rodrigogadgetsbr", avatar: "../img/reviews-avatars/unique/m_28.jpg", poster: "../videosprodutos/posters/video-produto-58-take4.jpg", video: "https://files.catbox.moe/v6io74.mp4", desc: "Design esférico sofisticado que combina com qualquer decoração de sala ou quarto. Vale cada centavo! 🌟🛋️ #smarthome #tecnologia #design" }
];
const CREATORS_ECHODOT_58 = ECHODOT_58_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25800 + i * 2800, commentsCount: 225 + i * 35, sharesCount: 82 + i * 19, savesCount: 2050 + i * 230, description: b.desc }));

// 9. P59: Mini Antena Internet Satélite Original
const STARLINK_59_VIDEOS_MAP = [
  { name: "Carlos Vida no Campo", username: "carlos_vidanocampo", avatar: "../img/reviews-avatars/unique/m_29.jpg", poster: "../videosprodutos/posters/video-produto-59.jpg", video: "https://files.catbox.moe/s6vnyh.mp4", desc: "Internet de 200 Megas no sítio onde não pegava nem sinal de celular! Essa mini antena via satélite é milagrosa! 📡🌾 #starlink #internetrural #sitio" },
  { name: "Renata Motorhome", username: "renatamotorhome_br", avatar: "../img/reviews-avatars/unique/w_16.jpg", poster: "../videosprodutos/posters/video-produto-59-take1.jpg", video: "https://files.catbox.moe/s6vnyh.mp4", desc: "Trabalho remoto viajando pelo Brasil todo no motorhome! Conexão estável em qualquer praia ou serra! 🚐✨ #nomadedigital #motorhome #viagem" },
  { name: "Marcos Agro Tech", username: "marcosagrotech", avatar: "../img/reviews-avatars/unique/m_30.jpg", poster: "../videosprodutos/posters/video-produto-59-take2.jpg", video: "https://files.catbox.moe/s6vnyh.mp4", desc: "Instalação fácil em 10 minutos pelo aplicativo. Aponta pro céu e o satélite conecta automático! 👏🛰️ #agronegocio #fazenda #tecnologia" },
  { name: "Thiago Conectado", username: "thiagoconectado", avatar: "../img/reviews-avatars/unique/m_31.jpg", poster: "../videosprodutos/posters/video-produto-59-take3.jpg", video: "https://files.catbox.moe/s6vnyh.mp4", desc: "Ping baixo pra jogos online e streaming em 4K sem travar nada. Produto original com 1 ano de garantia! 📦🎮 #internetrapida #viasatelite #stone" },
  { name: "Juliana Expedições", username: "juexpedicoes", avatar: "../img/reviews-avatars/unique/w_17.jpg", poster: "../videosprodutos/posters/video-produto-59-take4.jpg", video: "https://files.catbox.moe/s6vnyh.mp4", desc: "Leve e compacta, cabe na mochila de camping. A melhor aquisição para quem vive na estrada! 🌲🏕️ #aventura #offroad #conexao" }
];
const CREATORS_STARLINK_59 = STARLINK_59_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 29800 + i * 3200, commentsCount: 270 + i * 40, sharesCount: 102 + i * 24, savesCount: 2380 + i * 270, description: b.desc }));

// 10. P61: Caixa de Som Joog Amplificada Break X1 Touch 13" 800W Android
const JOOG_BREAK_61_VIDEOS_MAP = [
  { name: "DJ Sandro Eventos", username: "djsandro_eventos", avatar: "../img/reviews-avatars/unique/m_32.jpg", poster: "../videosprodutos/posters/video-produto-61.jpg", video: "https://files.catbox.moe/32ulh9.mp4", desc: "Joog Break X1 com 800W e tela touch de 13 polegadas com sistema Android! Você abre o YouTube direto nela e canta! 🎤🔥 #joogbreakx1 #somprofissional #dj" },
  { name: "Camila Festas VIP", username: "camilafestas_vip", avatar: "../img/reviews-avatars/unique/w_18.jpg", poster: "../videosprodutos/posters/video-produto-61-take1.jpg", video: "https://files.catbox.moe/32ulh9.mp4", desc: "Parece um karaokê de shopping em casa! Os 2 microfones sem fio têm alcance enorme e zero delay! 👏🎶 #karaokeprofissional #festas #luxo" },
  { name: "Rodrigo Bass Master", username: "rodrigobassmaster", avatar: "../img/reviews-avatars/unique/m_33.jpg", poster: "../videosprodutos/posters/video-produto-61-take2.jpg", video: "https://files.catbox.moe/32ulh9.mp4", desc: "800W de pancada limpa! Roda Spotify, YouTube, Netflix e jogos direto na tela touchscreen de 13 pol! 🚀🔊 #caixadesom #touchscreen #android" },
  { name: "Fernanda Família Feliz", username: "nandafamilia_", avatar: "../img/reviews-avatars/unique/w_19.jpg", poster: "../videosprodutos/posters/video-produto-61-take3.jpg", video: "https://files.catbox.moe/32ulh9.mp4", desc: "Todo sábado a família se reúne para cantar com as letras passando na tela. Melhor presente que já comprei! 💖🎉 #familia #diversao #fimdesemana" },
  { name: "Eduardo Tech Som", username: "edutechsom", avatar: "../img/reviews-avatars/unique/m_34.jpg", poster: "../videosprodutos/posters/video-produto-61-take4.jpg", video: "https://files.catbox.moe/32ulh9.mp4", desc: "Chegou impecável pela Stone Shop com nota fiscal e garantia. Acabamento premium e som potente! 📦💥 #unboxing #qualidade #recomendo" }
];
const CREATORS_JOOG_BREAK_61 = JOOG_BREAK_61_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 32400 + i * 3500, commentsCount: 310 + i * 48, sharesCount: 115 + i * 26, savesCount: 2600 + i * 300, description: b.desc }));

// 11. P63: Smartwatch Redmi Watch 5 Lite GPS
const REDMI_WATCH_63_VIDEOS_MAP = [
  { name: "Felipe Corredor", username: "felipecorredor_fit", avatar: "../img/reviews-avatars/unique/m_35.jpg", poster: "../videosprodutos/posters/video-produto-63.jpg", video: "https://files.catbox.moe/z40bo0.mp4", desc: "Redmi Watch 5 Lite com GPS integrado independente do celular! A precisão na corrida de rua é cirúrgica! 🏃‍♂️⌚ #redmiwatch5 #smartwatch #corrida" },
  { name: "Mariana Fitness Diário", username: "marifit_diario", avatar: "../img/reviews-avatars/unique/w_20.jpg", poster: "../videosprodutos/posters/video-produto-63-take1.jpg", video: "https://files.catbox.moe/z40bo0.mp4", desc: "Bateria que dura 18 dias sem recarregar! Monitora sono, batimentos, oxigênio e ciclo menstrual com perfeição! ✨💪 #saude #fitness #xiaomi" },
  { name: "Lucas Tech Geek", username: "lucastechgeek", avatar: "../img/reviews-avatars/unique/m_36.jpg", poster: "../videosprodutos/posters/video-produto-63-take2.jpg", video: "https://files.catbox.moe/z40bo0.mp4", desc: "Tela AMOLED linda com brilho forte mesmo debaixo de sol, atende chamadas com microfone duplo! 👏📱 #smartwatchxiaomi #tecnologia #dicas" },
  { name: "Bárbara Treino & Saúde", username: "barbaratreinos", avatar: "../img/reviews-avatars/unique/w_21.jpg", poster: "../videosprodutos/posters/video-produto-63-take3.jpg", video: "https://files.catbox.moe/z40bo0.mp4", desc: "Mais de 140 modos de treino esportivo e resistência à água de 5 ATM. Faço natação com ele tranquilamente! 🏊‍♀️💖 #natacao #academia #relogio" },
  { name: "Diego Unboxing BR", username: "diegounboxingbr", avatar: "../img/reviews-avatars/unique/m_37.jpg", poster: "../videosprodutos/posters/video-produto-63-take4.jpg", video: "https://files.catbox.moe/z40bo0.mp4", desc: "Original versão global lacrado com envio rápido da Stone Shop! Melhor custo-benefício disparado! 📦🔥 #xiaomibrasil #unboxing #achadinhos" }
];
const CREATORS_REDMI_WATCH_63 = REDMI_WATCH_63_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 24100 + i * 2600, commentsCount: 195 + i * 32, sharesCount: 76 + i * 18, savesCount: 1880 + i * 220, description: b.desc }));

// 12. P65: Sofá 3 Lugares Retrátil e Reclinável Cama inBox Senses 2,00m
const SOFA_SENSES_65_VIDEOS_MAP = [
  { name: "Juliana Decora Lar", username: "judecoralar", avatar: "../img/reviews-avatars/unique/w_23.jpg", poster: "../videosprodutos/posters/video-produto-65.jpg", video: "https://files.catbox.moe/my8eud.mp4", desc: "Chegou nosso Sofá Cama inBox Senses de 2 metros! Tecido Velusoft cinza super macio e retrátil que vira cama de casal! 🛋️✨ #sofaretratil #camainbox #saladeestar" },
  { name: "Thiago & Lu Apê", username: "thiagoelu_nossoap", avatar: "../img/reviews-avatars/unique/m_38.jpg", poster: "../videosprodutos/posters/video-produto-65-take1.jpg", video: "https://files.catbox.moe/my8eud.mp4", desc: "Molas ensacadas e espuma D33 que não afundam com o tempo. Maratona de filmes no fim de semana garantida! 🍿😍 #decoracao #apartamentopequeno #conforto" },
  { name: "Patrícia Casa Linda", username: "patycasalinda_", avatar: "../img/reviews-avatars/unique/w_24.jpg", poster: "../videosprodutos/posters/video-produto-65-take2.jpg", video: "https://files.catbox.moe/my8eud.mp4", desc: "O encosto reclinável tem vários estágios e o veludo é muito fácil de limpar. Aprovadíssimo! 👏🏡 #sofa #moveis #achadinhos" },
  { name: "Rodrigo Arquitetura", username: "rodrigoarquitetura_br", avatar: "../img/reviews-avatars/unique/m_39.jpg", poster: "../videosprodutos/posters/video-produto-65-take3.jpg", video: "https://files.catbox.moe/my8eud.mp4", desc: "Design moderno com braços almofadados e rodízios de silicone que não arranham o piso laminado. Top! 🛠️🛋️ #arquitetura #designdeinteriores #saladetv" },
  { name: "Camila Vida Nova", username: "camilavidanova_", avatar: "../img/reviews-avatars/unique/w_25.jpg", poster: "../videosprodutos/posters/video-produto-65-take4.jpg", video: "https://files.catbox.moe/my8eud.mp4", desc: "Entrega excelente da Stone Shop com montagem rápida! O sofá é gigante e aconchegante! 📦💖 #comprinhas #donadecasa #moveisnovos" }
];
const CREATORS_SOFA_SENSES_65 = SOFA_SENSES_65_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 28500 + i * 3000, commentsCount: 250 + i * 38, sharesCount: 90 + i * 21, savesCount: 2280 + i * 250, description: b.desc }));

// 13. P70: Secadora de Roupa Mueller Solaris 8kg
const SECADORA_MUELLER_70_VIDEOS_MAP = [
  { name: "Simone Dicas de Lavanderia", username: "simonelavanderia", avatar: "../img/reviews-avatars/unique/w_26.jpg", poster: "../videosprodutos/posters/video-produto-70.jpg", video: "https://files.catbox.moe/n5jecm.mp4", desc: "Secadora de parede Mueller Solaris 8kg! Salvou meus dias de chuva, roupa sequinha e cheirosa em menos de 1 hora! 👕☀️ #secadoraderoupa #mueller #lavanderia" },
  { name: "Renata Mãe Prática", username: "renatamaepratica", avatar: "../img/reviews-avatars/unique/w_27.jpg", poster: "../videosprodutos/posters/video-produto-70-take1.jpg", video: "https://files.catbox.moe/n5jecm.mp4", desc: "Vem com 6 varões e 5 cabides, as roupas já saem praticamente passadas sem amassados! Economiza muito tempo! 😍✨ #donadecasa #maternidade #praticidade" },
  { name: "Marcos Organiza Tudo", username: "marcosorganizatudo", avatar: "../img/reviews-avatars/unique/m_40.jpg", poster: "../videosprodutos/posters/video-produto-70-take2.jpg", video: "https://files.catbox.moe/n5jecm.mp4", desc: "Instalação fácil na parede que não ocupa nada de espaço no chão da área de serviço. Muito silenciosa! 👏🏡 #apartamento #areadeservico #dicas" },
  { name: "Aline Casa Limpa", username: "alinecasalimpa_", avatar: "../img/reviews-avatars/unique/w_28.jpg", poster: "../videosprodutos/posters/video-produto-70-take3.jpg", video: "https://files.catbox.moe/n5jecm.mp4", desc: "Ciclo de ar quente para secar e ar frio para amaciar os tecidos. A melhor compra pro inverno e dias úmidos! 🌧️💖 #secadoramueller #roupaslimpas #casa" },
  { name: "Fábio Dicas Úteis", username: "fabiodicasuteis", avatar: "../img/reviews-avatars/unique/m_41.jpg", poster: "../videosprodutos/posters/video-produto-70-take4.jpg", video: "https://files.catbox.moe/n5jecm.mp4", desc: "Comprei na Stone Shop com frete grátis e chegou em 3 dias. Produto robusto e econômico na conta de luz! 📦⚡ #economia #eletrodomesticos #stone" }
];
const CREATORS_SECADORA_MUELLER_70 = SECADORA_MUELLER_70_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 22600 + i * 2400, commentsCount: 192 + i * 28, sharesCount: 68 + i * 15, savesCount: 1780 + i * 190, description: b.desc }));

// 14. P73: Caixa Bluetooth Waaw Hyperboom 1000 by Alok
const WAAW_HYPERBOOM_73_VIDEOS_MAP = [
  { name: "DJ Bruno Alok Vibe", username: "brunodjvibe", avatar: "../img/reviews-avatars/unique/m_42.jpg", poster: "../videosprodutos/posters/video-produto-73.jpg", video: "https://files.catbox.moe/qd8ybp.mp4", desc: "Waaw Hyperboom 1000 assinada pelo Alok! Graves absurdos e show de luzes dinâmicas que sincronizam com a batida! 🔊🔥 #waaw #hyperboom1000 #alok" },
  { name: "Camila Baladas & Som", username: "camilabaladas", avatar: "../img/reviews-avatars/unique/w_29.jpg", poster: "../videosprodutos/posters/video-produto-73-take1.jpg", video: "https://files.catbox.moe/qd8ybp.mp4", desc: "A caixa é um monstro de potência! Entrada para violão e microfone, bateria que aguenta a festa toda! 🎉✨ #somportatil #balada #festas" },
  { name: "Rodrigo Bass Review", username: "rodrigobassreview", avatar: "../img/reviews-avatars/unique/m_43.jpg", poster: "../videosprodutos/posters/video-produto-73-take2.jpg", video: "https://files.catbox.moe/qd8ybp.mp4", desc: "Acabamento emborrachado com rodinhas reforçadas para transportar fácil. O grave dessa caixa impressiona qualquer um! 👏⚡ #somautomotivo #qualidade #waawbyalok" },
  { name: "Larissa Festas & Churras", username: "larissachurras_", avatar: "../img/reviews-avatars/unique/w_30.jpg", poster: "../videosprodutos/posters/video-produto-73-take3.jpg", video: "https://files.catbox.moe/qd8ybp.mp4", desc: "Conexão Bluetooth 5.0 super rápida sem picotes. Com o cupom da Stone Shop saiu quase pela metade do preço! 💖🎶 #musica #churrascoemfamilia #stoneshop" },
  { name: "Felipe Sound Pro", username: "felipesoundpro", avatar: "../img/reviews-avatars/unique/m_44.jpg", poster: "../videosprodutos/posters/video-produto-73-take4.jpg", video: "https://files.catbox.moe/qd8ybp.mp4", desc: "Entrega expressa, veio lacrada na caixa original. Nota máxima para atendimento e qualidade sonora! 📦🔊 #unboxing #recomendo #sompesado" }
];
const CREATORS_WAAW_HYPERBOOM_73 = WAAW_HYPERBOOM_73_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 27900 + i * 2900, commentsCount: 245 + i * 36, sharesCount: 88 + i * 20, savesCount: 2180 + i * 240, description: b.desc }));

// 15. P78: Extratora e Higienizadora Portátil WAP Spot Cleaner 127V
const WAP_EXTRATORA_78_VIDEOS_MAP = [
  { name: "Carla Dicas de Limpeza", username: "carladicasdelimpeza", avatar: "../img/reviews-avatars/unique/w_31.jpg", poster: "../videosprodutos/posters/video-produto-78.jpg", video: "https://files.catbox.moe/6ubsxb.mp4", desc: "A WAP Spot Cleaner tirou mancha antiga de café do sofá em 2 minutos! A água sai preta de tanta sujeira que puxa! 🧼✨ #wap #extratora #spotcleaner" },
  { name: "Renan Estética Automotiva", username: "renanautoclean", avatar: "../img/reviews-avatars/unique/m_45.jpg", poster: "../videosprodutos/posters/video-produto-78-take1.jpg", video: "https://files.catbox.moe/6ubsxb.mp4", desc: "Uso na higienização de bancos de carro e colchões. Poder de sucção excelente e reservatório duplo de água limpa e suja! 🚗👏 #higienizacao #carros #esteticaautomotiva" },
  { name: "Mariana Lar Organizado", username: "marilarorganizado", avatar: "../img/reviews-avatars/unique/w_32.jpg", poster: "../videosprodutos/posters/video-produto-78-take2.jpg", video: "https://files.catbox.moe/6ubsxb.mp4", desc: "Quem tem pet em casa precisa dessa máquina! Limpa xixi e sujeira de tapete e estofados num piscar de olhos! 🐶💖 #petlover #limpezadecasa #dicaspet" },
  { name: "Diego Reformas & Dicas", username: "diegoreformasbr", avatar: "../img/reviews-avatars/unique/m_46.jpg", poster: "../videosprodutos/posters/video-produto-78-take3.jpg", video: "https://files.catbox.moe/6ubsxb.mp4", desc: "Compacta, leve e fácil de guardar. Economizei centenas de reais não precisando contratar empresa de limpeza! 🛠️🏡 #economia #praticidade #facavocemesmo" },
  { name: "Vanessa Vida Real", username: "vanessavidareal_", avatar: "../img/reviews-avatars/unique/w_33.jpg", poster: "../videosprodutos/posters/video-produto-78-take4.jpg", video: "https://files.catbox.moe/6ubsxb.mp4", desc: "Chegou super rápido pela Stone Shop com todos os bicos e mangueira longa. Melhor compra do ano! 📦😍 #unboxing #achadinhos #donadecasa" }
];
const CREATORS_WAP_EXTRATORA_78 = WAP_EXTRATORA_78_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 33500 + i * 3600, commentsCount: 320 + i * 50, sharesCount: 120 + i * 28, savesCount: 2700 + i * 310, description: b.desc }));

// 16. P80: Panificadora 19 Programas Gallant 600W
const PANIFICADORA_80_VIDEOS_MAP = [
  { name: "Dona Maria Receitas", username: "donamariareceitas", avatar: "../img/reviews-avatars/unique/w_34.jpg", poster: "../videosprodutos/posters/video-produto-80.jpg", video: "https://files.catbox.moe/3a2qhi.mp4", desc: "Pão caseiro quentinho toda manhã sem sujar as mãos! A Panificadora Gallant com 19 programas bate, fermenta e assa sozinha! 🍞🥖 #panificadora #paocaseiro #cozinha" },
  { name: "Chef Bruno Cozinha", username: "chefbrunocozinha", avatar: "../img/reviews-avatars/unique/m_47.jpg", poster: "../videosprodutos/posters/video-produto-80-take1.jpg", video: "https://files.catbox.moe/3a2qhi.mp4", desc: "Faz pão integral, pão francês, massa de pizza, geleia e até bolo! Timer programável de até 15 horas super prático! 👏🍕 #gastronomia #massacaseira #culinaria" },
  { name: "Luciana Vida Saudável", username: "lucianavidasaudavel", avatar: "../img/reviews-avatars/unique/w_35.jpg", poster: "../videosprodutos/posters/video-produto-80-take2.jpg", video: "https://files.catbox.moe/3a2qhi.mp4", desc: "Agora só consumo pão sem conservantes feito em casa com ingredientes naturais. Vale a pena demais pra saúde! ✨🍞 #alimentacaosaudavel #semconservantes #fitness" },
  { name: "Rodrigo Pães Artesanais", username: "rodrigopaesartesanais", avatar: "../img/reviews-avatars/unique/m_48.jpg", poster: "../videosprodutos/posters/video-produto-80-take3.jpg", video: "https://files.catbox.moe/3a2qhi.mp4", desc: "Forma antiaderente de limpeza fácil e visor de vidro para acompanhar o ponto da casquinha dourada. Top! 😍🥖 #paocaseiroquentinho #confeitaria #dicas" },
  { name: "Patrícia Dicas do Lar", username: "patydicasdolar_", avatar: "../img/reviews-avatars/unique/w_36.jpg", poster: "../videosprodutos/posters/video-produto-80-take4.jpg", video: "https://files.catbox.moe/3a2qhi.mp4", desc: "Comprei na Stone Shop na promoção e chegou impecável com copo medidor e colher dosadora! 📦💖 #unboxing #achadinhos #stone" }
];
const CREATORS_PANIFICADORA_80 = PANIFICADORA_80_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 23400 + i * 2500, commentsCount: 205 + i * 30, sharesCount: 75 + i * 17, savesCount: 1850 + i * 200, description: b.desc }));

// 17. P85: Caixa De Som Karaokê Joog X2 300W Tela 10,1" 2 Microfones
const JOOG_X2_85_VIDEOS_MAP = [
  { name: "Tiago Karaokê Brasil", username: "tiagokaraoke_br", avatar: "../img/reviews-avatars/unique/m_49.jpg", poster: "../videosprodutos/posters/video-produto-85.jpg", video: "https://files.catbox.moe/k3u5ff.mp4", desc: "Caixa Joog X2 com 300W e tela integrada de 10,1 polegadas! Vem com 2 microfones sem fio de alta sensibilidade! 🎤🔊 #joogx2 #karaoke #festaemcasa" },
  { name: "Juliana Eventos & Som", username: "jueventos_som", avatar: "../img/reviews-avatars/unique/w_37.jpg", poster: "../videosprodutos/posters/video-produto-85-take1.jpg", video: "https://files.catbox.moe/k3u5ff.mp4", desc: "A tela sensível ao toque facilita escolher músicas no YouTube e cantar ao vivo! A diversão da galera foi garantida! 🎉✨ #animacao #festadeaniversario #som" },
  { name: "Carlos Som & Tecnologia", username: "carlossomtech", avatar: "../img/reviews-avatars/unique/m_50.jpg", poster: "../videosprodutos/posters/video-produto-85-take2.jpg", video: "https://files.catbox.moe/k3u5ff.mp4", desc: "Graves potentes de 300W e ajuste de eco nos microfones. Bateria recarregável com ótima autonomia! 👏🎶 #tecnologia #qualidadedesom #joog" },
  { name: "Renata Cantoria", username: "renatacantoria_", avatar: "../img/reviews-avatars/unique/w_38.jpg", poster: "../videosprodutos/posters/video-produto-85-take3.jpg", video: "https://files.catbox.moe/k3u5ff.mp4", desc: "Design moderno com alça confortável para transportar. As crianças e os adultos não largam o microfone! 💖🎤 #diversao #familia #karaokeshow" },
  { name: "Lucas Dicas de Compras", username: "lucascomprasbr", avatar: "../img/reviews-avatars/unique/m_51.jpg", poster: "../videosprodutos/posters/video-produto-85-take4.jpg", video: "https://files.catbox.moe/k3u5ff.mp4", desc: "Entrega expressa da Stone Shop, produto original lacrado e muito bem protegido com plástico bolha! 📦🔥 #unboxing #recomendo #stoneshop" }
];
const CREATORS_JOOG_X2_85 = JOOG_X2_85_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 26700 + i * 2800, commentsCount: 230 + i * 34, sharesCount: 84 + i * 19, savesCount: 2100 + i * 230, description: b.desc }));

// 18. P87: Calça Mom Jeans Feminina KISSMELADY com Cinto Preto
const MOM_JEANS_87_VIDEOS_MAP = [
  { name: "Larissa Moda & Estilo", username: "larissamoda_estilo", avatar: "../img/reviews-avatars/unique/w_39.jpg", poster: "../videosprodutos/posters/video-produto-87.jpg", video: "https://files.catbox.moe/80bwka.mp4", desc: "Meninas, olha o caimento dessa calça mom jeans da KISSMELADY! Modela a cintura perfeitamente e o cinto preto já vem junto! 👖✨ #momjeans #modafeminina #lookdodia" },
  { name: "Beatriz Provador", username: "biaprovadorfashion", avatar: "../img/reviews-avatars/unique/w_40.jpg", poster: "../videosprodutos/posters/video-produto-87-take1.jpg", video: "https://files.catbox.moe/80bwka.mp4", desc: "Jeans 100% algodão encorpado de alta qualidade que não desbota na lavagem! Super confortável para trabalhar ou sair! 😍👏 #jeansperfeito #achadinhosmoda #style" },
  { name: "Camila Looks Reais", username: "camilalooksreais", avatar: "../img/reviews-avatars/unique/w_41.jpg", poster: "../videosprodutos/posters/video-produto-87-take2.jpg", video: "https://files.catbox.moe/80bwka.mp4", desc: "Cintura alta que segura a barriguinha e valoriza o bumbum sem apertar. Peguei meu tamanho usual e ficou impecável! 💖👗 #looktrabalho #arrumesecomigo #jeans" },
  { name: "Mariana Fashion Tips", username: "marifashiontips", avatar: "../img/reviews-avatars/unique/w_42.jpg", poster: "../videosprodutos/posters/video-produto-87-take3.jpg", video: "https://files.catbox.moe/80bwka.mp4", desc: "O cinto preto com fivela é super elegante e combina com tênis, salto ou bota. Promoção imperdível na Stone Shop! 👠🌟 #tendencia #modatiktok #dicasdelook" },
  { name: "Letícia Tendências", username: "leticiatendencias_", avatar: "../img/reviews-avatars/unique/w_43.jpg", poster: "../videosprodutos/posters/video-produto-87-take4.jpg", video: "https://files.catbox.moe/80bwka.mp4", desc: "Chegou em 2 dias aqui em SP, embalagem muito cheirosa e acabamento das costuras nota dez! 📦✨ #unboxingroupas #comprinhas #kissmelady" }
];
const CREATORS_MOM_JEANS_87 = MOM_JEANS_87_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 29400 + i * 3100, commentsCount: 265 + i * 38, sharesCount: 96 + i * 22, savesCount: 2350 + i * 260, description: b.desc }));

// 19. P89: Kit Conjunto Panelas de Ferro Esmaltadas Luxo 18 Peças
const PANELAS_FERRO_89_VIDEOS_MAP = [
  { name: "Chef Helena Gastronomia", username: "chefhelenagastro", avatar: "../img/reviews-avatars/unique/w_44.jpg", poster: "../videosprodutos/posters/video-produto-89.jpg", video: "https://files.catbox.moe/t5xtp1.mp4", desc: "Jogo de panelas de ferro esmaltadas luxo 18 peças! Retenção térmica espetacular e a comida fica com sabor de fogão à lenha! 🥘🔥 #panelasdeferro #cozinha #gastronomia" },
  { name: "Rodrigo Culinária Prática", username: "rodrigoculinariabr", avatar: "../img/reviews-avatars/unique/m_52.jpg", poster: "../videosprodutos/posters/video-produto-89-take1.jpg", video: "https://files.catbox.moe/t5xtp1.mp4", desc: "Esmalte vitrificado que não gruda nada e é super fácil de lavar. Vão do fogão direto pro forno e pra mesa com elegância! 👏🍳 #receitas #culinaria #panelas" },
  { name: "Vanessa Cozinha & Lar", username: "vanessacozinhalar", avatar: "../img/reviews-avatars/unique/w_45.jpg", poster: "../videosprodutos/posters/video-produto-89-take2.jpg", video: "https://files.catbox.moe/t5xtp1.mp4", desc: "Pesadas, firmes e lindas demais na cor vermelha degrade! O jogo mais completo que já tive na minha vida! 😍✨ #mesaposta #cozinhadecorada #donadecasa" },
  { name: "Diego Carnes & Assados", username: "diegocarneseassados", avatar: "../img/reviews-avatars/unique/m_53.jpg", poster: "../videosprodutos/posters/video-produto-89-take3.jpg", video: "https://files.catbox.moe/t5xtp1.mp4", desc: "Aquece por igual sem queimar o fundo. Fiz um ensopado de carne de panela que desmanchou na boca! 🥩🍲 #carnedepanela #churrasco #fogao" },
  { name: "Juliana Enxoval Novo", username: "juenxovalnovo", avatar: "../img/reviews-avatars/unique/w_46.jpg", poster: "../videosprodutos/posters/video-produto-89-take4.jpg", video: "https://files.catbox.moe/t5xtp1.mp4", desc: "Veio super bem protegida em caixa reforçada com manual de cuidados. O melhor investimento para sua cozinha! 📦💖 #enxoval #comprinhas #stone" }
];
const CREATORS_PANELAS_FERRO_89 = PANELAS_FERRO_89_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25300 + i * 2700, commentsCount: 218 + i * 32, sharesCount: 78 + i * 18, savesCount: 1980 + i * 220, description: b.desc }));

// 20. P91: Pipoqueira Classic Retrô Philco PPI04V
const PIPOQUEIRA_91_VIDEOS_MAP = [
  { name: "Mariana Cinema em Casa", username: "maricinemaemcasa", avatar: "../img/reviews-avatars/unique/w_47.jpg", poster: "../videosprodutos/posters/video-produto-91.jpg", video: "https://files.catbox.moe/xqpya7.mp4", desc: "Pipoqueira Classic Retrô Philco! Misturador automático e bandeja para servir, parece cinema de verdade em casa! 🍿🎬 #pipoqueira #philco #cinemaemcasa" },
  { name: "Felipe Filmes & Séries", username: "felipefilmesbr", avatar: "../img/reviews-avatars/unique/m_54.jpg", poster: "../videosprodutos/posters/video-produto-91-take1.jpg", video: "https://files.catbox.moe/xqpya7.mp4", desc: "Estoura 100% dos milhos sem queimar nenhum graças à haste giratória automática! Pipoca crocante e quentinha em 3 minutos! 👏🍿 #maratona #filmes #pipoca" },
  { name: "Camila Dicas de Mãe", username: "camiladicasdemae", avatar: "../img/reviews-avatars/unique/w_48.jpg", poster: "../videosprodutos/posters/video-produto-91-take2.jpg", video: "https://files.catbox.moe/xqpya7.mp4", desc: "A criançada pira vendo o milho estourar pela portinha de acrílico! Design retrô vintage lindo na bancada da cozinha! 😍✨ #maternidade #lanchedatarde #diversao" },
  { name: "Lucas Geek Snacks", username: "lucasgeeksnacks", avatar: "../img/reviews-avatars/unique/m_55.jpg", poster: "../videosprodutos/posters/video-produto-91-take3.jpg", video: "https://files.catbox.moe/xqpya7.mp4", desc: "Super fácil de desmontar e limpar após o uso. Aquece rápido e consome pouca energia! 🚀🍿 #gadgetscozinha #geek #snacks" },
  { name: "Bárbara Utilidades", username: "barbarautilidades_", avatar: "../img/reviews-avatars/unique/w_1.jpg", poster: "../videosprodutos/posters/video-produto-91-take4.jpg", video: "https://files.catbox.moe/xqpya7.mp4", desc: "Chegou super rápido pela Stone Shop, na cor vermelha metálica impecável. Recomendo a todos! 📦💖 #unboxing #achadinhos #stone" }
];
const CREATORS_PIPOQUEIRA_91 = PIPOQUEIRA_91_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21800 + i * 2300, commentsCount: 185 + i * 28, sharesCount: 65 + i * 16, savesCount: 1720 + i * 190, description: b.desc }));

// 21. P92: Conjunto Panelas de Ferro Fundido Esmaltado 10 Peças
const PANELAS_FERRO_92_VIDEOS_MAP = [
  { name: "Chef Marcelo Carnes", username: "chefmarcelocarnes", avatar: "../img/reviews-avatars/unique/m_56.jpg", poster: "../videosprodutos/posters/video-produto-92.jpg", video: "https://files.catbox.moe/sdcjn0.mp4", desc: "Conjunto 10 Peças em ferro fundido esmaltado! Distribuição homogênea de calor que sela bifes com crosta perfeita! 🥩🔥 #panelasferrofundido #culinaria #chef" },
  { name: "Ana Receitas Caseiras", username: "anareceitascaseiras", avatar: "../img/reviews-avatars/unique/w_2.jpg", poster: "../videosprodutos/posters/video-produto-92-take1.jpg", video: "https://files.catbox.moe/sdcjn0.mp4", desc: "Revestimento antiaderente esmaltado de alta densidade que não solta resíduos nos alimentos. Panelas pra durar gerações! 👏🍲 #panelasdesaude #semquimicos #comidacaseira" },
  { name: "Thiago Fogão & Brasa", username: "thiagofogaobrasa", avatar: "../img/reviews-avatars/unique/m_57.jpg", poster: "../videosprodutos/posters/video-produto-92-take2.jpg", video: "https://files.catbox.moe/sdcjn0.mp4", desc: "Tampas pesadas com sistema de condensação que mantém todo o suco e vapor dentro da panela. O assado fica suculento demais! 😍🥘 #gastronomia #panelatop #churrasco" },
  { name: "Carla Mesa Posta", username: "carlamesaposta_", avatar: "../img/reviews-avatars/unique/w_3.jpg", poster: "../videosprodutos/posters/video-produto-92-take3.jpg", video: "https://files.catbox.moe/sdcjn0.mp4", desc: "A cor e o brilho do esmalte deixam a mesa do almoço de domingo um espetáculo! Valeu cada centavo investido! 💖🍽️ #mesadealmoco #donadecasa #elegancia" },
  { name: "Gabriel Compras Inteligentes", username: "gabrielcomprasbr", avatar: "../img/reviews-avatars/unique/m_1.jpg", poster: "../videosprodutos/posters/video-produto-92-take4.jpg", video: "https://files.catbox.moe/sdcjn0.mp4", desc: "Entrega relâmpago da Stone Shop, caixas muito reforçadas e panelas super protegidas! 📦✨ #unboxingpanelas #qualidade #recomendo" }
];
const CREATORS_PANELAS_FERRO_92 = PANELAS_FERRO_92_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 24700 + i * 2600, commentsCount: 212 + i * 31, sharesCount: 76 + i * 18, savesCount: 1940 + i * 210, description: b.desc }));

// 22. P94: Bicicleta Bike Ergometrica Spinning Academia Fitness 120kg (Desacoplada da Bike 6)
const BIKE_SPINNING_94_VIDEOS_MAP = [
  { name: "Lucas Treino & Spinning", username: "lucasspinning_fit", avatar: "../img/reviews-avatars/unique/m_9.jpg", poster: "../videosprodutos/posters/video-produto-94.jpg", video: "https://files.catbox.moe/perlvk.mp4", desc: "Bike de Spinning profissional suporta até 120kg! Roda de inércia pesada com frenagem macia e silenciosa no apartamento! 🚴‍♂️🔥 #spinning #bikeindoor #treinoemcasa" },
  { name: "Larissa Personal Trainer", username: "larissapersonal_fit", avatar: "../img/reviews-avatars/unique/w_5.jpg", poster: "../videosprodutos/posters/video-produto-94-take1.jpg", video: "https://files.catbox.moe/perlvk.mp4", desc: "Regulagem completa de selim e guidão, monitor digital com batimentos cardíacos, tempo e calorias queimadas! Top! 💪✨ #fitness #cardio #emagrecimento" },
  { name: "Thiago Treino em Casa", username: "thiagofit_home", avatar: "../img/reviews-avatars/unique/m_10.jpg", poster: "../videosprodutos/posters/video-produto-94-take2.jpg", video: "https://files.catbox.moe/perlvk.mp4", desc: "Pedalo 45 minutos às 6h da manhã sem acordar ninguém em casa. Estrutura de aço muito estável! 👏🚴 #queimacalorias #saude #vidafit" },
  { name: "Renata Bike Indoor", username: "renatabike_indoor", avatar: "../img/reviews-avatars/unique/w_6.jpg", poster: "../videosprodutos/posters/video-produto-94-take3.jpg", video: "https://files.catbox.moe/perlvk.mp4", desc: "Pedais com presilhas firmes para sapatilha ou tênis. Muito confortável e fácil de movimentar com as rodinhas frontais! 💖🏋️‍♀️ #academia #motivação #pedal" },
  { name: "Carlos Spinning Pro", username: "carlosspinning_pro", avatar: "../img/reviews-avatars/unique/m_11.jpg", poster: "../videosprodutos/posters/video-produto-94-take4.jpg", video: "https://files.catbox.moe/perlvk.mp4", desc: "Comprei com super desconto na Stone Shop e a entrega foi pontual. Montagem fácil com as ferramentas inclusas! 📦🚴 #unboxingbike #qualidade #recomendo" }
];
const CREATORS_BIKE_SPINNING_94 = BIKE_SPINNING_94_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 26300 + i * 2800, commentsCount: 228 + i * 34, sharesCount: 82 + i * 19, savesCount: 2080 + i * 230, description: b.desc }));

// 23. P95: YESOP Máquina De Gelo Portátil 12kg/dia Turbo Ice
const MAQUINA_GELO_95_VIDEOS_MAP = [
  { name: "Felipe Drinks & Bar", username: "felipedrinksbar", avatar: "../img/reviews-avatars/unique/m_14.jpg", poster: "../videosprodutos/posters/video-produto-95.jpg", video: "https://files.catbox.moe/0qd90i.mp4", desc: "Máquina de Gelo Portátil YESOP 12kg/dia! Faz os primeiros cubos ocos em apenas 6 minutos! Nunca mais comprei saco de gelo! 🧊🍹 #maquinadegelo #yesop #drinks" },
  { name: "Camila Churrasco & Festas", username: "camilachurrasfestas", avatar: "../img/reviews-avatars/unique/w_8.jpg", poster: "../videosprodutos/posters/video-produto-95-take1.jpg", video: "https://files.catbox.moe/0qd90i.mp4", desc: "Perfeita para a área gourmet e churrasco de domingo! Reservatório inteligente que avisa quando o cesto tá cheio ou falta água! 😍👏 #churrasco #areagourmet #gelo" },
  { name: "Rodrigo Bartender Pro", username: "rodrigobartenderpro", avatar: "../img/reviews-avatars/unique/m_15.jpg", poster: "../videosprodutos/posters/video-produto-95-take2.jpg", video: "https://files.catbox.moe/0qd90i.mp4", desc: "Cubos translúcidos em formato bala que resfriam o drink sem aguá-lo rapidamente. Silenciosa e muito rápida! 🧊🍸 #coquetelaria #bartender #bar" },
  { name: "Patrícia Dicas de Casa", username: "patydicasdecasa_", avatar: "../img/reviews-avatars/unique/w_9.jpg", poster: "../videosprodutos/posters/video-produto-95-take3.jpg", video: "https://files.catbox.moe/0qd90i.mp4", desc: "Design compacto preto fosco super sofisticado na bancada. Limpeza automática com um toque de botão! 💖✨ #praticidade #donadecasa #eletrodomesticos" },
  { name: "Diego Utilidades BR", username: "diegoutilidadesbr", avatar: "../img/reviews-avatars/unique/m_16.jpg", poster: "../videosprodutos/posters/video-produto-95-take4.jpg", video: "https://files.catbox.moe/0qd90i.mp4", desc: "Entrega expressa da Stone Shop, veio com pá de gelo e cesto removível inclusos. Vale muito a pena! 📦❄️ #unboxing #achadinhos #stone" }
];
const CREATORS_MAQUINA_GELO_95 = MAQUINA_GELO_95_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 31500 + i * 3300, commentsCount: 285 + i * 42, sharesCount: 105 + i * 24, savesCount: 2450 + i * 270, description: b.desc }));

// 24. P96: Aparelho de Jantar/Chá Oxford Ryo Maresia 30 Peças
const APARELHO_RYO_96_VIDEOS_MAP = [
  { name: "Carla Mesa Posta Luxo", username: "carlamesapostabr", avatar: "../img/reviews-avatars/unique/w_11.jpg", poster: "../videosprodutos/posters/video-produto-96.jpg", video: "https://files.catbox.moe/i9wuhf.mp4", desc: "Aparelho de Jantar Oxford Ryo Maresia 30 peças! Formato orgânico inspirado na praia e acabamento fosco acetinado divino! 🍽️🌊 #oxfordporcelanas #mesaposta #ryomaresia" },
  { name: "Chef Thiago Alta Cozinha", username: "chefthiagocozinha", avatar: "../img/reviews-avatars/unique/m_18.jpg", poster: "../videosprodutos/posters/video-produto-96-take1.jpg", video: "https://files.catbox.moe/i9wuhf.mp4", desc: "Porcelana premium resistente a micro-ondas e lava-louças. O empratamento fica no nível dos melhores restaurantes! 👏🍲 #gastronomia #altagastronomia #chef" },
  { name: "Juliana Decoração & Mesa", username: "judecoracaomesa", avatar: "../img/reviews-avatars/unique/w_12.jpg", poster: "../videosprodutos/posters/video-produto-96-take2.jpg", video: "https://files.catbox.moe/i9wuhf.mp4", desc: "Peças pesadas e firmes com bordas irregulares artesanais exclusivas. Deixou meu jantar com convidados inesquecível! 😍✨ #jantarromantico #receberbem #elegancia" },
  { name: "Mariana Lar & Charme", username: "marilarcharme", avatar: "../img/reviews-avatars/unique/w_13.jpg", poster: "../videosprodutos/posters/video-produto-96-take3.jpg", video: "https://files.catbox.moe/i9wuhf.mp4", desc: "Kit completo com pratos rasos, fundos, sobremesa e xícaras de chá com pires. Melhor compra para enxoval de casamento! 💖👰 #noivas #enxoval #casamento" },
  { name: "Fábio Dicas Gourmet", username: "fabiodicasgourmet", avatar: "../img/reviews-avatars/unique/m_19.jpg", poster: "../videosprodutos/posters/video-produto-96-take4.jpg", video: "https://files.catbox.moe/i9wuhf.mp4", desc: "Chegou super bem embalado em caixa anti-impacto sem nenhuma avaria pela Stone Shop. Nota dez! 📦🍽️ #unboxingporcelana #oxford #stoneshop" }
];
const CREATORS_APARELHO_RYO_96 = APARELHO_RYO_96_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 28200 + i * 2900, commentsCount: 248 + i * 36, sharesCount: 92 + i * 20, savesCount: 2240 + i * 240, description: b.desc }));

// 25. P97: Jogo de Jantar Canyon Porcelana Decorada 20 Peças Tramontina
const JOGO_JANTAR_97_VIDEOS_MAP = [
  { name: "Renata Mesa & Afeto", username: "renatamesaeafeto", avatar: "../img/reviews-avatars/unique/w_14.jpg", poster: "../videosprodutos/posters/video-produto-97.jpg", video: "https://files.catbox.moe/0hhasi.mp4", desc: "Jogo de Jantar Tramontina Canyon Porcelana Decorada 20 peças! Os tons terrosos e as estampas geométricas são um escândalo! 🍽️✨ #tramontina #jogodejantar #mesaposta" },
  { name: "Lucas Gastronomia em Casa", username: "lucasgastroemcasa", avatar: "../img/reviews-avatars/unique/m_21.jpg", poster: "../videosprodutos/posters/video-produto-97-take1.jpg", video: "https://files.catbox.moe/0hhasi.mp4", desc: "Porcelana tradicional de altíssima resistência mecânica e porosidade quase zero. Tramontina é garantia de durabilidade! 👏🍲 #culinaria #qualidade #porcelana" },
  { name: "Aline Estilo & Lar", username: "alineestilolar", avatar: "../img/reviews-avatars/unique/w_16.jpg", poster: "../videosprodutos/posters/video-produto-97-take2.jpg", video: "https://files.catbox.moe/0hhasi.mp4", desc: "Cores vivas que não desbotam com as lavagens frequentes. Dá um destaque acolhedor maravilhoso na mesa de jantar! 😍🏡 #mesadejantar #decoracaodecasa #recebercomamor" },
  { name: "Rodrigo Casa & Sabor", username: "rodrigocasasabor", avatar: "../img/reviews-avatars/unique/m_22.jpg", poster: "../videosprodutos/posters/video-produto-97-take3.jpg", video: "https://files.catbox.moe/0hhasi.mp4", desc: "Pratos fundos com excelente capacidade e pratos de sobremesa charmosos. Ótimo custo-benefício na Stone Shop! 💖🍴 #dicasdeporcelana #tramontinabrasil #promocao" },
  { name: "Camila Compras do Mês", username: "camilacomprasdomes", avatar: "../img/reviews-avatars/unique/w_17.jpg", poster: "../videosprodutos/posters/video-produto-97-take4.jpg", video: "https://files.catbox.moe/0hhasi.mp4", desc: "Entrega segura, produto original com nota fiscal e proteção reforçada entre cada prato. Recomendo muito! 📦🌟 #unboxing #achadinhos #stone" }
];
const CREATORS_JOGO_JANTAR_97 = JOGO_JANTAR_97_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 25600 + i * 2700, commentsCount: 220 + i * 32, sharesCount: 80 + i * 18, savesCount: 2020 + i * 220, description: b.desc }));
"""

# Substitui as declarações vazias antigas pelo bloco completo
old_empty_datasets = """const CREATORS_BOLA_PENALTY_21 = [];
const CREATORS_COLCHAO_BESTWAY_22 = [];"""

if old_empty_datasets in code:
    code = code.replace(old_empty_datasets, NEW_DATASETS_CODE)
    print("Empty datasets 21 & 22 replaced with all dedicated datasets successfully!")
else:
    print("WARNING: old_empty_datasets not found!")

# 4. Atualizar o bloco de chaveamento no initCarousel
old_branches = """    } else if (prodId === 21 || pageText.includes('bola penalty') || pageText.includes('penalty')) {
      activeDataset = CREATORS_BOLA_PENALTY_21;
      contextType = 'bola_21';
    } else if (prodId === 22 || pageText.includes('colchao bestway') || pageText.includes('bestway')) {
      activeDataset = CREATORS_COLCHAO_BESTWAY_22;
      contextType = 'colchao_22';
    } else {"""

new_branches = """    } else if (prodId === 20 || pageText.includes('gt sprint mx7') || (pageText.includes('bicicleta') && pageText.includes('gt sprint'))) {
      activeDataset = CREATORS_BIKE_GT_20;
      contextType = 'bike_gt_20';
    } else if (prodId === 21 || pageText.includes('bola penalty') || pageText.includes('penalty')) {
      activeDataset = CREATORS_BOLA_PENALTY_21;
      contextType = 'bola_21';
    } else if (prodId === 22 || pageText.includes('colchao bestway') || pageText.includes('colchão inflável') || pageText.includes('colchao inflavel') || pageText.includes('bestway')) {
      activeDataset = CREATORS_COLCHAO_BESTWAY_22;
      contextType = 'colchao_22';
    } else if (prodId === 35 || pageText.includes('boombox 4') || (pageText.includes('jbl') && pageText.includes('boombox 4'))) {
      activeDataset = CREATORS_JBL_BOOMBOX4_35;
      contextType = 'jbl_boombox4_35';
    } else if (prodId === 52 || pageText.includes('pad 11') || pageText.includes('geração a16') || pageText.includes('geracao a16')) {
      activeDataset = CREATORS_PAD11_52;
      contextType = 'pad11_52';
    } else if (prodId === 55 || pageText.includes('switch desbloqueado') || pageText.includes('switch')) {
      activeDataset = CREATORS_SWITCH_55;
      contextType = 'switch_55';
    } else if (prodId === 57 || pageText.includes('joog one') || pageText.includes('j 200w')) {
      activeDataset = CREATORS_JOOG_ONE_57;
      contextType = 'joog_one_57';
    } else if (prodId === 58 || pageText.includes('echo dot 5') || pageText.includes('alaxe echo')) {
      activeDataset = CREATORS_ECHODOT_58;
      contextType = 'echodot_58';
    } else if (prodId === 59 || pageText.includes('internet rápida via satélite') || pageText.includes('antena original') || pageText.includes('via satélite')) {
      activeDataset = CREATORS_STARLINK_59;
      contextType = 'starlink_59';
    } else if (prodId === 61 || pageText.includes('break x1') || (pageText.includes('joog') && pageText.includes('800w'))) {
      activeDataset = CREATORS_JOOG_BREAK_61;
      contextType = 'joog_break_61';
    } else if (prodId === 63 || pageText.includes('redmi watch 5') || pageText.includes('watch 5 lite')) {
      activeDataset = CREATORS_REDMI_WATCH_63;
      contextType = 'redmi_watch_63';
    } else if (prodId === 65 || pageText.includes('cama inbox senses') || (pageText.includes('senses') && pageText.includes('2,00m'))) {
      activeDataset = CREATORS_SOFA_SENSES_65;
      contextType = 'sofa_senses_65';
    } else if (prodId === 70 || pageText.includes('solaris 8 kg') || pageText.includes('secadora mueller')) {
      activeDataset = CREATORS_SECADORA_MUELLER_70;
      contextType = 'secadora_mueller_70';
    } else if (prodId === 73 || pageText.includes('waaw hyperboom') || pageText.includes('hyperboom 1000')) {
      activeDataset = CREATORS_WAAW_HYPERBOOM_73;
      contextType = 'waaw_hyperboom_73';
    } else if (prodId === 78 || pageText.includes('spot cleaner') || pageText.includes('fw009214')) {
      activeDataset = CREATORS_WAP_EXTRATORA_78;
      contextType = 'wap_extratora_78';
    } else if (prodId === 80 || pageText.includes('panificadora') || pageText.includes('gpa1e19a')) {
      activeDataset = CREATORS_PANIFICADORA_80;
      contextType = 'panificadora_80';
    } else if (prodId === 85 || pageText.includes('joog x2') || pageText.includes('karaokê joog') || pageText.includes('karaoke joog')) {
      activeDataset = CREATORS_JOOG_X2_85;
      contextType = 'joog_x2_85';
    } else if (prodId === 87 || pageText.includes('kissmelady') || pageText.includes('calça mom jeans') || pageText.includes('calca mom jeans')) {
      activeDataset = CREATORS_MOM_JEANS_87;
      contextType = 'mom_jeans_87';
    } else if (prodId === 89 || (pageText.includes('panelas de ferro') && pageText.includes('18')) || pageText.includes('luxo 18 peças') || pageText.includes('luxo 18 pecas')) {
      activeDataset = CREATORS_PANELAS_FERRO_89;
      contextType = 'panelas_ferro_89';
    } else if (prodId === 91 || pageText.includes('pipoqueira') || pageText.includes('ppi04v')) {
      activeDataset = CREATORS_PIPOQUEIRA_91;
      contextType = 'pipoqueira_91';
    } else if (prodId === 92 || (pageText.includes('panelas de ferro') && pageText.includes('10')) || pageText.includes('fundido esmaltado 10')) {
      activeDataset = CREATORS_PANELAS_FERRO_92;
      contextType = 'panelas_ferro_92';
    } else if (prodId === 94 || pageText.includes('spinning academia fitness profissional') || (pageText.includes('bike') && pageText.includes('spinning') && pageText.includes('120kg'))) {
      activeDataset = CREATORS_BIKE_SPINNING_94;
      contextType = 'bike_spinning_94';
    } else if (prodId === 95 || pageText.includes('máquina de gelo') || pageText.includes('maquina de gelo') || pageText.includes('yesop')) {
      activeDataset = CREATORS_MAQUINA_GELO_95;
      contextType = 'maquina_gelo_95';
    } else if (prodId === 96 || pageText.includes('oxford ryo maresia') || pageText.includes('ryo maresia')) {
      activeDataset = CREATORS_APARELHO_RYO_96;
      contextType = 'aparelho_ryo_96';
    } else if (prodId === 97 || pageText.includes('jantar canyon') || pageText.includes('porcelana decorada 20') || pageText.includes('canyon porcelana')) {
      activeDataset = CREATORS_JOGO_JANTAR_97;
      contextType = 'jogo_jantar_97';
    } else {"""

if old_branches in code:
    code = code.replace(old_branches, new_branches)
    print("initCarousel branches updated successfully!")
else:
    print("WARNING: old_branches not found!")

with open(JS_PATH, 'w', encoding='utf-8') as f:
    f.write(code)

print("File written successfully!")
