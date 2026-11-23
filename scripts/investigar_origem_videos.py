import os
import re

videos = [
    'u5toyv.mp4', '2t30kf.mp4', 'm3uloo.mp4', '0hhasi.mp4',
    'n5jecm.mp4', 'bjcwqr.mp4', 'e7z9vc.mp4', 's6vnyh.mp4',
    'sdcjn0.mp4', '1ig8lo.mp4', 'k3u5ff.mp4', 's313zy.mp4',
    'a8zjrb.mp4', 'perlvk.mp4', 'h5x3n6.mp4', '18m1t8.mp4'
]

# Checar em scripts ou histórico ou nos próprios HTMLs por menções aos nomes dos arquivos
for v in videos:
    print(f'=== Video {v} ===')
    # Buscar nos scripts onde esse vídeo foi baixado ou criado
    for sfile in os.listdir('scripts'):
        if sfile.endswith('.py') or sfile.endswith('.json') or sfile.endswith('.md'):
            try:
                content = open(os.path.join('scripts', sfile), encoding='utf-8', errors='ignore').read()
                if v in content:
                    print(f'  Found in script: {sfile}')
            except:
                pass
