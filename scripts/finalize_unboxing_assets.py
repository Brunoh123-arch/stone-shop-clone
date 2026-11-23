import os
from PIL import Image

# 1. PROCESSAR UNBOXING DO POCO X7 PRO (poco_36)
os.makedirs('img/reviews-unboxing/poco_36', exist_ok=True)

# unboxing 1: poster_5 (caixa na mão com planta)
with Image.open('img/posters-poco/poster_5.jpg') as im:
    im.convert('RGB').save('img/reviews-unboxing/poco_36/unboxing_1.jpg', 'JPEG', quality=92)

# unboxing 2: poster_3 (celular na mesa com caixa atrás)
with Image.open('img/posters-poco/poster_3.jpg') as im:
    im.convert('RGB').save('img/reviews-unboxing/poco_36/unboxing_2.jpg', 'JPEG', quality=92)

# unboxing 3: poster_4 (celular amarelo na mão)
with Image.open('img/posters-poco/poster_4.jpg') as im:
    im.convert('RGB').save('img/reviews-unboxing/poco_36/unboxing_3.jpg', 'JPEG', quality=92)

# unboxing 4: poster_2 (caixa lacrada na mão)
with Image.open('img/posters-poco/poster_2.jpg') as im:
    im.convert('RGB').save('img/reviews-unboxing/poco_36/unboxing_4.jpg', 'JPEG', quality=92)

# unboxing 5: poster_1 cortado para remover o texto "Unboxing POCO X7 PRO"
with Image.open('img/posters-poco/poster_1.jpg') as im:
    # O texto fica no topo (até y=350). Cortar de y=340 até o fim
    w, h = im.size
    cropped = im.crop((0, int(h * 0.33), w, h))
    cropped.convert('RGB').save('img/reviews-unboxing/poco_36/unboxing_5.jpg', 'JPEG', quality=92)

print("POCO unboxing fotos processadas!")

# 2. PROCESSAR UNBOXING DA SABALA DR-909 (sabala_31)
os.makedirs('img/reviews-unboxing/sabala_31', exist_ok=True)

# unboxing 1: temp_tt_photo_2 (duas Sabala no chão de cerâmica com LED RGB aceso)
with Image.open('temp_tt_photo_2.jpg') as im:
    im.convert('RGB').save('img/reviews-unboxing/sabala_31/unboxing_1.jpg', 'JPEG', quality=92)

# unboxing 2: poster_1 (criador com sabala no ombro) cortado no produto
with Image.open('img/posters-sabala/poster_1.jpg') as im:
    w, h = im.size
    # pegar close da caixa de som no ombro
    cropped = im.crop((0, 0, w, int(h * 0.55)))
    cropped.convert('RGB').save('img/reviews-unboxing/sabala_31/unboxing_2.jpg', 'JPEG', quality=92)

# unboxing 3: poster_2 cortado para remover sticker do rodapé
with Image.open('img/posters-sabala/poster_2.jpg') as im:
    w, h = im.size
    cropped = im.crop((0, 0, w, int(h * 0.85)))
    cropped.convert('RGB').save('img/reviews-unboxing/sabala_31/unboxing_3.jpg', 'JPEG', quality=92)

# unboxing 4: slide_1 da Sabala no chão/mesa (temp_sabala/909.jpg)
with Image.open('temp_sabala/909.jpg') as im:
    im.convert('RGB').save('img/reviews-unboxing/sabala_31/unboxing_4.jpg', 'JPEG', quality=92)

# unboxing 5: temp_tt_photo_2 close da caixa ligada
with Image.open('temp_tt_photo_2.jpg') as im:
    w, h = im.size
    cropped = im.crop((int(w * 0.45), int(h * 0.2), w, h))
    cropped.convert('RGB').save('img/reviews-unboxing/sabala_31/unboxing_5.jpg', 'JPEG', quality=92)

print("Sabala unboxing fotos processadas!")
