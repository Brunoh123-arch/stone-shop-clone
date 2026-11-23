with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

import re

zeros = [
    'AIWA_7_VIDEOS_MAP',
    'JBL_BOOMBOX4_35_VIDEOS_MAP',
    'APARELHO_76_VIDEOS_MAP',
    'CREATORS_HISENSE_82',
    'COPOS_98_VIDEOS_MAP'
]

for z in zeros:
    pos = vc.find(f"const {z}")
    if pos != -1:
        print(f"=== {z} at {pos} ===")
        print(vc[pos:pos+400])
        print("-" * 50)
    else:
        print(f"=== {z} NOT FOUND ===")
