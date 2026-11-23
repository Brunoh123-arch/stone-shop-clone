with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """// 4. P35: Caixa de Som JBL Boombox 4 Bluetooth 210W
const JBL_BOOMBOX4_35_VIDEOS_MAP = [
  { name: "Caio Sound Test", username: "caiosoundtest", avatar: "../img/reviews-avatars/unique/m_14.jpg", poster: "../videosprodutos/posters/video-produto-35.jpg", video: "https://files.catbox.moe/s313zy.mp4", desc: "A monstra chegou! JBL Boombox 4 com 210W de potência real e graves que fazem a parede tremer! 🔊🔥 #jbl #boombox4 #sompesado" }
];"""

replacement = """// 4. P35: Caixa de Som JBL Boombox 4 Bluetooth 210W
const JBL_BOOMBOX4_35_VIDEOS_MAP = [
  {
    name: "Caio Sound Test",
    username: "caiosoundtest",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_14.jpg",
    poster: "../videosprodutos/posters/video-produto-35.jpg",
    video: "https://files.catbox.moe/s313zy.mp4",
    desc: "A monstra chegou! JBL Boombox 4 com 210W de potência real e graves que fazem a parede tremer! 🔊🔥 #jbl #boombox4 #sompesado"
  },
  {
    name: "Thiago Bass & Áudio",
    username: "thiagobass.som",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_22.jpg",
    poster: "../img/poster-criador-4-1.jpg",
    video: "https://files.catbox.moe/vyssbh.mp4",
    desc: "JBL Boombox no volume máximo! O subwoofer dedicado de 3 vias faz as janelas vibrarem! Potência absurda! 🔊💥 #jbl #somautomotivo #bassboost"
  },
  {
    name: "Rodrigo Tech & Som",
    username: "rodrigo.techaudio",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_30.jpg",
    poster: "../img/poster-criador-4-2.jpg",
    video: "https://files.catbox.moe/6isg2y.mp4",
    desc: "Bass Test insano com funk e eletrônica na Boombox: graves limpos e encorpados sem distorção. A melhor caixa bluetooth sem dúvidas! 🎶🔥"
  },
  {
    name: "Marcelo Áudio Pro",
    username: "marcelo.audiopro",
    avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_35.jpg",
    poster: "../videosprodutos/posters/video-produto-35.jpg",
    video: "https://files.catbox.moe/2txroy.mp4",
    desc: "Testando a bateria e a potência da JBL no churrasco com a galera! Durou o dia todo e o som cobriu todo o sítio! 🚀🔊"
  }
];"""

if target in js:
    js = js.replace(target, replacement)
    with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Sucesso: JBL_BOOMBOX4_35_VIDEOS_MAP atualizado com 4 criadores unicos e avatares reais do TikTok!")
else:
    print("Erro: Target não encontrado exatamente")
