with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

# 1. Blindar desacoplamento
old_decouple = '''// Desacoplamento estrito entre o vídeo oficial da descrição e os vídeos de criadores
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
    }'''

new_decouple = '''// Desacoplamento estrito entre o vídeo oficial da descrição e os vídeos de criadores (BLINDADO)
    const descVidEl = document.querySelector('#tt-product-video, .product-video-player, #product-desc-video');
    const descVidSrc = descVidEl ? (descVidEl.getAttribute('src') || '').trim() : '';
    if (descVidSrc && Array.isArray(activeDataset) && activeDataset.length > 0) {
      const filtered = activeDataset.filter(item => {
        const itemVid = (item.video || item.localVideo || '').trim();
        return itemVid && itemVid !== descVidSrc;
      });
      // Se houver outros vídeos de criadores distintos, usa a lista filtrada.
      // Se esse era o único vídeo disponível, NÃO mata o carrossel: mantém ativo para prova social!
      if (filtered.length > 0) {
        activeDataset = filtered;
      }
    }

    if (!activeDataset || activeDataset.length === 0) {
      if (targetContainer) {
        targetContainer.innerHTML = '';
        targetContainer.style.setProperty('display', 'none', 'important');
      }
      return;
    }'''

assert old_decouple in vc, "old_decouple not found"
vc = vc.replace(old_decouple, new_decouple)
print("1. Decoupling logic blindada com sucesso!")

# 2. P7: AIWA_7_VIDEOS_MAP
old_aiwa_7 = "const AIWA_7_VIDEOS_MAP = [];"
new_aiwa_7 = '''const AIWA_7_VIDEOS_MAP = [
    {
      name: "Rodrigo Tech Sound",
      username: "rodrigo.techsound",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_14.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/poster-criador-7-1.jpg",
      video: "https://files.catbox.moe/k3u5ff.mp4",
      startTime: 0.2,
      desc: "Testando a AIWA Boombox Plus 200W no talo! Grave absurdo, proteção IP66 contra água e bateria que dura mais de 24 horas! 🔊🔥 #aiwa #boombox #som"
    },
    {
      name: "Carlos Audio BR",
      username: "carlosaudio.br",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_18.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/poster-criador-7-2.jpg",
      video: "https://files.catbox.moe/8ynmxe.mp4",
      startTime: 0.2,
      desc: "Caixa de Som AIWA Boombox Plus AWS-BBS-01B! Graves potentes sem distorcer e alça super confortável de carregar! 💥🎶 #caixadesom #aiwaboombox"
    },
    {
      name: "Marcos Bass Test",
      username: "marcosbasstest",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_22.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/poster-criador-7-3.jpg",
      video: "https://files.catbox.moe/32ulh9.mp4",
      startTime: 0.2,
      desc: "Pressão sonora dessa AIWA de 200W é surreal! Bate de frente com caixas muito mais caras, recomendo demais! 🎧✨ #aiwa #bassboost"
    }
  ];'''

assert old_aiwa_7 in vc, "old_aiwa_7 not found"
vc = vc.replace(old_aiwa_7, new_aiwa_7)
print("2. P7 AIWA_7_VIDEOS_MAP populado!")

# 3. P35: JBL_BOOMBOX4_35_VIDEOS_MAP
old_jbl_35 = "const JBL_BOOMBOX4_35_VIDEOS_MAP = [];"
new_jbl_35 = '''const JBL_BOOMBOX4_35_VIDEOS_MAP = [
    {
      name: "Felipe Bass Som",
      username: "felipebass.som",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_34.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-35-take1.jpg",
      video: "https://files.catbox.moe/s313zy.mp4",
      startTime: 0.2,
      desc: "JBL Boombox 4 Camuflada 210W! A caixa mais bruta que já testei, graves que tremem a janela da sala! 🔊🔥 #jblboombox #sompesado"
    },
    {
      name: "Thiago Review Audio",
      username: "thiago.audiobr",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_38.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-35-take2.jpg",
      video: "https://files.catbox.moe/zlnumo.mp4",
      startTime: 0.2,
      desc: "Bateria infinita e acabamento camuflado de altíssimo padrão. Vale cada centavo pra quem curte som de verdade! 🎶✨ #jbl #boombox4"
    },
    {
      name: "Lucas Som Automotivo",
      username: "lucassom.oficial",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_42.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-35-take3.jpg",
      video: "https://files.catbox.moe/pj5xsi.mp4",
      startTime: 0.2,
      desc: "Testando a Boombox 4 no sítio! Encheu a piscina toda de som com nitidez cristalina nos médios e agudos! 💥🏖️ #jbl #festa"
    }
  ];'''

assert old_jbl_35 in vc, "old_jbl_35 not found"
vc = vc.replace(old_jbl_35, new_jbl_35)
print("3. P35 JBL_BOOMBOX4_35_VIDEOS_MAP populado!")

# 4. P76: APARELHO_76_VIDEOS_MAP
old_aparelho_76 = "const APARELHO_76_VIDEOS_MAP = [];"
new_aparelho_76 = '''const APARELHO_76_VIDEOS_MAP = [
    {
      name: "Mariana Mesa Posta",
      username: "marianamesaposta",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_55.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-97.jpg",
      video: "https://files.catbox.moe/0hhasi.mp4",
      startTime: 0.2,
      desc: "Montando mesa posta com o Aparelho de Jantar Orgânico 30 peças! Acabamento impecável e textura única! 🍽️✨ #mesaposta #aparelhodejantar"
    },
    {
      name: "Camila Lar & Decor",
      username: "camilalardecor",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_59.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/poster-criador-5-1.jpg",
      video: "https://files.catbox.moe/i9wuhf.mp4",
      startTime: 0.2,
      desc: "Unboxing do jogo de jantar completo! Chegou super bem embalado, cerâmica pesada e ultra resistente! 📦❤️ #decoracao #casa"
    }
  ];'''

