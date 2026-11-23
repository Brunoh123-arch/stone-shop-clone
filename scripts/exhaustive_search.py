import glob
import re
from bs4 import BeautifulSoup
import json

files = sorted(glob.glob('pages/produto-*.html'), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0)

# Form prefixes typical of Shopee / AliExpress reviews
field_names = [
    'aroma', 'usabilidade', 'forma e tamanho', 'forma', 'tamanho', 'qualidade do produto',
    'qualidade', 'desempenho', 'cor', 'textura', 'durabilidade', 'fixação', 'fixacao',
    'pigmentação', 'pigmentacao', 'cheiro', 'sabor', 'material', 'materiais', 'conforto',
    'design', 'capacidade', 'qualidade do trabalho', 'entrega', 'embalagem', 'produto',
    'custo benefício', 'custo-benefício', 'acabamento', 'parecido com anúncio',
    'parecido com o anúncio', 'conforme anúncio', 'conforme o anúncio', 'atendimento',
    'projeção', 'projecao', 'potência', 'potencia', 'cobertura'
]

# Regex to find these followed by a colon
prefix_regex = re.compile(
    r'(?:\b|^|\n|\r|["\'>])(' + '|'.join([re.escape(fn) for fn in field_names]) + r')\s*:\s*',
    re.IGNORECASE
)

# Also check marketplace names: shopee, aliexpress, shein, moedas, pontos
mkt_regex = re.compile(r'\b(shopp?ee?|ali\s*express|shein|moedas?)\b', re.IGNORECASE)

# Pontos in context of marketplace rewards: e.g. "pontos da shopee", "ganhar pontos", "avaliando por pontos", "pra ganhar pontos"
pontos_reward_regex = re.compile(r'(?:ganhar|pelos?|por|acumular)\s+pontos?|pontos?\s+(?:da|do|no|na)\s+(?:app|loja|shopp?ee?)|moedas?', re.IGNORECASE)

detected = []

for f in files:
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        html = fp.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    cards = soup.find_all(class_=re.compile(r'review-card'))
    
    for idx, card in enumerate(cards):
        comment_p = card.find(class_=re.compile(r'review-comment'))
        text = comment_p.get_text() if comment_p else ''
        data_c = card.get('data-author-comment', '')
        
        # Combined check
        full_text = text if text else data_c
        
        field_matches = prefix_regex.findall(full_text)
        mkt_matches = mkt_regex.findall(full_text)
        pontos_matches = pontos_reward_regex.findall(full_text)
        
        # Check if there is something suspicious
        # Filter out false positives:
        # e.g. "cor: branco" in a bread recipe is technically a recipe setting, but let's see
        # e.g. "conheça a caixa de som aiwa: som potente" is a sentence, but "qualidade: ótima" is a form field
        
        reasons = []
        if field_matches:
            # Check context
            for fm in set([m.lower() for m in field_matches]):
                reasons.append(f"field:{fm}")
        if mkt_matches:
            for mm in set([m.lower() for m in mkt_matches]):
                reasons.append(f"mkt:{mm}")
        if pontos_matches:
            for pm in set([m.lower() for m in pontos_matches]):
                reasons.append(f"reward:{pm}")
                
        if reasons:
            detected.append({
                'file': f,
                'card_index': idx,
                'author': card.get('data-author-name', ''),
                'variation': card.get('data-author-variation', ''),
                'date': card.get('data-author-date', ''),
                'reasons': reasons,
                'text': text,
                'data_c': data_c
            })

print(f"Total detected items: {len(detected)}")
with open('scripts/all_detected_form_reviews.json', 'w', encoding='utf-8') as out:
    json.dump(detected, out, indent=2, ensure_ascii=False)

for d in detected:
    print(f"[{d['file']}] Card {d['card_index']} ({d['author']}) -> {d['reasons']}")
    print(f"   Text: {d['text'][:120].replace(chr(10), ' ')}")
