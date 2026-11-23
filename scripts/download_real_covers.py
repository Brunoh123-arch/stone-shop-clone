import urllib.request, os

# Baixar as capas reais do TikTok que extraímos via Playwright
covers = {
    'img/poster-churras-1.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oskpIUicEDAZ1QjFuOF3BRpBJESgRBPNQbffpE~tplv-tiktokx-origin.image?dr=14575&x-expires=1794715200&x-signature=cABNx1zTbE1Gt2Sx3pKVuZ%2BxrlM%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2',
    'img/poster-churras-2.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-v-97b414-sg/oMlSApDB0IqiFOrYQgfC9fSAh9UklZfGHEDA3E~tplv-tiktokx-origin.image?dr=14575&x-expires=1794715200&x-signature=ljCHksUyohu0cremlYIkZHS1Uow%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2',
    'img/poster-churras-3.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-p-0068/cef9d199726e4f4fab9a90380f00330d_1703710755~tplv-tiktokx-origin.image?dr=14575&x-expires=1794715200&x-signature=9IjI%2BKss7sJOKKCiqnSiEYNCF%2BM%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2',
    'img/poster-churras-4.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o06BfopVAyRsEsFEFMAYTIIDsgwcLSyBWlfO2v~tplv-tiktokx-origin.image?dr=14575&x-expires=1794715200&x-signature=yEG9uoemTLGskSAR%2BZ6eA1fS1zg%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2',
    'img/poster-churras-5.jpg': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oEeAIDALfEAuCrAAcXELirICuXFLGePFSWrVGW~tplv-tiktokx-origin.image?dr=14575&x-expires=1794715200&x-signature=03sLgYkIkMT7zz0cd0xegfT0nRk%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2',
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for path, url in covers.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp, open(path, 'wb') as f:
            f.write(resp.read())
        print(f"Baixado: {path} ({os.path.getsize(path)} bytes)")
    except Exception as e:
        print(f"Erro em {path}: {e}")
