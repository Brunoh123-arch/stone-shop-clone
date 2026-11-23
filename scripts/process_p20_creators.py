import urllib.request
import subprocess
import os
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Referer': 'https://www.tiktok.com/'
}

items = [
    {
        "id": "bike20_1",
        "url": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o48QUIHdgA6LBCmgRFfaQqDBeXjqcEEiTyqPPa/?a=1988&bti=ODszNWYuMDE6&&bt=390&ft=I~da4oKyD12Nv-a_slIxRcOSwlBF-UjNS3opiX&mime_type=video_mp4&rc=PDQ5aDppOjg0NzQ1PDllM0BpM2pvbW05cjZqZDMzODczNEAvMTBhXjUzNjAxM2ItMGEyYSM0L14tMmRzcTNhLS1kMTFzcw%3D%3D&expire=1795470214&l=2026112205432474E60461FE591F772B98&ply_type=2&policy=2&signature=b5a6e35ca3ff7c08194879aea08a0b48&tk=tt_chain_token&btag=e000b0000",
        "name": "Sérgia Stefany",
        "username": "achadinhos.by.sergia",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/a94d22a807c8d5d549fc71dce3f41e16~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b8d51ba9&x-expires=1795467600&x-signature=PS5dnFXXJcCmfbO5JNyVVzYwS0I%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
        "desc": "🚴‍♀️ Bicicleta Aro 29 GT Sprint MX7 24V! Leve, resistente e perfeita para trilhas, passeios e uso no dia a dia. Suspensão dianteira, freio a disco e quadro em alumínio! 🔥 #BicicletaAro29 #BikeMTB #GTSprint #MountainBike"
    },
    {
        "id": "bike20_2",
        "url": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/oYKxteIIQDAVnTTeHwL4Nid8ezM4HIADGCcjUx/?a=1988&bti=ODszNWYuMDE6&&bt=601&ft=-Csk_mrMPD12N.vFuY-Ux7vvWY6e3wv25AcAp&mime_type=video_mp4&rc=ZmdkZTxkNTQ5ZmY6N2k5N0BpamVyZnY5cjdoZDMzODczNEBiLjQ0M14wXy4xNF8zLTZjYSNjcmM1MmRzMGdhLS1kMWBzcw%3D%3D&expire=1795470243&l=202611220543555C9F1461D6CBED6DA9EF&ply_type=2&policy=2&signature=b02b448097edd73c9fcf8cb064854e18&tk=tt_chain_token&btag=e000b0000",
        "name": "Vitrine Esperta",
        "username": "vitrineesperta.achados",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/73925911304ddf7f8cb21c607e012ea4~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=59f6801a&x-expires=1795467600&x-signature=2nKCc8PgiWkczEWXL0%2BUzWKo4v0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
        "desc": "🚴‍♂️ Para encarar a cidade e os passeios com muito mais estilo! Bicicleta GT Sprint MX7 com aro 29, 24 marchas, quadro de alumínio, suspensão dianteira e freios a disco! 🔥🚵‍♂️ #BicicletaAro29 #MountainBike #Ciclismo"
    },
    {
        "id": "bike20_3",
        "url": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/ogZDEcCXHBHAdAJ8wStSP8IQiBliaEiaVYKlX/?a=1988&bti=ODszNWYuMDE6&&bt=2473&ft=-Csk_mrMPD12NfkFuY-UxdJFVY6e3wv25scAp&mime_type=video_mp4&rc=aDdkNTppODNpNGY3M2c7N0BpanE8b3Y5cnQ7PDMzODczNEBjX2AuYF8uXy4xLy80LWFiYSMwbG4uMmQ0YjZhLS1kMTFzcw%3D%3D&expire=1795470210&l=2026112205425797BDD39C5A621F41742D&ply_type=2&policy=2&signature=ca5b387555f0aaa88c4afbdce3853b8a&tk=tt_chain_token&btag=e00088000",
        "name": "Renato Ciclista",
        "username": "renatosantos214",
        "avatar": "https://p19-common-sign.tiktokcdn.com/tos-maliva-avt-0068/ab1710d6fd751c8e227d2dacd467a9d6~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=1f0a7fcc&x-expires=1795467600&x-signature=TDb7CTimAFhuOZYZC5w2XDZiamk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
        "desc": "Bicicleta aro 29 com freios de alta precisão, 24 marchas e suspensão com trava! Custo-benefício top demais pra trilha e asfalto! 🚵‍♂️💨 #bikearo29 #bike #bicicletaaro29 #mtb"
    },
    {
        "id": "bike20_4",
        "url": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037/o86qCwxTJA18gV9XgQFUnfUDofLv2LvEBCB89I/?a=1988&bti=ODszNWYuMDE6&&bt=2581&ft=-Csk_mrMPD12NkvFuY-UxKvFPY6e3wv25zcAp&mime_type=video_mp4&rc=Njc1NDQ3ZDk5OWdpOGk6OkBpM3E6a3g5cnRpZDMzODgzNEBeLWI1M2FjX2ExYjA1MzJjYSNpamFiMmQ0bGNhLS1kLzFzcw%3D%3D&expire=1795470235&l=2026112205434074E60461FE591F773097&ply_type=2&policy=2&signature=220fe625829549d6a163592adaaa8493&tk=tt_chain_token&btag=e000b8000",
        "name": "Melô Dicas",
        "username": "dicasdamelo66",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/8f0b0078c7d663e044d73197c8a217ae~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=588ed822&x-expires=1795467600&x-signature=mT9980c7lwJNNbJRTBTM%2BqNx1jo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
        "desc": "Bicicleta Aro 29 MTB 24V linda demais! Chegou super bem embalada e a montagem foi muito fácil! Super recomendo! 🚴‍♀️✨ #bike #aro29 #ciclismo"
    }
]

os.makedirs("temp_bike20", exist_ok=True)
os.makedirs("videosprodutos/posters", exist_ok=True)

uploaded = []

for item in items:
    mp4_file = f"temp_bike20/{item['id']}.mp4"
    poster_file = f"videosprodutos/posters/poster-criador-20-{item['id'].split('_')[1]}.jpg"
    print(f"Downloading {item['id']}...")
    req = urllib.request.Request(item['url'], headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp, open(mp4_file, 'wb') as f:
        f.write(resp.read())
    size = os.path.getsize(mp4_file)
    print(f"Downloaded {mp4_file}: {size} bytes")

    # Generate poster
    subprocess.run(["ffmpeg", "-y", "-i", mp4_file, "-ss", "00:00:01", "-vframes", "1", poster_file], capture_output=True)
    print(f"Poster generated: {poster_file}")

    # Upload to Catbox
    print(f"Uploading {mp4_file} to Catbox...")
    with open(mp4_file, 'rb') as f:
        r = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f}, timeout=60)
        catbox_url = r.text.strip()
        print(f"Catbox URL: {catbox_url}")
        uploaded.append({
            "name": item["name"],
            "username": item["username"],
            "avatar": item["avatar"],
            "poster": f"../videosprodutos/posters/poster-criador-20-{item['id'].split('_')[1]}.jpg",
            "video": catbox_url,
            "desc": item["desc"]
        })

print("\nFINAL MAPPING:")
import json
print(json.dumps(uploaded, indent=2, ensure_ascii=False))
with open("temp_bike20/result.json", "w", encoding="utf-8") as f:
    json.dump(uploaded, f, indent=2, ensure_ascii=False)
