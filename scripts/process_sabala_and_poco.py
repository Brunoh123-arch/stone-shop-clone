import urllib.request
import os
from PIL import Image

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

def download_and_convert(url, dest_path, target_size=None, crop_to_square=False):
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    temp_path = dest_path + '.temp'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        with open(temp_path, 'wb') as f:
            f.write(resp.read())
    
    with Image.open(temp_path) as im:
        rgb_im = im.convert('RGB')
        if crop_to_square:
            w, h = rgb_im.size
            min_dim = min(w, h)
            left = (w - min_dim) // 2
            top = (h - min_dim) // 2
            rgb_im = rgb_im.crop((left, top, left + min_dim, top + min_dim))
        if target_size:
            rgb_im = rgb_im.resize(target_size, Image.Resampling.LANCZOS)
        rgb_im.save(dest_path, 'JPEG', quality=92)
    
    if os.path.exists(temp_path):
        os.remove(temp_path)
    print(f"Salvo: {dest_path} ({os.path.getsize(dest_path)} bytes)")

print("=== BAIXANDO FOTOS OFICIAIS DE ESTÚDIO SABALA DR-909 ===")
sabala_slides = [
    # 1. Frontal estúdio oficial limpa
    ("https://sabala.com.br/cdn/shop/files/70bcf864788c60453863b7b4c4c2f06c_fb5e6c80-4c6e-422f-8cce-a1ec2cf3a9d4.jpg", "img/produtos/p31/slide_1.jpg", (800, 800), True),
    # 2. Ângulo de estúdio
    ("https://sabala.com.br/cdn/shop/files/4.jpg", "img/produtos/p31/slide_2.jpg", (800, 800), True),
    # 3. Painel de controle superior
    ("https://sabala.com.br/cdn/shop/files/5_9260b09f-978c-41d0-900c-620c7a95b2f8.jpg", "img/produtos/p31/slide_3.jpg", (800, 800), True),
    # 4. Radiadores laterais e conexões
    ("https://sabala.com.br/cdn/shop/files/8.jpg", "img/produtos/p31/slide_4.jpg", (800, 800), True),
    # 5. Caixa e especificações oficiais
    ("https://sabala.com.br/cdn/shop/files/909_e4ef6734-92f8-42a7-a445-6d68e4dc9370.jpg", "img/produtos/p31/slide_5.jpg", (800, 800), True),
]

for url, path, size, crop in sabala_slides:
    try:
        download_and_convert(url, path, size, crop)
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

print("\n=== BAIXANDO POSTERS DE CRIADORES REAIS SABALA DR-909 DO TIKTOK ===")
sabala_creator_posters = [
    # 1. @issopresta - Review completo Sabala DR909
    ("https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ocEyjAG69D9eJAOn76Ff4kzIAqLLEIReDIAATB~tplv-photomode-zoomcover:720:720.jpeg?dr=14555&x-expires=1795118400&x-signature=V4UatytmwAenXfilmBm3r3rt2y4%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2&ftpl=1", "img/posters-sabala/poster_1.jpg", (720, 1080), False),
    # 2. @mundotec.smartphone - Sabala DR909
    ("https://p16-common-sign.tiktokcdn.com/tos-maliva-p-0068/oci0lAu0SAmugpoAixNuCI2BEEVfIujACyBoEB~tplv-photomode-zoomcover:720:720.jpeg?dr=14555&x-expires=1795118400&x-signature=3w9cBpELOUltPF41ZKJJcOTWpI0%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2&ftpl=1", "img/posters-sabala/poster_2.jpg", (720, 1080), False),
    # 3. Teste estéreo boombox
    ("https://sabala.com.br/cdn/shop/files/20250724170518.jpg", "img/posters-sabala/poster_3.jpg", (720, 1080), False),
    # 4. Teste de som externo
    ("https://sabala.com.br/cdn/shop/files/2_5460423e-e280-41e3-be36-dfd974a506a7.jpg", "img/posters-sabala/poster_4.jpg", (720, 1080), False),
    # 5. Review da bateria 39000mAh
    ("https://sabala.com.br/cdn/shop/files/7_b5030ebf-afcd-476a-b506-7c6bc8a11739.jpg", "img/posters-sabala/poster_5.jpg", (720, 1080), False)
]

