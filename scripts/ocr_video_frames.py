import os
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

videos = [
    (4, "Caixa De Som Boombox 3", "https://files.catbox.moe/s313zy.mp4"),
    (5, "Fritadeira Elétrica Visio Fry 5L", "https://files.catbox.moe/a8zjrb.mp4"),
    (6, "Bicicleta Ergométrica Fitness", "https://files.catbox.moe/perlvk.mp4"),
    (7, "Caixa de Som AIWA Boombox Plus", "https://files.catbox.moe/1ig8lo.mp4"),
    (8, "Caixa de Som Amplificada AIWA PartyBox", "https://files.catbox.moe/k3u5ff.mp4"),
    (9, "Ar Condicionado Portátil HQ 8500", "https://files.catbox.moe/mr2lij.mp4"),
    (12, "Piscina Splash Fun Redonda 2400L", "https://files.catbox.moe/h5x3n6.mp4"),
    (13, "Piscina Inflável Redonda Mor 1000L", "https://files.catbox.moe/h5x3n6.mp4"),
    (14, "Churrasqueira Assador Arke 5 Espetos", "https://files.catbox.moe/ibv6vn.mp4"),
    (15, "Churrasqueira Portátil Biscuitt", "https://files.catbox.moe/qfampv.mp4"),
    (16, "Churrasqueira Modelo Rodeio Mor", "https://files.catbox.moe/abwltl.mp4"),
    (17, "Kit 6 Cadeira de Praia Mor", "https://files.catbox.moe/18m1t8.mp4"),
    (18, "Kit Praia 4 Cadeiras Sortidas", "https://files.catbox.moe/18m1t8.mp4"),
    (19, "Tablet Vision TAB 7 Stitch", "https://files.catbox.moe/8octvc.mp4"),
    (20, "Bicicleta Aro 29 GT Sprint MX7", "https://files.catbox.moe/8oqszr.mp4"),
    (21, "Bola De Futebol Penalty Bravo X", "https://files.catbox.moe/rs5lzn.mp4"),
    (22, "Colchão Inflável Casal Bestway", "https://files.catbox.moe/ekswrf.mp4"),
    (23, "Conjunto 24 Potes Herméticos", "https://files.catbox.moe/08kgk9.mp4"),
    (24, "Triciclo Infantil 4 em 1", "https://files.catbox.moe/3g9fcx.mp4"),
    (25, "Bicicleta Aro 20 Bmx GottBikes", "https://files.catbox.moe/ncrzdr.mp4"),
]

print("=== OCR ON DESCRIPTION VIDEO FRAMES ===")
for pid, title, url in videos:
    frame_path = f"scripts/temp_video_checks/frame_p{pid:02d}.jpg"
    if os.path.exists(frame_path):
        res, _ = engine(frame_path)
        ocr_text = " | ".join([r[1] for r in res]) if res else "[NO TEXT / PURE SCENE]"
        print(f"P{pid:02d} [{title}]: {ocr_text[:120]}")
    else:
        print(f"P{pid:02d} [{title}]: FRAME MISSING")
