import urllib.request
import os
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def download_file(url, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    # Se a url tem resize crop webp, converter para resize-jpeg 800:800
    if '~tplv-aphluv4xwc' in url:
        base = url.split('~tplv-aphluv4xwc')[0]
        url = base + '~tplv-aphluv4xwc-resize-jpeg:800:800.jpeg'
    
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

revs_106 = [
    {
        "id": "c1",
        "name": "a**e l**a",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/72b8aab1194b00623fe9b99dbdb7963a~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=8381b753&x-expires=1794405600&x-signature=R2nuhJBa35PGHrCciuEgB%2BV8UFs%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "14/06",
        "variation": "Lilás, M",
        "comment": "O body é lindíssimo e chegou super rápido, amei minha compra, vou comprar outras cores.",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/98b14621d2274c94bb114a15f0a7be0d~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/66c4dc11589d4589b0d82b97b3093885~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/1d9175faeb304f55b4144392f22ba790~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    },
    {
        "id": "c2",
        "name": "m**📚",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/a34fbaf0fe157b47080b3ee0d5085b4e~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=3e6a7ba2&x-expires=1794405600&x-signature=on5e%2FLXNGkgwEQgpEndMvTn3pG8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "09/06",
        "variation": "Bege, G",
        "comment": "Qualidade do produto: Excelente. Gostei, o material é uma malha bem fria, muito boa! Não machuca.",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/3b4b6538cdf2454ea6bac6ec57ec7126~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/59e0445cbc494b7996b5b525b8f84724~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/20605617b8064b5f93f60a223c10bf4d~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/72b7674ef04c4615bf05f70f8fdeae68~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    },
    {
        "id": "c3",
        "name": "𝐋**🌵",
        "avatar": "",
        "date": "06/06",
        "variation": "Bege, P",
        "comment": "Está de parabéns... amei e bem confortável pra ser um tamanho P, eu visto 44. Gostei muito.",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/00263a448dfa45f3b6dd22c44e62f007~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/e4ab292db17649dcbd228cc63cb6f60a~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    },
    {
        "id": "c4",
        "name": "G**e M**a",
        "avatar": "https://p19-common-sign.tiktokcdn.com/tos-alisg-avt-0068/c4c20355519744258a196d845a4a9bcb~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=4fbd7594&x-expires=1794405600&x-signature=62EdxkcbERRva5u67idA1v6Rr5s%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "31/10",
        "variation": "Bege, G",
        "comment": "Cara eu to apaixonada já fiz o teste amei ela cai muito bem no corpo e linda eu gosto 44 pegue a G e ficou ótima maravilhosa vou até comprar mais uma e outra chegou bem rápido demorou só 1 dia para chegar muito obrigado a loja.",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/474f14415edf4d399e7843c5bd33b22c~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/6598398bf86e488ea8b6bf70698281af~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/02037d85cc394d3bace4fd6aa6b7ffc1~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    },
    {
        "id": "c5",
        "name": "P**a F**a",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/9977e77ffbee8fe7a4ec21e9d52c0ab5~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=234e2238&x-expires=1794405600&x-signature=oUwQ9xx6WOH16Ry0iIhI2s751bw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "27/06",
        "variation": "Preto, P",
        "comment": "Qualidade do produto: Gostei muito do body. O tecido é confortável, tem ótima compressão e o tamanho P vestiu muito bem. Vale a pena!",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/20ce17a0fe8b4989ad23105c95417831~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/8b2d63372c824b928fca889c7a673f84~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/561eddd317764c89855b7769ec0ffa97~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    },
    {
        "id": "c6",
        "name": "L**a G**s",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/7328905498856538119~tplv-tiktokx-cropcenter:100:100.jpg?dr=14579&refresh_token=9ca6ea2f&x-expires=1794405600&x-signature=RyrA0%2BvJTVFHF7edPc7WeS1zzDE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=5f8d3399&idc=my2",
        "date": "14/08",
        "variation": "Bege, P",
        "comment": "Ela é perfeita, superou minhas expectativas. Modela perfeitamente o corpo!",
        "photos": [
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/adfe44bf62b0474da83dae5c22a9cf67~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p19-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/1578e78a1f64474a9d80232238efa32b~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/29064fe3b2b24d8bbc3f33da5cd84f48~tplv-aphluv4xwc-crop-webp:300:300.webp",
            "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/f516e1ba178f4d6f9b7220d557e8cd32~tplv-aphluv4xwc-crop-webp:300:300.webp"
        ]
    }
]

with open('reviews_106_real.json', 'w', encoding='utf-8') as f:
    json.dump(revs_106, f, ensure_ascii=False, indent=2)

for r in revs_106:
    rid = r['id']
    if r['avatar']:
        av_path = f"img/reviews-avatars/review-user-106-{rid}.jpg"
        download_file(r['avatar'], av_path)
    for idx, p_url in enumerate(r['photos']):
        p_path = f"img/review-106-{rid}-{idx+1}.jpg"
        download_file(p_url, p_path)

print("ALL 106 REVIEWS PROCESSED!")
