import urllib.request
import os

headers = {'User-Agent': 'Mozilla/5.0'}

slides = [
    ("https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/c54373a89a0c42b08a4b867da65228a5~tplv-o3syd03w52-resize-webp:800:800.webp", "img/forno-hq-slide-1.webp"),
    ("https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/0bc528bf046b406eb6eac6398664d778~tplv-o3syd03w52-resize-webp:800:800.webp", "img/forno-hq-slide-2.webp"),
    ("https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/f3f8cdc5529c48e0889f50ca66868bb5~tplv-o3syd03w52-resize-webp:800:800.webp", "img/forno-hq-slide-3.webp"),
    ("https://p16-oec-va.ibyteimg.com/tos-maliva-i-o3syd03w52-us/4f1dca4f31e944af9c9919eb98b03264~tplv-o3syd03w52-resize-webp:800:800.webp", "img/forno-hq-slide-4.webp")
]

reviews = [
    ("https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/e601bd0ee2d54a4e866c6d29cb47fab8~tplv-aphluv4xwc-crop-webp:600:600.webp", "img/review-115-c1-1.webp"),
    ("https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/b074010e257544179253d9edd9a2103e~tplv-aphluv4xwc-crop-webp:600:600.webp", "img/review-115-c1-2.webp"),
    ("https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/4eea858b881a4d4cadd650128a4f90af~tplv-aphluv4xwc-crop-webp:600:600.webp", "img/review-115-c1-3.webp"),
    
    ("https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/73d834fa0c124b2fb50045b6afa0b815~tplv-aphluv4xwc-crop-webp:600:600.webp", "img/review-115-c2-1.webp"),
    ("https://p19-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/d5d4ee3098cd40fc977a2f725517a3d1~tplv-aphluv4xwc-crop-webp:600:600.webp", "img/review-115-c2-2.webp"),
    ("https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/aebd58164cb34567a6058c95412e52ef~tplv-aphluv4xwc-crop-webp:600:600.webp", "img/review-115-c2-3.webp"),
    
    ("https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/db7441e1e85248088f1c739e484fb8ed~tplv-aphluv4xwc-crop-webp:600:600.webp", "img/review-115-c3-1.webp"),
    ("https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/ad8e25bd63d042b3b20979c65dd43b6d~tplv-aphluv4xwc-crop-webp:600:600.webp", "img/review-115-c3-2.webp")
]

avatars = [
    ("https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/6df3044ea86aee7e95b579ab87bc6433~tplv-tiktokx-cropcenter:100:100.jpg", "img/avatars-forno-hq/buyer-m.jpg"),
    ("https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/b0967ab348ed0636fc51f4a7f47e1b43~tplv-tiktokx-cropcenter:100:100.jpg", "img/avatars-forno-hq/buyer-d.jpg"),
    ("https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/64fd64c20e46821a1010352b51ef5584~tplv-tiktokx-cropcenter:100:100.jpg", "img/avatars-forno-hq/buyer-j.jpg")
]

all_downloads = slides + reviews + avatars

for url, path in all_downloads:
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = resp.read()
            with open(path, 'wb') as f:
                f.write(data)
            print(f"[OK] {path} ({len(data)} bytes)")
    except Exception as e:
        print(f"[ERRO] {path}: {e}")