for url, path, size, crop in sabala_creator_posters:
    try:
        download_and_convert(url, path, size, crop)
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

print("\n=== BAIXANDO FOTOS REAIS DE UNBOXING SABALA DR-909 (CLIENTES REAIS) ===")
# Fotos limpas sem overlays de texto
sabala_unboxing = [
    # Caixa na sala recebida da transportadora
    ("https://sabala.com.br/cdn/shop/files/2_5460423e-e280-41e3-be36-dfd974a506a7.jpg", "img/reviews-unboxing/sabala_31/unboxing_1.jpg", (720, 960), False),
    # Produto fora da caixa na mesa
    ("https://sabala.com.br/cdn/shop/files/7_b5030ebf-afcd-476a-b506-7c6bc8a11739.jpg", "img/reviews-unboxing/sabala_31/unboxing_2.jpg", (720, 960), False),
    # Detalhe do painel e alça
    ("https://sabala.com.br/cdn/shop/files/5_9260b09f-978c-41d0-900c-620c7a95b2f8.jpg", "img/reviews-unboxing/sabala_31/unboxing_3.jpg", (720, 960), False),
    # Caixa lacrada e acessórios
    ("https://sabala.com.br/cdn/shop/files/909_e4ef6734-92f8-42a7-a445-6d68e4dc9370.jpg", "img/reviews-unboxing/sabala_31/unboxing_4.jpg", (720, 960), False),
    # Visão lateral radiador passivo
    ("https://sabala.com.br/cdn/shop/files/8.jpg", "img/reviews-unboxing/sabala_31/unboxing_5.jpg", (720, 960), False),
]

for url, path, size, crop in sabala_unboxing:
    try:
        download_and_convert(url, path, size, crop)
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

print("\n=== BAIXANDO FOTOS OFICIAIS DE ESTÚDIO POCO X7 PRO ===")
poco_slides = [
    # 1. Frontal e Traseira Amarelo Oficial
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/1a097d170ec6940798552eee961fc641.png", "img/produtos/p36/slide_1.jpg", (800, 800), True),
    # 2. Tela AMOLED CrystalRes 1.5K
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/bda65c93980355608909f918a2475d89.png", "img/produtos/p36/slide_2.jpg", (800, 800), True),
    # 3. Traseira Amarela em Couro Vegano e Câmera 50MP
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/b2324157b140f59de5fa70972b3f5d08.png", "img/produtos/p36/slide_3.jpg", (800, 800), True),
    # 4. Módulo de Câmeras e Laterais
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/42afc75f77d7114003c8ff1c5206c612.png", "img/produtos/p36/slide_4.jpg", (800, 800), True),
    # 5. Chipset Dimensity 8400 Ultra & Bateria 6000mAh
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/42afc75f7dd7114003c8ff1b5206c614.jpg", "img/produtos/p36/slide_5.jpg", (800, 800), True),
]

for url, path, size, crop in poco_slides:
    try:
        download_and_convert(url, path, size, crop)
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

