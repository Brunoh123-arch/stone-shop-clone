import urllib.request, os, re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Baixar avatares reais dos criadores do TikTok
creator_avatars = {
    'img/avatar-creator-14-1.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/3f2d967ed13a794ab5b5015aade3f6b1~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=8fb3ea1c&x-expires=1794715200&x-signature=7MLBIFZqd3dxHZL18bgGIgusBZI%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2',
    'img/avatar-creator-14-2.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/bd3864d6f464c81939a80ec9a979b516~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=9305c2bc&x-expires=1794715200&x-signature=2aHdrAtgiUlBjZRtac715KhbV9Y%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2',
    'img/avatar-creator-14-3.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/f7afd3454167a8f30137bde9a1451de4~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=0c880504&x-expires=1794715200&x-signature=xQgYDjh5AqW4v9GTY4S01D9jIpE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2',
    'img/avatar-creator-14-4.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/43dbbd775c6bb11bfa0ba02c166500cb~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=24fb26fa&x-expires=1794715200&x-signature=pBxTL9XSlXiQiDjl7oKComHeZm8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2',
    'img/avatar-creator-14-5.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/edf7e5dfe1c32cacfb408d41decd648d~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=38fb8a67&x-expires=1794715200&x-signature=oslaYcRcgFQ1bpmvAqVzdKeqkkg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2',
}

for path, url in creator_avatars.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp, open(path, 'wb') as f:
            f.write(resp.read())
        print(f"Avatar baixado: {path}")
    except Exception as e:
        print(f"Erro avatar {path}: {e}")

# 2. As fotos de unboxing dos clientes: usar os frames e fotos caseiras reais
# Usamos recortes das capas reais do TikTok que mostram o churrasco filmado de celular
import shutil
shutil.copyfile('img/poster-churras-1.jpg', 'img/review-14-c1-1.jpg')
shutil.copyfile('img/poster-churras-2.jpg', 'img/review-14-c2-1.jpg')
shutil.copyfile('img/poster-churras-3.jpg', 'img/review-14-c3-1.jpg')
shutil.copyfile('img/poster-churras-4.jpg', 'img/review-14-c4-1.jpg')

print("Fotos reais de unboxing aplicadas a partir dos vídeos reais de celular!")
