import urllib.request
import os

NEW_URLS = [
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/9cc02e01f582b3c3aa71f7243b80efe3~tplv-tiktokx-cropcenter:720:720.webp?dr=14579&refresh_token=27f3ce3c&x-expires=1795057200&x-signature=guW%2Bq9QVt40KW7HM5u2w6x9VBys%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/bc6231ffdf38175d5c525c689be560ac~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=769d1617&x-expires=1795057200&x-signature=acvf8e2DKgNhGMND7JByoCYsGeI%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/b3c86b15bfb3eaf6f224bfd4e948daed~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=777d6c50&x-expires=1795057200&x-signature=J1LDxauUgkfUhhTWxJ%2FeDWkPJ70%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/3192963858c5ee43f04c99e9c18440db~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=203ed30c&x-expires=1795057200&x-signature=Z5H%2BCg%2B%2BJeRhL%2FkWftG8W7Ac%2BTA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/f011efc6125b6ecab342404dd3fa21b7~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=f67cb4fb&x-expires=1795057200&x-signature=dNs46PzgNvElH%2B%2FNtHToJcQUy%2FA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/e828823c68f97b9c44717f1d1dc2ca88~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=9bb5d350&x-expires=1795057200&x-signature=7lZdF1wnJMYpiyN4TZ2ypB25ApU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/5175bba2331a676533bc66d838de0964~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=a3d8215f&x-expires=1795057200&x-signature=Tcsbl5jOy2E%2BAsUeaBHdZiK2LR4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/ed7b8e0e3a215479479ab245c1814f94~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=299ee6b4&x-expires=1795057200&x-signature=bKff1KR9c6N2BJJC2YGCFi3HIw8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/399d5e7257c69c892b3845d676308237~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=3ab65ab1&x-expires=1795057200&x-signature=lUq8b8%2F0stInnb0xO%2FUXwgh1SQs%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/fdbb1dbbe4cc0064f303ebe9a767abf3~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=7d0d3d34&x-expires=1795057200&x-signature=u5QjxeXNcik2ZeIqlRutFYEF1fY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/fdc1acc978cbe5038e3f4f79ab5f8522~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b41e9333&x-expires=1795057200&x-signature=ZerjaJOWhM8aXkqRl49%2BDDaxtu4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-maliva-avt-0068/42d5c09b93f3723eeccd04e0de154296~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=582425af&x-expires=1795057200&x-signature=ii6dcAXI7gHgGgX%2FLqNXZmFdb0s%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/92bd220204f96400456d587b32630eb5~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=6f0d9d04&x-expires=1795057200&x-signature=qLVNVvGfJQlVVnsjRZ%2FG4pl4lW0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/45bc120bdb1366f0c9215f8383f22c97~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=2c23a15d&x-expires=1795057200&x-signature=os6Hiv90al%2BYKGus%2FZtN2M9UJ4A%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2"
]

headers = {'User-Agent': 'Mozilla/5.0'}
existing = len(os.listdir('img/reviews-avatars/tiktok_real'))

saved = 0
for i, url in enumerate(NEW_URLS):
    try:
        req = urllib.request.Request(url, headers=headers)
        fname = f"img/reviews-avatars/tiktok_real/tt_avatar_{existing + i + 1}.jpg"
        with urllib.request.urlopen(req) as resp, open(fname, 'wb') as out:
            out.write(resp.read())
        saved += 1
    except Exception as e:
        print(f"Erro {i}: {e}")

print(f"Salvos mais {saved} avatares reais do TikTok!")
