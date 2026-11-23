with open('js/videos-criadores.js', encoding='utf-8') as f:
    text = f.read()

import re

for varname in ['FORNO_HQ_115_VIDEOS_MAP', 'CHINELO_VIDEOS_MAP', 'BODY_106_VIDEOS_MAP', 'BIKE_GT_20_VIDEOS_MAP', 'AIRFRYER_5_VIDEOS_MAP']:
    idx = text.find(varname)
    if idx != -1:
        # Procurar onde ele é usado além da definição
        second_idx = text.find(varname, idx + len(varname) + 10)
        print(f"=== {varname} ===")
        print(f"  Definição em: {idx}")
        if second_idx != -1:
            print(f"  Segundo uso em {second_idx}:")
            print("   ", text[second_idx-50:second_idx+150])
        else:
            print("  Não tem segundo uso direto!")
