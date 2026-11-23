# -*- coding: utf-8 -*-
import json
from tiktok_catbox_downloader import download_and_upload_to_catbox

videos = [
    {
        'username': 'brendanuness_1',
        'nickname': 'Brenda Nunes',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/fa211b39b15489b0f64210abed21010f~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=b6c11c4d&x-expires=1795363200&x-signature=%2BsQOAgXEeRPfaw31D%2B8xh1bRejw%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Kit com 10 camisetas Dry Fit conforto estilo e rendimento pro treino ou dia a dia',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/ocuNJaiEZmQ4IxA73AmYBEV1BQVkEq72iBiKP/?a=1988&bti=ODszNWYuMDE6&&bt=1016&ft=-Csk_mrMPD12N_34uY-UxW1vNY6e3wv252cAp&mime_type=video_mp4&rc=N2YzNjc3MzNnNTo5aWU5N0BpM2g7eHI5cjlsODMzODczNEAxLzIxYzY0X14xNjZiXjAvYSMvb21xMmQ0YWBhLS1kMTFzcw%3D%3D&expire=1795366344&l=2026112100520966321EFF0503BEFA6E3E&ply_type=2&policy=2&signature=5071c40e5c75ebc8d54d50a5d2d401e4&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/owBVuFAEAqmkEmjEYAiiKnZaUNI4P7VAEBY7J~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=ufEMI7oHOHRygm%2FLqhwM4RzWvs4%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'matheuzshop',
        'nickname': 'Matheus Shop',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/537a00a1d349bfa5ffdd6c6f4efc4698~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=97784515&x-expires=1795363200&x-signature=x90MKy%2F%2FfWLn4M80%2BhecKC7EDzU%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Kit 10 camisas dry fit masculinas tecido leve anti suor',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/oUnfJrqIRyGLARSgVFLnA2PGA0w4EGese9fRFs/?a=1988&bti=ODszNWYuMDE6&&bt=551&ft=-Csk_mrMPD12N5O4uY-Ux2H2NY6e3wv25pcAp&mime_type=video_mp4&rc=ZWk0aTRoZ2RoOWRnNzxnZEBpanNlaXU5cmt4OjMzODczNEAvX2FiYjRgNS8xX15fMS80YSNyLzEyMmQ0bnNhLS1kMWBzcw%3D%3D&expire=1795366360&l=202611210052246975B6A448EAC5F0FF76&ply_type=2&policy=2&signature=56c590de235f659e19f027f701a1f591&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o8en1FGfRDGfLftIC7LqJgdWG0WygAFs9nJwrA~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=ABq%2F5ezUs2MiBkfg22n3t%2BH3two%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'shoptresmeiacinco365',
        'nickname': 'Loja 365',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/0b22f899d16e0c3d97b82454a5aa2d11~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=7f06809e&x-expires=1795363200&x-signature=%2FHQb%2FQDMdFNS1HzNvi7DYWWiF%2BQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Kit com 10 camisas Dry Fit perfeitas para treino e caminhada',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/owzqBfkHEHpFncOAjgXQn8aORqdlDBgiEfdI7c/?a=1988&bti=ODszNWYuMDE6&&bt=1907&ft=-Csk_mrMPD12NrO4uY-Ux~U2VY6e3wv25QcAp&mime_type=video_mp4&rc=OTY0NGY6NDlkO2c2OTU4Z0BpM3dlbWs5cjRtZDMzODczNEBgLTE1Xi5eNl4xLV42X2MyYSNzNGozMmRzaWNhLS1kMWBzcw%3D%3D&expire=1795366402&l=20261121005307B703487AF2BF7DF38FFD&ply_type=2&policy=2&signature=373c7892903aba5aedf465376fd215d9&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oAeLebPADXCInPA0ElG34VgSPgnUfdjhnL4Ip7~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=zSXActFVJQtWAaohetgPz%2BUeH%2Fk%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'd.v.variedades',
        'nickname': 'David Souza',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/c80e6942835d5a4931af72ebe908f5b1~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=56918a12&x-expires=1795363200&x-signature=c2OhrOw%2FA3HL3ThfZT6mX40xpEQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Kit com 10 camisetas Dry Fit alta durabilidade e secagem ultrarrapida',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o0DgDfiQEEDcIYQxSgpgFBXBQHRUAe7WKBrCbS/?a=1988&bti=ODszNWYuMDE6&&bt=733&ft=-Csk_mrMPD12N514uY-Ux515PY6e3wv25scAp&mime_type=video_mp4&rc=OWY7OWk3NWk1ZWZlZDU7Z0BpanJxbGs5cm5uOTMzODczNEBeMzQxNTZjXi0xXjNeLzYvYSNpb3ExMmQ0Li1hLS1kMWBzcw%3D%3D&expire=1795366425&l=202611210053290140749B02E42DEF5127&ply_type=2&policy=2&signature=c1d3749dee3ec3027eb6f1ec2641f779&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/og7hGECsgIi36feDogTICGwCAgHu43NeAAkLUj~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=5hHYD9nuRJSWIHEJ5T4SMxHPic4%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'elitemasculinashop',
        'nickname': 'Elite Masculina',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/6cf48bed9fab1db43f9322e1cdd8ecfd~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=82214b65&x-expires=1795363200&x-signature=IJNoI8jTFMcil7PbTIHLSuX4wRY%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Kit 10 camisetas dry fit esportivas caimento impecavel no corpo',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/o0yEefxP4gURDTBEQW1EA0BcGBzFIcR4pmq8xr/?a=1988&bti=ODszNWYuMDE6&&bt=1077&ft=-Csk_mrMPD12N914uY-UxGw5PY6e3wv25HcAp&mime_type=video_mp4&rc=OjY5ODY5aGU5NDxoOTc1OEBpM21nOnQ5cmdrOjMzODczNEAuNDAuNi4xNjIxNV40YjIxYSNjbC5zMmQ0aTRhLS1kMWBzcw%3D%3D&expire=1795366437&l=20261121005344E8CEF2D198C291FAF8CE&ply_type=2&policy=2&signature=51a0d190a151f921a403b74d840f83b0&tk=tt_chain_token&btag=e000b0000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/osmP08qEi4RWEIKIKBFpAGvDgecUDB7yfxzE41~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=H80jYNSP4P8ku8LITFJXNQsczN0%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
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

with open('scripts/p75_videos_result.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("FINALIZADO COM SUCESSO!")
