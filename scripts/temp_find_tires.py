with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

for name in ['CREATORS_TIRES', 'CREATORS_SCOOTER_102']:
    print(name, "in file?", name in vc)
    pos = vc.find(name)
    while pos != -1:
        print(f"  found at {pos}:", vc[pos:pos+100])
        pos = vc.find(name, pos+1)
