# -*- coding: utf-8 -*-
import json
from tiktok_catbox_downloader import download_and_upload_to_catbox

videos = [
    {
        'username': 'favoritosdadaii',
        'nickname': 'Dai',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/b0aa42ecf317bbabef3a8e097b6edabe~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=4a0084bf&x-expires=1795363200&x-signature=qm58PS5FZ%2Fl9HaVqp9jS2cGlTi8%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Secador de Cabelos Philco PSC3500 4 em 1 Dobravel',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/o0fECfD48grRDZHIgT8EAnBUdBXFQuUJpPvHAa/?a=1988&bti=ODszNWYuMDE6&&bt=989&ft=-Csk_mrMPD12N0C4uY-UxKJFVY6e3wv25icAp&mime_type=video_mp4&rc=OjY1OWlmZWllNDU6ZGg6ZUBpajo6c3g5cnM2ODMzODczNEBiLS4xXy0yNS8xNTIwLTJeYSNkcDIuMmRza2JhLS1kMTFzcw%3D%3D&expire=1795365372&l=20261121003542CE7CAF55F1A985EE4EA1&ply_type=2&policy=2&signature=9ef016a7851665367b5fbf9fb8305048&tk=tt_chain_token&btag=e000b8000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/o8SJBTfDUQ8OR8pEHdmCyXPD4BfAQEvnFDonQg~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=%2B6DDUBUGL%2BZiz1k1jhZ7R%2FuwzzE%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'dailykarenm',
        'nickname': 'Karen Mendes',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/b5c2a344b08b17e9a8b78a7b9e1a2956~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=da553ffb&x-expires=1795363200&x-signature=cY1Wt%2BTHJ%2Bm%2FPbl7SYlu3%2FIIsVo%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Secador Philco 4 em 1 PSC3500 pratico demais',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/ogGuvIZgqITBfLfRgwwe28kdQFRCFGAfDrQpAG/?a=1988&bti=ODszNWYuMDE6&&bt=1476&ft=I~da4oKyD12NvZ~kslIxR4CjQlBF-UjNS2opiX&mime_type=video_mp4&rc=aWZnODc8Omk0Zjc1ZmQ4O0Bpampyd3A5cmV0ZTMzODczNEBjMzQzMDJeX18xYi9jL2JiYSMtMm9jMmRzYS1hLS1kMWBzcw%3D%3D&expire=1795365409&l=20261121003600F88A6CEA62CA9AF4474D&ply_type=2&policy=2&signature=b269cca8d770db8eadbdaf16b400044d&tk=tt_chain_token&btag=e00088000',
        'cover': 'https://p19-common-sign.tiktokcdn.com/tos-alisg-p-0037/okBquyaHAAAeARtdgEFvwpcD7fvGMraEBECDBI~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=oAx3GtPgOJaky%2B86BeQRa%2Fmlz8s%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'mandasoaris',
        'nickname': 'Amanda',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/cd2f0569e641e79e0ddea8bbf6f74f1c~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=6acc78b7&x-expires=1795363200&x-signature=kRSTxB9d2oSpscID9f1NL0ur5yc%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'O ps5 das garotas secador philco 4 em 1',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/owGRAgfAGCbgnAG46xUdeDbeieHYRFsbwUTGCR/?a=1988&bti=ODszNWYuMDE6&&bt=1065&ft=I~da4oKyD12NvYRkslIxRHJSQlBF-UjNSdopiX&mime_type=video_mp4&rc=NDs4ODw6Mzw3NGc8ODs2O0BpamlnPG05cjxqOjMzODczNEBiNGIzYDIyXmMxLjQwYGExYSNmaC9xMmRrbGJhLS1kMWBzcw%3D%3D&expire=1795365393&l=2026112100361984B26EBAE7A62BC2E48A&ply_type=2&policy=2&signature=920cfb67f42dd0b69c4ff9d7586b2a8d&tk=tt_chain_token&btag=e000b0000',
        'cover': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-p-0037/oEIABldvMACizTGEaJ0ddB6dDXiIaNOYP7NkW~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=9bWlITJMWCuDlHZfA49qqeH5Myg%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'lilianmaurente',
        'nickname': 'Lilian Maurente',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/42dfadf07e4311ff312b724e5370f981~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=77521f81&x-expires=1795363200&x-signature=i91BX4JjJESTv%2BwchCLI1QO6aKE%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Testei o secador 4 em 1 Philco PSC3500 resultado incrivel',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-ve-0068c800-sg/oEa8qQI1OIcEAxESkYAiXAF6BPjctDiOBB4An/?a=1988&bti=ODszNWYuMDE6&&bt=899&ft=-Csk_mrMPD12Nex4uY-UxMHFNY6e3wv25AcAp&mime_type=video_mp4&rc=PDUzZDg8ODllZTUzaTQ3aEBpajNvZ2s5cnZkPDMzODczNEBfMi4zLWNeNjExMTEuY2EtYSNlbDViMmQ0YzRhLS1kMWBzcw%3D%3D&expire=1795365428&l=202611210036370E847180F1B583CCF31A&ply_type=2&policy=2&signature=6f7bfe2bf915a24f43278b398074d8d4&tk=tt_chain_token&btag=e00088000',
        'cover': 'https://p19-common-sign.tiktokcdn.com/tos-alisg-p-0037/okwRfCLOlIGUzJAAfcAAeLIVpdQnGpCGwAfpTJ~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=Ma8C4sHGbpeIsDG0V2xaPbt5xps%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
    },
    {
        'username': 'leandraklisievicz',
        'nickname': 'Leandra Klisievicz',
        'avatar': 'https://p16-common-sign.tiktokcdn.com/tos-alisg-avt-0068/2949064d3ef15ebe92bff1902b76b9a0~tplv-tiktokx-cropcenter:100:100.jpeg?dr=14579&refresh_token=f856a52e&x-expires=1795363200&x-signature=Q9yHvruyzgc5%2F8YWsmDbt1oT5pQ%3D&t=4d5b0474&ps=13740610&shp=a5d48078&shcp=81f88b70&idc=my3',
        'desc': 'Review sincera do secador da Philco PSC3500',
        'playAddr': 'https://v16-webapp-prime.tiktok.com/video/tos/alisg/tos-alisg-pve-0037c001/oQtVEY36wi87swGX1aaZv9PujsEQBiuIOEABA/?a=1988&bti=ODszNWYuMDE6&&bt=565&ft=-Csk_mrMPD12Nhx4uY-Ux7w2NY6e3wv251cAp&mime_type=video_mp4&rc=N2hkPDs3ZzNlZzozM2QzO0BpanVqaXc5cnFkZTMzODczNEAuNDI0MC4tXjYxYi41XjQ0YSNqcS1rMmRrcTBhLS1kMWBzcw%3D%3D&expire=1795365744&l=202611210037080AAA8E47BA1297C7C670&ply_type=2&policy=2&signature=e25d84748b002c155e682afa29bca1b4&tk=tt_chain_token&btag=e000a0000',
        'cover': 'https://p19-common-sign.tiktokcdn.com/tos-alisg-p-0037/oknBYAaGAlEoJA5cAAiBos3wERADsamIEPiGk~tplv-tiktokx-origin.image?dr=14575&x-expires=1795363200&x-signature=Pzj89SMoUWzzEQJ6AXzh4WOXg04%3D&t=4d5b0474&ps=13740610&shp=81f88b70&shcp=43f4a2f9&idc=my2'
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

with open('scripts/p39_videos_result.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)

print("FINALIZADO COM SUCESSO!")
