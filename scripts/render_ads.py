import subprocess, os

font_path = os.path.abspath('fonts/SF-Pro-Display-Bold.otf').replace('\\', '/').replace(':', '\\:')
vf = (
    'scale=720:1280,'
    'drawbox=y=60:color=black@0.65:width=iw:height=140:t=fill,'
    f"drawtext=fontfile='{font_path}':text='EFEITO LIPO IMEDIATO':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=80,"
    f"drawtext=fontfile='{font_path}':text='CINTA ALTA COMPRESSAO INVISIVEL':fontcolor=0x25F4EE:fontsize=24:x=(w-text_w)/2:y=130,"
    'drawbox=y=ih-220:color=black@0.75:width=iw:height=160:t=fill,'
    f"drawtext=fontfile='{font_path}':text='PROMO 11.11 TIKTOK SHOP':fontcolor=0xFE2C55:fontsize=26:x=(w-text_w)/2:y=ih-195,"
    f"drawtext=fontfile='{font_path}':text='DE R$ 119,90 POR APENAS R$ 29,90':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=ih-155,"
    f"drawtext=fontfile='{font_path}':text='FRETE GRATIS PARA TODO BRASIL':fontcolor=0x25D366:fontsize=22:x=(w-text_w)/2:y=ih-110"
)
cmd = [
    'ffmpeg', '-y', '-i', 'videosprodutos/video-produto-106.mp4',
    '-vf', vf,
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23',
    '-c:a', 'aac',
    '-movflags', '+faststart',
    'criativos_tiktok_ads/criativo_ads_body_modelador.mp4'
]
res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print('Error:', res.stderr[-500:])
else:
    print('Sucesso!')
