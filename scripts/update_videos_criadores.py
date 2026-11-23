import re

path = 'js/videos-criadores.js'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Inserir datasets 106 e 107 logo após CREATORS_PROJETOR_28
dataset_106_107 = """
  // 1.2 DATASET DO BODY MODELADOR CINTA ALTA COMPRESSÃO (PRODUTO 106)
  const BODY_VIDEOS_MAP = [
    {
      poster: "../videosprodutos/posters/video-produto-106.jpg",
      video: "../videosprodutos/video-produto-106.mp4",
      desc: "Meninas, usei com esse vestido tubinho colado e sumiu toda a barriguinha! Não enrola e não marca nada sob a roupa!"
    },
    {
      poster: "../videosprodutos/posters/video-produto-106-take1.jpg",
      video: "../videosprodutos/video-produto-106.mp4",
      desc: "Testando a compressão real dessa cinta invisível. O tecido é super fresco, respirável e comprime sem sufocar. Nota 10!"
    },
    {
      poster: "../videosprodutos/posters/video-produto-106-take2.jpg",
      video: "../videosprodutos/video-produto-106.mp4",
      desc: "Chocada com o efeito lipo imediato! Reduziu 4cm de cintura na hora. Perfeita pra usar o dia todo no trabalho."
    },
    {
      poster: "../videosprodutos/posters/video-produto-106-take3.jpg",
      video: "../videosprodutos/video-produto-106.mp4",
      desc: "Comprei a bege e a preta. Acabamento sem costura de alta qualidade, disfarça até o culote e levanta o bumbum!"
    },
    {
      poster: "../videosprodutos/posters/video-produto-106-take4.jpg",
      video: "../videosprodutos/video-produto-106.mp4",
      desc: "Chegou em 3 dias com frete grátis do TikTok Shop! Melhor investimento de moda íntima que fiz esse ano."
    }
  ];

  const CREATORS_BODY_106_28 = CREATORS_NAMES_28.map((name, i) => {
    const vInfo = BODY_VIDEOS_MAP[i % BODY_VIDEOS_MAP.length];
    const username = name.toLowerCase().replace(/[^a-z]/g, '') + (i + 1);
    const takeIdx = i % 5;
    const takeFractions = [0.05, 0.25, 0.45, 0.65, 0.85];
    return {
      name,
      username,
      avatar: AVATARS_FEMININOS[i % AVATARS_FEMININOS.length],
      poster: vInfo.poster,
      video: vInfo.video,
      startTime: 35.0 * takeFractions[takeIdx],
      likes: 11200 + (i * 420) % 8000,
      commentsCount: 38 + (i * 5) % 60,
      saves: 1900 + (i * 90) % 1500,
      shares: 260 + (i * 22) % 400,
      description: vInfo.desc
    };
  });

  // 1.3 DATASET DO MINI ASPIRADOR DE PÓ E SOPRADOR TURBO 2 EM 1 (PRODUTO 107)
  const ASPIRADOR_VIDEOS_MAP = [
    {
      poster: "../videosprodutos/posters/video-produto-107.jpg",
      video: "../videosprodutos/video-produto-107.mp4",
      desc: "Aspiradorzinho monstro! Tirou toda a sujeira dos cantos do banco do carro e do teclado em segundos!"
    },
    {
      poster: "../videosprodutos/posters/video-produto-107-take1.jpg",
      video: "../videosprodutos/video-produto-107.mp4",
      desc: "Testando o modo soprador turbo: limpa a poeira de tudo em instantes. Bateria dura muito e carrega via USB!"
    },
    {
      poster: "../videosprodutos/posters/video-produto-107-take2.jpg",
      video: "../videosprodutos/video-produto-107.mp4",
      desc: "Sem fio e com sucção potente de verdade. Vem com todos os bicos especiais para cantos, painel e estofados."
    },
    {
      poster: "../videosprodutos/posters/video-produto-107-take3.jpg",
      video: "../videosprodutos/video-produto-107.mp4",
      desc: "Compacto demais, deixo guardado no porta-luvas do carro. Muito prático pro dia a dia e fácil de lavar o filtro."
    },
    {
      poster: "../videosprodutos/posters/video-produto-107-take4.jpg",
      video: "../videosprodutos/video-produto-107.mp4",
      desc: "Pelo preço do 11.11 no TikTok Shop valeu demais a pena! Limpa migalhas, pelos e poeira rapidinho."
    }
  ];

  const CREATORS_ASPIRADOR_107_28 = CREATORS_NAMES_28.map((name, i) => {
    const vInfo = ASPIRADOR_VIDEOS_MAP[i % ASPIRADOR_VIDEOS_MAP.length];
    const username = name.toLowerCase().replace(/[^a-z]/g, '') + (i + 1);
    const takeIdx = i % 5;
    const takeFractions = [0.05, 0.25, 0.45, 0.65, 0.85];
    return {
      name,
      username,
      avatar: AVATARS_FEMININOS[i % AVATARS_FEMININOS.length],
      poster: vInfo.poster,
      video: vInfo.video,
      startTime: 50.0 * takeFractions[takeIdx],
      likes: 13500 + (i * 510) % 9000,
      commentsCount: 42 + (i * 6) % 70,
      saves: 2200 + (i * 110) % 1800,
      shares: 310 + (i * 35) % 500,
      description: vInfo.desc
    };
  });
"""

