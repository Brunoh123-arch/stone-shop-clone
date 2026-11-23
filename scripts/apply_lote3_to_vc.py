# -*- coding: utf-8 -*-
"""
Aplica o Lote 3 de Tech & Casa aos arquivos js/videos-criadores.js e js/videos-criadores-v3.js.
Preserva o vídeo 1 existente e adiciona 3 novos vídeos de criadores reais, totalizando 4 vídeos cada.
"""
import json
import re
import os

ARRAY_NAMES = {
    "52": "PAD11_52_VIDEOS_MAP",
    "53": "STARLINK_53_VIDEOS_MAP",
    "55": "SWITCH_55_VIDEOS_MAP",
    "59": "STARLINK_59_VIDEOS_MAP",
    "63": "REDMI_WATCH_63_VIDEOS_MAP",
    "65": "SOFA_SENSES_65_VIDEOS_MAP",
    "78": "SPOTCLEANER_78_VIDEOS_MAP",
    "116": "SMART_TV_116_VIDEOS_MAP"
}

def make_js_array_items(items):
    lines = []
    for it in items:
        lines.append("  {\n")
        lines.append(f"    name: {json.dumps(it['name'], ensure_ascii=False)},\n")
        lines.append(f"    username: {json.dumps(it['username'], ensure_ascii=False)},\n")
        lines.append(f"    avatar: {json.dumps(it['avatar'], ensure_ascii=False)},\n")
        lines.append(f"    poster: (typeof isPagesDir !== 'undefined' && isPagesDir ? '../' : '') + {json.dumps(it['poster'], ensure_ascii=False)},\n")
        lines.append(f"    video: {json.dumps(it['video'], ensure_ascii=False)},\n")
        lines.append(f"    startTime: {it.get('startTime', 0.2)},\n")
        lines.append(f"    desc: {json.dumps(it['desc'], ensure_ascii=False)}\n")
        lines.append("  }")
    return lines

def run_apply():
    ready_file = 'scripts/data/lote3_ready.json'
    if not os.path.exists(ready_file):
        print(f"[-] {ready_file} ainda nao existe!")
        return False
        
    with open(ready_file, 'r', encoding='utf-8') as f:
        lote3 = json.load(f)

    for js_file in ['js/videos-criadores.js', 'js/videos-criadores-v3.js']:
        with open(js_file, 'r', encoding='utf-8') as f:
            content = f.read()

        for pid_str, arr_name in ARRAY_NAMES.items():
            new_items = lote3.get(pid_str, [])
            if not new_items:
                continue

            pattern = r'(const\s+' + arr_name + r'\s*=\s*\[)([\s\S]*?)(\];)'
            m = re.search(pattern, content)
            if not m:
                print(f"[-] Nao encontrou {arr_name} em {js_file}")
                continue

            existing_body = m.group(2).strip()
            if existing_body.endswith(','):
                existing_body = existing_body[:-1].strip()

            new_js_items = make_js_array_items(new_items)
            combined_items_str = existing_body + ",\n" + ",\n".join(new_js_items)

            replacement = r'\g<1>\n' + combined_items_str + r'\n\g<3>'
            content = re.sub(pattern, replacement, content, count=1)
            print(f"[+] {js_file} -> {arr_name}: adicionados {len(new_items)} novos criadores!")

        # Também atualiza WAP_EXTRATORA_78_VIDEOS_MAP se existir
        if "78" in lote3:
            wap_pattern = r'(const\s+WAP_EXTRATORA_78_VIDEOS_MAP\s*=\s*\[)([\s\S]*?)(\];)'
            m_wap = re.search(wap_pattern, content)
            if m_wap:
                existing_body = m_wap.group(2).strip()
                if existing_body.endswith(','):
                    existing_body = existing_body[:-1].strip()
                new_js_items = make_js_array_items(lote3["78"])
                combined = existing_body + ",\n" + ",\n".join(new_js_items)
                content = re.sub(wap_pattern, r'\g<1>\n' + combined + r'\n\g<3>', content, count=1)
                print(f"[+] {js_file} -> WAP_EXTRATORA_78_VIDEOS_MAP atualizado!")

        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(content)

    print("\n[+] Lote 3 aplicado com sucesso aos arquivos JS!")
    return True

if __name__ == '__main__':
    run_apply()
