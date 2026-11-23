from bs4 import BeautifulSoup

for pid in [101, 80, 87]:
    path = f"pages/produto-{pid}.html"
    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    print(f"\n--- P{pid} buy elements ---")
    for el in soup.find_all(True):
        t = el.text.strip().replace("\n", " ")
        if "comprar agora" in t.lower() and len(t) < 50:
            print(f"  <{el.name}> id={el.get('id')}, class={el.get('class')}, onclick={el.get('onclick')}, href={el.get('href')}, text='{t}'")
