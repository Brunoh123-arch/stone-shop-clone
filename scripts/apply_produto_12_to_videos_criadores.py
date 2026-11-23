import json
import re

with open('scripts/creators_produto_12_dataset.json', 'r', encoding='utf-8') as f:
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
  // 1.15 DATASET DA PISCINA SPLASH FUN MOR 2400L (PRODUTO 12) - 32 CRIADORES E VÍDEOS REAIS (CATBOX CLOUD CDN)
  const PISCINA_12_VIDEOS_MAP = {js_array};
  const CREATORS_PISCINA_12 = PISCINA_12_VIDEOS_MAP.map((vInfo, i) => ({{
    name: vInfo.name,
    username: vInfo.username,
    avatar: vInfo.avatar,
    poster: vInfo.poster,
    video: vInfo.video,
    startTime: 0.2,
    likes: 14200 + (i * 410) % 18000,
    commentsCount: 68 + (i * 11) % 145,
    sharesCount: 42 + (i * 8) % 85,
    savesCount: 1150 + (i * 90) % 2100,
    description: vInfo.desc
  }}));
"""

with open('js/videos-criadores.js', 'r', encoding='utf-8') as f:
    vc = f.read()

# Check if already present
if 'PISCINA_12_VIDEOS_MAP' in vc:
    vc = re.sub(r'// 1\.15 DATASET DA PISCINA SPLASH FUN MOR 2400L.*?const CREATORS_PISCINA_12 = .*?\n  \}\)\);', dataset_block.strip(), vc, flags=re.DOTALL)
    print("Substituido PISCINA_12_VIDEOS_MAP existente.")
else:
    target = '  // 2. DATASET AUTOMOTIVO / PNEUS PIRELLI (PRODUTO-101)'
    if target in vc:
        vc = vc.replace(target, dataset_block + '\n\n' + target)
        print("Inserido PISCINA_12_VIDEOS_MAP antes de DATASET AUTOMOTIVO.")
    else:
        print("Target DATASET AUTOMOTIVO nao encontrado!")

# Check initCarousel isPiscina condition
if 'const isPiscina' not in vc:
    vc = vc.replace(
        "const isJBLBoombox = prodId === 4 || pageText.includes('jbl boombox') || (pageText.includes('boombox') && !pageText.includes('aiwa')) || pageText.includes('boombox 3');",
        "const isPiscina = prodId === 12 || pageText.includes('splash fun') || (pageText.includes('piscina') && pageText.includes('mor')) || pageText.includes('piscina inflavel') || pageText.includes('piscina redonda');\n    const isJBLBoombox = prodId === 4 || pageText.includes('jbl boombox') || (pageText.includes('boombox') && !pageText.includes('aiwa')) || pageText.includes('boombox 3');"
    )
    print("Adicionada flag isPiscina.")

if 'if (isPiscina)' not in vc:
    vc = vc.replace(
        "if (isJBLBoombox) {",
        "if (isPiscina) {\n      activeDataset = CREATORS_PISCINA_12;\n      contextType = 'piscina12';\n    } else if (isJBLBoombox) {"
    )
    print("Adicionado branch if (isPiscina) em initCarousel.")

with open('js/videos-criadores.js', 'w', encoding='utf-8') as f:
    f.write(vc)

print("js/videos-criadores.js atualizado com sucesso!")
