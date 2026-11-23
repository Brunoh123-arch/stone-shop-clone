import glob, re, subprocess

pages = glob.glob('pages/produto-*.html')
pages.sort(key=lambda p: int(re.search(r'produto-(\d+)\.html', p).group(1)))

syntax_errors = []

for p in pages:
    pid = int(re.search(r'produto-(\d+)\.html', p).group(1))
    with open(p, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Extrai o script que declara PRODUTO_ATUAL
    scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', html, re.DOTALL)
    for idx, s in enumerate(scripts):
        if 'PRODUTO_ATUAL' in s:
            # Testa a sintaxe com node
            cmd = ['node', '--check', '-']
            res = subprocess.run(cmd, input=s, text=True, capture_output=True)
            if res.returncode != 0:
                err_line = res.stderr.strip().splitlines()[-1] if res.stderr else "Syntax Error"
                syntax_errors.append((pid, p, err_line, s))

print(f"Total de produtos auditados: {len(pages)}")
print(f"Total de páginas com ERRO DE SINTAXE JS: {len(syntax_errors)}")
for pid, path, err, _ in syntax_errors:
    print(f"  [X] P{pid}: {err}")
