with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

pos = vc.find("default:")
if pos == -1:
    pos = vc.find("case 124:")
print(vc[pos:pos+1500])
