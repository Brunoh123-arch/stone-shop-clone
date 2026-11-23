# -*- coding: utf-8 -*-
import json
from tiktok_catbox_downloader import download_and_upload_to_catbox

videos = [
    {
        'username': 'kevelybr',
        'nickname': 'Kevely',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/05c6c43d70fe6940c755598a46fc6076~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=0ac40fe9&x-expires=1795363200&x-signature=Gz4vkh4WcUyfXEEA0uJnOFhzeQw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Vestido longo feminino costas nuas e fenda lateral caimento deslumbrante',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o4DASVXCLZLIIhLjORRAUpA4suAeUpYaeftgZG/?a=1988&bti=ODszNWYuMDE6&&bt=1325&ft=-Csk_mrMPD12NhZ4uY-UxWJFNY6e3wv25pcAp&mime_type=video_mp4&rc=aDs2aDU5NTk7ZjNkOWc6O0Bpam5mZnA5cndlZTMzODczNEAxMzBiNV4yNTMxLzBjYDRiYSNeYC4uMmQ0ZmFhLS1kMWBzcw%3D%3D&expire=1795366738&l=202611210058284DE4D7B5B95713F0F25D&ply_type=2&policy=2&signature=b1ca0b954f651f778aaf96f1998002aa&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p19-common-sign.tiktokcdn.com/tos-alisg-p-0037/oAG184epgCZtsgIjxejcIeYDGLNUXARAFLA9LV~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=APqNVMUgi%2BEwB0Zws4SrAsDqQ9Y%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'cassycorrea0',
        'nickname': 'Cassy Correa',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/41f23794ddda8760c59f18e25afbb4f9~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b1ba9bb0&x-expires=1795363200&x-signature=k2sdfeQF6sRsBPFcH7a0MTH1fL8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Vestido suplex longo colado fenda lateral costas nuas elegancia pura',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/ooX1Df1KEECUEzNReQpgFBBVI9RTAhSbrB2B7T/?a=1988&bti=ODszNWYuMDE6&&bt=615&ft=-Csk_mrMPD12N6o4uY-UxsJ5WY6e3wv25pcAp&mime_type=video_mp4&rc=OmRkZ2VmO2U8OzxmO2Q8Z0BpamtnM3Q5cmxtOjMzODczNEAxM18uYzMyNjYxM2M2YGIvYSNhMWNzMmRrX15hLS1kMTFzcw%3D%3D&expire=1795366787&l=202611210059273BB4EED978A392F590EB&ply_type=2&policy=2&signature=d0b20807298b2a38f28c80b2bfc6125a&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/okbR11Ej7BedoVUzEBXKNTgIDfA3FBBRSBspTI~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=2B0cLYcJcyg7R85vW7XgApVJ7JY%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'keylasbraga',
        'nickname': 'Keyla Braga',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/e28a7593958079a7cc8e4940fb288183~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=2b7093ed&x-expires=1795363200&x-signature=nWVCRINsri0uksIa9hek3o%2BrM8U%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Vestido longo festa costas nua e fenda lateral tecido encorpado',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o8eMJUjIGGj7gIUQfCLVASHGAYo2LD9PeEzIVo/?a=1988&bti=ODszNWYuMDE6&&bt=1135&ft=-Csk_mrMPD12NNg4uY-Uxt~FPY6e3wv25HcAp&mime_type=video_mp4&rc=aTRlODllZWRoOjc1aWVlZUBpM3l1anQ5cnM1ZTMzODczNEAwLjQ0NDViX2ExLy0wXjNjYSMzXmEvMmQ0NWdhLS1kMTFzcw%3D%3D&expire=1795366826&l=202611210059465964A2B8C131DCFCFD6C&ply_type=2&policy=2&signature=6ac3de9644480919999712d83c161eb1&tk=tt_chain_token&btag=e00088000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o4MRWEUDqBJ0fPqFET7i0AIKEBdmf5DgDRIHPk~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=A%2FOfVAUL%2Br6Oxo8Ntm1dhMr5qA4%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'andreia.alves.aaa',
        'nickname': 'Andreia Alves',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/bfc39abd16fc669833f454124c81b786~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=c42ddd84&x-expires=1795366800&x-signature=EDNOLCbetVFBQuwjt5ttcg%2F1Ub0%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Vestido longo fenda e costas nuas look impecavel e chique',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/oUGLxeEIQDAUD4efn1Fo2grusco3pIAUDC2jg0/?a=1988&bti=ODszNWYuMDE6&&bt=1018&ft=-Csk_mrMPD12NJg4uY-UxGw5PY6e3wv25HcAp&mime_type=video_mp4&rc=aDU6PGRmMzllOzY8aGk8OEBpM3JpN3Q5cjNwPDMzODczNEBhMzEuMjMtNmMxX2BgYzItYSNvYnMyMmRzaHFhLS1kMTFzcw%3D%3D&expire=1795366827&l=2026112101000389847EF89D5FEFF50E02&ply_type=2&policy=2&signature=ba276dc70778664b17742677added746&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o0r790AIEcDAeozF2vESBUareAhDjIAAEDtwf9~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=rmCcuOCqUdkDMUVj9zA1O9qt%2FEo%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'ericamcabeluda',
        'nickname': 'Erica Leao',
        'avatar': 'https://p19-common-sign.tiktokcdn.com/tos-maliva-avt-0068/47a24c9b06d824ac35a6d56fcf87fa72~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=6f3a8bf3&x-expires=1795366800&x-signature=pB2fc18pY5oIovGq%2F162XzGs1WE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Vestido longo fenda e costas nuas valoriza muito o corpo',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/ocE1FImTDIsfCZwvADFgcTRLmBfEqOBQEIgCEj/?a=1988&bti=ODszNWYuMDE6&&bt=1306&ft=-Csk_mrMPD12Ngg4uY-Ux4T2LY6e3wv251cAp&mime_type=video_mp4&rc=OzhpNzszOTw7PDpoOWZmOEBpam1kcnI5cmw7ZDMzODczNEAwNF5hLS8tNmExYS82NC1iYSMtMF8xMmRzazNhLS1kMWBzcw%3D%3D&expire=1795366870&l=202611210100268532EEE18349F8D96721&ply_type=2&policy=2&signature=8ea274c590a6cac3ecb07672d488cfd6&tk=tt_chain_token&btag=e00088000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/ooEAQcIfIeEICnERlFjqIAFvcAdDQEgBAirWZC~tplv-tiktokx-origin.image?dr=14575&x-expires=1795366800&x-signature=4PbnmgxRyO4l8kKstS%2FiNhnUKgY%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
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

with open('scripts/p103_videos_result.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("FINALIZADO COM SUCESSO!")
