import urllib.request
import os

BATCH_3 = [
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/ebff87f3cafae8f6507906790f473eb7~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=c8c67f18&x-expires=1795057200&x-signature=z2QXfNQKzfAsYpqxpI7%2FQllaLfA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/e8328eb236d71debfd3ba16477d63956~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=22cb55f6&x-expires=1795057200&x-signature=QiBa9nRwwXnnjlC8Tf0gd6%2BsgyU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/6a8051e5c521b34fe1f75b009f971f36~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=71705d88&x-expires=1795057200&x-signature=ktAh8uFZee8H2YOYcYN321q3RvQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/595cf19fc8cdae289d6ae2648a8e5a16~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=cdfc55c4&x-expires=1795057200&x-signature=CONUUnShRClGW74M9FjMkYYTVGM%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/558b8526791d22d251577f04403d748d~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=25a51dc4&x-expires=1795057200&x-signature=gsoKyc0kVT4Ev4CbcBDmVf9TwKo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/ef2cc335b94f2f2aecaff674fb2dff61~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=7128bb6d&x-expires=1795057200&x-signature=HfIGoeGntoBSyWK12C2iFO86Kho%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/72c295c01b703789f1f792412094d8ae~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=53bdbd95&x-expires=1795057200&x-signature=0VAG%2Bh94a6Rk%2BHpqqPCZC7mAWzg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/5644ea13b3886bd24d4b17374a9fc787~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=4fe7ef76&x-expires=1795057200&x-signature=8DhAFJ7xNmtGmKkGlPmcUgxjKKM%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/09b5900a5fc2b3dafaf320230c50fa87~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b5d1d661&x-expires=1795057200&x-signature=JmXePjPpb1%2BPYkHDwchG8kVJNsI%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/ce8b4e78d13c532c8d44c30d5650e5fb~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=093d6ae5&x-expires=1795057200&x-signature=nkpTzwbEsktHrfuan7W9G9Ds1%2BY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/add98ce19bacd6728cb697dad22b3408~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=9908b91e&x-expires=1794970800&x-signature=aiA7NxOYNThc3524ihSSBJESdW4%3D&t=4d5b0474&ps=13740610&shp=30310797&shcp=c1333099&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/e9ed0e920040d7c970900987dbe5476f~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=89294123&x-expires=1795057200&x-signature=arNaHmnJyTtE3%2FVdaMU5mFpu75g%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-maliva-avt-0068/a6559b36be2f1afe42a942c005c66b14~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=5a550992&x-expires=1795057200&x-signature=7jMq3s4asspNQj7Vv8UnvW9B%2Bbs%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2"
]

headers = {'User-Agent': 'Mozilla/5.0'}
existing = len(os.listdir('img/reviews-avatars/tiktok_real'))

saved = 0
for i, url in enumerate(BATCH_3):
    try:
        req = urllib.request.Request(url, headers=headers)
        fname = f"img/reviews-avatars/tiktok_real/tt_avatar_{existing + i + 1}.jpg"
        with urllib.request.urlopen(req) as resp, open(fname, 'wb') as out:
            out.write(resp.read())
        saved += 1
    except Exception as e:
        print(f"Erro {i}: {e}")

print(f"Salvos mais {saved} avatares reais do TikTok!")
