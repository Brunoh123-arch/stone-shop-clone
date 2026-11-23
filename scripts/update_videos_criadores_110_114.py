import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('js/videos-criadores.js', encoding='utf-8') as f:
    content = f.read()

# 1. Update DEDICATED_VIDEOS
old_dedicated = "DEDICATED_VIDEOS = [5, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 35, 52, 55, 57, 58, 59, 60, 61, 63, 64, 65, 70, 72, 73, 75, 78, 80, 81, 83, 85, 87, 89, 91, 92, 94, 95, 96, 97, 106, 107];"
new_dedicated = "DEDICATED_VIDEOS = [5, 14, 15, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 35, 52, 55, 57, 58, 59, 60, 61, 63, 64, 65, 70, 72, 73, 75, 78, 80, 81, 83, 85, 87, 89, 91, 92, 94, 95, 96, 97, 106, 107, 108, 109, 110, 111, 112, 113, 114];"
if old_dedicated in content:
    content = content.replace(old_dedicated, new_dedicated)
    print("DEDICATED_VIDEOS updated successfully.")
else:
    print("Note: DEDICATED_VIDEOS string not exact match, checking pattern...")

# 2. Add New Video Maps after CREATORS_MODELADOR_109
new_maps = """
  // 1.6 DATASET DO TÊNIS KAPPA PULSE RX (PRODUTO 110)
  const KAPPA_110_VIDEOS_MAP = [
    {
      name: "Lucas Corrida & Fit",
      username: "lucascorridafit",
      avatar: "../img/creators-auto/creator-1.jpg",
      poster: "../videosprodutos/posters/poster-produto-110.jpg",
      video: "../videosprodutos/video-produto-110.mp4",
      startTime: 0.2,
      desc: "Tênis Kappa Pulse RX original no precinho! Amortecimento em EVA muito macio, testado e aprovado pro corre diário 🔥"
    },
    {
      name: "Rodrigo Tênis Review",
      username: "rodrigo.tenisreview",
      avatar: "../img/creators-auto/creator-2.jpg",
      poster: "../videosprodutos/posters/poster-produto-110-criadora2.jpg",
      video: "../videosprodutos/video-produto-110-criadora2.mp4",
      startTime: 0.2,
      desc: "Conforto e estilo em cada passo! O Kappa Pulse RX segura o impacto na corrida e caminhada. Custo-benefício absurdo!"
    },
    {
      name: "Bruna Fit & Run",
      username: "brunafit.corrida",
      avatar: "../img/creators-auto/creator-3.jpg",
      poster: "../videosprodutos/posters/poster-produto-110-criadora3.jpg",
      video: "../videosprodutos/video-produto-110-criadora3.mp4",
      startTime: 0.2,
      desc: "Uso na academia e pra correr na rua! Não esquenta o pé por causa do mesh respirável e não machuca nada 😍"
    },
    {
      name: "Marcos Runners SP",
      username: "marcosrunner_sp",
      avatar: "../img/creators-auto/creator-4.jpg",
      poster: "../videosprodutos/posters/poster-produto-110-criadora4.jpg",
      video: "../videosprodutos/video-produto-110-criadora4.mp4",
      startTime: 0.2,
      desc: "Review sincero do Kappa Pulse: sola com aderência surreal e acabamento impecável. Por menos de R$ 70 é presente!"
    },
    {
      name: "Felipe Tênis & Estilo",
      username: "felipetenis_oficial",
      avatar: "../img/creators-auto/creator-5.jpg",
      poster: "../videosprodutos/posters/poster-produto-110-criadora5.jpg",
      video: "../videosprodutos/video-produto-110-criadora5.mp4",
      startTime: 0.2,
      desc: "Unboxing e teste no pé! Leve demais, parece que tá descalço. Quem comprou sabe a qualidade da Kappa!"
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

  // 1.7 DATASET DO PROJETOR DE ÁRVORE DE NATAL 3D (PRODUTO 111)
  const PROJETOR_111_VIDEOS_MAP = [
    {
      name: "Decor & Magia Natalina",
      username: "decormagianatal",
      avatar: "../img/creators-aspirador/creator-1.jpg",
      poster: "../videosprodutos/posters/poster-produto-111.jpg",
      video: "../videosprodutos/video-produto-111.mp4",
      startTime: 0.2,
      desc: "Olha a perfeição desse projetor de árvore de Natal! 6 cenas 3D em alta definição, ilumina a sala inteira 🎄✨"
    },
    {
      name: "Lar da Camila",
      username: "lardacamila.home",
      avatar: "../img/creators-aspirador/creator-2.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora2.jpg",
      video: "../videosprodutos/video-produto-111-criadora2.mp4",
      startTime: 0.2,
      desc: "A magia do Natal na minha casa! Conecta no USB e roda 360° com efeito de neve e Papai Noel. As crianças amaram! ❤️"
    },
    {
      name: "Achadinhos de Natal",
      username: "achadinhosdenatal",
      avatar: "../img/creators-aspirador/creator-3.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora3.jpg",
      video: "../videosprodutos/video-produto-111-criadora3.mp4",
      startTime: 0.2,
      desc: "Melhor compra de Natal do ano! Menos de 50 reais e a projeção no teto parece de cinema. Corre pro carrinho!"
    },
    {
      name: "Família & Casa Decor",
      username: "familiacasa_decor",
      avatar: "../img/creators-aspirador/creator-4.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora4.jpg",
      video: "../videosprodutos/video-produto-111-criadora4.mp4",
      startTime: 0.2,
      desc: "Projetor natalino USB com rotação suave. Não esquenta e economiza energia. Ficou lindo na árvore!"
    },
    {
      name: "Cantinho Iluminado",
      username: "cantinhoiluminado",
      avatar: "../img/creators-aspirador/creator-5.jpg",
      poster: "../videosprodutos/posters/poster-produto-111-criadora5.jpg",
      video: "../videosprodutos/video-produto-111-criadora5.mp4",
      startTime: 0.2,
      desc: "Testei na escuridão total e o resultado impressiona muito! Super nítido e com 6 estampas diferentes."
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
      name: "Mamãe Brincalhona",
      username: "mamae.brincalhona",
      avatar: "../img/creators-avatars/creator-1.jpg",
      poster: "../videosprodutos/posters/poster-produto-112.jpg",
      video: "../videosprodutos/video-produto-112.mp4",
      startTime: 0.2,
      desc: "O brinquedo mais fofo do TikTok! Os patinhos sobem a escada e descem a pista sozinhos enquanto o caminhão anda com LED e música 🚒🦆"
    },
    {
      name: "Dicas da Tia Ju Kids",
      username: "dicasdatiaju_kids",
      avatar: "../img/creators-avatars/creator-2.jpg",
      poster: "../videosprodutos/posters/poster-produto-112-criadora2.jpg",
      video: "../videosprodutos/video-produto-112-criadora2.mp4",
      startTime: 0.2,
      desc: "Meu sobrinho ficou hipnotizado! Sistema bate e volta automático, não trava nos cantos da casa. Vale cada centavo!"
    },
    {
      name: "Mundo do Enzo",
      username: "omundodoenzo",
      avatar: "../img/creators-avatars/creator-3.jpg",
      poster: "../videosprodutos/posters/poster-produto-112-criadora3.jpg",
      video: "../videosprodutos/video-produto-112-criadora3.mp4",
      startTime: 0.2,
      desc: "Brinquedo 2 em 1: caminhão de bombeiro com som e montanha-russa de patinhos! Muito resistente e seguro."
    },
    {
      name: "Brinquedos Incríveis",
      username: "brinquedos_incriveis",
      avatar: "../img/creators-avatars/creator-4.jpg",
      poster: "../videosprodutos/posters/poster-produto-112-criadora4.jpg",
      video: "../videosprodutos/video-produto-112-criadora4.mp4",
      startTime: 0.2,
      desc: "A diversão dos pequenos tá garantida! Os patinhos descem correndo e voltam pra fila sem parar. Muito show!"
    },
    {
      name: "Rotina de Mãe Real",
      username: "rotinademae_oficial",
      avatar: "../img/creators-avatars/creator-5.jpg",
      poster: "../videosprodutos/posters/poster-produto-112-criadora5.jpg",
      video: "../videosprodutos/video-produto-112-criadora5.mp4",
      startTime: 0.2,
      desc: "Comprei pelo precinho de 44 reais e chegou super rápido. Plástico reforçado, sem rebarbas. Recomendo muito!"
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
      name: "Vet Dicas & Saúde Pet",
      username: "vetdicas_pet",
      avatar: "../img/creators-avatars/creator-6.jpg",
      poster: "../videosprodutos/posters/poster-produto-113.jpg",
      video: "../videosprodutos/video-produto-113.mp4",
      startTime: 0.2,
      desc: "Como veterinária recomendo: comedouro elevado com inclinação de 15° evita refluxo e protege a coluna dos cães e gatos 🐾"
    },
    {
      name: "Gatinhos da Lu",
      username: "gatinhosdalu",
      avatar: "../img/creators-avatars/creator-7.jpg",
      poster: "../videosprodutos/posters/poster-produto-113-criadora2.jpg",
      video: "../videosprodutos/video-produto-113-criadora2.mp4",
      startTime: 0.2,
      desc: "Meus gatinhos comeram muito mais confortáveis! O acrílico transparente é lindo e super fácil de lavar na pia."
    },
    {
      name: "Cão Feliz & Saudável",
      username: "caofeliz_saudavel",
      avatar: "../img/creators-avatars/creator-8.jpg",
      poster: "../videosprodutos/posters/poster-produto-113-criadora3.jpg",
      video: "../videosprodutos/video-produto-113-criadora3.mp4",
      startTime: 0.2,
      desc: "Tigela dupla pra água e ração! Base firme com borrachinhas antiderrapantes, o cachorro não empurra pela cozinha."
    },
    {
      name: "Vida de Pet Oficial",
      username: "vidadepet_oficial",
      avatar: "../img/creators-avatars/creator-9.jpg",
      poster: "../videosprodutos/posters/poster-produto-113-criadora4.jpg",
      video: "../videosprodutos/video-produto-113-criadora4.mp4",
      startTime: 0.2,
      desc: "Acabou a sujeira no chão! A altura certa faz toda diferença na digestão dos bichinhos. Preço imperdível!"
    },
    {
      name: "Lar com Bichinhos",
      username: "larcombichinhos",
      avatar: "../img/creators-avatars/creator-10.jpg",
      poster: "../videosprodutos/posters/poster-produto-113-criadora5.jpg",
      video: "../videosprodutos/video-produto-113-criadora5.mp4",
      startTime: 0.2,
      desc: "Design clean que combina com qualquer ambiente. Material atóxico e muito resistente. Amei demais!"
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

  // 1.10 DATASET DO CONTROLE ARCADE STICK 7 EM 1 (PRODUTO 114)
  const ARCADE_114_VIDEOS_MAP = [
    {
      name: "Nostalgia Gamer BR",
      username: "nostalgiagamer_br",
      avatar: "../img/creators-tech/creator-1.jpg",
      poster: "../videosprodutos/posters/poster-produto-114.jpg",
      video: "../videosprodutos/video-produto-114.mp4",
      startTime: 0.2,
      desc: "Sensação pura dos fliperamas dos anos 90! Controle Arcade Stick 7 em 1 com microswitch mecânico e zero delay 🕹️🔥"
    },
    {
      name: "Fliperama em Casa",
      username: "fliperamaemcasa",
      avatar: "../img/creators-tech/creator-2.jpg",
      poster: "../videosprodutos/posters/poster-produto-114-criadora2.jpg",
      video: "../videosprodutos/video-produto-114-criadora2.mp4",
      startTime: 0.2,
      desc: "Testei no PS4 e no PC: plug and play na hora! Os combos em The King of Fighters e Street Fighter saem lisos!"
    },
    {
      name: "Retro Station Games",
      username: "retrostation_games",
      avatar: "../img/creators-tech/creator-3.jpg",
      poster: "../videosprodutos/posters/poster-produto-114-criadora3.jpg",
      video: "../videosprodutos/video-produto-114-criadora3.mp4",
      startTime: 0.2,
      desc: "Alavanca esférica 360 graus ultra precisa com 8 botões de alta resposta. Construção robusta que aguenta o tranco!"
    },
    {
      name: "Tech & Play Review",
      username: "techandplay_review",
      avatar: "../img/creators-tech/creator-4.jpg",
      poster: "../videosprodutos/posters/poster-produto-114-criadora4.jpg",
      video: "../videosprodutos/video-produto-114-criadora4.mp4",
      startTime: 0.2,
      desc: "Compatível com PS4, PS3, Xbox, Switch, PC e celular via OTG! Menos de 90 reais em um fightstick desse porte é surreal."
    },
    {
      name: "Mundo Arcade Brasil",
      username: "mundoarcade_br",
      avatar: "../img/creators-tech/creator-5.jpg",
      poster: "../videosprodutos/posters/poster-produto-114-criadora5.jpg",
      video: "../videosprodutos/video-produto-114-criadora5.mp4",
      startTime: 0.2,
      desc: "Cabo de 2.5m blindado e ventosas fortes na base pra não escorregar da mesa. Review 10/10 com louvor!"
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
"""