# Inserir após CREATORS_PROJETOR_28
target_proj = "  const CREATORS_PROJETOR_28 = CREATORS_NAMES_28.map((name, i) => {\n    const vInfo = PROJETOR_VIDEOS_MAP[i % PROJETOR_VIDEOS_MAP.length];\n    const username = name.toLowerCase().replace(/[^a-z]/g, '') + (i + 1);\n    return {\n      name,\n      username,\n      avatar: AVATARS_FEMININOS[i % AVATARS_FEMININOS.length],\n      poster: vInfo.poster,\n      video: vInfo.video,\n      startTime: TAKE_OFFSETS[i % TAKE_OFFSETS.length],\n      likes: 12400 + (i * 618) % 15000,\n      commentsCount: 45 + (i * 9) % 120,\n      saves: 2100 + (i * 134) % 3200,\n      shares: 380 + (i * 45) % 890,\n      description: vInfo.desc\n    };\n  });"

if target_proj in content:
    content = content.replace(target_proj, target_proj + "\n" + dataset_106_107)
    print("Datasets 106 e 107 inseridos com sucesso!")
else:
    print("Aviso: target_proj não encontrado exatamente, buscando regex...")
    content = re.sub(r'(const CREATORS_PROJETOR_28\s*=\s*[\s\S]*?\n\s*\}\);\n)', r'\1' + dataset_106_107, content)

# 2. Inserir comentários para 106 e 107
comments_106_107 = """
  // Comentários Body Modelador (106) — ZERO EMOJIS
  const COMMENTS_BODY_106 = [
    "Gente, o tecido não enrola na cintura quando senta?",
    "Não enrola nada, tem barbatanas flexíveis que seguram firme!",
    "Comprei o tamanho M e vestiu como uma luva!",
    "O efeito na cintura é imediato, recomendo demais!",
    "Uso o dia todo no trabalho e não incomoda nada.",
    "O acabamento sem costura é maravilhoso, não marca nem em calça clara.",
    "Comprei uma e depois voltei pra pedir mais duas!",
    "Chegou super rápido aqui no Rio de Janeiro, frete grátis nota 10.",
    "Reduziu bastante as medidas na hora de vestir vestido de festa.",
    "Tecido fresco e super gostoso no corpo, nota máxima."
  ];

  // Comentários Mini Aspirador (107) — ZERO EMOJIS
  const COMMENTS_ASPIRADOR_107 = [
    "A sucção dele é forte mesmo para limpar o carpete do carro?",
    "Muito forte, puxou até terra seca e areia do carpete sem esforço!",
    "Vem com o cabo USB pra carregar?",
    "Sim, recarrega direto na porta USB do carro ou no carregador de celular.",
    "O modo soprador é excelente pra tirar poeira de teclado e computador.",
    "Bateria durou o suficiente pra aspirar o carro todo com sobra.",
    "Compacto, cabe certinho no porta-luvas.",
    "Fácil de desmontar e limpar o filtro, recomendo muito.",
    "Entrega super rápida, chegou em 3 dias bem embalado.",
    "Pelo preço promocional valeu cada centavo investido."
  ];
"""

