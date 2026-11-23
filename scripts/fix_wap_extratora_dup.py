# -*- coding: utf-8 -*-
import re

orig_wap = """const WAP_EXTRATORA_78_VIDEOS_MAP = [
{ name: "Carla Dicas de Limpeza", username: "carladicasdelimpeza", avatar: "../img/reviews-avatars/tiktok_real/tt_avatar_62.jpg", poster: "../videosprodutos/posters/video-produto-78.jpg", video: "https://files.catbox.moe/6ubsxb.mp4", desc: "A WAP Spot Cleaner tirou mancha antiga de café do sofá em 2 minutos! A água sai preta de tanta sujeira que puxa! 🧼✨ #wap #extratora #spotcleaner" }
];"""

for fname in ['js/videos-criadores.js', 'js/videos-criadores-v3.js']:
    content = open(fname, 'r', encoding='utf-8').read()
    pat = r'const\s+WAP_EXTRATORA_78_VIDEOS_MAP\s*=\s*\[[\s\S]*?\];'
    content = re.sub(pat, orig_wap, content, count=1)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[+] Restaurado WAP_EXTRATORA_78_VIDEOS_MAP em {fname}")
