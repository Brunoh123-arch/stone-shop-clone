import re

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace CREATORS_CHURRASQUEIRA_RODEIO_16 with 100% unique creators, zero duplicate videos
clean_p16_dataset = """const CREATORS_CHURRASQUEIRA_RODEIO_16 = [
    {
      name: 'Família Egídio',
      username: 'familiaegidioc',
      avatar: '../img/reviews-avatars/tiktok_real/tt_avatar_18.jpg',
      poster: '../videosprodutos/posters/video-produto-16-take1.jpg',
      video: "https://files.catbox.moe/u5toyv.mp4",
      startTime: 0.0,
      likes: 18400,
      commentsCount: 92,
      saves: 1450,
      shares: 310,
      desc: 'Saiu aquele churrasco caprichado com a churrasqueira Mor Rodeio! Bacia esmaltada e grelha firme 🥩🔥 #churrasco #mor #churrasqueira'
    },
    {
      name: 'Chef Marcelo Carnes',
      username: 'chefmarcelocarnes',
      avatar: '../img/reviews-avatars/tiktok_real/tt_avatar_25.jpg',
      poster: '../videosprodutos/posters/video-produto-16-take2.jpg',
      video: "https://files.catbox.moe/sdcjn0.mp4",
      startTime: 0.2,
      likes: 24100,
      commentsCount: 145,
      saves: 2100,
      shares: 480,
      desc: 'Ponto perfeito da carne na grelha esmaltada! A retenção de calor do carvão fica sensacional! 🍖✨ #churrascoemcasa #grelha #carnes'
    },
    {
      name: 'Rodrigo Barbecue',
      username: 'rodrigobbq',
      avatar: '../img/reviews-avatars/tiktok_real/tt_avatar_42.jpg',
      poster: '../videosprodutos/posters/video-produto-16-take3.jpg',
      video: "https://files.catbox.moe/t5xtp1.mp4",
      startTime: 0.1,
      likes: 19800,
      commentsCount: 110,
      saves: 1680,
      shares: 340,
      desc: 'Costela e linguiça assando no capricho! Churrasqueira Mor portátil e prática demais pro final de semana! 🔥🍺 #bbqbrasil #domingo #churras'
    }
  ];"""

pattern = r'const CREATORS_CHURRASQUEIRA_RODEIO_16\s*=\s*\[.*?\];'
if re.search(pattern, text, re.DOTALL):
    text = re.sub(pattern, clean_p16_dataset, text, flags=re.DOTALL)
    with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
        f.write(text)
    print('CREATORS_CHURRASQUEIRA_RODEIO_16 sanitizado com ZERO vídeos repetidos!')
else:
    print('Pattern not matched in js/videos-criadores.js')
