import glob
import re

pages = glob.glob('pages/produto-*.html')

def get_pid(p):
    m = re.search(r'produto-(\d+)\.html', p)
    return int(m.group(1)) if m else 9999

pages.sort(key=get_pid)

out_lines = []
out_lines.append(f"TOTAL NO CATALOGO: {len(pages)} PRODUTOS\n")

for p in pages:
    pid = get_pid(p)
    try:
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read(1500)
        tm = re.search(r'<title>([^<]+)</title>', c)
        title = tm.group(1).replace(' - Stone Shop', '').strip() if tm else f'Produto {pid}'
        out_lines.append(f"ID {pid:>3}: {title}")
    except Exception as e:
        out_lines.append(f"ID {pid:>3}: [Erro {e}]")

with open('scripts/todos_os_produtos.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out_lines))

print(f"Salvo {len(pages)} produtos em scripts/todos_os_produtos.txt")
