import urllib.request
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def download_file(url, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
            with open(out_path, 'wb') as f:
                f.write(data)
            print(f"Downloaded: {out_path} ({len(data)} bytes)")
            return True
    except Exception as e:
        print(f"Error {url} -> {out_path}: {e}")
        return False

revs_105 = [
    {
        "id": "c1",
        "name": "M**s S**a",
        "avatar": "https://p16-common-sign.tiktokcdn.com/musically-maliva-obj/1594805258216454~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=6272e8dd&x-expires=1794402000&x-signature=vwJ3%2F8jkZBy7jxapRoQGJh%2FV7gk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "13/08",
        "variation": "PADRÃO, BIVOLT",
        "comment": "Muito boa qualidade Clareza da lente: Muito bom Qualidade do trabalho: Muito bom",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/3ddfff0b3b0a41bc9dc343ea232446f5~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/4d9ce44fe78346c4bdf7a6c29e7d0abd~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c2",
        "name": "u**3",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/0f3080df3f229028764333d3c17634e8~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=5f790f48&x-expires=1794402000&x-signature=U23KSWTbg4m%2F7g3sATh4hK9j4gU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "11/08",
        "variation": "PADRÃO, BIVOLT",
        "comment": "Gosteiii, comprem. Ele conecta rápido na internet e o som é okk. Ameiii",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/8a49bd783b94435193af081808792e3c~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/19ec023f5faa433486d7fba3e175e191~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c3",
        "name": "J**a S**🌈",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/1e3d2408853232b15d191905a9e530af~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=fda7a4f0&x-expires=1794402000&x-signature=JCYyzCYDqhxusMB4NrQVWvyFowY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "05/08",
        "variation": "PADRÃO, BIVOLT",
        "comment": "Perfeito muito boa mesmo Qualidade do trabalho: Muito boa a qualidade muito fácil de mexer bem manual junto com a caixa chegou rápido a imagem é muito boa eu super recompraria e fiquei muito satisfeito com minha compra compensa muito",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/a449690c3bac402786a95fe955ddb3b7~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/dcbd304cbb284b1fbe8e626266d5256e~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c4",
        "name": "R**l C**a",
        "avatar": "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/15ff8b1a92b4344f3ed6a1452dda9d8e~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=5a9b8711&x-expires=1794402000&x-signature=wSCvnBmJZAJ0uzHfnZF%2BojvJLiI%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "08/06",
        "variation": "PADRÃO, BIVOLT",
        "comment": "Produto bom e espero q satisfaça minhas expectativas mas aparentemente e de boa qualidade e a entrega foi muito rápida, obrigada ao vendedor e a tik Tok. Clareza da lente: Sim top",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/96728ff585744ad49b051b9fa7e0915a~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/4d7c39f7194a4d04aa535da003467105~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    }
]

for r in revs_105:
    rid = r['id']
    av_path = f"img/reviews-avatars/review-user-105-{rid}.jpg"
    download_file(r['avatar'], av_path)
    for idx, p_url in enumerate(r['photos']):
        p_path = f"img/review-105-{rid}-{idx+1}.jpg"
        download_file(p_url, p_path)

print("ALL 105 REVIEWS DOWNLOADED!")
