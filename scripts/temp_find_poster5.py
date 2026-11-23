import os, glob

# Check where poster-criador-5 is referenced
with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

for p in ["poster-criador-5-1", "poster-criador-5-2", "poster-criador-5-3", "poster-criador-7"]:
    print(f"'{p}' in vc?", p in vc)

# Let's search for poster-criador-5 in vc
pos = vc.find("poster-criador-5")
if pos != -1:
    print("Found around pos:", vc[pos-100:pos+500])
