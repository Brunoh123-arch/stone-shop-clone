# -*- coding: utf-8 -*-
import json
from tiktok_catbox_downloader import download_and_upload_to_catbox

videos = [
    {
        'username': 'beatrizfalasca',
        'nickname': 'Beatriz Falasca',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/9fbbf28d916a9abd0ccc3c7ab2d40756~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=256897dd&x-expires=1795363200&x-signature=47hcXxeC0S%2Bo432fQHkAb0mzrAU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Conjunto alfaiataria feminino elegante caimento perfeito no corpo',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/oQAQ7F9Vz9faD7JIjfxCeSI8A4EqDPKEDTvCIb/?a=1988&bti=ODszNWYuMDE6&&bt=902&ft=-Csk_mrMPD12Nad4uY-UxTv2WY6e3wv25AcAp&mime_type=video_mp4&rc=ZTo1ZzY6ZWhnPDM2NDxnNkBpajZldng5cm94OjMzODczNEA1YC80MzZeNjAxXmBiY180YSNhbjVjMmRjbXFhLS1kMWBzcw%3D%3D&expire=1795366588&l=20261121005513926BF7B53399C4F8F66E&ply_type=2&policy=2&signature=5bcf753d229856f3ccc837e21f097cfb&tk=tt_chain_token&btag=e00090000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o8Z7E7iNA64J7yK7DABAIbezjxTA7EDIAfivfZ~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=WXcuxfpDRapJpH6wdxrRCiNzXnU%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'samarafashion_modesta',
        'nickname': 'Samara Fashion',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/a7eaf8d058298caa6626c6603411e0d6~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b63390d8&x-expires=1795363200&x-signature=GI%2FZvYOuyr%2BDe9IQCIhbPaJ58G8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Conjunto de calca e colete alfaiataria verao elegante para trabalho',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/oADB2iDvFBXi2LatuRYgABoEykfIEcQfgqiHuE/?a=1988&bti=ODszNWYuMDE6&&bt=1394&ft=I~da4oKyD12Nvt1kslIxRhFSQlBF-UjNSdopiX&mime_type=video_mp4&rc=NzRlZTlkOWc5ZDlpM2U8ZEBpM3F4amw5cjs1ZTMzODczNEAvYzE2YDMzX18xMl9eLWAuYSNkZHNgMmRrb2FhLS1kMWBzcw%3D%3D&expire=1795366570&l=2026112100555902A782B240EF64F0B110&ply_type=2&policy=2&signature=2de45f7b6ba3bb051ae466c168ea7be8&tk=tt_chain_token&btag=e000b0000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o8VA4Lay1EsEFALjfDrIIhrAAtIbA0eDFwLGIe~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=50UVgtSyGqLv%2Buczak%2BXNzQKvGI%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'lariicloset',
        'nickname': 'Larissa Closet',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/acb0f8f99eb857bd8a082d05f9d2346a~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=59396d7a&x-expires=1795363200&x-signature=Pbxn%2Fsyh3UPzA0hB07I%2F8iYV2Cc%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Conjunto social feminino colete com calca alfaiataria acabamento premium',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o4306QByIgAiBDy3fCAwE8pikhUD9KmW3PqI0K/?a=1988&bti=ODszNWYuMDE6&&bt=853&ft=-Csk_mrMPD12NrD4uY-Ux7vvWY6e3wv25AcAp&mime_type=video_mp4&rc=ZzdmN2c7NjNkZjg7ODo6OEBpMzltZ2w5cjQ1OjMzODczNUBeMV4tYWJgXjQxMjQxYTAtYSMyMnBpMmRzal5hLS1kMTZzcw%3D%3D&expire=1795366594&l=2026112100561885E91B46BCD6F3F4ABBA&ply_type=2&policy=2&signature=42dac941ec30371cf85ec98f664dfdd4&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ocpDsAaAED5AI3Fgpd1AOKCfXt2RC3E1UEBU7f~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=%2OiC7475AUjvUnLDbCCuoZAHBVU%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'manuela_souzahh0',
        'nickname': 'Manuela Souza',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/eeb81dbcafab88c29ea6f3f0ef11c678~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=c6d79b75&x-expires=1795363200&x-signature=L7ozqErahCwg1mOeAMgO%2F%2FI4rRk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Conjunto alfaiataria colete e calca corte reto chic e confortavel',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/oAQaFYovD6AXaFQ9iiNPvEIjwIABBZBBiAEsA/?a=1988&bti=ODszNWYuMDE6&&bt=784&ft=-Csk_mrMPD12NlB4uY-Uxl4FPY6e3wv25HcAp&mime_type=video_mp4&rc=ZTdkNDVlOmU8NDYzNTw7N0BpMzU0amo5cmozZTMzODczNEA2YTE1YmI0XjYxMi0wNjQzYSNqZzZyMmQ0LXFhLS1kMWBzcw%3D%3D&expire=1795366611&l=20261121005637CFE11EEC6A0AAFD18590&ply_type=2&policy=2&signature=6366a01f0135f39840b27e6fc00959fd&tk=tt_chain_token&btag=e000b0000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ok9IiXA7iyVGXA6CYEABwBaZoBI7PMsiQIEAv~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=3LN4JJU%2F4vQWVtZN9tinnE06NaY%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'dudaleal.outfits',
        'nickname': 'Duda Leal',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/4e7ac21ede7afa4eade351bd5e519ce9~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=cd94497e&x-expires=1795363200&x-signature=zFNndbuy6sD9uggnrHFm%2B0IMwhk%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Look de trabalho completo conjunto alfaiataria impecavel e sofisticado',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o8Q1IgBGR1UuAeDqzFVafW0J4mqE8ECgc9uUBn/?a=1988&bti=ODszNWYuMDE6&&bt=875&ft=-Csk_mrMPD12N9B4uY-UxrOFPY6e3wv252cAp&mime_type=video_mp4&rc=Omk5M2hmZmU6OzpoZDw6M0BpM2U8c285cmloZDMzODczNEA2MF4yYy1gNjMxYF4wYi8yYSNicTJgMmQ0Z3FhLS1kMWBzcw%3D%3D&expire=1795366625&l=2026112100565533D4073DBF4CCAE8DCEF&ply_type=2&policy=2&signature=1fe54d0c0b6cc536533fead4e0765d18&tk=tt_chain_token&btag=e000b0000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oIPXp0wcNiA8GA11AzAXI6E6fVCCgBAOSB5IXi~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=%2BVHw00dOh7h%2BpUygVEFwjWGA3cw%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
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

with open('scripts/p88_videos_result.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("FINALIZADO COM SUCESSO!")