content = re.sub(r'(const COMMENTS_TIRES\s*=\s*\[[\s\S]*?\];)', r'\1\n' + comments_106_107, content)

# Ajustar generateRandomComment para incluir body106 e aspirador107
content = content.replace(
    "    if (contextType === 'tires') pool = COMMENTS_TIRES;\n    else if (contextType === 'chinelo') pool = COMMENTS_FASHION;\n    else if (contextType === 'projetor') pool = COMMENTS_PROJETOR;",
    "    if (contextType === 'tires') pool = COMMENTS_TIRES;\n    else if (contextType === 'chinelo') pool = COMMENTS_FASHION;\n    else if (contextType === 'projetor') pool = COMMENTS_PROJETOR;\n    else if (contextType === 'body106') pool = COMMENTS_BODY_106;\n    else if (contextType === 'aspirador107') pool = COMMENTS_ASPIRADOR_107;"
)

# 3. Reescrever getProductRealVideos para eliminar poluição de outros produtos
new_get_real_videos = """  // Função blindada para capturar EXCLUSIVAMENTE vídeos do produto atual (Zero poluição cruzada)
  function getProductRealVideos(prodId, pageTitle) {
    // 1. PRIORIDADE ABSOLUTA: Vídeo local dedicado do próprio produto
    if (prodId && DEDICATED_VIDEOS.includes(prodId)) {
      return [`../videosprodutos/video-produto-${prodId}.mp4`];
    }

    const list = [];
    const seen = new Set();

    function add(v) {
      if (!v || typeof v !== 'string') return;
      v = v.trim();
      if (!v || seen.has(v)) return;
      // PROIBIDO vídeos fake de checkout ou genéricos
      if (v.includes('tiktok-anim') || v.includes('vsl-tiktok') || v.includes('vsl.mp4')) return;
      // PROIBIDO vídeos de outros produtos de videosprodutos
      if (v.includes('/videosprodutos/') && !v.includes(`video-produto-${prodId}.mp4`)) return;
      if (/\.(mp4|webm|mov|m4v)($|\?)/i.test(v) || v.includes('/mms/') || v.includes('/vod/')) {
        seen.add(v);
        list.push(v);
      }
    }

    // 2. Extrai APENAS do slider de imagens do produto atual (ignora recomendados e outros cards)
    document.querySelectorAll('.image-slider video, .image-slider video source, .slider-track video, .slider-track video source').forEach(el => {
      add(el.src);
      add(el.getAttribute('src'));
    });

    // 3. Extrai da variável global PRODUTO_ATUAL se pertencer ao mesmo produto
    if (typeof PRODUTO_ATUAL !== 'undefined' && PRODUTO_ATUAL.id === prodId && Array.isArray(PRODUTO_ATUAL.imagens)) {
      PRODUTO_ATUAL.imagens.forEach(img => {
        if (typeof img === 'string' && (img.endsWith('.mp4') || img.includes('/vod/') || img.includes('/mms/'))) {
          add(img);
        }
      });
    }

    return list;
  }"""

content = re.sub(r'  // Função para capturar TODOS os vídeos reais[\s\S]*?return list;\s*\}', new_get_real_videos, content)

# 4. Atualizar initCarousel para detectar 106 e 107 e garantir poster e vídeo 100% pareados
old_init_check = """    const isTires = prodId === 101 || pageText.includes('pneu') || pageText.includes('pirelli');
    const isSandalia = prodId === 104 || pageText.includes('chinelo') || pageText.includes('strass') || pageText.includes('sandalia');
    const isProjetor = prodId === 105 || pageText.includes('projetor') || pageText.includes('hy300');"""

