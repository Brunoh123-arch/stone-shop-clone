with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

import re
print("AIWA mentions in videos-criadores.js:")
for m in re.finditer(r'.{0,40}aiwa.{0,60}', vc, re.IGNORECASE):
    print(m.group(0).strip())

pos8 = vc.find("AIWA_PARTYBOX_8")
if pos8 != -1:
    print("\nAIWA 8 dataset:")
    print(vc[pos8:pos8+800])
