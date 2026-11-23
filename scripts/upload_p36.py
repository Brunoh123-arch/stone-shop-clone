# -*- coding: utf-8 -*-
import json
from tiktok_catbox_downloader import download_and_upload_to_catbox

videos = [
    {
        'username': 'tukemperial',
        'nickname': 'Tuk',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/522ccc97986d0d2a8d739f5c7c05fedc~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=01d4cd71&x-expires=1795366800&x-signature=FL7xG%2FhBSlQr9nCxVDZQbYJ87%2BQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Poco X7 Pro o rei dos intermediarios premium com Dimensity 8400',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/oIIegDMEREWAHJPfhKIQ2VDn7OcFEBaCBQ6AIi/?a=1988&bti=ODszNWYuMDE6&&bt=983&ft=I~da4oKyD12Nv7bkslIxRGkSQlBF-UjNSxopiX&mime_type=video_mp4&rc=OjtmaDQ1OmU4ODc5ZWQ2OUBpMzNlcGo5cjk1eDMzNzczM0A0NGBfXjRfNTIxMGNjNC00YSNicW1pMmRrLTFgLS1kMTZzcw%3D%3D&expire=1795367188&l=20261121010556347194C3B8A506C90D2C&ply_type=2&policy=2&signature=bf52f24583d23a5c02517691c9dd67c6&tk=tt_chain_token&btag=e00088000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-p-0068/oIvICgZBbYQ9EUiAUgCuiLIBKiAA4BGiIEoAR~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=4ZkqG2FqTrx9uJSuNraBcq2z%2FOI%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'day.syndell',
        'nickname': 'Day Syndell',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/e75c438ac8747ad3c1307a28df62556b~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=4ed6f03f&x-expires=1795366800&x-signature=h90CLnuC9X7EOIBINvQi7aiX0JQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Unboxing Poco X7 Pro Xiaomi troquei meu iPhone por essa maquina',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/osqISEk0gASTCcfQjLeeSRGCKYU7pIIEwBv5Qo/?a=1988&bti=ODszNWYuMDE6&&bt=977&ft=-Csk_mrMPD12NdQ4uY-Ux5~2NY6e3wv25IcAp&mime_type=video_mp4&rc=ZTlnNjw4aTs1OjQ5aDg2ZkBpamp2Onk5cnE8NTMzNzczM0AxNDEuLl9fXl4xMmMxX2M2YSNoNWlrMmQ0MWhhLS1kMTZzcw%3D%3D&expire=1795367439&l=20261121010718380D090F5D764FF321F5&ply_type=2&policy=2&signature=7270da96d42d2af862978cb25db11435&tk=tt_chain_token&btag=e00098000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-p-0068/ooCjAaEoEDAiYiEkCWILyVfNAlBdgBAIiAr0No~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=6t%2Fjqo190S7RzS93p4DPqUPhUQk%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'brabostore22',
        'nickname': 'Brabo Store',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/87123ea6231d9d7da3b4620724d5fd08~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=81d31585&x-expires=1795366800&x-signature=rH5ulwnDSiMdmhx4wDJihbQGr4c%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Poco X7 Pro em maos visual gamer agressivo e carregador turbo de 90W',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o05nuvOnWYcAirnQTIAOaBIEXNhEYYKBi0SBv/?a=1988&bti=ODszNWYuMDE6&&bt=525&ft=I~da4oKyD12Nvw9kslIxRyFNDlBF-UjNSdopiX&mime_type=video_mp4&rc=aTU4aWQ1PGc4PGg6ODY5NkBpM2xoNnM5cnJ2ZTMzODczNEAvL2EwNS82XjUxYjVeMGA2YSNfYl5iMmRrcGlhLS1kMWBzcw%3D%3D&expire=1795367269&l=2026112101073586E955448B4666F23FD6&ply_type=2&policy=2&signature=320376205f60ad4b07b180a0a7b1b09a&tk=tt_chain_token&btag=e000b0000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ocvrnOaS5YA5EYXBOvzcNh0BLihAuBHiIIWbT~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=w1CPH%2BH%2FpO9dMs3xbBAtb6mWDFk%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'cellofertas.brasi',
        'nickname': 'Cellofertas',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/07aafa1a760cdd12170f10494a2a56f0~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=e0ef512d&x-expires=1795366800&x-signature=XrfpfqfXQc4FA1T1Y672BPmufAU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Poco X7 Pro 512GB potencia sem limites tela AMOLED 120Hz fluida',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/oIClE6IwuJAiriYHcxIl8HfoT4BxAABEgQI117/?a=1988&bti=ODszNWYuMDE6&&bt=366&ft=-Csk_mrMPD12NnQ4uY-Ux515PY6e3wv25scAp&mime_type=video_mp4&rc=ZTxlPGQ0aWZkNTQ4Njc1OUBpajhwdHY5cndrOzMzODczNEBhNDQxMmE0NjAxYWFhMzMzYSNpLjFuMmRjbHFhLS1kMWBzcw%3D%3D&expire=1795367301&l=20261121010752BD1420646BFD47F54120&ply_type=2&policy=2&signature=8c5e28342d6b050f653ee8e006433053&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oM7W5FBRcDqUOLExHg2RAYIBQfL1rhBEYxQfxB~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=xHigwz%2FqwcrWSEZP5bJe5zv1pVc%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'bloomfofa',
        'nickname': 'Bloom Fofa',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-avt-0068/33d6f9be69fce8466cff54d0d615b87c~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=2c37201d&x-expires=1795366800&x-signature=AFf%2FjFVLDA0lWcI%2BLJ%2FR6IXA%2FJY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Unboxing do meu celular Poco X7 Pro roda tudo no ultra',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/o8yifAM6gFEQq7678RAAREjX9meRnsOmewfGka/?a=1988&bti=ODszNWYuMDE6&&bt=1075&ft=-Csk_mrMPD12NKQ4uY-Uxh15WY6e3wv25BcAp&mime_type=video_mp4&rc=aTM2O2Q5NmY8PDRkOGY1ZUBpajZ3eXk5cmxtNTMzNzczM0A0YWJiLWM0XjUxNmAwXjMyYSNpcTJfMmQ0NnNhLS1kMTZzcw%3D%3D&expire=1795367372&l=20261121010811147CC1EFAFD4ECDD5BC3&ply_type=2&policy=2&signature=3b2fc09261a9d188073d12480a38679c&tk=tt_chain_token&btag=e00090000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-maliva-p-0068/os8HAecFmiyNIAQPNfuXtRwMIJAYfQGfuNkAAF~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=WGSEbbLfVQVVafS7wo8reMZkPrQ%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    }
]

res = []
for v in videos:
    user = v['username']
    print(f"Baixando e subindo {user}...")
    catbox = download_and_upload_to_catbox(v['playAddr'], f"{user}.mp4")
    print(f"-> {catbox}")
    v['catbox'] = catbox
    res.append(v)

with open('scripts/p36_videos_result.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("FINALIZADO COM SUCESSO!")