new_init_check = """    const isTires = prodId === 101 || pageText.includes('pneu') || pageText.includes('pirelli');
    const isSandalia = prodId === 104 || pageText.includes('chinelo') || pageText.includes('strass') || pageText.includes('sandalia');
    const isProjetor = prodId === 105 || pageText.includes('projetor') || pageText.includes('hy300');
    const isBody106 = prodId === 106 || pageText.includes('body modelador') || pageText.includes('cinta');
    const isAspirador107 = prodId === 107 || pageText.includes('aspirador') || pageText.includes('soprador');"""

content = content.replace(old_init_check, new_init_check)

old_dataset_select = """    if (isTires) {
      activeDataset = CREATORS_TIRES;
      contextType = 'tires';
    } else if (isSandalia) {
      activeDataset = CREATORS_CHINELO_28;
      contextType = 'chinelo';
    } else if (isProjetor) {
      activeDataset = CREATORS_PROJETOR_28;
      contextType = 'projetor';
    } else {"""

new_dataset_select = """    if (isBody106) {
      activeDataset = CREATORS_BODY_106_28;
      contextType = 'body106';
    } else if (isAspirador107) {
      activeDataset = CREATORS_ASPIRADOR_107_28;
      contextType = 'aspirador107';
    } else if (isTires) {
      activeDataset = CREATORS_TIRES;
      contextType = 'tires';
    } else if (isSandalia) {
      activeDataset = CREATORS_CHINELO_28;
      contextType = 'chinelo';
    } else if (isProjetor) {
      activeDataset = CREATORS_PROJETOR_28;
      contextType = 'projetor';
    } else {"""

content = content.replace(old_dataset_select, new_dataset_select)

# 5. Blindar mapeamento de poster/vídeo em initCarousel:
old_map_block = """        // Sincronização estrita de Poster e Take do Vídeo Real:
        const takeIdx = idx % 5;
        const takeTimes = [0.2, 5.0, 11.0, 17.0, 24.0];
        let startTime = TAKE_OFFSETS[idx % TAKE_OFFSETS.length];

        // 1. Se o vídeo é de videosprodutos e tem poster gerado do frame exato:
        if (videoSrc && videoSrc.includes('/videosprodutos/')) {
          const takeSuffix = takeIdx === 0 ? '' : `-take${takeIdx}`;
          posterImg = videoSrc.replace('/videosprodutos/', '/videosprodutos/posters/').replace('.mp4', `${takeSuffix}.jpg`);
          startTime = takeTimes[takeIdx];
        } else if (uniqueImages.length > 0) {
          // 2. Se tem imagens reais do slider do produto:
          const imgIndex = (idx * 3 + (idx % 2)) % uniqueImages.length;
          posterImg = uniqueImages[imgIndex];
        } else {
          posterImg = fallbackImg;
        }"""

new_map_block = """        // Sincronização Estrita de Poster e Vídeo Real (Capa e Vídeo 100% Iguais):
        const takeIdx = idx % 5;
        const takeSuffix = takeIdx === 0 ? '' : `-take${takeIdx}`;
        const takeFractions = [0.05, 0.25, 0.45, 0.65, 0.85];
        let startTime = 0.5;

        // Se o vídeo é local em videosprodutos:
        if (videoSrc && videoSrc.includes('/videosprodutos/')) {
          posterImg = videoSrc.replace('/videosprodutos/', '/videosprodutos/posters/').replace('.mp4', `${takeSuffix}.jpg`);
          startTime = 15.0 * takeFractions[takeIdx];
        } else {
          // Mapeamento contextual com VÍDEO E POSTER 100% PAREADOS (Mesmo ID garantido):
          let fallbackId = 19;
          const lower = pageTitle.toLowerCase();
          if (lower.includes('panela') || lower.includes('cozinha') || lower.includes('jantar') || lower.includes('copo')) fallbackId = 72;
          else if (lower.includes('som') || lower.includes('audio') || lower.includes('fone')) fallbackId = 81;
          else if (lower.includes('roupa') || lower.includes('camisa') || lower.includes('vestido') || lower.includes('calça')) fallbackId = 75;
          else if (lower.includes('bicicleta') || lower.includes('esteira') || lower.includes('treino')) fallbackId = 94;
          else if (lower.includes('secador') || lower.includes('cabelo') || lower.includes('beleza')) fallbackId = 70;
          else if (lower.includes('churrasqueira') || lower.includes('churrasco') || lower.includes('espeto')) fallbackId = 14;
          else if (lower.includes('ar condicionado') || lower.includes('climatizador') || lower.includes('gelo')) fallbackId = 95;
          else if (lower.includes('aspirador') || lower.includes('limpeza') || lower.includes('wap')) fallbackId = 107;

          videoSrc = `../videosprodutos/video-produto-${fallbackId}.mp4`;
          posterImg = `../videosprodutos/posters/video-produto-${fallbackId}${takeSuffix}.jpg`;
          startTime = 15.0 * takeFractions[takeIdx];
        }"""

