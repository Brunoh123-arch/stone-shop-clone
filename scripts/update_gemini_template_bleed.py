import os

path = r'c:\Users\Dell\Downloads\ds\GEMINI.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '#### 5. Formatação Padronizada da Página & Integridade Estrutural do DOM (`Final Depth: 0`):'

rule = '''#### 5. Formatação Padronizada da Página & Integridade Estrutural do DOM (`Final Depth: 0`):
- **PROIBIÇÃO ABSOLUTA DE CONTAMINAÇÃO CRUZADA DE TEMPLATE (ZERO TEMPLATE BLEED / STATE LEAK)**:
  - **O Problema do 'Template Bleed'**: Ocorre quando um dev ou script clona o HTML de um produto existente (ex: Escova Secadora 108) para criar um novo produto (ex: Tênis Kappa 110 ou Comedouro Pet 113) e esquece nós internos estáticos com dados do produto antigo. O cliente clica no Tênis e dá de cara com H1, carrossel de criadores ou descrição da Escova Secadora. Isso é amadorismo puro e destrói as vendas.
  - **Paridade Obrigatória 1:1 no DOM**:
    1. `<title>` DEVE bater milimetricamente com `<h1 class="product-title">`.
    2. `PRODUTO_ATUAL.nome` e `PRODUTO_ATUAL.id` DEVEM corresponder estritamente ao produto da página.
    3. `#creators-section`: Os vídeos e posters instanciados pelo `videos-criadores.js` DEVEM corresponder ao nicho do produto atual (jamais carregar criadores ou posters da Escova 108 em páginas de Tênis, Brinquedo ou Pet).
    4. `.description-section` e `.product-details-block`: Devem conter especificações técnicas autênticas do produto em questão, NUNCA atributos genéricos ou herdados de outro item.
  - **Auditoria Automatizada Obrigatória Pré-Deploy**: Nenhum commit ou deploy pode subir sem passar pelo script de auditoria que valida se `h1.product-title == title == catalogo[id].nome`.'''

if target in content:
    content = content.replace(target, rule, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Atualizado ds/GEMINI.md com sucesso!")
else:
    print("Target nao encontrado!")

# Sincroniza para stone_shop_clone
dst = r'C:\Users\Dell\Downloads\stone_shop_clone\GEMINI.md'
with open(dst, 'w', encoding='utf-8') as f:
    f.write(content)
print("Sincronizado para stone_shop_clone/GEMINI.md com sucesso!")
