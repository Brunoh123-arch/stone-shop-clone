with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

pos = vc.find("switch (prodId)")
print(vc[pos+3000:pos+5000])
