import re

replacements = {
    17: ("https://files.catbox.moe/m3uloo.mp4", "https://files.catbox.moe/2t0aot.mp4"),
    39: ("https://files.catbox.moe/3rtr42.mp4", "https://files.catbox.moe/e7z9vc.mp4"),
    45: ("https://files.catbox.moe/3rtr42.mp4", "https://files.catbox.moe/bjcwqr.mp4"),
    47: ("https://files.catbox.moe/3rtr42.mp4", "https://files.catbox.moe/6ubsxb.mp4"),
    49: ("https://files.catbox.moe/3rtr42.mp4", "https://files.catbox.moe/6ubsxb.mp4"),
    50: ("https://files.catbox.moe/3rtr42.mp4", "https://files.catbox.moe/n5jecm.mp4"),
    68: ("https://files.catbox.moe/3rtr42.mp4", "https://files.catbox.moe/sdcjn0.mp4"),
}

for pid, (old_v, new_v) in replacements.items():
    filepath = f"pages/produto-{pid}.html"
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        
        if old_v in content:
            new_content = content.replace(old_v, new_v)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"Sucesso: P{pid} atualizado ({old_v} -> {new_v})")
        else:
            print(f"Aviso: {old_v} não encontrado em P{pid}")
    except Exception as e:
        print(f"Erro em P{pid}: {e}")
