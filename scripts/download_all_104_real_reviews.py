import urllib.request
import os
import json

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
        print(f"Error downloading {url} -> {out_path}: {e}")
        return False

# Reviews data structure
reviews = [
    {
        "id": "c4",
        "name": "k**e R**e R**u",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/2a47fd669282ce36c5ecde82bec1dadb~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=45f4d56e&x-expires=1794398400&x-signature=GbW%2FykKazKIALYq9jcHnZ9FQL8E%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "BRANCO, 35/36",
        "date": "17/09",
        "comment": "Forma e tamanho: 35 cor branca Muito linda ameiiii",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/be2aab981a7e4a859ab61c19f7dc73e1~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/5db65f9ceacf43c38c54d26a06d05d64~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/2b644168c97a450c9ae3bbd9c0601509~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/7280538d494044f2a223ea857ad1aa25~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/4aabe9e6f9b0497b8e0d773bc0574339~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/ea049b38a3234e0490dad33a762d6561~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c5",
        "name": "S**a",
        "avatar_url": None,
        "variation": "BRANCO, 37/38",
        "date": "25/09",
        "comment": "Eu estava com medo de comprar e não ser do mesmo jeito que estava na propaganda. Mas quando chegou fiquei impressionada com a qualidade e conforto do produto. Com certeza",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/2715ebf27bc8433ca57068278fb321ef~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/6fb8832708ce43c5b6f75f575ccfa8e4~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/6e5bf823d0b8446bb686f0a18ca011a2~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c6",
        "name": "k**💟",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/9754f19712bb2212d8473d310f774117~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=4c2fbd1b&x-expires=1794398400&x-signature=NbIfZGB2fvZPEGZ%2BLj5fr7Yxdco%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "BRANCO, 37/38",
        "date": "07/09",
        "comment": "Recomendo para quem for comprar muito bonita material bom detalhes bonitos calço 37 comprei um 37/38 e ficou excelente no meu pé vou comprar mas uma novamente mas em outra cor Cor: Branca Usabilidade: Boa Aroma: Bom Forma e tamanho: 37/38",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/745b3a3322144ec28df316ef1b8c8995~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/6fe513c3fa034e1ea053af94ed045d0a~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/0ca295af6b0b4a79b5783d054a265f2d~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/52ed7c3f45e44f398b02184466e4bac7~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/47765bcf3d3542fd806bd411a984e0b7~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c7",
        "name": "A**1",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/e40a19318c56a7512ac95b9a47c48544~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=621d048d&x-expires=1794398400&x-signature=hDqshW0a88B0q4tZKMNI08tX6Go%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "BRANCO, 37/38",
        "date": "25/08",
        "comment": "Chegou no prazo certo, muito linda ela, amei gente super recomendo, foi a minha primeira compra no tiktok eu amei 😍 Cor: Branca Aroma: Muito cheirosa ela Forma e tamanho: Tanha 37:38 perfeita",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/fb287494dddc4e959e6d52cef445c401~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/f3c29d03774b47bfa893b5a3370f144c~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/6243be527e0e4732a6e5ba759956e7d3~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/6bff7152e3df4f09ace1fd950700950b~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c8",
        "name": "e**h",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/76b707dd5a0a3ba896016d8600b39ef1~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=4bd7d12c&x-expires=1794398400&x-signature=7Ntc6EoQ0fBkdUWIab3%2BhzeurHU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "CARAMELO, 37/38",
        "date": "07/07",
        "comment": "Linda e muito confortável Calço 36 mas pedi o 37 e ficou muito boa Forma e tamanho: Bom Cor: Perfeita Aroma: Sem cheiro Usabilidade: Para qualquer lugar",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/68afea3b1bd14a269b4d20694275564a~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/b1fc4e045a0941cdb7218e1e5d1a2e09~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/4e1287972eab4db0814c305ae2f8db51~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/afa97599ee5b4e0ebc47da6a67b38752~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c9",
        "name": "C**e C**🐆",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/dae151c75519d9fc360641f8f0e0ee7f~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=bf4de62e&x-expires=1794398400&x-signature=g%2B0bwxJmSnPlHlpHccAQHbwtYsU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "CARAMELO, 37/38",
        "date": "15/07",
        "comment": "Lindas. Forma e tamanho: Bom Aroma: Nenhum Usabilidade: Boa Cor: Cores bonitas",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/9ea59c9aed894288a7b18d87f066dfef~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/a7954f5ed78f414dbe276baba7e5aed0~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/bc590f960a21465481d1fc9d03f9c4d6~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c10",
        "name": "L**a L**",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/7334499173544230918~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=d7424583&x-expires=1794398400&x-signature=RkXK5QlMa7rYkUpRgBwPQfn9wa4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "BRANCO, 35/36",
        "date": "02/09",
        "comment": "Cor: Igual anúncio Forma e tamanho: Serviu direitinho conforme medidas de pesquisa Usabilidade: Para varias ocasiões. Chegou dentro do prazo. O único problema e q pedi com brilho em toda lateral, mas não veio Mas, vou ficar assim mesmo, pq gostei muito",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/43444579079a4d199a263ce88bbb355d~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/c7cbf96dd4ec48838a983806b9244e53~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/a57323064ed24553bf2cbc536f0f3e95~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c11",
        "name": "2**_",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/2473956c83c56455b783fcbd23d69047~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=f71849c2&x-expires=1794398400&x-signature=i%2FlfQCRP0fzvygbMAT33KaHtfhU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "BRANCO, 35/36",
        "date": "16/07",
        "comment": "Eu gostei demais, extremamente lindo e brilhoso. Recomendo super e chegou no dentro do prazo certinho. Lembrando que eu peguei 35/36 e eu uso 36, e ficou bem certinho",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/ff40fe479f464cc1892f015641f84fe3~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c12",
        "name": "K**n G**s",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/c302e30f427c156e729576ced1a2de77~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=0d59f600&x-expires=1794398400&x-signature=lHgqDlobdflMVbK89NtxzSyaQ0Y%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "PRETO, 35/36",
        "date": "29/08",
        "comment": "Amei e achei muito confortável, se for comprar compra o número que usa certinho",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/c84d8983825645eca96b0d31cc20bed1~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c13",
        "name": "L**a C**a",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/a4118d886853805a1d9af528970d2b36~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=7e474d5a&x-expires=1794398400&x-signature=eFAv10QSBgl8Tr8sSTCcwT5IhF4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "BRANCO, 39/0",
        "date": "10/10",
        "comment": "Forma e tamanho: Padrão Aroma: Sem Usabilidade: Perfeita Cor: Linda Os chinelos são lindos… Valem super a pena! Podem comprar sem medo! 🤍",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/a7bded3dd2324337aa76f1a0433bb519~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    },
    {
        "id": "c14",
        "name": "V**a L**a R**g",
        "avatar_url": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/7324571125537898498~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=d218d3ea&x-expires=1794398400&x-signature=GdvqWC1b7qC1dB59%2BKJUXxRpzRE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "variation": "BRANCO, 37/38",
        "date": "07/11",
        "comment": "Ela nao é branca é creme",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/8e9eb19d05be4d2fa144893de75321f9~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg"
        ]
    }
]

for r in reviews:
    rid = r['id']
    # download avatar if present
    if r['avatar_url']:
        av_path = f"img/reviews-avatars/review-user-104-{rid}.jpg"
        download_file(r['avatar_url'], av_path)
    
    # download photos
    for idx, p_url in enumerate(r['photos']):
        p_path = f"img/review-104-{rid}-{idx+1}.jpg"
        download_file(p_url, p_path)

print("ALL ASSETS DOWNLOAD SCRIPT COMPLETED!")
