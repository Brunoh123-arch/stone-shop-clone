with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Substituir bloco P31
old_p31 = """    } else if (prodId === 31 || (pageText.includes('sabala') && (pageText.includes('200w') || pageText.includes('39000mah')))) {
      activeDataset = [
        { name: "Som Pesado Automotivo", username: "sompesadobr", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_31.jpg", poster: "../videosprodutos/posters/video-produto-60-take1.jpg", video: "https://files.catbox.moe/1ig8lo.mp4", desc: "Caixa Sabala 200W com bateria monstra de 39.000mAh e proteção IPX6 contra água! O grave estremece o chão! 🔊💥 #sabala #sombluetooth #graves" }
      ];
      contextType = 'sabala_31';"""

new_p31 = """    } else if (prodId === 31 || pageText.includes('sabala') || pageText.includes('dr-909')) {
      activeDataset = CREATORS_SABALA_31;
      contextType = 'sabala_31';"""

if old_p31 in c:
    c = c.replace(old_p31, new_p31)
    print("Bloco P31 substituído com sucesso!")
else:
    print("AVISO: old_p31 não encontrado literalmente!")

# 2. Substituir bloco P36
old_p36 = """    } else if (prodId === 36 || pageText.includes('xiaomi poco')) {
      activeDataset = [
        { name: "Lucas Geek Brasil", username: "lucasgeek_tech", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_36.jpg", poster: "../videosprodutos/posters/video-produto-63.jpg", video: "https://files.catbox.moe/8octvc.mp4", desc: "Poco X7 Pro 5G com 512GB na cor amarela icônica! Roda qualquer jogo no talo em 120fps liso! 📱⚡ #pocox7pro #xiaomi #smartphonegamer" }
      ];
      contextType = 'poco_36';"""

new_p36 = """    } else if (prodId === 36 || pageText.includes('xiaomi poco') || pageText.includes('poco x7') || pageText.includes('poco')) {
      activeDataset = CREATORS_POCO_X7_PRO_36;
      contextType = 'poco_36';"""

if old_p36 in c:
    c = c.replace(old_p36, new_p36)
    print("Bloco P36 substituído com sucesso!")
else:
    print("AVISO: old_p36 não encontrado literalmente!")

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("js/videos-criadores.js salvo!")
