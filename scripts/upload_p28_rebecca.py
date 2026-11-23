# -*- coding: utf-8 -*-
import json, sys, os
sys.path.append(os.path.abspath('scripts'))
from tiktok_catbox_downloader import download_and_upload_to_catbox

videos = [
  {
    "username": "danydantas56",
    "nickname": "Daniela Martins",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/808c31a4f5970f7d83f0a3c9e224bfcd~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=2d0f590f&x-expires=1795366800&x-signature=3GWczwZ%2Fc5jQRJsdmW8y8duznEo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Kit Rebecca Bonbon completo com mochila reforçada, lancheira térmica e estojo box! Apaixonada!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/ogWh7qNLfABnQQDLEJnwyiEgyFRZO80CBUEIBf/?a=1988&bti=ODszNWYuMDE6&&bt=1763&ft=-Csk_mrMPD12NEhruY-Ux~t2VY6e3wv25IcAp&mime_type=video_mp4&rc=aDNoZmc3ZGVpNTlkN2Q8M0BpamU3bGo5cjVoZTMzODczNEBiY18yXjRhNmIxYDNeYzQ0YSNjLjBsMmRzbWxhLS1kMTFzcw%3D%3D&expire=1795367915&l=202611210118250B4AA0EA2D93F1D08831&ply_type=2&policy=2&signature=f0a5fbc9e587cb724d447aa914d32375&tk=tt_chain_token&btag=e000b0000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/osQ7JDRfqjBpWWywBhFEgyDLE8ARNLrIIifBUO~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=z66mbNyGspOFkUOSVhbhTM7Ushc%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  },
  {
    "username": "evi_ribeiro1",
    "nickname": "Evilyn Ribeiro",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/2d3eb5487cc8efae10a1c0004661c8f4~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=9ee4ca70&x-expires=1795366800&x-signature=z6r7VYIqVvBo4%2BiYaC%2FvoDY%2B6%2F4%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Abrindo a mochila Rebecca Bonbon da minha filha! Material impecável, detalhes dourados e muito espaço!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o81uoFDHjIDgCIvT2fEQQTCAVgJAjrxBfSfEG7/?a=1988&bti=ODszNWYuMDE6&&bt=2645&ft=-Csk_mrMPD12NWhruY-Ux2H2NY6e3wv25pcAp&mime_type=video_mp4&rc=aDlnNzs3aTZkOzs4N2hnNUBpMzY1bG85cm5vODMzODczNEA1MTQyMV80NWExMzZjYjUzYSMuNi1vMmRzNnNhLS1kMTFzcw%3D%3D&expire=1795368002&l=2026112101184646E57571302BF6DC8FBC&ply_type=2&policy=2&signature=e3f87b0faa549c70f3fa63b0a386a9f2&tk=tt_chain_token&btag=e00090000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ogSeBFvIAyGHAgBQUJLlAqHGAsQWAGWeeqfRo4~tplv-tiktokx-dmt-logom:tos-alisg-i-0068/oMgSfzaAHV0Gz7ggAAAN7fedizMLeqILAQ4g8f.image?dr=14573&x-expires=1795366800&x-signature=OrNifCyz063tEGLW%2BeNa60yejz4%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  },
  {
    "username": "mae_madrasta",
    "nickname": "Mãe e Madrasta",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/26b28a5bec8a8c312250e738380e1695~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=6d6a8511&x-expires=1795366800&x-signature=G7T8Nzz9DB6ECJMz3ZolQv2rg%2Bo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Chegou a mochila Rebecca Bonbon original! Qualidade surreal, chaveiro lindo do cachorrinho e super resistente!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/ooDMeErgeIc5nFLIqodft6rLM77ACjAaySQNAD/?a=1988&bti=ODszNWYuMDE6&&bt=1634&ft=-Csk_mrMPD12NjYruY-UxgOFLY6e3wv25ycAp&mime_type=video_mp4&rc=ZTZnNDY6O2Q1OTU6OWZkNEBpM29va285cjw5ODMzODczNEAuMS0yM2MzNS0xYi4vNDBiYSMtb2dqMmRzc21hLS1kMTFzcw%3D%3D&expire=1795368100&l=202611210119109F8878BD00D47DD8EBFB&ply_type=2&policy=2&signature=f4f0bd8e05796319faa15c901104e28c&tk=tt_chain_token&btag=e00090000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o4AVDITSoEnGyjeQeAkfCF45bDSUaNQrqU76MA~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=sTij3y4nzH1MiNgDUaaAhwZQLgM%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  },
  {
    "username": "daysesantos777",
    "nickname": "Dayse Santos",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/7323233900525436934~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=185c420d&x-expires=1795366800&x-signature=Mm0%2FmUUd75CdKH5Tdi3eoiux6jY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Unboxing da minha mochila da Rebecca Bonbon! Perfeita em todos os ângulos, super confortável nas costas!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/osp07BajVYARZiRQkijbkHXI0E5YPBmk3Av3E/?a=1988&bti=ODszNWYuMDE6&&bt=1361&ft=-Csk_mrMPD12NfYruY-UxWeFNY6e3wv25AcAp&mime_type=video_mp4&rc=OjM1aDxoNTo5ZzNmZmY1Z0BpanVrZW45cmt0OzMzODczNEAwYjZeXy1iNi4xXzMuMTYtYSM1YnBmMmQ0M3BhLS1kMTFzcw%3D%3D&expire=1795368119&l=2026112101192938A9020B1694F3F82FB8&ply_type=2&policy=2&signature=c1dfb986a815d25843435afcd87a1717&tk=tt_chain_token&btag=e00090000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ocIOQoue0q2IIBIjJScUSCLaiseGfJADAuSFzC~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=YTPpQHy%2BclP9eBw2f5GnBAR30c0%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  },
  {
    "username": "larihdailyy_",
    "nickname": "Larissa Daily",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/af9046555e71170b8fcfc4e95abaff83~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=f5b21b95&x-expires=1795366800&x-signature=%2FZxne7944nr4u7HC7fLEWaDTGyg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Unboxing da minha mochila escolar Rebecca Bonbon! Cabe tudo e mais um pouco, tecido impermeável top!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/useast2a/tos-useast2a-pve-0068/oAfCNkNRegsGoCuCgHSngeImLIAjYAHCukTSTg/?a=1988&bti=ODszNWYuMDE6&&bt=1478&ft=-Csk_mrMPD12NWYruY-Uxl4FPY6e3wv25HcAp&mime_type=video_mp4&rc=aWQ4ZTQ7Nzw1OWQ1OWU0OUBpanVoZGo5cjNqdDMzNzczM0AtL2FfMWI2Ni8xYzFhYS4xYSMxNi5mMmRzNjRgLS1kMTZzcw%3D%3D&expire=1795368016&l=202611210119509444D7754A1581D1FDCE&ply_type=2&policy=2&signature=f6b92922f8540ed1207e2793e8df7be0&tk=tt_chain_token&btag=e000b8000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-maliva-p-0068/4e0c57c5ad994984b959952ecb268a76_1720649014~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=kJI4CuLNMsXHh%2BXtPNt6gCWwSpk%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  }
]

results = []
for i, v in enumerate(videos):
    print(f"[*] Processando video {i+1}/5 (@{v['username']})...")
    catbox = download_and_upload_to_catbox(v['playAddr'], f"rebecca_bonbon_{v['username']}.mp4")
    print(f"    [+] Catbox: {catbox}")
    v['catbox'] = catbox
    results.append(v)

with open('scripts/p28_videos_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n[+] SUCESSO TOTAL! 5 vídeos de Rebecca Bonbon (P28) no Catbox!")
