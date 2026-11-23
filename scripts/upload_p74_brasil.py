# -*- coding: utf-8 -*-
import json, sys, os
sys.path.append(os.path.abspath('scripts'))
from tiktok_catbox_downloader import download_and_upload_to_catbox

videos = [
  {
    "username": "sportfinoo",
    "nickname": "SportFino",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/0373174d8c8ac28c3e0967aa99c9c857~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=e1aaeef9&x-expires=1795366800&x-signature=gDr8AmFk%2FfU6d46937CcldGaNdw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Detalhes da camisa oficial da Seleção Brasileira versão torcedor! Escudo bordado de altíssima qualidade!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/oUIUfDjIIDAemEISQURAfhQqoCLwIVJGKMHHYi/?a=1988&bti=ODszNWYuMDE6&&bt=424&ft=I~da4oKyD12NvWPKslIxRJjSHlBF-UjNSWopiX&mime_type=video_mp4&rc=OGQ5aGY7PDM1aGk0NjplPEBpajt4NnI5cjM4OzMzODczNEBeYF81XzMtXjExYmBfMTY1YSNkaHNmMmRzYDZhLS1kMTFzcw%3D%3D&expire=1795368884&l=20261121013341E101C389C0F1BAEB7D62&ply_type=2&policy=2&signature=a4d550b7254e2288ab3d222645d37301&tk=tt_chain_token&btag=e00090000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o8Xwl0uUJATUDRHGQEfK0jVCozS8QwfeIhCAQM~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=yBbh5u7VGw1sVDGfj%2FxpaOqHHiI%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  },
  {
    "username": "jumedeirosr",
    "nickname": "Juliana Medeiros",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/15abe20ad26603a031b6707a4dad5462~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=bfc1c8bb&x-expires=1795366800&x-signature=Pqii2VxxQv8%2BtIEf5aF8wmR0BPg%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "A nova camisa da Seleção Brasileira! Mostrando cada detalhe do tecido Dri-FIT e do caimento impecável!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/o05aWY2bvNcXbaQOiihPcEIr8ynnaXBBTAEOA/?a=1988&bti=ODszNWYuMDE6&&bt=1248&ft=-Csk_mrMPD12N59ruY-UxfK2KY6e3wv25bcAp&mime_type=video_mp4&rc=ZjNkaDdkMzk8NDQ5OzppM0BpM208PHY5cnNzOjMzODczNEAyNF4uYjYwNjAxXmAuYjQtYSM0YnI0MmQ0bTNhLS1kMWBzcw%3D%3D&expire=1795369014&l=202611210134004ED35D890813D1F8FDA8&ply_type=2&policy=2&signature=0d5f263418f4c8e33bce8219ee3358e8&tk=tt_chain_token&btag=e00090000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oMzAjCEZPIDAR0gYzjAeFNNBf5cADpIEnOEzvI~tplv-tiktokx-dmt-logom:tos-alisg-i-0068/ogAdnsHlBIDPFN75AYiAOEI40Bfj0AAEixw8C5.image?dr=14573&x-expires=1795366800&x-signature=tgcMEgwen2AhO%2FHpRcTx6hTAEYY%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  },
  {
    "username": "eitiporai",
    "nickname": "Eiti por aí",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/097ad4b466543d26fb6680f2c85e3727~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=781c27ba&x-expires=1795366800&x-signature=MA%2FNlFdOP0l5PqffMPb%2FZSaaWI8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Unboxing e review sincero da camisa amarela do Brasil! O tecido é muito leve, respirável e confortável no corpo!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/oYGCEfNhYwcIBsSEQ54iAgAqvA8iIBWq0G0IO3/?a=1988&bti=ODszNWYuMDE6&&bt=1502&ft=-Csk_mrMPD12NY9ruY-Ux~t2VY6e3wv25IcAp&mime_type=video_mp4&rc=Ozk1Zmg0ZDZpOThmNTc5ZUBpMzk4ZHI5cmp1OjMzODczNEBeYGE0LjY2NjExYS4wL19hYSMvZGsxMmRjaGRhLS1kMTFzcw%3D%3D&expire=1795368961&l=202611210134224F091F1E8BBDDC000E60&ply_type=2&policy=2&signature=5b4971280e3100f60239f4b86228adf9&tk=tt_chain_token&btag=e00090000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/owhI68iDkALBthK7CE3duGwEBfA6iAAWDBA0NI~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=DhWAM4rhaarLZLierqbH6YsasBE%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  },
  {
    "username": "ritmodascamisas",
    "nickname": "Matheus Silva",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/c9359eff55edd496645c3a0c2b972481~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=5fe2b60b&x-expires=1795366800&x-signature=1iCW0oFCJ39XeShB%2Fz%2BvuLuUc1Q%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Nova camisa da Seleção Canarinho! As aplicações cheias de textura e o tecido tecnológico deixam a camisa surreal!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/oQGDcnGqL52NlGVeRjL8ACvIWifQI4geATR8BI/?a=1988&bti=ODszNWYuMDE6&&bt=1371&ft=-Csk_mrMPD12N89ruY-UxdN5PY6e3wv25xcAp&mime_type=video_mp4&rc=NWQ2NDtmZ2UzMzs0ZzNnZEBpM3V5dXI5cjQ7OjMzODczNEA2MjMwNGFiXjYxYl40YjFgYSNjY21mMmRrazJhLS1kMWBzcw%3D%3D&expire=1795369051&l=202611210134403A9426AAF97BA8F4A459&ply_type=2&policy=2&signature=b73a976da02129a3e702acddb1215be4&tk=tt_chain_token&btag=e00090000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ocLc9PAEEMiyAwKBKAMjKQinBpAYDqRADIaMm~tplv-tiktokx-dmt-logom:tos-alisg-i-0068/ociIzWIK2D5FA5BrBwfpijAOAZELKAORAU50jC.image?dr=14573&x-expires=1795366800&x-signature=jW8BPVaMGRW%2FCJJGuNFHDVAJDuI%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  },
  {
    "username": "juliastofel_",
    "nickname": "Júlia Stofel",
    "avatar": "https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/632db09b3d96fb6e4c459b21f5ff8e09~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=d4e723cf&x-expires=1795366800&x-signature=aTstWpbkhFR3cwLYkUqh0%2FgSAFw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3",
    "desc": "Recebidos da camisa da Seleção Brasileira! Linda demais, tecido super macio e caimento perfeito!",
    "playAddr": "https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/o81cx7licYVVaB49mCQLKZ2OIAcxCEEVABPil/?a=1988&bti=ODszNWYuMDE6&&bt=1279&ft=-Csk_mrMPD12NkEruY-UxfK2KY6e3wv25bcAp&mime_type=video_mp4&rc=PDloOzw3Mzc8NTc3NTtkOEBpanM0ams5cjg8OjMzODczNEAxL180LmI2NmMxXl4yNTViYSMybGtsMmQ0Xy5hLS1kMTFzcw%3D%3D&expire=1795369003&l=20261121013508F5C5DE2A0259B9FF471F&ply_type=2&policy=2&signature=4e1ee9667493ee55249a66a65e95598f&tk=tt_chain_token&btag=e00090000",
    "cover": "https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ooCIcACERIIAkUtffDEAIoDpAksFEBLpCg9Zlw~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=rxpvxeRhf6LfsypmPv11UTClNEo%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2"
  }
]

results = []
for i, v in enumerate(videos):
    print(f"[*] Processando video {i+1}/5 (@{v['username']})...")
    catbox = download_and_upload_to_catbox(v['playAddr'], f"brasil74_{v['username']}.mp4")
    print(f"    [+] Catbox: {catbox}")
    v['catbox'] = catbox
    results.append(v)

with open('scripts/p74_videos_result.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n[+] SUCESSO TOTAL! 5 vídeos de Camisa Seleção Brasil (P74) no Catbox!")
