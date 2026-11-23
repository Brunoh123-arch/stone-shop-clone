with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

import re
for pid in [101, 102]:
    m = re.search(r'case\s+' + str(pid) + r'\s*:\s*(.*?)(?=case|\bdefault:|$)', vc, re.DOTALL)
    if m:
        print(f"Case {pid}:", m.group(1).strip())
    else:
        print(f"Case {pid} NOT FOUND")
