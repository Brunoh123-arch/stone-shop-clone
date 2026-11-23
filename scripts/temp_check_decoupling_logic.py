with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

pos = vc.find("Desacoplamento estrito entre o vídeo oficial")
print(vc[pos:pos+1200])
