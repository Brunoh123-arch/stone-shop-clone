with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

import re
pos1 = vc.find("PNEU_VIDEOS =")
print("PNEU_VIDEOS:", vc[pos1:pos1+500])

pos2 = vc.find("SCOOTER_CREATORS_INFO =")
print("SCOOTER_CREATORS_INFO:", vc[pos2:pos2+500])
