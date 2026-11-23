# -*- coding: utf-8 -*-
import json
import re

with open('scripts/data/lote1_ready.json', 'r', encoding='utf-8') as f:
    lote1 = json.load(f)

ARRAY_NAMES = {
    "57": "JOOG_ONE_57_VIDEOS_MAP",
    "58": "ECHODOT_58_VIDEOS_MAP",
    "60": "SABALA_60_VIDEOS_MAP",
    "61": "JOOG_BREAK_61_VIDEOS_MAP",
    "73": "WAAW_HYPERBOOM_73_VIDEOS_MAP",
    "85": "JOOG_X2_85_VIDEOS_MAP"
}

def make_js_array(items):
    lines = ["[\n"]
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

for js_file in ['js/videos-criadores.js', 'js/videos-criadores-v3.js']:
    with open(js_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for pid, arr_name in ARRAY_NAMES.items():
        if pid in lote1:
            js_arr = make_js_array(lote1[pid])
            pattern = rf'const\s+{arr_name}\s*=\s*\[.*?\];'
            if re.search(pattern, content, flags=re.DOTALL):
                content = re.sub(pattern, f'const {arr_name} = {js_arr};', content, flags=re.DOTALL)
                print(f"  [+] {arr_name} atualizado em {js_file}!")
            else:
                print(f"  [-] {arr_name} nao bateu pattern em {js_file}!")
                
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(content)

print("[+] Lote 1 de audio integrado com sucesso!")
