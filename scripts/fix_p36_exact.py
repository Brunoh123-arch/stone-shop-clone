with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    c = f.read()

target = """    } else if (prodId === 36 || pageText.includes('poco x7 pro') || pageText.includes('xiaomi poco')) {
      activeDataset = [
        { name: "Lucas Geek Brasil", username: "lucasgeek_tech", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_36.jpg", poster: "../videosprodutos/posters/video-produto-63.jpg", video: "https://files.catbox.moe/8octvc.mp4", desc: "Poco X7 Pro 5G com 512GB na cor amarela icônica! Roda qualquer jogo no talo em 120fps liso! 📱⚡ #pocox7pro #xiaomi #smartphonegamer" }
      ];
      contextType = 'poco_36';"""

replacement = """    } else if (prodId === 36 || pageText.includes('poco x7 pro') || pageText.includes('xiaomi poco') || pageText.includes('poco x7') || pageText.includes('poco')) {
      activeDataset = CREATORS_POCO_X7_PRO_36;
      contextType = 'poco_36';"""

if target in c:
    c = c.replace(target, replacement)
    print("Sucesso: Bloco P36 substituído por CREATORS_POCO_X7_PRO_36!")
else:
    print("ERRO: Target não encontrado!")

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(c)
