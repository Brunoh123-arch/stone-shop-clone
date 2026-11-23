import json
import re

with open('scripts/creators_produto_4_dataset.json', 'r', encoding='utf-8') as f:
    dataset = json.load(f)

# Build JS array string
lines = []
for it in dataset:
    clean_desc = it['title'].replace('"', '\\"').replace('\n', ' ')
    lines.append(f"""    {{
      name: "{it['name']}",
      username: "{it['username']}",
      avatar: "{it['avatar']}",
      poster: "{it['poster']}",
      video: "{it['video']}",
      startTime: 0.2,
      desc: "{clean_desc}"
    }}""")

js_array = "[\n" + ",\n".join(lines) + "\n  ]"

dataset_block = f"""
  // 1.14 DATASET DA CAIXA DE SOM JBL BOOMBOX 3 (PRODUTO 4) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const JBL_4_VIDEOS_MAP = {js_array};
  const CREATORS_JBL_4 = JBL_4_VIDEOS_MAP.map((vInfo, i) => ({{
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 13800 + (i * 420) % 16500,
    commentsCount: 78 + (i * 13) % 150,
    sharesCount: 45 + (i * 9) % 90,
    savesCount: 1250 + (i * 110) % 2100,
    description: vInfo.desc
  }}));
"""

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    vc = f.read()

# 1. Insert or replace dataset definition
if 'JBL_4_VIDEOS_MAP' in vc:
    vc = re.sub(r'// 1\.14 DATASET DA CAIXA DE SOM JBL BOOMBOX 3.*?const CREATORS_JBL_4 = .*?\n  \}\)\);', dataset_block.strip(), vc, flags=re.DOTALL)
    print("Substituido JBL_4_VIDEOS_MAP existente.")
else:
    target = '  // 2. DATASET AUTOMOTIVO / PNEUS PIRELLI (PRODUTO-101)'
    if target in vc:
        vc = vc.replace(target, dataset_block + '\n\n' + target)
        print("Inserido JBL_4_VIDEOS_MAP antes de DATASET AUTOMOTIVO.")
    else:
        print("ERRO: Target DATASET AUTOMOTIVO nao encontrado!")

# 2. Check isJBLBoombox flag
if 'const isJBLBoombox' not in vc:
    old_aiwa_str = "const isAiwa = prodId === 7 || pageText.includes('aiwa') || pageText.includes('boombox') || pageText.includes('aws-bbs');"
    new_str = "const isJBLBoombox = prodId === 4 || pageText.includes('jbl boombox') || (pageText.includes('boombox') && !pageText.includes('aiwa')) || pageText.includes('boombox 3');\n    const isAiwa = (prodId === 7 || pageText.includes('aiwa') || pageText.includes('aws-bbs')) && !isJBLBoombox;"
    if old_aiwa_str in vc:
        vc = vc.replace(old_aiwa_str, new_str)
        print("Adicionada flag isJBLBoombox e ajustada flag isAiwa.")
    else:
        print("WARN: old_aiwa_str nao encontrado diretamente.")

# 3. Check initCarousel branching
if 'if (isJBLBoombox)' not in vc:
    old_branch = "if (isAirFryer) {"
    new_branch = "if (isJBLBoombox) {\n      activeDataset = CREATORS_JBL_4;\n      contextType = 'jbl4';\n    } else if (isAirFryer) {"
    if old_branch in vc:
        vc = vc.replace(old_branch, new_branch, 1)
        print("Adicionado branch if (isJBLBoombox) no initCarousel.")
    else:
        print("WARN: old_branch nao encontrado.")

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(vc)

print("js/videos-criadores.js atualizado com sucesso!")
