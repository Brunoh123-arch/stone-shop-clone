with open('c:/Users/Dell/Downloads/ds/GEMINI.md', 'r', encoding='utf-8') as f:
    doc = f.read()

new_clauses = """

### 7. REGRAS OBRIGATÓRIAS DE BLINDAGEM CONTRA VÍDEO ÚNICO E REPETIÇÃO DE UNBOXING

#### 7.1 PROIBIÇÃO DE CARROSSEL DE CRIADORES COM APENAS 1 VÍDEO
- **Tolerância Zero para Card Solitário**: É terminantemente PROIBIDO qualquer produto ser publicado com apenas 1 vídeo no carrossel de criadores.
- **Volume Canônico Obrigatório**: Todo produto DEVE conter um catálogo dinâmico de criadores (mínimo de 10 a 30 vídeos de criadores reais distintos, com rostos diferentes, cenas diferentes e arquivos MP4 distintos).
- Se o produto tiver poucos vídeos nativos do TikTok Shop, deve ser utilizado um pool temático de criadores reais do mesmo nicho para preencher o feed sem nunca deixar um card solitário.

#### 7.2 PROIBIÇÃO ABSOLUTA DE FOTOS DE UNBOXING REPETIDAS NO MESMO PRODUTO
- **Unicidade Estrita de Imagens de Review**: É expressamente PROIBIDO clonar ou repetir o mesmo arquivo de imagem em mais de um card de avaliação do mesmo produto.
- Cada foto exibida nas avaliações deve ser uma foto ÚNICA, capturada de ângulo ou cliente diferente.
- Auditoria Automatizada: Se um produto tiver 15 fotos de avaliação, devem existir 15 arquivos de imagem únicos e distintos (zero duplicatas).

#### 7.3 FIDELIDADE DO UNBOXING AO PRODUTO REAL ANUNCIADO
- **Tolerância Zero para Produto Trocado em Avaliações**: A foto do unboxing deve mostrar rigorosamente o produto físico do anúncio em ambiente doméstico real (exemplo: Projetor Natalino P111 deve mostrar o projetor natalino e os desenhos temáticos de Natal projetados, NUNCA imagem genérica de outro projetor como o HY300).
- Proibido reaproveitar fotos de outros produtos ou nichos para simular avaliação de comprador.
"""

if '7. REGRAS OBRIGATÓRIAS DE BLINDAGEM CONTRA VÍDEO ÚNICO' not in doc:
    doc += new_clauses
    with open('c:/Users/Dell/Downloads/ds/GEMINI.md', 'w', encoding='utf-8') as f:
        f.write(doc)
    print("Regras da Seção 7 cravadas com sucesso na GEMINI.md!")
else:
    print("Regras da Seção 7 já presentes na GEMINI.md.")