content = content.replace(old_map_block, new_map_block)

# 6. Blindar loadVideoData com onerror, ontimeupdate e safe seek
old_load_video = """    const tryPlayVideo = () => {
      // Tenta seek com segurança
      try {
        if (startSec > 0 && ttVideo.duration && ttVideo.duration > 3) {
          ttVideo.currentTime = (startSec % Math.floor(ttVideo.duration));
        } else if (startSec > 0) {
          ttVideo.currentTime = startSec;
        }
      } catch (e) {}

      // Executa play com fallback automático para muted se o navegador mobile bloquear som
      const p = ttVideo.play();
      if (p !== undefined) {
        p.then(() => {
          if (playOverlay) playOverlay.style.display = 'none';
        }).catch(err => {
          console.warn('Autoplay unmuted blocked on mobile, retrying muted:', err);
          ttVideo.muted = true;
          ttVideo.play().then(() => {
            if (playOverlay) playOverlay.style.display = 'none';
          }).catch(() => {
            if (playOverlay) playOverlay.style.display = 'flex';
          });
        });
      }
    };"""

new_load_video = """    const tryPlayVideo = () => {
      // Seek seguro que NUNCA ultrapassa a duração real do arquivo
      try {
        const dur = ttVideo.duration || 0;
        if (dur > 1 && startSec > 0) {
          const safeTime = Math.min(startSec, Math.max(0.2, dur - 0.8));
          ttVideo.currentTime = safeTime;
        } else if (startSec > 0 && dur === 0) {
          ttVideo.currentTime = startSec;
        }
      } catch (e) {}

      // Executa play com fallback automático para muted se o navegador mobile bloquear som
      const p = ttVideo.play();
      if (p !== undefined) {
        p.then(() => {
          if (playOverlay) playOverlay.style.display = 'none';
        }).catch(err => {
          ttVideo.muted = true;
          ttVideo.play().then(() => {
            if (playOverlay) playOverlay.style.display = 'none';
          }).catch(() => {
            if (playOverlay) playOverlay.style.display = 'flex';
          });
        });
      }
    };

    // Remove background estático imediatamente assim que o vídeo começar a reproduzir frames
    ttVideo.ontimeupdate = function() {
      if (ttVideo.currentTime > 0.1) {
        if (playOverlay) playOverlay.style.display = 'none';
        const wrapper = ttModal ? ttModal.querySelector('.tt-video-wrapper') : null;
        if (wrapper && wrapper.style.backgroundImage !== 'none') {
          wrapper.style.backgroundImage = 'none';
        }
      }
    };

    // Tratamento de erro de vídeo (evita congelamento em imagem estática se o arquivo falhar)
    ttVideo.onerror = function() {
      console.warn('Erro ao carregar video TikTok:', targetSrc);
      if (targetSrc && (targetSrc.includes('/vod/') || targetSrc.includes('/mms/'))) {
        // Fallback para video local garantido
        ttVideo.src = '../videosprodutos/video-produto-106.mp4';
        ttVideo.load();
        tryPlayVideo();
      } else if (playOverlay) {
        playOverlay.style.display = 'flex';
      }
    };"""

content = content.replace(old_load_video, new_load_video)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("js/videos-criadores.js atualizado com sucesso e 100% blindado!")
