import os
import json
import urllib.request
import urllib.parse
import time
import subprocess

raw_urls = [
  "https://www.tiktok.com/@dry2867/video/7696242002018438407",
  "https://www.tiktok.com/@marliseshop/video/7703795384241392916",
  "https://www.tiktok.com/@jamileeanderson0/video/7695430610130865428",
  "https://www.tiktok.com/@dry2867/video/7682871855518059783",
  "https://www.tiktok.com/@dry2867/video/7688423542639054088",
  "https://www.tiktok.com/@jamilesantos737/video/7688396853959822613",
  "https://www.tiktok.com/@marliseshop/video/7703794101912603925",
  "https://www.tiktok.com/@dry2867/video/7668379648572525842",
  "https://www.tiktok.com/@tky740/video/7703413636429106439",
  "https://www.tiktok.com/@tky740/video/7693927278337641735",
  "https://www.tiktok.com/@mirelacavalieri/video/7701068842558147860",
  "https://www.tiktok.com/@mirelacavalieri/video/7699990743900835080",
  "https://www.tiktok.com/@tky740/video/7703026530313686279",
  "https://www.tiktok.com/@tky740/video/7689269524620791058",
  "https://www.tiktok.com/@mirelacavalieri/video/7699976593367764245",
  "https://www.tiktok.com/@tky740/video/7681121687445703944",
  "https://www.tiktok.com/@mirelacavalieri/video/7697705380801006856",
  "https://www.tiktok.com/@mirelacavalieri/video/7693649362806754580",
  "https://www.tiktok.com/@leilacarvalho47/video/7689606688646778113",
  "https://www.tiktok.com/@jamileeanderson0/video/7686539590764727572",
  "https://www.tiktok.com/@ky.ster1/video/7689286856113949972",
  "https://www.tiktok.com/@julianatenoriop/video/7688167540937198868",
  "https://www.tiktok.com/@jefinshop/video/7693363072689343765",
  "https://www.tiktok.com/@jamileeanderson0/video/7689446217905999124",
  "https://www.tiktok.com/@renatanunesofc/video/7663113700785622290",
  "https://www.tiktok.com/@brendinhashop_/video/7697724504704929042",
  "https://www.tiktok.com/@lar1.69/video/7664761479975128341",
  "https://www.tiktok.com/@juliamilagres3/video/7688935625927462145",
  "https://www.tiktok.com/@juliamilagres3/video/7697393555744017685",
  "https://www.tiktok.com/@alynesmachado/video/7699564723297094933",
  "https://www.tiktok.com/@nilmmxdrkze/video/7680161785323719957",
  "https://www.tiktok.com/@stiloz6/video/7680669747943378183",
  "https://www.tiktok.com/@gabisoficiall/video/7658456965428907271",
  "https://www.tiktok.com/@elisseixasdicas/video/7694746407588121877",
  "https://www.tiktok.com/@gdsousa75/video/7662411159311518996",
  "https://www.tiktok.com/@loroofertasfc/video/7701321815502654728",
  "https://www.tiktok.com/@thalitar.02/video/7678103120450161940",
  "https://www.tiktok.com/@achadinhos.shopcreator/video/7577795647642848530",
  "https://www.tiktok.com/@mary_oficial612/video/7687596821538934037",
  "https://www.tiktok.com/@cortesviralbr07/video/7593387388345257224",
  "https://www.tiktok.com/@tokoffofc/video/7565737615509523730",
  "https://www.tiktok.com/@edushoporiginal/video/7674188599146908948",
  "https://www.tiktok.com/@begomesh/video/7663942112286657810",
  "https://www.tiktok.com/@segredostiktokshopoficia/video/7683244426327526663",
  "https://www.tiktok.com/@pink_br_shop_3/video/7680996451404614919",
  "https://www.tiktok.com/@garimpofeminiino/video/7701578556706508040",
  "https://www.tiktok.com/@achadiinhosdacris/video/7695023577724112135",
  "https://www.tiktok.com/@jamileeanderson0/video/7697417770908028180",
  "https://www.tiktok.com/@mahpereiraa90/video/7687248446817881352",
  "https://www.tiktok.com/@juliamilagres3/video/7689684969970584833",
  "https://www.tiktok.com/@renatanunesofc/video/7656534818611612946",
  "https://www.tiktok.com/@begomesh/video/7607657922608319752",
  "https://www.tiktok.com/@larissalopesdeabreu/video/7690241953656622357",
  "https://www.tiktok.com/@shayashop/video/7704350040873241876",
  "https://www.tiktok.com/@yamaguti.indica/video/7702287762099080456",
  "https://www.tiktok.com/@carinevgarcia/video/7564454564049554696",
  "https://www.tiktok.com/@ky.ster1/video/7699662470285200661",
  "https://www.tiktok.com/@vibeglowshop/video/7667742540723981585",
  "https://www.tiktok.com/@marci_reis/video/7694688502411185415",
  "https://www.tiktok.com/@yamaguti.indica/video/7699995592935755015"
]

# Dedup
seen_urls = set()
unique_urls = []
for u in raw_urls:
    if u not in seen_urls:
        seen_urls.add(u)
        unique_urls.append(u)

print(f"Total urls unicas: {len(unique_urls)}")

os.makedirs('temp_chinelo_meta', exist_ok=True)

results = []
for i, u in enumerate(unique_urls):
    api_url = f"https://www.tikwm.com/api/?url={urllib.parse.quote(u)}"
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('code') == 0 and data.get('data') and data['data'].get('play'):
                d = data['data']
                item = {
                    'tiktok_url': u,
                    'title': d.get('title', ''),
                    'author_name': d.get('author', {}).get('nickname', 'Criadora'),
                    'username': d.get('author', {}).get('unique_id', 'criadora'),
                    'avatar': d.get('author', {}).get('avatar', ''),
                    'play_url': d.get('play'),
                    'duration': d.get('duration', 0),
                    'likes': d.get('digg_count', 1200),
                    'comments': d.get('comment_count', 45)
                }
                results.append(item)
                print(f"[{len(results)}] OK: @{item['username']} - {item['title'][:40]}")
                if len(results) >= 32:
                    break
            else:
                print(f"Skip ({u}): code {data.get('code')}")
    except Exception as e:
        print(f"Err ({u}): {e}")
    time.sleep(0.5)

print(f"\nTotal extraidos com sucesso: {len(results)}")
with open('temp_chinelo_meta/valid_creators.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
