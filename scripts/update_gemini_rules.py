# -*- coding: utf-8 -*-
with open(r'c:\Users\Dell\Downloads\ds\GEMINI.md', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = """2. **IMAGENS DE PRODUTO (SLIDES DO CARROSSEL PRINCIPAL)**:
   - **FONTE PRINCIPAL: TIKTOK SHOP**: Puxar as fotos oficiais de catálogo com fundo branco do anúncio do TikTok Shop via Playwright.
   - **FALLBACK OFICIAL: MERCADO LIVRE**: Se o anúncio do TikTok Shop não tiver fotos suficientes ou de boa qualidade, extrair as fotos oficiais de catálogo do anúncio do mesmo produto no **Mercado Livre** via Playwright.
   - **ZERO IMAGENS QUEBRADAS OU VAZIAS**: Todos os slides do carrossel (ex: 1/5) DEVEM carregar imagens reais, nítidas e válidas. Proibido subir arquivo corrompido, placeholder cinza ou link quebrado.

3. **AVALIAÇÕES E FOTOS DE UNBOXING DE CLIENTES**:
   - **FONTE PRINCIPAL: TIKTOK SHOP**: Fotos reais de unboxing de compradores na aba de avaliações do TikTok Shop.
   - **FALLBACK OFICIAL: MERCADO LIVRE**: Se o anúncio do TikTok Shop tiver poucas fotos de unboxing, extrair as fotos reais de compradores nas avaliações do **Mercado Livre** via Playwright.
   - **ZERO PRODUTO TROCADO**: A foto de unboxing deve ser rigorosamente do produto anunciado.
   - **ZERO FUNDO BRANCO EM REVIEWS**: Foto de review é de cliente em ambiente real (sala, cozinha, chão, desembalando)."""

new_block = """2. **IMAGENS DE PRODUTO (SLIDES DO CARROSSEL PRINCIPAL - MÍNIMO 4 A 8 SLIDES)**:
   - **PROIBIÇÃO DE SLIDER COM 1 FOTO SOLITÁRIA**: É terminantemente PROIBIDO produto com apenas 1 imagem no slider do topo (`1/1`). Todo produto DEVE conter entre 4 e 8 fotos oficiais de catálogo em alta resolução cobrindo ângulos variados (frente, verso, detalhes, dimensões, em uso).
   - **FONTE PRINCIPAL: TIKTOK SHOP**: Puxar as fotos oficiais de catálogo com fundo branco do anúncio do TikTok Shop via Playwright.
   - **FALLBACK OFICIAL: MERCADO LIVRE**: Se o anúncio do TikTok Shop não tiver fotos suficientes ou de boa qualidade, extrair as fotos oficiais de catálogo do anúncio do mesmo produto no **Mercado Livre** via Playwright.
   - **ZERO IMAGENS QUEBRADAS OU VAZIAS**: Todos os slides do carrossel (ex: 1/5) DEVEM carregar imagens reais, nítidas e válidas. Proibido subir arquivo corrompido, placeholder cinza ou link quebrado.

2.1. **GRADE DE VARIAÇÕES E SKUS (CORES, TAMANHOS, VOLTAGEM)**:
   - **COERÊNCIA VISUAL 1:1 ESTRITA**: Se o seletor possui botões de cores ("Preto", "Rosa", "Verde-Água", "Azul"), CADA botão DEVE exibir a miniatura correspondente àquela cor específica.
   - **TROCA ATIVA NO SLIDER**: Clicar na variação DEVE alterar a foto principal para a cor selecionada. É expressamente PROIBIDO botões com imagens genéricas, imagens repetidas para cores diferentes ou cores fantasmas sem estoque.

3. **AVALIAÇÕES E FOTOS DE UNBOXING DE CLIENTES (ZERO COMPRADOR/CENÁRIO REPETIDO)**:
   - **PROIBIÇÃO ABSOLUTA DE FATIAMENTO E REUSO DE COMPRADOR**: Cada avaliação com foto DEVE pertencer a um comprador físico e ambiente 100% único. É terminantemente PROIBIDO fatiar fotos do mesmo cliente/criança/sala (ex: a mesma menina sentada no sofá com a TV atrás) e distribuir em 2 ou mais avaliações fingindo serem compradores diferentes (`M**e C**o` e `A**e M**s`).
   - **COERÊNCIA RIGOROSA COM A VARIAÇÃO COMPRADA (`data-author-variation`)**: Se a avaliação diz que o cliente comprou "Preto Metalizado", as fotos do unboxing DEVEM mostrar o produto PRETO, e não verde ou rosa!
   - **FONTE PRINCIPAL: TIKTOK SHOP**: Fotos reais de unboxing de compradores na aba de avaliações do TikTok Shop.
   - **FALLBACK OFICIAL: MERCADO LIVRE**: Se o anúncio do TikTok Shop tiver poucas fotos de unboxing, extrair as fotos reais de compradores nas avaliações do **Mercado Livre** via Playwright.
   - **ZERO PRODUTO TROCADO**: A foto de unboxing deve ser rigorosamente do produto anunciado.
   - **ZERO FUNDO BRANCO EM REVIEWS**: Foto de review é de cliente em ambiente real (sala, cozinha, chão, desembalando).

3.1. **CARROSSEL DE CRIADORES (ZERO HTML HARDCODED E ZERO FLICKER)**:
   - **DIV VAZIA NO HTML**: A tag no HTML é SEMPRE `<div class="creators-section" id="creators-section"></div>` 100% vazia. É terminantemente PROIBIDO injetar `<div class="creator-card">` diretamente no HTML estático para evitar o flicker/flash onde outro produto aparece por 50ms antes do JavaScript rodar.
   - **POSTERS 1:1 EXTRAÍDOS VIA FFMPEG**: Toda capa estática de criador deve ser gerada compulsoriamente a partir do frame 1 do respectivo vídeo MP4. Proibido reaproveitar posters de outros produtos.
   - **CACHE-BUSTING GLOBAL MANDATÓRIO**: Todos os posters e mídias devem carregar carimbo de versão `?v=...` para anular a política de cache imutável (`Cache-Control: immutable`) dos CDNs."""

# Normaliza quebras de linha
text_norm = text.replace('\r\n', '\n')
old_norm = old_block.replace('\r\n', '\n')
new_norm = new_block.replace('\r\n', '\n')

if old_norm in text_norm:
    text_norm = text_norm.replace(old_norm, new_norm)
    with open(r'c:\Users\Dell\Downloads\ds\GEMINI.md', 'w', encoding='utf-8') as f:
        f.write(text_norm)
    print("[+] GEMINI.md atualizado com as novas regras soberanas de integridade total!")
else:
    print("[-] Bloco alvo nao encontrado em GEMINI.md!")
