from bs4 import BeautifulSoup

SHARD_IDS = [80, 82, 85, 87, 88, 89, 90, 91, 92, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104]

for pid in SHARD_IDS:
    path = f"pages/produto-{pid}.html"
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    el = soup.find(id="creators-section")
    if el:
        print(f"P{pid}: <div id='creators-section' class='{el.get('class')}' style='{el.get('style', '')}'>")
    else:
        print(f"P{pid}: #creators-section NOT FOUND")
