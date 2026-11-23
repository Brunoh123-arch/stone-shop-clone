import subprocess
import os
import requests
import json

videos = [
    {
        "id": "sergia",
        "url": "https://www.tiktok.com/@achadinhos.by.sergia/video/7677808936585579796",
        "name": "Sérgia Stefany",
        "username": "achadinhos.by.sergia",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/a94d22a807c8d5d549fc71dce3f41e16~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b8d51ba9&x-expires=1795467600&x-signature=PS5dnFXXJcCmfbO5JNyVVzYwS0I%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
        "desc": "🚴‍♀️ Bicicleta Aro 29 GT Sprint MX7 24V! Leve, resistente e perfeita para trilhas, passeios e uso no dia a dia. Suspensão dianteira, freio a disco e quadro em alumínio! 🔥 #BicicletaAro29 #BikeMTB #GTSprint #MountainBike"
    },
    {
        "id": "vitrine",
        "url": "https://www.tiktok.com/@vitrineesperta.achados/video/7685077822209035538",
        "name": "Vitrine Esperta",
        "username": "vitrineesperta.achados",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/73925911304ddf7f8cb21c607e012ea4~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=59f6801a&x-expires=1795467600&x-signature=2nKCc8PgiWkczEWXL0%2BUzWKo4v0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
        "desc": "🚴‍♂️ Para encarar a cidade e os passeios com muito mais estilo! Bicicleta GT Sprint MX7 com aro 29, 24 marchas, quadro de alumínio, suspensão dianteira e freios a disco! 🔥🚵‍♂️ #BicicletaAro29 #MountainBike #Ciclismo"
    },
    {
        "id": "melo",
        "url": "https://www.tiktok.com/@dicasdamelo66/video/7682855774804020498",
        "name": "Melô Dicas",
        "username": "dicasdamelo66",
        "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/8f0b0078c7d663e044d73197c8a217ae~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=588ed822&x-expires=1795467600&x-signature=mT9980c7lwJNNbJRTBTM%2BqNx1jo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
        "desc": "Bicicleta Aro 29 MTB 24V linda demais! Chegou super bem embalada e a montagem foi muito fácil! Super recomendo! 🚴‍♀️✨ #bike #aro29 #ciclismo"
    },
    {
        "id": "renato",
        "url": "https://www.tiktok.com/@renatosantos214/video/7661337005921455378",
        "name": "Renato Ciclista",
        "username": "renatosantos214",
        "avatar": "https://p19-common-sign.tiktokcdn.com/tos-maliva-avt-0068/ab1710d6fd751c8e227d2dacd467a9d6~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=1f0a7fcc&x-expires=1795467600&x-signature=TDb7CTimAFhuOZYZC5w2XDZiamk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
        "desc": "Bicicleta aro 29 com freios de alta precisão, 24 marchas e suspensão com trava! Custo-benefício top demais pra trilha e asfalto! 🚵‍♂️💨 #bikearo29 #bike #bicicletaaro29 #mtb"
    }
]

os.makedirs("temp_bike20", exist_ok=True)
os.makedirs("videosprodutos/posters", exist_ok=True)

for v in videos:
    raw_file = f"temp_bike20/{v['id']}_raw.mp4"
    clean_file = f"temp_bike20/{v['id']}.mp4"
    if v['id'] == 'renato' and os.path.exists("temp_bike20/renato.mp4"):
        raw_file = "temp_bike20/renato.mp4"
    else:
        print(f"Downloading {v['id']}...")
        subprocess.run(["yt-dlp", "--impersonate", "chrome", v['url'], "-o", raw_file], check=True)
    
    # Re-encode to standard h264 / aac to ensure 100% universal browser compatibility
    print(f"Encoding {v['id']} to h264...")
    subprocess.run([
        "ffmpeg", "-y", "-i", raw_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart",
        clean_file
    ], capture_output=True, check=True)
    
    # Extract poster at 1.5s
    poster_path = f"videosprodutos/posters/poster-criador-20-{v['id']}.jpg"
    subprocess.run(["ffmpeg", "-y", "-i", clean_file, "-ss", "00:00:01.5", "-vframes", "1", poster_path], capture_output=True, check=True)
    print(f"Poster extracted: {poster_path}")
    
    # Upload to Catbox
    print(f"Uploading {v['id']} to Catbox...")
    with open(clean_file, "rb") as f:
        resp = requests.post("https://catbox.moe/user/api.php", data={"reqtype": "fileupload"}, files={"fileToUpload": f}, timeout=60)
        cat_url = resp.text.strip()
        print(f"Catbox URL for {v['id']}: {cat_url}")
        v['catbox_video'] = cat_url
        v['local_poster'] = f"../videosprodutos/posters/poster-criador-20-{v['id']}.jpg"

with open("temp_bike20/final_creators.json", "w", encoding="utf-8") as f:
    json.dump(videos, f, indent=2, ensure_ascii=False)
print("ALL DONE!")
