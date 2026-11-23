# -*- coding: utf-8 -*-
import re

for js_path in ['js/videos-criadores-v3.js', 'js/videos-criadores.js']:
    content = open(js_path, 'r', encoding='utf-8').read()
    
    # Remove linhas que são apenas vírgula com ou sem espaços
    # Ex: "\n  {\n,\n    name:" -> "\n  {\n    name:"
    fixed = re.sub(r'\n\s*,\s*\n', '\n', content)
    
    # Também qualquer caso de vírgula duplicada: ",\s*,"
    fixed = re.sub(r',\s*,', ',', fixed)
    
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(fixed)
    print(f"[+] Limpo {js_path}")