assert old_aparelho_76 in vc, "old_aparelho_76 not found"
vc = vc.replace(old_aparelho_76, new_aparelho_76)
print("4. P76 APARELHO_76_VIDEOS_MAP populado!")

# 5. P82: CREATORS_HISENSE_82
old_hisense_82 = "const CREATORS_HISENSE_82 = [];"
new_hisense_82 = '''const HISENSE_82_VIDEOS_MAP = [
    {
      name: "Larissa Lar Doce Lar",
      username: "larissa.lardocelar",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_72.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-70.jpg",
      video: "https://files.catbox.moe/iawt94.mp4",
      startTime: 0.2,
      desc: "Testando a Lava e Seca 11kg Titanium! O ciclo rápido de 15 minutos e a secagem a vapor deixam a roupa pronta pro armário! 🧺✨ #lavaeseca #lavanderia"
    },
    {
      name: "Fernanda Organiza",
      username: "fernandaorganiza.lar",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_76.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-70-take1.jpg",
      video: "https://files.catbox.moe/dst456.mp4",
      startTime: 0.2,
      desc: "Silenciosa demais! Motor inverter direct drive não treme nada e economiza muita água e energia! 👏❤️ #dicasdecasa #eletrodomesticos"
    },
    {
      name: "Juliana Dicas de Casa",
      username: "juliana.dicascasa",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_80.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-70-take2.jpg",
      video: "https://files.catbox.moe/h9xx40.mp4",
      startTime: 0.2,
      desc: "A melhor aquisição pra minha casa! Roupa sai cheirosa, sequinha e quase sem amarrotar! Super recomendo! 👗👕 #lavaeseca #donadecasa"
    }
  ];
  const CREATORS_HISENSE_82 = HISENSE_82_VIDEOS_MAP.map((b, i) => ({ ...b, startTime: 0.2, likes: 21500 + i * 1200, commentsCount: 180 + i * 25, sharesCount: 65 + i * 15, savesCount: 1700 + i * 180, description: b.desc }));'''

assert old_hisense_82 in vc, "old_hisense_82 not found"
vc = vc.replace(old_hisense_82, new_hisense_82)
print("5. P82 CREATORS_HISENSE_82 populado!")

# 6. P98: COPOS_98_VIDEOS_MAP
old_copos_98 = "const COPOS_98_VIDEOS_MAP = [];"
new_copos_98 = '''const COPOS_98_VIDEOS_MAP = [
    {
      name: "Beatriz Drinks & Lar",
      username: "beatrizdrinks",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_91.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-97-take1.jpg",
      video: "https://files.catbox.moe/i9wuhf.mp4",
      startTime: 0.2,
      desc: "Copos de Cristal Long Drink 490ml! O brilho e a transparência do cristal dão um toque super sofisticado na mesa! 🍸✨ #coposdecristal #drinks"
    },
    {
      name: "Larissa Recepções",
      username: "larissa.recepcoes",
      avatar: (isPagesDir ? "../" : "") + "img/reviews-avatars/tiktok_real/tt_avatar_95.jpg",
      poster: (isPagesDir ? "../" : "") + "videosprodutos/posters/video-produto-97-take2.jpg",
      video: "https://files.catbox.moe/0hhasi.mp4",
      startTime: 0.2,
      desc: "Jogo de 12 copos de cristal impecável! Borda fina, peso equilibrado e qualidade nota 10 para qualquer evento! 🥂💫 #mesaposta"
    }
  ];'''

assert old_copos_98 in vc, "old_copos_98 not found"
vc = vc.replace(old_copos_98, new_copos_98)
print("6. P98 COPOS_98_VIDEOS_MAP populado!")

# 7. Adicionar cases 79, 81, 83, 84 no switch (prodId) para os redirects
old_case80 = '''      case 80:
        activeDataset = CREATORS_PANIFICADORA_80;
        contextType = 'panificadora_80';
        break;'''

new_case80 = '''      case 79:
        activeDataset = CREATORS_PRAXIS_34;
        contextType = 'praxis_34';
        break;
      case 80:
        activeDataset = CREATORS_PANIFICADORA_80;
        contextType = 'panificadora_80';
        break;
      case 81:
        activeDataset = CREATORS_WAAW_HYPERBOOM_73;
        contextType = 'waaw_hyperboom_73';
        break;
      case 83:
        activeDataset = CREATORS_JOOG_BREAK_61;
        contextType = 'joog_break_61';
        break;
      case 84:
        activeDataset = CREATORS_PANIFICADORA_48_84;
        contextType = 'panificadora_84';
        break;'''

assert old_case80 in vc, "old_case80 not found"
vc = vc.replace(old_case80, new_case80)
print("7. Cases 79, 81, 83, 84 adicionados ao switch!")

with open("js/videos-criadores.js", "w", encoding="utf-8") as f:
    f.write(vc)

print("TUDO GRAVADO COM SUCESSO EM js/videos-criadores.js!")
