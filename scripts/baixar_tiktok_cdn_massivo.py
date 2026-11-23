import urllib.request
import os
import re
from PIL import Image

# Coleta de URLs do TikTok CDN
all_urls = set()

# 1. URLs encontradas nos scripts anteriores
if os.path.exists('scripts/all_found_tiktok_cdn_urls.txt'):
    with open('scripts/all_found_tiktok_cdn_urls.txt', 'r', encoding='utf-8') as f:
        for line in f:
            u = line.strip()
            if u:
                all_urls.add(u)

# 2. URLs adicionais capturadas agora via Playwright
NEW_PLAYWRIGHT_URLS = [
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/551c69cf42df67ecc7ee04b070525292~tplv-tiktokx-cropcenter:720:720.jpeg?dr=14579&refresh_token=b768ea38&x-expires=1795093200&x-signature=E0KQE4iLjWfnvPInTy5BMYQ26%2B0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/23010a3cc33edefef4a317e4b910c2de~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=cc8885c3&x-expires=1795093200&x-signature=GCbsEFDgeXot0qwVOhPo2504iW4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/ddf967f7cb45a1582d83272da2f64ddf~tplv-tiktokx-cropcenter:720:720.webp?dr=14579&refresh_token=db29a377&x-expires=1795093200&x-signature=s2K2zGEZLRw%2BiwUdM6ynt0fnUyc%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/877a6cf3a699a1a6c18c2583fb9cc4c2~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=c0bbf0ea&x-expires=1795093200&x-signature=nqWh84xQ6aX4iV0v3ZRxBHhBiAk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/f011efc6125b6ecab342404dd3fa21b7~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=8902e905&x-expires=1795093200&x-signature=MzIkRCd32Hxq7cOLEz%2FNZVXRO%2BA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/ed7b8e0e3a215479479ab245c1814f94~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=708d3f84&x-expires=1795093200&x-signature=pcjW9a03ibSKfLQRDO16ccxcuL0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/2da572c0afc2d8c147fcfd4f90519b54~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=cca65a40&x-expires=1795093200&x-signature=mFI9g4KXMYHaaiBK5hqnQPm8Ey0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/1761f33d5bf5e299e88861276f123a2f~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=8ef1c690&x-expires=1795093200&x-signature=8tDxze4iAwlBFvT%2BHT%2BoLRFuHhE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/37c11dcf057d99807aea70b918f5eda0~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=1316e3cb&x-expires=1795093200&x-signature=4A391zlLxatYnDYqL%2Be7u2xrYVw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/fdbb1dbbe4cc0064f303ebe9a767abf3~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=3c76a507&x-expires=1795093200&x-signature=3WQSWu9nP3KjrDaBvEKir23M3j0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/727a9726ba5b325b4bd46ae6e0470e04~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=ba1ed2e8&x-expires=1795093200&x-signature=M2G3YC3jcDdPKhiPYzsTprH%2B7Ic%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/524fe6c323ef4ef7ae9eba0c471d3bf7~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=6511d4dd&x-expires=1795093200&x-signature=ty7pvNuxOeaPjpzXE2XWyTaSsgw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/cdb6106f19950029db3f13bbc326e157~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=307ca17e&x-expires=1795093200&x-signature=Z3O264ND6GHOeQp6t2NLB%2FJTwvo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/9c5194d4cb263477d67626219cc7781a~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=4f4482f1&x-expires=1795093200&x-signature=FzILMomsqafB%2F6Od4mHHTrUESXs%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/5ea3a45b14f0e3810b5b43c50c70d4b7~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=d46d234d&x-expires=1795093200&x-signature=7yCEZWxgGDjaNKNKooAPY3CE7Sw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/b63e994358fec029c04c4c885d63b4f9~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b611118f&x-expires=1795093200&x-signature=Bwqv26GIpQQ4%2Flsk%2FjEtk81T22U%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=fdd36af4&idc=my",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/5148171bbebad928df5590bfc9504f28~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=10cb2a94&x-expires=1795093200&x-signature=W%2F01KVQdCzXVkqZP2V7eUJFj6%2FA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/5b9a3884efcecf1f853f88cc1c830897~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=303f7bf7&x-expires=1795093200&x-signature=gaM7vRoekeU2HeNH3bfRC6b7jE4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/f1d0b9f1ceba2ab51d6b9e35927ce925~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=46fda021&x-expires=1795093200&x-signature=X0wM5mGAB%2FO0q1VJtcpnkLCaF1g%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/09b5900a5fc2b3dafaf320230c50fa87~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=e1918e67&x-expires=1795093200&x-signature=Wfhyxu6fvrgFssFA67RTaqnPytg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/1b8c951ff015b8a1b6b3f4a679fad603~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=0f512831&x-expires=1795093200&x-signature=1kWfx3hIFpqQL%2B512ESXetkK7GE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/f22a1faf77981d786eaa3c478776b2fa~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=7fa032b6&x-expires=1795093200&x-signature=JwFKh4BQDCgXgajxduyrn2Q0Icg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/8e2c1bd935f0e75689f2d9f8b2437d15~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=956be701&x-expires=1795093200&x-signature=ZUX0UTa%2FFOQpjj8yB3rRn7QhVL4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/cbdefee444050868f47cc6e28f6c1ec0~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=bbad58b6&x-expires=1795093200&x-signature=jR3ZEmsF2jMybmFPGmuN%2BxcRm3Y%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/53e14a1c81ff02df7490348c1affd7c2~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=53cf57bc&x-expires=1795093200&x-signature=8S7%2Fq85kdSgP9GwvOPTdBMP7xq4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-maliva-avt-0068/6a483e9e256d2e2eaf1f8783e5d31e35~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=438d771b&x-expires=1795093200&x-signature=hCEUMzZotlTKDGgKq2OxN2HN7Ek%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/d8433fe18c3b56320af53a4d1cf051c4~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=c0153d37&x-expires=1795093200&x-signature=vgHg2MlVUcT7sOkq7rlmg6vWwvk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/fa3b14e9499d24911902c156a222f8eb~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=d8777733&x-expires=1795093200&x-signature=hcMP5tDHpH5CFtvjjC%2FYK%2BI%2FTwg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/fe3d04ae1d9c6aaf4d22a2692af390e9~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=5afadc5e&x-expires=1795093200&x-signature=T0M4%2Fn6xdJGfMj74pmJlZnQycSc%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/0abd6ba3e1f8e6a5d0dc81dc3847bbc0~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=6a4046fe&x-expires=1795093200&x-signature=LPN74anWVCpbLxMoIKiofhohs4c%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/0601d7db6c08660d5a58dfe08e0e2a80~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=83ea798d&x-expires=1795093200&x-signature=3elimzJDn7v%2BI2zVK%2Bro7UkEiDo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/5e03bf4d2d535cbff38bf782c7160b4d~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=4b15b8b9&x-expires=1795093200&x-signature=0XKv4l4cAdiblQeKtyP4PdcMdGQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/3ffcf365c9ba2020838aa841d0a54807~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=047021eb&x-expires=1795093200&x-signature=w66Gv%2BOrg66Tc7GUnh7WEgp936g%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/fd22dae4a248c50d9c476759dc7b8ed4~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=cc408ef7&x-expires=1795093200&x-signature=l2%2B%2BjkvohBkryYlc3mryHXKFRaA%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/40546a99d929d1104bd4394123b31be9~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=9488b9d7&x-expires=1795093200&x-signature=xWg%2BWgnTxIauGASlQDyYWPk5Ggs%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2",
  "https://p19-common-sign.tiktokcdn.com/tos-maliva-avt-0068/825cc0b0cbb770a0b25181f9a9265019~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=e9be16fb&x-expires=1795093200&x-signature=kaPklgJPm3NI7tYXpZer4hO4ttk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my2"
]

