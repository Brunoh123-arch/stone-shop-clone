from bs4 import BeautifulSoup

with open('pages/produto-114.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

cards = soup.find_all('div', class_='review-card')
print(f"Total cards in produto-114: {len(cards)}")
for i, c in enumerate(cards):
    author = c.find('div', class_='review-user-name')
    author_name = author.get_text(strip=True) if author else f'Card {i}'
    print(f"Card {i} [{author_name}]: {c.prettify()[:200]}...")