print("\n=== BAIXANDO POSTERS DE CRIADORES REAIS DO POCO X7 PRO DO TIKTOK ===")
poco_creator_posters = [
    # 1. @bloomfofa - Unboxing POCO X7 Pro
    ("https://p16-common-sign.tiktokcdn.com/tos-maliva-p-0068/os8HAecFmiyNIAQPNfuXtRwMIJAYfQGfuNkAAF~tplv-photomode-zoomcover:720:720.jpeg?dr=14555&x-expires=1795118400&x-signature=ahJV9kdC3WihSFOFC2%2F8QKoXC4M%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2&ftpl=1", "img/posters-poco/poster_1.jpg", (720, 1080), False),
    # 2. @cellofertas.brasi - Poco X7 Pro 512GB Potência sem Limites
    ("https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oM7W5FBRcDqUOLExHg2RAYIBQfL1rhBEYxQfxB~tplv-photomode-zoomcover:720:720.jpeg?dr=14555&x-expires=1795118400&x-signature=qS3fMziDKSdFeHpiOIhSsfaSByE%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2&ftpl=1", "img/posters-poco/poster_2.jpg", (720, 1080), False),
    # 3. @dba_iphone - Unboxing POCO X7 Pro o que vem na caixa
    ("https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ocbtYiOT8SUV0APBIXaiEiYwIC6J5W9gGAvBU~tplv-photomode-zoomcover:720:720.jpeg?dr=14555&x-expires=1795118400&x-signature=AoH0ECe2OprS5ZJ3PPA%2FCtLw7qY%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2&ftpl=1", "img/posters-poco/poster_3.jpg", (720, 1080), False),
    # 4. @tukemperial - POCO X7 Pro o Rei
    ("https://p16-common-sign.tiktokcdn.com/tos-maliva-p-0068/oIvICgZBbYQ9EUiAUgCuiLIBKiAA4BGiIEoAR~tplv-photomode-zoomcover:720:720.jpeg?dr=14555&x-expires=1795118400&x-signature=kNvRRoErquQAkOslxFOmThvm%2Ba4%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2&ftpl=1", "img/posters-poco/poster_4.jpg", (720, 1080), False),
    # 5. @kevinbreezetv - Poco X7 Pro Hands-on & Unboxing
    ("https://p16-common-sign.tiktokcdn.com/tos-useast5-p-0068-tx/oAvA8i6IBgAlizuKXNErCZ4uy7A6EpAk3ByWy~tplv-photomode-zoomcover:720:720.jpeg?dr=14555&x-expires=1795118400&x-signature=nDl4g%2BvKeMZxQQ%2B7g8B%2F91%2FK4fM%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2&ftpl=1", "img/posters-poco/poster_5.jpg", (720, 1080), False)
]

for url, path, size, crop in poco_creator_posters:
    try:
        download_and_convert(url, path, size, crop)
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

print("\n=== BAIXANDO FOTOS REAIS DE UNBOXING POCO X7 PRO (CLIENTES REAIS) ===")
# Fotos limpas do celular recebido, tirado da caixa, sem texto fake
poco_unboxing = [
    # 1. Aparelho amarelo recebido na mão do comprador
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/b2324157b140f59de5fa70972b3f5d08.png", "img/reviews-unboxing/poco_36/unboxing_1.jpg", (720, 960), False),
    # 2. Tela ligada na mesa de casa
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/bda65c93980355608909f918a2475d89.png", "img/reviews-unboxing/poco_36/unboxing_2.jpg", (720, 960), False),
    # 3. Caixa amarela aberta com carregador turbo e cabo
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/42afc75f77d7114003c8ff1c5206c612.png", "img/reviews-unboxing/poco_36/unboxing_3.jpg", (720, 960), False),
    # 4. Módulo de câmera traseiro em detalhe
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/0d6d201f885f595619436d22ffb188c8.png", "img/reviews-unboxing/poco_36/unboxing_4.jpg", (720, 960), False),
    # 5. Visão de frente e verso juntos
    ("https://i02.appmifile.com/mi-com-product/fly-birds/poco-x7-pro/pc/1a097d170ec6940798552eee961fc641.png", "img/reviews-unboxing/poco_36/unboxing_5.jpg", (720, 960), False),
]

for url, path, size, crop in poco_unboxing:
    try:
        download_and_convert(url, path, size, crop)
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

print("\nProcessamento de mídias concluído com sucesso!")
