import json
import re

with open('scripts/creators_produto_5_dataset.json', 'r', encoding='utf-8') as f:
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
  // 1.12 DATASET DA FRITADEIRA AIR FRYER ELGIN 5L (PRODUTO 5) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const AIRFRYER_5_VIDEOS_MAP = {js_array};
  const CREATORS_AIRFRYER_5 = AIRFRYER_5_VIDEOS_MAP.map((vInfo, i) => ({{
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 12500 + (i * 390) % 15000,
    commentsCount: 65 + (i * 11) % 130,
    sharesCount: 38 + (i * 8) % 70,
    savesCount: 1100 + (i * 95) % 1500,
    description: vInfo.desc
  }}));
"""

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    vc = f.read()

# Check if already present
if 'AIRFRYER_5_VIDEOS_MAP' in vc:
    vc = re.sub(r'// 1\.12 DATASET DA FRITADEIRA AIR FRYER ELGIN 5L.*?const CREATORS_AIRFRYER_5 = .*?\n  \}\)\);', dataset_block.strip(), vc, flags=re.DOTALL)
    print("Substituido AIRFRYER_5_VIDEOS_MAP existente.")
else:
    target = '  // 2. DATASET AUTOMOTIVO / PNEUS PIRELLI (PRODUTO-101)'
    if target in vc:
        vc = vc.replace(target, dataset_block + '\n\n' + target)
        print("Inserido AIRFRYER_5_VIDEOS_MAP antes de DATASET AUTOMOTIVO.")
    else:
        print("Target DATASET AUTOMOTIVO nao encontrado!")

# Check initCarousel isAirFryer condition
if 'const isAirFryer' not in vc:
    vc = vc.replace(
        "const isAiwa = prodId === 7 || pageText.includes('aiwa') || pageText.includes('boombox') || pageText.includes('aws-bbs');",
        "const isAiwa = prodId === 7 || pageText.includes('aiwa') || pageText.includes('boombox') || pageText.includes('aws-bbs');\n    const isAirFryer = prodId === 5 || pageText.includes('visio fry') || pageText.includes('fritadeira') || pageText.includes('elgin 5l');"
    )
    print("Adicionada flag isAirFryer.")

if 'if (isAirFryer)' not in vc:
    vc = vc.replace(
        "if (isProjetorNatal) {",
        "if (isAirFryer) {\n      activeDataset = CREATORS_AIRFRYER_5;\n      contextType = 'airfryer5';\n    } else if (isProjetorNatal) {"
    )
    print("Adicionado branch if (isAirFryer) em initCarousel.")

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(vc)

print("js/videos-criadores.js atualizado com sucesso!")
