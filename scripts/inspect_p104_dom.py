from bs4 import BeautifulSoup

soup = BeautifulSoup(open('pages/produto-104.html', encoding='utf-8'), 'html.parser')
for sel in ['.creators-section', '.reviews-section', '#reviews', '.customer-protection']:
    el = soup.select_one(sel)
    if el:
        parent = el.parent
        print(f"Selector {sel} found! Parent: <{parent.name}> class={parent.get('class')} id={parent.get('id')}")
    else:
        print(f"Selector {sel} NOT found!")
