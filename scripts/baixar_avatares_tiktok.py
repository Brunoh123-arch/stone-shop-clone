import urllib.request
import json
import os
import re

os.makedirs('img/reviews-avatars/tiktok_real', exist_ok=True)
os.makedirs('img/reviews-avatars/tiktok_real/men', exist_ok=True)
os.makedirs('img/reviews-avatars/tiktok_real/women', exist_ok=True)

# URLs iniciais já capturadas da busca do TikTok via Playwright
AVATAR_URLS = [
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/551c69cf42df67ecc7ee04b070525292~tplv-tiktokx-cropcenter:720:720.jpeg?dr=14579&refresh_token=912ba3a0&x-expires=1795057200&x-signature=%2Fimnym2NFk5qQWKj%2FK1lscKjxQg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/23010a3cc33edefef4a317e4b910c2de~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=12f6b264&x-expires=1795057200&x-signature=VV0Z9Z%2F%2BoYNSxeXh3Lhfjl0SqO8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/86f7d14fa6b8b6595146d0bdb175f34c~tplv-tiktokx-cropcenter:720:720.webp?dr=14579&refresh_token=accb5778&x-expires=1795057200&x-signature=SFHlAnLDo7AzKvj25xCLuim6vyU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/87505a2ed926c478fd30b410d8aa42d7~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=560e2740&x-expires=1795057200&x-signature=cdZG69OnozDrar%2FcSGhbW9FQqvE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my2",
    "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/2e6e833480891ecb4195b07a73774796~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=22b2455c&x-expires=1795057200&x-signature=aBIDxrCqN3L2TeY%2Br1CeWac2JVc%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/66f352a63fe8470bdf1c24d0a69bf8c9~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=8549d8a9&x-expires=1795057200&x-signature=KrqjR1q0%2B8HiS90dEXuTvlu08nA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/5b9a3884efcecf1f853f88cc1c830897~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=7da6f321&x-expires=1795057200&x-signature=bdE5tZja7Q%2FOnKS2Zj%2BWlLfPBdc%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/1cc0bc7596a6018521736918cbb674e1~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=c5d5d0a9&x-expires=1795057200&x-signature=h8mUqHp7xkCgBX9p2qYoiWrZZ2Q%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/4d5d64189d0793354c37550356fa7a1c~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=3a825827&x-expires=1795057200&x-signature=J87Ds6jN9%2FMJgXL7jtRPNx88w5s%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/cec185b705d290cece694ad44f693f50~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=2b85bdfd&x-expires=1795057200&x-signature=bsqHEc35St8Od8vyV4DxDOfvizo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/cbdefee444050868f47cc6e28f6c1ec0~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=c9e629e1&x-expires=1795057200&x-signature=3vPjDk%2Ftg9Axm1ztnyzi7ZOJiPk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/27ccef9d913c97996b9b0c6488a8c568~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=75ac76d1&x-expires=1795057200&x-signature=FSApdYaBmqNc5SlDnwEQ3eP2TOk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/fcf36cae6630fd652faa11fe85160f95~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=430c9921&x-expires=1795057200&x-signature=LsBY3eud943bt3bEq3k5Bn7BwTM%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/7d99534d6ad273f976c141731451d2ae~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=ee98c0cf&x-expires=1794970800&x-signature=wy4ROGtGCfc6gHeAD7ADyk76Hbg%3D&t=4d5b0474&ps=13740610&shp=30310797&shcp=c1333099&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/e6e75a60e09995449e2ae34765534a5a~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=443933a8&x-expires=1794970800&x-signature=h83U5Min9oDSkimN7weKud2R4hM%3D&t=4d5b0474&ps=13740610&shp=30310797&shcp=c1333099&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/4ab8d225e6abf0c52505be0526d71516~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b0e244ae&x-expires=1794970800&x-signature=YXTp3uBwcgA%2BPgb7WEXNVExIq3Q%3D&t=4d5b0474&ps=13740610&shp=30310797&shcp=c1333099&idc=my2",
    "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/b9946f3607cc4cd5bc5a9c28fc61bee2~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=4ce5b9d4&x-expires=1795057200&x-signature=goc37O4JWwCgaEXiavAu8SCLfHM%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
    "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/fd7100cc0d7f11807e1468cb0159faa3~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=7b483ff6&x-expires=1795057200&x-signature=Le%2BcApN61njovpj1%2FvUkfq%2Bdwx8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2"
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

saved = 0
for i, url in enumerate(AVATAR_URLS):
    try:
        req = urllib.request.Request(url, headers=headers)
        fname = f"img/reviews-avatars/tiktok_real/tt_avatar_{i+1}.jpg"
        with urllib.request.urlopen(req) as resp, open(fname, 'wb') as out:
            out.write(resp.read())
        saved += 1
    except Exception as e:
        print(f"Erro {i+1}: {e}")

print(f"Total baixado com sucesso do TikTok CDN: {saved}")
