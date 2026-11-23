# -*- coding: utf-8 -*-
import json
import re

with open('scripts/data/zeros_ready.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    vc = f.read()

def make_js_array(items):
    lines = []
    lines.append("[\n")
    for it in items:
        lines.append("    {\n")
        lines.append(f"      name: {json.dumps(it['name'], ensure_ascii=False)},\n")
        lines.append(f"      username: {json.dumps(it['username'], ensure_ascii=False)},\n")
        lines.append(f"      avatar: {json.dumps(it['avatar'], ensure_ascii=False)},\n")
        lines.append(f"      poster: (isPagesDir ? \"../\" : \"\") + {json.dumps(it['poster'], ensure_ascii=False)},\n")
        lines.append(f"      video: {json.dumps(it['video'], ensure_ascii=False)},\n")
        lines.append(f"      startTime: 0.2,\n")
        lines.append(f"      desc: {json.dumps(it['desc'], ensure_ascii=False)}\n")
        lines.append("    },\n")
    lines.append("  ]")
    return "".join(lines)

# Substitui AIWA_7_VIDEOS_MAP
aiwa_js = make_js_array(data["7"])
vc = re.sub(r'const AIWA_7_VIDEOS_MAP = \[.*?\];', f'const AIWA_7_VIDEOS_MAP = {aiwa_js};', vc, flags=re.DOTALL)

# Substitui JBL_BOOMBOX4_35_VIDEOS_MAP
jbl_js = make_js_array(data["35"])
vc = re.sub(r'const JBL_BOOMBOX4_35_VIDEOS_MAP = \[.*?\];', f'const JBL_BOOMBOX4_35_VIDEOS_MAP = {jbl_js};', vc, flags=re.DOTALL)

# Substitui APARELHO_76_VIDEOS_MAP
aparelho_js = make_js_array(data["76"])
vc = re.sub(r'const APARELHO_76_VIDEOS_MAP = \[.*?\];', f'const APARELHO_76_VIDEOS_MAP = {aparelho_js};', vc, flags=re.DOTALL)

# Substitui HISENSE_82_VIDEOS_MAP
hisense_js = make_js_array(data["82"])
vc = re.sub(r'const HISENSE_82_VIDEOS_MAP = \[.*?\];', f'const HISENSE_82_VIDEOS_MAP = {hisense_js};', vc, flags=re.DOTALL)

# Substitui COPOS_98_VIDEOS_MAP
copos_js = make_js_array(data["98"])
vc = re.sub(r'const COPOS_98_VIDEOS_MAP = \[.*?\];', f'const COPOS_98_VIDEOS_MAP = {copos_js};', vc, flags=re.DOTALL)

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(vc)

print("[+] js/videos-criadores.js atualizado com sucesso!")
