with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

pos = vc.find("CREATORS_SCOOTER_102 =")
print(vc[pos:pos+800])
