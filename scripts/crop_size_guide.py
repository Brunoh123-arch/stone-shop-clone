# -*- coding: utf-8 -*-
from PIL import Image

im = Image.open('img/guia-tamanhos-87.png')
# A tabela com margem confortável termina em y=370
cropped = im.crop((0, 0, 890, 372))
cropped.save('img/guia-tamanhos-87.png', optimize=True)
print("Crop concluído! Nova dimensão:", cropped.size)
