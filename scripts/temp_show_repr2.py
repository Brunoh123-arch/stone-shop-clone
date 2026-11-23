with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

pos = vc.find("Desacoplamento estrito")
print(vc[pos-50:pos+700])