all_urls.update(NEW_PLAYWRIGHT_URLS)
print(f"Total de URLs para download do TikTok CDN: {len(all_urls)}")

target_dir = 'img/reviews-avatars/tiktok_cdn_real'
os.makedirs(target_dir, exist_ok=True)

success_count = 0
for i, url in enumerate(sorted(all_urls)):
    # Remover o arquivo da Barbie (tt_avatar_5/30) e Jesus (tt_avatar_32)
    if 'ebff87f3cafae8f6507906790f473eb7' in url or 'e8328eb236d71debfd3ba16477d63956' in url:
        print(f"Descartando meme/barbie conhecido na URL {i+1}")
        continue
        
    dest = os.path.join(target_dir, f"tt_cdn_{success_count + 1}.jpg")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = resp.read()
        if len(data) > 1000:
            with open(dest, 'wb') as out:
                out.write(data)
            # Validar com PIL
            try:
                im = Image.open(dest).convert('RGB')
                w, h = im.size
                if w >= 80 and h >= 80:
                    # Checar se não é imagem sólida (branca/preta)
                    pixels = list(im.getdata())
                    r_tot = sum(p[0] for p in pixels)
                    avg_r = r_tot / len(pixels)
                    if 20 < avg_r < 240:
                        success_count += 1
                        print(f"[{success_count}] Baixado e aprovado: {dest} ({w}x{h}, {len(data)} bytes)")
                    else:
                        os.remove(dest)
                else:
                    os.remove(dest)
            except Exception:
                if os.path.exists(dest):
                    os.remove(dest)
    except Exception as e:
        pass

print(f"\nTotal final de avatares autênticos do TikTok CDN em disco: {success_count}!")