target_pos = content.find("const CREATORS_MODELADOR_109 =")
end_pos = content.find("}));", target_pos) + 4

if target_pos != -1:
    content = content[:end_pos] + new_maps + content[end_pos:]
    print("New maps inserted after CREATORS_MODELADOR_109.")
else:
    print("ERROR: could not find CREATORS_MODELADOR_109")

# 3. Add condition checks in the main handler
old_checks = "const isModelador = prodId === 109 || pageText.includes('modelador de cachos') || pageText.includes('babyliss sem fio') || pageText.includes('cachos automatico');"
new_checks = """const isModelador = prodId === 109 || pageText.includes('modelador de cachos') || pageText.includes('babyliss sem fio') || pageText.includes('cachos automatico');
    const isKappa = prodId === 110 || pageText.includes('kappa pulse') || pageText.includes('tenis kappa');
    const isProjetorNatal = prodId === 111 || pageText.includes('arvore de natal') || pageText.includes('cenas festivas');
    const isCaminhao = prodId === 112 || pageText.includes('caminhao de bombeiro') || pageText.includes('montanha-russa de patinhos') || pageText.includes('patinhos');
    const isComedouro = prodId === 113 || pageText.includes('comedouro') || pageText.includes('tigela dupla') || pageText.includes('anti-engasgo');
    const isArcade = prodId === 114 || pageText.includes('controle arcade') || pageText.includes('arcade stick') || pageText.includes('fightstick');"""

content = content.replace(old_checks, new_checks)

old_branch = """    } else if (isModelador) {
      activeDataset = CREATORS_MODELADOR_109;
      contextType = 'modelador109';
    } else {"""

new_branch = """    } else if (isModelador) {
      activeDataset = CREATORS_MODELADOR_109;
      contextType = 'modelador109';
    } else if (isKappa) {
      activeDataset = CREATORS_KAPPA_110;
      contextType = 'kappa110';
    } else if (isProjetorNatal) {
      activeDataset = CREATORS_PROJETOR_111;
      contextType = 'projetor111';
    } else if (isCaminhao) {
      activeDataset = CREATORS_CAMINHAO_112;
      contextType = 'caminhao112';
    } else if (isComedouro) {
      activeDataset = CREATORS_COMEDOURO_113;
      contextType = 'comedouro113';
    } else if (isArcade) {
      activeDataset = CREATORS_ARCADE_114;
      contextType = 'arcade114';
    } else {"""

content = content.replace(old_branch, new_branch)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("js/videos-criadores.js updated successfully!")
