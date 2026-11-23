with open("js/videos-criadores.js", "r", encoding="utf-8") as f:
    vc = f.read()

import re
zero_names = [
    'AIWA_7', 'AR_HQ_9', 'PISCINA_PIXLAR_13', 'CHURRASQUEIRA_ARKE_14',
    'CHURRASQUEIRA_BISCUITT_15', 'JBL_BOOMBOX4_35', 'APARELHO_76', 'HISENSE_82', 'COPOS_98'
]

for name in zero_names:
    print(f"=== {name} ===")
    matches = re.findall(r'const\s+([A-Z0-9_]*' + name + r'[A-Z0-9_]*)\s*=\s*(.*?);', vc, re.DOTALL)
    for varname, body in matches:
        vids = re.findall(r'https?://[^\s"\'<>]+\.mp4', body)
        print(f"  {varname}: {len(vids)} mp4s, body_preview={body[:80].strip()}")
