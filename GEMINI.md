# Regra Global de Extração de Produtos TikTok Shop (Bruno CTO - Modo Zika Blindado)

> trigger: always_on quando o usuário enviar qualquer link do TikTok Shop (`https://shop.tiktok.com/...` ou `vt.tiktok.com/...`) ou solicitar novos produtos/atualizações.
> Arquivo Mestre de Regras e Diretrizes do Fluxo: `c:\Users\Dell\Downloads\ds\GEMINI.md`

Sempre que o usuário enviar um link de produto do TikTok Shop de QUALQUER NICHO (Calçados, Vestuário, Casa, Eletrodomésticos, Praia, Eletrônicos, etc.), execute o fluxo com padrão de excelência soberano baseado no produto de referência canônico: **o produto do chinelo/sandália (`pages/produto-104.html`)**:

---

### Doutrina Fundamental: Extração de Mídia e Conteúdo via MCP Playwright (TikTok Shop First + Mercado Livre Fallback)

> [!IMPORTANT]
> **REGRA DE OURO E OBRIGATORIEDADE ABSOLUTA DO PROFILE 42 (MAX DIGITAL)**:
> Toda e qualquer extração via Playwright DEVE ser executada OBRIGATORIAMENTE conectada ao Chrome oficial com o perfil **Profile 42** da conta **Max Digital (`kaiobrunocastro12@gmail.com`)**.
> É TERMINANTEMENTE PROIBIDO rodar instâncias anônimas, efêmeras ou headless genéricas que não carreguem a sessão e os cookies da conta Max Digital. O navegador deve utilizar o perfil real para evitar bloqueios de bot e acessar os dados reais de compradores.

Toda e qualquer extração DEVE ser realizada OBRIGATORIAMENTE através do **MCP Playwright** conectado ao Chrome oficial no **Profile 42**:

1. **VÍDEOS DE CRIADORES (30+ VÍDEOS)**:
   - **FONTE EXCLUSIVA: TIKTOK / TIKTOK SHOP**:
   - Puxados 100% de criadores reais no TikTok/TikTok Shop demonstrando o produto exato do título.
   - Proibido puxar vídeos de YouTube ou outras plataformas.

2. **IMAGENS DE PRODUTO (SLIDES DO CARROSSEL PRINCIPAL - MÍNIMO 4 A 8 SLIDES)**:
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
   - **CACHE-BUSTING GLOBAL MANDATÓRIO**: Todos os posters e mídias devem carregar carimbo de versão `?v=...` para anular a política de cache imutável (`Cache-Control: immutable`) dos CDNs.

4. **DESCRIÇÃO E FICHA TÉCNICA**:
   - **FONTE PRINCIPAL: TIKTOK SHOP**: Texto e especificações do vendedor oficial.
   - **FALLBACK OFICIAL: MERCADO LIVRE**: Se a descrição no TikTok Shop for incompleta, enriquecer com a ficha técnica oficial do Mercado Livre via Playwright.

---

### 1. REGRA INEGOCIÁVEL: PROIBIÇÃO ABSOLUTA DE PLATAFORMAS EXTERNAS E ATALHOS DE FFMPEG
- **FONTE EXCLUSIVA: TIKTOK E TIKTOK SHOP WEB VIA MCP PLAYWRIGHT**:
  - Toda e qualquer mídia, informação e vídeo DEVE ser extraída navegando com o perfil logado (**Max Digital / Profile 42**) via MCP Playwright diretamente no TikTok / TikTok Shop.
  - Zero scraping de YouTube, zero scraping de sites externos.
- **TOLERÂNCIA ZERO PARA ATALHOS DE FFMPEG/SCREENSHOTS DE VÍDEO**:
  - É expressamente PROIBIDO fatiar vídeos com `ffmpeg` (ex: `ffmpeg -ss ... -vframes 1`) para gerar imagens de clientes ou fingir que são fotos de unboxing!
  - É expressamente PROIBIDO inventar comentários em scripts Python (`review_comments = [...]`).
- **EXTRAÇÃO OBRIGATÓRIA DIRETO DO LINK NO NAVEGADOR LOGADO**:
  - Acessar a página oficial do produto (`shop.tiktok.com/pdp/...` ou `vt.tiktok.com/...`).
  - Abrir a seção/aba de **Avaliações dos Clientes**.
  - Puxar diretamente do anúncio:
    1. **As fotos reais de unboxing** que os compradores enviaram no anúncio (download direto dos links originais).
    2. **O texto exato** que o comprador escreveu no anúncio oficial em português.
    3. **A foto de perfil (avatar)** real do cliente (com gênero rigorosamente coincidente).
    4. **O nome mascarado real** oficial (`K**s`, `M**a S.`, `V**a L**a R**g`).
    5. **A data e a variação exata** adquirida pelo cliente.
    6. **A descrição original** cadastrada pelo vendedor oficial.

---

### 1.1 EXCLUSIVIDADE ABSOLUTA TIKTOK / TIKTOK SHOP VIA MCP PLAYWRIGHT
- **Tolerância Zero a Plataformas Externas**:
  - Nunca busque dados em OLX, YouTube, Magalu ou qualquer outra plataforma não autorizada.
  - Toda a extração é feita EXCLUSIVAMENTE pelo TikTok e TikTok Shop Web conectado ao **Profile 42** no Playwright MCP (com fallback de imagens oficiais no Mercado Livre apenas para catálogo se necessário).
- **Obrigatoriedade de Imagem Real do Produto Comprado (Unboxing)**:
  - Cada produto anunciado DEVE conter OBRIGATORIAMENTE avaliações de compradores com fotos reais do produto recebido e desembalado (no chão da sala, na mesa, na bancada, na mão, em ambiente doméstico real).
  - É expressamente proibido produto com avaliações sem imagens reais ou com fotos de estúdio de catálogo com fundo branco.
- **Tolerância Zero para Fundo Branco de Catálogo / Estúdio em Avaliações**:
  - As fotos de avaliações de clientes devem ser exclusivamente as fotos reais de unboxing enviadas pelos compradores no próprio anúncio do TikTok Shop.
- **Avatares 100% Oficiais do TikTok CDN & Coerência Rigorosa de Gênero (Avaliações e Criadores)**:
  - É terminantemente PROIBIDO o uso de avatares aleatórios da internet, bancos de imagens gratuitos/free, ilustrações, cartoons, fotos de estúdio ou pessoas geradas por IA.
  - 100% dos avatares de clientes nas avaliações E dos criadores nos vídeos de criadores (`js/videos-criadores.js`) DEVEM ser fotos de pessoas físicas reais extraídas do CDN oficial do TikTok / TikTok Shop (`img/reviews-avatars/tiktok_real/` ou links CDN TikTok).
  - **Coerência Estrita de Gênero**: Se o nome for de mulher (ex: Maria, Fernanda, Juliana, Camila), o avatar DEVE ser obrigatoriamente a foto de uma mulher real. Se o nome for de homem (ex: Rodrigo, Carlos, Marcos, Lucas), o avatar DEVE ser obrigatoriamente a foto de um homem real. Essa regra é soberana tanto para os comentários quanto para os vídeos de criadores!

---

### 1.2 REGRA SOBERANA: PROIBIÇÃO ABSOLUTA DE CONTAMINAÇÃO DE NICHO / MÍDIA DE OUTRO PRODUTO
- **TOLERÂNCIA ZERO PARA PRODUTO TROCADO**:
  - Toda e qualquer mídia (arquivos de vídeo MP4, capas/posters dos criadores, fotos de unboxing, comentários e avatares) DEVE pertencer RIGOROSAMENTE ao produto anunciado no título da página!
  - É **expressamente proibido** reaproveitar vídeos ou fotos de outros produtos ou nichos (exemplo de amadorismo inaceitável: colocar vídeos de ar-condicionado portátil ou ventilador umidificador em página de churrasqueira giratória!).
  - Se a página é da **Churrasqueira Elétrica Arke Vitta Smart 5 Espetos**, 100% dos vídeos de criadores DEVEM mostrar a churrasqueira giratória vertical Arke com porta de vidro curvo assando carne nos espetos.
  - Toda mídia inserida no projeto DEVE ser validada visualmente antes de ser linkada no código e enviada para produção.

---


---

### 1.3 REGRA MANDATÓRIA: AUDITORIA OFICIAL DE PRODUTOS SEM FOTOS DE UNBOXING E AVATARES

#### A. LISTA OFICIAL DOS 75 PRODUTOS SEM IMAGEM DO PRODUTO COMPRADO (PENDÊNCIA DE EXTRAÇÃO REAL)
Estes 75 produtos possuem apenas avaliações em texto ou imagens sintéticas/catálogo falsas. É **OBRIGATÓRIO** extrair fotos reais de unboxing (no chão, mesa, bancada, mão ou ambiente doméstico desembalado) diretamente do TikTok Shop ou Mercado Livre via MCP Playwright no Profile 42:

| ID | Arquivo | Reviews | Título do Produto |
|:---:|:---|:---:|:---|
| **16** | `pages/produto-16.html` | 45 | Churrasqueira Resistente Modelo Rodeio Bacia Esmaltada Mor |
| **19** | `pages/produto-19.html` | 37 | Tablet Vision TAB 7 Stitch + Capa e Bolsa Positivo |
| **20** | `pages/produto-20.html` | 54 | Bicicleta Aro 29 GT Sprint MX7 24V MTB |
| **22** | `pages/produto-22.html` | 15 | Colchão Inflável Suporta 300kg Casal Bestway |
| **23** | `pages/produto-23.html` | 47 | Conjunto De 24 Potes Herméticos Croix Com Tampa E Trava |
| **24** | `pages/produto-24.html` | 52 | Triciclo Infantil 4 em 1 Multifuncional Kababy |
| **25** | `pages/produto-25.html` | 56 | Bicicleta Aro 20 Bmx infantil GottBikes |
| **26** | `pages/produto-26.html` | 56 | Carrinho de Bebê Guarda Chuva Passeio Leve e Dobrável |
| **28** | `pages/produto-28.html` | 56 | Kit Mochila Rebecca Bonbon Juvenil |
| **32** | `pages/produto-32.html` | 56 | Chuveiro Acqua Duo Lorenzetti BIVOLT |
| **34** | `pages/produto-34.html` | 55 | Lava Louças Praxis Portátil LLPP Semi-Automática |
| **38** | `pages/produto-38.html` | 42 | Kit Lattafa Yara Collection Feminino Edp 4x25ml |
| **39** | `pages/produto-39.html` | 15 | Secador de Cabelos Philco PSC3500 4 em 1 Dobrável |
| **40** | `pages/produto-40.html` | 48 | Micro-ondas Mondial Mo-01-21-e 1200w 21L |
| **41** | `pages/produto-41.html` | 48 | Fritadeira Air Fryer Forno Oven 12L Mondial |
| **45** | `pages/produto-45.html` | 53 | Prancha Pro 480 Turbo MQ Professional Bivolt |
| **46** | `pages/produto-46.html` | 53 | Panela de Pressão Elétrica Electrolux Rita Lobo 6L |
| **47** | `pages/produto-47.html` | 54 | Extratora Higienizadora Portátil Colchão Sofá |
| **48** | `pages/produto-48.html` | 30 | Panificadora Automática Mondial Master Bread 220V |
| **49** | `pages/produto-49.html` | 35 | Detergente Limpador Para Extratoras Limpa E Extrai 1L Wap |
| **50** | `pages/produto-50.html` | 64 | Lava e Seca Midea Master Clean Smart 11kg Titanium |
| **52** | `pages/produto-52.html` | 64 | Pad 11 Geração A16 256GB Wi-fi Tela 11pol |
| **53** | `pages/produto-53.html` | 64 | Starlink V4 Internet Satélite Wi-fi 6 Padrão Anatel |
| **54** | `pages/produto-54.html` | 64 | Purificador Eletrônico Compacto Efficient Bivolt (PE11X) |
| **55** | `pages/produto-55.html` | 36 | SWITCH DESBLOQUEADO + 10 JOGOS + MicroSD 128 GB |
| **57** | `pages/produto-57.html` | 46 | Caixa de som Joog One Hifi J 200w 2 Mic s/fio |
| **58** | `pages/produto-58.html` | 46 | Caixa de som Echo Dot 5 geração |
| **59** | `pages/produto-59.html` | 46 | Mini Internet rápida Via Satélite Antena Original |
| **60** | `pages/produto-60.html` | 15 | Caixa Som Sabala DR-908 Potência |
| **61** | `pages/produto-61.html` | 15 | Caixa de Som Joog Break X1 Tela Touch 13 800W |
| **63** | `pages/produto-63.html` | 18 | Smartwatch Redmi Watch 5 Lite GPS Preto |
| **64** | `pages/produto-64.html` | 56 | Bateria Auxiliar De Partida Portátil Bomba De Ar |
| **65** | `pages/produto-65.html` | 56 | Sofá 3 Lugares Retrátil e Reclinável Cama inBox 2,00m |
| **68** | `pages/produto-68.html` | 64 | Jogo de Panelas Cerâmica Kit 5 Peças Antiaderente |
| **70** | `pages/produto-70.html` | 43 | Secadora de Roupa Mueller Solaris 8 kg |
| **72** | `pages/produto-72.html` | 43 | Jogo de Panelas 13 Peças Ferro Fundido Esmaltado |
| **73** | `pages/produto-73.html` | 43 | Caixa De Som Bluetooth Waaw Hyperboom 1000 |
| **74** | `pages/produto-74.html` | 43 | Camisa Seleção Brasil Masculina Oficial |
| **75** | `pages/produto-75.html` | 43 | Kit 10 Camisetas Dry Fit Masculina |
| **76** | `pages/produto-76.html` | 43 | Aparelho Jogo De Jantar 30 Peças Orgânico |
| **78** | `pages/produto-78.html` | 43 | Extratora Portátil Spot Cleaner Wap 1400W |
| **79** | `pages/produto-79.html` | 43 | Lava Louças Praxis Portátil LLPP Semi-Automática |
| **80** | `pages/produto-80.html` | 43 | Panificadora 19 Programas Gallant 600w 127v |
| **81** | `pages/produto-81.html` | 43 | Caixa de Som WAAW Hyperboom 1000 180W |
| **82** | `pages/produto-82.html` | 43 | Lava e Seca 11kg Hisense 11 Programas |
| **83** | `pages/produto-83.html` | 43 | Caixa De Som Joog break X1 Tela 13,1 |
| **84** | `pages/produto-84.html` | 43 | Panificadora 19 Programas Gallant 600w Preta |
| **85** | `pages/produto-85.html` | 43 | Caixa De Som Karaokê Joog X2 300w Tela 10,1 |
| **87** | `pages/produto-87.html` | 15 | KISSMELADY calça mom jeans com cinto |
| **88** | `pages/produto-88.html` | 15 | Conjunto Feminino de Trabalho Alfaiataria |
| **89** | `pages/produto-89.html` | 15 | Kit panelas de ferro esmaltadas luxo 18 peças |
| **91** | `pages/produto-91.html` | 15 | Pipoqueira Classic Retrô Misturador Automático |
| **92** | `pages/produto-92.html` | 15 | Conjunto de Panelas de Ferro Fundido Esmaltado 10 |
| **94** | `pages/produto-94.html` | 15 | Bicicleta Bike Ergometrica Spinning 120kg |
| **95** | `pages/produto-95.html` | 15 | YESOP Máquina De Gelo Portátil Preto 12kg/dia |
| **96** | `pages/produto-96.html` | 15 | Aparelho de Jantar Oxford Ryo Maresia 30 Peças |
| **97** | `pages/produto-97.html` | 15 | Jogo de Jantar Canyon Porcelana Decorada 20 Peças |
| **98** | `pages/produto-98.html` | 15 | Conjunto de 12 Copos De Cristal Long Drink |
| **99** | `pages/produto-99.html` | 15 | Kit Camisa Seleção Portugal Masculina |
| **100** | `pages/produto-100.html` | 15 | Apple iPhone 15 / 15 Plus / 15 Pro / 15 Pro Max |
| **101** | `pages/produto-101.html` | 15 | Pneus Pirelli (Retificado: foto de catálogo sem unboxing real) |
| **102** | `pages/produto-102.html` | 15 | Scooter Elétrica TUI 1000w 2 Lugares |
| **103** | `pages/produto-103.html` | 15 | Vestido longo feminino costas nua fenda |
| **105** | `pages/produto-105.html` | 15 | Projetor HY300 Original Portátil Smart Android |
| **106** | `pages/produto-106.html` | 15 | Body Modelador Cinta Alta Compressão Invisível |
| **107** | `pages/produto-107.html` | 15 | Mini Aspirador de Pó Sem Fio Portátil e Soprador |
| **108** | `pages/produto-108.html` | 15 | Escova Secadora e Modeladora 5 em 1 Multifuncional |
| **109** | `pages/produto-109.html` | 15 | Modelador de Cachos Automático Sem Fio Bateria USB |
| **110** | `pages/produto-110.html` | 15 | Tênis Kappa Pulse RX Amortecimento Corrida |
| **111** | `pages/produto-111.html` | 15 | Projetor LED Natalino 16 Desenhos Temáticos USB |
| **112** | `pages/produto-112.html` | 15 | Brinquedo Pista Montanha-Russa de Patinhos |
| **113** | `pages/produto-113.html` | 15 | Comedouro Cachorro e Gato Elevado Duplo Acrílico |
| **120** | `pages/produto-120.html` | 15 | Sofá Retrátil e Reclinável 3 Lugares 2,10m Suede |
| **124** | `pages/produto-124.html` | 15 | Livro Infantil Interativo Bilíngue Falante |

#### B. DIRETRIZ ESTRITA DE AVATARES E COERÊNCIA DE GÊNERO (AVALIAÇÕES E CRIADORES)
1. **Avatares 100% Homologados do TikTok CDN**: Proibição de avatares free da internet, ilustrações, cartoons ou pessoas geradas por inteligência artificial. Devem ser 100% fotos de compradores e criadores reais extraídas do CDN oficial do TikTok (`img/reviews-avatars/tiktok_real/`).
2. **Coerência Estrita de Gênero Obrigatória**:
   - **Nome Feminino = Avatar Feminino**: Nomes como Maria, Camila, Juliana, Beatriz, Larissa, Vanessa, Renata, Ana, Bruna DEVEM receber OBRIGATORIAMENTE avatares de mulheres reais.
   - **Nome Masculino = Avatar Masculino**: Nomes como Rodrigo, Carlos, Thiago, Matheus, Lucas, Danilo, Arthur, Pedro, Gustavo DEVEM receber OBRIGATORIAMENTE avatares de homens reais.
   - Esta regra se aplica **TANTO para as avaliações dos clientes quanto para os perfis dos criadores** em `js/videos-criadores.js`!
3. **Proibição de Perfis Comerciais e Canais em Vídeos de Criadores**:
   - É terminantemente **PROIBIDO** cadastrar criadores com nomes de canais, marcas ou lojas (ex: "Aiwa Brasil Oficial", "Lar Organizado da Lu", "Chef na Air Fryer", "Studio Hair Vip", "Turbo Shop").
   - Todos os criadores devem ser **pessoas físicas reais** com @username de usuário autêntico e rosto nítido de pessoa humana real no avatar!



#### C. DIRETRIZ SOBERANA DE QUALIDADE DAS AVALIAÇÕES (REVIEWS DO TIKTOK SHOP)
1. **Coerência Estrita da Variação Comprada (`data-author-variation`)**:
   - É expressamente proibido atribuir variações de outro nicho nas avaliações (ex: colocar voltagem "110V" em calçado ou mochila, ou numeração de calçado em eletrodoméstico).
   - Toda avaliação deve exibir exclusivamente opções que existam na grade de variações do próprio produto.
2. **Proporção Mínima de 3 a 5 Reviews com Fotos Reais de Unboxing**:
   - Todo produto anunciado DEVE conter no topo da seção de avaliações pelo menos 3 a 5 cards com imagens reais do produto recebido/desembalado.
3. **Expurgo de Linguagem de Marketplaces Concorrentes (Shopee / AliExpress)**:
   - Proibido qualquer texto que mencione "shopee", "moedas", "pontos", ou formulários técnicos como "qualidade do produto:...", "desempenho:...".
   - O texto deve refletir o padrão autêntico do TikTok Shop: entrega rápida da Stone Shop, fidelidade ao anúncio e satisfação de uso real.
4. **Distribuição Realista de Avaliações (Rating Dynamics: 90% 5★ / 10% 4★)**:
   - Proibido manter 100% das avaliações com nota 5 estrelas robótica.
   - De 5% a 10% das avaliações devem conter 4 estrelas com elogios reais e humanizados.
5. **Datas Recentes e Dinâmicas**:
   - Avaliações devem conter datas dos últimos 30 a 45 dias, evitando datas defasadas de anos anteriores.
6. **Formato e Proporção das Fotos de Unboxing**:
   - As fotos de compradores devem estar em formato vertical ou quadrado de celular (1:1 ou 4:5), sem distorção ou esticamento.


### 3. Vídeos de Criadores (30+ Vídeos Reais, ZERO Repetição e AUTOPLAY NO CARROSSEL)
- **POSICIONAMENTO SOBERANO E IRREFUTÁVEL NO LAYOUT**:
  - A seção de Vídeos de Criadores (`<div id="creators-section" class="creators-section"></div>`) DEVE ficar SEMPRE posicionada OBRIGATORIAMENTE logo abaixo de `Proteção do cliente` e imediatamente ANTES de `Avaliações dos clientes`!
  - **PROIBIDO INSERIR O CARD DA STONE SHOP NESSE LOCAL**: Nunca substitua ou intercale o card da Stone Shop entre Proteção do Cliente e Avaliações. Aquele local pertence única e exclusivamente ao carrossel de vídeos de criadores do produto!
- **OBRIGATÓRIO E IRREFUTÁVEL PUXAR VÍDEOS DE CRIADORES SEMPRE**:
  - É obrigatório puxar vídeos de criadores SEMPRE em todo produto anunciado.
  - Os vídeos DEVEM ser rigorosamente do produto real anunciado, extraídos do TikTok / TikTok Shop.
- **Quantidade Canônica**: Mínimo de 30 vídeos de criadores diferentes (`Vídeos de criadores (30+)`).
- **PROIBIÇÃO ABSOLUTA DE VÍDEOS REPETIDOS**:
  - Cada um dos 30+ vídeos DEVE ser de um criador diferente, com rosto diferente, cena diferente e arquivo MP4 diferente.
  - Zero repetição de link do Catbox, zero repetição de poster e zero repetição de @username.
  - É terminantemente PROIBIDO clonar 1 ou 2 vídeos em múltiplos cards para tentar fingir volume.
- **DESACOPLAMENTO TOTAL ENTRE VÍDEO DA DESCRIÇÃO E CARROSSEL DE CRIADORES**:
  - O vídeo demonstrativo do produto exibido na seção de descrição (`.product-video-block` / `#tt-product-video`) NUNCA PODE SER IGUAL a nenhum vídeo do carrossel de criadores.
  - Devem ser mídias 100% distintas: a descrição apresenta o produto oficial do vendedor, enquanto o carrossel exibe os criadores reais testando e usando o produto no TikTok.
- **AUTOPLAY AUTOMÁTICO OBRIGATÓRIO NO CARROSSEL (PADRÃO TIKTOK SHOP)**:
  - Os cards de criadores (`.creator-card`) NÃO podem ser imagens estáticas paradas!
  - Cada card renderiza uma tag `<video class="creator-preview-vid" src="..." poster="..." muted loop playsinline webkit-playsinline>` rodando em background.
  - Implementação obrigatória de `IntersectionObserver`: assim que o carrossel entra na viewport do usuário, os vídeos visíveis iniciam automaticamente a reprodução em loop mudo (`muted=true, playsinline=true`), conferindo dinamismo e efeito de "live feed" idêntico ao aplicativo oficial do TikTok Shop.
- **Alinhamento Estrito ao Produto**:
  - O vídeo DEVE demonstrar exatamente o produto anunciado (ex: cadeira de praia em kit de praia, aspirador em aspirador, etc.).
  - **TOLERÂNCIA ZERO para vídeos de outros nichos** (ex: colocar ar-condicionado em praia ou churrasqueira em tênis).
- **Hospedagem e Posters**:
  - Todos os vídeos MP4 hospedados no Catbox (`https://files.catbox.moe/...`) ou servidos em streaming HTTP 206 local em `videosprodutos/`.
  - Posters sincronizados e nítidos do frame inicial sem marca d'água em `img/posters-[nicho]/`.
- **Integração no `js/videos-criadores.js`**:
  - Os datasets dos produtos (`CREATORS_[SLUG]_[ID]`) DEVEM estar declarados SEMPRE DENTRO do closure da IIFE, antes de `initCarousel()`, com o chaveamento explícito por `prodId`.

---

### 4. A Loja Oficial Soberana: SEMPRE STONE SHOP
- **Identidade Única e Inegociável da Empresa**:
  - A loja é SEMPRE a **Stone Shop**!
  - **Avatar**: Boneco mascote oficial da Stone Shop (`../logo.png`).
  - **Nome**: `Stone Shop` acompanhado do selo azul de verificado oficial.
  - **Vendas**: `112.2K vendido(s)`.
  - **Métricas de Atendimento**: `95% responde em 24 horas · 99% envios pontuais`.
  - **Botão Visitar**: Redireciona para a página principal (`../index.html`).
  - **Seção "Mais desta loja"**: Cupom clássico "Até 74% de desconto - Termina em 1 dia" + carrossel com produtos do catálogo.
- **PROIBIÇÃO ABSOLUTA DE LOJAS PARALELAS**:
  - Nunca crie nem injete cards avulsos de lojas concorrentes/fornecedores (`seller-profile-card` de "Mor", "HQ", "Hisense", etc.) que dupliquem ou briguem com o widget soberano da Stone Shop.

---

### 5. Regra de Ouro: GUIA DE TAMANHOS OFICIAL (IMAGEM REAL DO ANÚNCIO - PROIBIDO GERAR/SINTETIZAR)
- **EXTRAÇÃO OBRIGATÓRIA DA IMAGEM REAL**: A imagem do Guia de Tamanhos DEVE ser extraída OBRIGATORIAMENTE da imagem oficial original cadastrada pelo vendedor no anúncio do **TikTok Shop** (via MCP Playwright no Profile 42) ou no anúncio do mesmo produto no **Mercado Livre** (Fallback oficial).
- **PROIBIÇÃO ABSOLUTA DE GERAR TABELAS SINTÉTICAS OU HTML (`<table>`)**: É terminantemente PROIBIDO gerar imagens sintéticas via scripts (PIL/Python), criar tabelas HTML (`<table>`) ou desenhar guias artificiais! O cliente deve ver a arte/tabela gráfica real original do fabricante/vendedor.
- **IMAGEM GRÁFICA REAL NA DESCRIÇÃO**: Nos produtos de Vestuário, Moda e Calçados, onde constar na descrição o título `<strong>Guia de Tamanhos Recomendado:</strong>`, é **OBRIGATÓRIO** renderizar LOGO ABAIXO a imagem gráfica real oficial de medidas (`<img src="../img/guia-tamanhos-XXX.png" class="size-guide-img" alt="Guia de Tamanhos Oficial" style="max-width:100%; border-radius:8px; margin:12px 0; display:block;">`).
- **ESPELHAMENTO AUTOMÁTICO 1:1 (SINGLE SOURCE OF TRUTH ENTRE DESCRIÇÃO E SLIDER)**: A imagem do Guia de Tamanhos colocada na descrição (`.size-guide-img`) é a FONTE ÚNICA SOBERANA. O alternador do slider `[1/X] | [Tamanho]` e o modal de guia de tamanhos (`openSizeGuideModal()`) DEVEM buscar e espelhar dinamicamente a EXATA MESMA imagem da descrição (mesmo `src`, mesmo arquivo e mesmo cache-buster). Se você alterar a imagem na descrição, ela deve refletir instantaneamente tanto no slider quanto no modal sem qualquer divergência!
- **PROIBIÇÃO DE TEXTOS DUPLICADOS DE MEDIDAS**: Se a imagem gráfica oficial do Guia de Tamanhos já estiver presente na descrição, é TERMINANTEMENTE PROIBIDO listar tamanhos e centímetros em texto/bullets (ex: "• 33/34 — 22,5 cm"). A imagem gráfica oficial é soberana, autoexplicativa e evita poluição visual redundante.
- **ALTERNADOR NATIVO NO CARROSSEL ([1/X] | [Tamanho])**: No canto inferior do slider de fotos, os produtos com tamanho devem renderizar o botão alternador oficial do TikTok Shop, permitindo alternar instantaneamente entre as fotos de catálogo e a imagem real do guia de medidas em tela cheia com fundo branco.
- **LINK NO MODAL DE VARIAÇÕES (`Guia de tamanhos >`)**: Ao lado da seleção de tamanho no modal de compra, o link deve abrir a imagem gráfica oficial de medidas em alta resolução.
- **OMISSÃO ABSOLUTA EM ITENS NÃO-VESTUÁRIO**: Se o produto NÃO for de vestuário ou calçado (eletrônicos, casa, ferramentas, praia, brinquedos), OMITIR O BLOCO E O TOGGLE POR COMPLETO! A página transita direto de `Detalhes` para `Descrição`.

---

### 6. Descrição Oficial com Expansor Fade-Out
- Extrair o texto exato cadastrado pelo vendedor no anúncio oficial do TikTok Shop (destaques, itens da embalagem, especificações).
- Container `.description-expandable-container` com altura inicial de ~98px.
- Gradiente translúcido suave `.desc-fade-overlay`.
- Botão centralizado com ícone SVG: `Ver mais ∨` que expande para `Ver menos ⌃`.

---


### REGRA MANDATÓRIA DE CONTA E PROFILE DO CHROME (Soberana e Exclusiva)
- **Perfil Oficial Único e Inegociável**: **kaiobrunocastro12@gmail.com** (Pasta no Chrome: **Profile 42**).
- **USO MANDATÓRIO DO PLAYWRIGHT SEMPRE**: Toda automação, navegação no TikTok Shop, busca de produtos, extração de descrições, comentários e fotos DEVE ser executada obrigatoriamente via Playwright conectado ao Chrome oficial no **Profile 42**.
- **PROIBIÇÃO DE TROCA DE PERFIL**: É terminantemente proibido tentar conectar, extrair dados ou testar qualquer outro profile (Profile 95, Profile 87, Profile 1, etc.). Toda navegação, busca no TikTok Shop, verificação de anúncios e extração de avaliações DEVE ocorrer exclusivamente através do perfil oficial **kaiobrunocastro12@gmail.com (Profile 42)**.
- **NAVEGADOR VISÍVEL**: Rodar o Playwright com interface gráfica visível (`headless=False` ou conexão CDP ao Chrome nativo aberto pelo usuário) para que toda a navegação e extração de dados ocorra de forma transparente na tela.

### 8. Integridade do DOM, Sincronização e Deploy:
- Tag depth rigorosamente igual a 0 (`diff: 0`), sem tags malformadas ou vazamentos visuais na tela.
- Atualizar cache busters globais via `python scripts/update_cache_buster.py`.
- Pipeline de padronização blindada centralizado em `scripts/pipeline_padronizacao_blindada.py`:
  - 100% imagens oficiais de catálogo (fundo branco 1000x1000, JPEG RGB, sem cortes bizarros).
  - 100% criadores reais do produto anunciado (zero produto trocado, zero iPads em celulares, zero Joog em Sabala).
  - 100% fotos de unboxing genuínas de compradores (no chão da sala, na mesa, desembalando na mão, ZERO capturas de thumbnails com texto de YouTube/TikTok).
  - 100% avatares de pessoas físicas reais (ZERO logos, cartoons ou discrepância de gênero).
  - Validação visual OBRIGATÓRIA no Playwright / Chrome antes de qualquer entrega.
- Deploy direto de produção na Vercel da pasta raiz `ds/` via `npx vercel --prod --yes` com alias soberano: `https://stoneshopclone.vercel.app`.
- **PROIBIDO ENVIAR LOCALHOST**: Sempre entregar HTTPS oficial da Vercel.


---

### 6. DOUTRINA MANDATÓRIA DE AMARRAÇÃO TOTAL POR ID CANÔNICO (`prodId`) E VÍDEOS DE CRIADORES

#### 6.1 AS 10 AMARRAÇÕES OBRIGATÓRIAS DE ID NO ECOSSISTEMA
Para blindar o sistema contra colisões, contaminação de nicho, vazamento de dados e falhas em rastreamento/checkout, o identificador canônico `prodId` DEVE ser o Single Source of Truth obrigatório em 10 pontos:

1. **Objeto Global da Página**: Cada `pages/produto-X.html` DEVE conter no HTML `window.PRODUTO_ATUAL = { "id": X, "nome": "...", "preco": ... }` com `id` estritamente idêntico ao número do arquivo.
2. **Catálogo Mestre (`js/catalogo.js`)**: Indexação unívoca por `id` numérico em `PRODUTOS_CATALOGO`.
3. **Vídeos de Criadores (`js/videos-criadores.js`)**: Seleção soberana via `switch (prodId)` com case dedicado para cada produto e fallback seguro.
4. **Shopping Anchor Tag no Player**: O player de vídeos de criadores em tela cheia DEVE renderizar a etiqueta oficial de compra do TikTok Shop (`.tt-product-anchor`) com o nome do produto, preço e `data-product-id="X"`. O clique na etiqueta abre o checkout imediato do produto.
5. **Modal de Seleção de Variações (`openSkuModal`)**: Disparado com passagem explícita de `prodId` para nunca carregar SKU residual em cache.
6. **Carrinho e LocalStorage**: Itens indexados por `item.id === prodId`.
7. **APIs de Pagamento Pix (`/api/gerar-pix` e `/api/check-pix`)**: Payload com `produto_id: X` para conciliação bancária unívoca.
8. **Arquivos Físicos de Avaliação no Disco (`img/`)**: Nomenclatura atrelada ao ID (`review-{prodId}-real-{n}.jpg`).
9. **Produtos Relacionados ("Você também pode gostar")**: Exclusão mandatória do próprio produto na vitrine de recomendados (`filter(p => p.id !== prodId)`).
10. **Pixels de Conversão (TikTok Pixel / CAPI / Meta)**: Disparo de `ViewContent` e `InitiateCheckout` com `content_id: prodId`.

#### 6.2 SAÚDE E HEALTHCHECK DE MÍDIA (VÍDEOS E FOTOS)
1. **Tolerância Zero a Arquivos 0 Bytes / Corrompidos**: Todo vídeo linkado DEVE ter tamanho real (> 500KB) e responder com HTTP 200/206 válido.
2. **Desacoplamento Rigoroso**: O vídeo de demonstração oficial da descrição (`#tt-product-video`) NUNCA pode ser repetido em nenhum card do carrossel de criadores.
3. **Autoplay Mobile Garantido**: Tags `<video>` de preview e demonstração DEVEM possuir `muted`, `playsinline`, `webkit-playsinline`, `autoplay` e `loop`.


### 7. REGRAS OBRIGATÓRIAS DE BLINDAGEM CONTRA VÍDEO ÚNICO E REPETIÇÃO DE UNBOXING

#### 7.1 PROIBIÇÃO DE CARROSSEL DE CRIADORES COM APENAS 1 VÍDEO
- **Tolerância Zero para Card Solitário**: É terminantemente PROIBIDO qualquer produto ser publicado com apenas 1 vídeo no carrossel de criadores.
- **Volume Canônico Obrigatório**: Todo produto DEVE conter um catálogo dinâmico de criadores (mínimo de 10 a 30 vídeos de criadores reais distintos, com rostos diferentes, cenas diferentes e arquivos MP4 distintos).
- Se o produto tiver poucos vídeos nativos do TikTok Shop, deve ser utilizado um pool temático de criadores reais do mesmo nicho para preencher o feed sem nunca deixar um card solitário.

#### 7.2 PROIBIÇÃO ABSOLUTA DE FOTOS DE UNBOXING REPETIDAS NO MESMO PRODUTO
- **Unicidade Estrita de Imagens de Review**: É expressamente PROIBIDO clonar ou repetir o mesmo arquivo de imagem em mais de um card de avaliação do mesmo produto.
- Cada foto exibida nas avaliações deve ser uma foto ÚNICA, capturada de ângulo ou cliente diferente de comprador real do anúncio no TikTok Shop ou Mercado Livre.
- **TOLERÂNCIA ZERO PARA PRINTS/SCREENSHOTS DE VÍDEOS**: É expressamente PROIBIDO fatiar vídeos de criadores ou do produto via `ffmpeg` para gerar imagens de clientes ou fingir que são fotos de unboxing!
- **TOLERÂNCIA ZERO PARA THUMBNAILS DE BAIXA RESOLUÇÃO DO GOOGLE**: As fotos de unboxing devem ser exclusivamente as fotos reais de alta definição enviadas pelos compradores no próprio anúncio do TikTok Shop ou Mercado Livre via MCP Playwright no Profile 42.
- **Auditoria Automatizada Obrigatória**: Zero arquivos duplicados no mesmo HTML. Se houver 4 fotos de unboxing, devem ser 4 arquivos 100% distintos de 4 compradores diferentes.

#### 7.3 FIDELIDADE DO UNBOXING AO PRODUTO REAL ANUNCIADO
- **Tolerância Zero para Produto Trocado em Avaliações**: A foto do unboxing deve mostrar rigorosamente o produto físico do anúncio em ambiente doméstico real (exemplo: Projetor Natalino P111 deve mostrar o projetor natalino, caixa recebida, tomada e os desenhos temáticos de Natal projetados, NUNCA imagem genérica de outro projetor como o HY300).
- Proibido reaproveitar fotos de outros produtos ou nichos para simular avaliação de comprador.

#### 7.4 AUDITORIA CONTÍNUA DE VÍDEOS ÚNICOS E REVIEWS DUPLICADAS
- **Produtos com Apenas 1 Vídeo ou Zero Vídeos**: Devem ser imediatamente enriquecidos com pools de criadores de nicho autênticos em `js/videos-criadores.js` para manter o efeito feed dinâmico e interativo do TikTok Shop (proibido carrossel vazio ou card solitário).
- **Varredura Pré-Deploy Obrigatória**: O script `python scripts/deduplicate_all_html_reviews.py` e auditoria de sanidade devem ser executados antes de todo deploy em produção para garantir 0 imagens duplicadas no HTML.

#### 7.5 PROIBIÇÃO DE SCRAPING DE REVIEW ÚNICO (RATE-LIMITING DE COMPRADOR)
- **Tolerância Zero para Clonagem de Comprador**: É expressamente PROIBIDO extrair 3 a 5 fotos enviadas por um único comprador em uma única avaliação do Mercado Livre / TikTok Shop (mesmo `review_id`) e distribuí-las falsamente como se fossem avaliações de compradores diferentes (ex: Carlos, Mariana, Rodrigo).
- Cada card de avaliação com imagem DEVE pertencer a um comprador real e único, com texto coerente com a experiência de uso dele e avatar com gênero coincidente.

#### 7.6 OBRIGATORIEDADE DO APARELHO / EMBALAGEM FÍSICA NO UNBOXING
- **Unboxing Significa Produto Físico Recebido**: Fotos que mostram exclusivamente o resultado final (ex: apenas a luz projetada na parede no escuro, ou apenas a grama cortada, ou apenas a comida pronta), SEM MOSTRAR a caixa recebida, o aparelho sobre a mesa/bancada, a tomada ou o produto em mãos, NÃO são aceitas como unboxing de alta conversão!
- O comprador precisa ver o produto real, físico, recebido em casa, exatamente como ele vai desembalar ao receber a encomenda da Stone Shop.

#### 7.7 PROIBIÇÃO ABSOLUTA DE CONTAMINAÇÃO DE NICHO NO CARROSSEL DE CRIADORES
- É terminantemente PROIBIDO mapear produtos para datasets de criadores de nichos totalmente diferentes no `switch (prodId)` de `js/videos-criadores.js` (como iPhone usando vídeos de Xiaomi Poco, Chuveiro usando Fogão, ou Camisas de futebol usando Calça Jeans).
- Se não houver vídeos específicos suficientes para aquele ID, utilize criadores do nicho exato (ex: eletrônicos com eletrônicos, vestuário esportivo com vestuário esportivo).

#### 7.8 PROTOCOLO OBRIGATÓRIO DE EXTRAÇÃO VIA PLAYWRIGHT MCP PARA PRODUTOS SEM VÍDEO OU COM 1 VÍDEO
- **MANDATO SOBERANO E IRREVOGÁVEL (PLAYWRIGHT MCP FIRST)**: Quando um produto ID não tiver vídeos reais em `js/videos-criadores.js` ou possuir apenas 1 vídeo solitário, é EXPRESSAMENTE PROIBIDO inventar dados, mapear produtos trocados ou deixar o feed com card solitário. O agente DEVE OBRIGATORIAMENTE utilizar o **MCP Playwright** conectado ao navegador Chrome oficial no **Profile 42** para pesquisar o produto diretamente no **TikTok Shop** (`shop.tiktok.com`) com navegador visível, extrair os criadores autênticos demonstrando aquele produto específico, obter as URLs MP4, gerar os posters do primeiro frame e cadastrar o dataset canônico.
- **NAVEGAÇÃO VISÍVEL E AUDITÁVEL**: A busca deve ser feita pelo título exato do produto no TikTok Shop, coletando o feed de criadores reais com avatares e @usernames de pessoas físicas.

#### 7.9 LISTA OFICIAL DOS PRODUTOS COM APENAS 1 VÍDEO NATIVO DE CRIADOR (PENDÊNCIA PLAYWRIGHT MCP)
Estes produtos possuem apenas 1 vídeo nativo registrado em seu dataset base, necessitando de expansão obrigatória para 30+ criadores reais via MCP Playwright no TikTok Shop:

| ID | Produto | Dataset Nativo | Vids Atuais | Pendência Playwright MCP |
|:---:|:---|:---|:---:|:---|
| **9** | Ar Condicionado Portátil HQ 8.500 BTU | `CREATORS_AR_HQ_9` | 1 | Extrair 30 criadores no TikTok Shop |
| **10** | Ar Condicionado Portátil Hisense 12.000 BTU | `CREATORS_AR_HISENSE_10` | 1 | Extrair 30 criadores no TikTok Shop |
| **20** | Bicicleta Aro 29 GT Sprint MX7 24V | `CREATORS_BIKE_GT_20` | 1 | Extrair 30 criadores no TikTok Shop |
| **21** | Bola De Futebol De Campo Penalty Bravo X | `CREATORS_BOLA_PENALTY_21` | 1 | Extrair 30 criadores no TikTok Shop |
| **27** | Ar-condicionado Portátil LG Dual Inverter 14000 BTU | `CREATORS_AR_LG_27` | 1 | Extrair 30 criadores no TikTok Shop |
| **29** | Ar Condicionado Portátil HQ 8.500 BTU | `CREATORS_AR_HQ_29` | 1 | Extrair 30 criadores no TikTok Shop |
| **52** | Pad 11 Geração A16 256GB Wi-fi | `CREATORS_PAD11_52` | 1 | Extrair 30 criadores no TikTok Shop |
| **55** | SWITCH DESBLOQUEADO + 10 JOGOS | `CREATORS_SWITCH_55` | 1 | Extrair 30 criadores no TikTok Shop |
| **57** | Caixa de som Joog One Hifi J 200w 2 Mic | `CREATORS_JOOG_ONE_57` | 1 | Extrair 30 criadores no TikTok Shop |
| **58** | Caixa de som Echo Dot 5 geração | `CREATORS_ECHODOT_58` | 1 | Extrair 30 criadores no TikTok Shop |
| **59** | Mini Internet rápida Via Satélite Antena Original | `CREATORS_STARLINK_59` | 1 | Extrair 30 criadores no TikTok Shop |
| **61** | Caixa de Som Joog Break X1 Tela Touch 13 800W | `CREATORS_JOOG_BREAK_61` | 1 | Extrair 30 criadores no TikTok Shop |
| **63** | Smartwatch Redmi Watch 5 Lite GPS Preto | `CREATORS_REDMI_WATCH_63` | 1 | Extrair 30 criadores no TikTok Shop |
| **65** | Sofá 3 Lugares Retrátil e Reclinável Cama inBox | `CREATORS_SOFA_SENSES_65` | 1 | Extrair 30 criadores no TikTok Shop |
| **70** | Secadora de Roupa Mueller Solaris 8 kg | `CREATORS_SECADORA_MUELLER_70` | 1 | Extrair 30 criadores no TikTok Shop |
| **73** | Caixa De Som Bluetooth Waaw Hyperboom 1000 | `CREATORS_WAAW_HYPERBOOM_73` | 1 | Extrair 30 criadores no TikTok Shop |
| **78** | Extratora Portátil Spot Cleaner Wap 1400W | `CREATORS_WAP_EXTRATORA_78` | 1 | Extrair 30 criadores no TikTok Shop |
| **80** | Panificadora 19 Programas Gallant 600w | `CREATORS_PANIFICADORA_80` | 1 | Extrair 30 criadores no TikTok Shop |
| **85** | Caixa De Som Karaokê Joog X2 300w Tela 10,1 | `CREATORS_JOOG_X2_85` | 1 | Extrair 30 criadores no TikTok Shop |
| **87** | KISSMELADY calça mom jeans com cinto | `CREATORS_MOM_JEANS_87` | 1 | Extrair 30 criadores no TikTok Shop |
| **89** | Kit panelas de ferro esmaltadas luxo 18 peças | `CREATORS_PANELAS_FERRO_89` | 1 | Extrair 30 criadores no TikTok Shop |
| **91** | Pipoqueira Classic Retrô Misturador Automático | `CREATORS_PIPOQUEIRA_91` | 1 | Extrair 30 criadores no TikTok Shop |
| **92** | Conjunto de Panelas de Ferro Fundido Esmaltado 10 | `CREATORS_PANELAS_FERRO_92` | 1 | Extrair 30 criadores no TikTok Shop |
| **94** | Bicicleta Bike Ergometrica Spinning 120kg | `CREATORS_BIKE_SPINNING_94` | 1 | Extrair 30 criadores no TikTok Shop |
| **95** | YESOP Máquina De Gelo Portátil Preto 12kg/dia | `CREATORS_MAQUINA_GELO_95` | 1 | Extrair 30 criadores no TikTok Shop |
| **96** | Aparelho de Jantar Oxford Ryo Maresia 30 Peças | `CREATORS_APARELHO_RYO_96` | 1 | Extrair 30 criadores no TikTok Shop |
| **97** | Jogo de Jantar Canyon Porcelana Decorada 20 Peças | `CREATORS_JOGO_JANTAR_97` | 1 | Extrair 30 criadores no TikTok Shop |

#### 7.10 AUDITORIA OFICIAL DE DESDUPLICAÇÃO DE REVIEWS (ZERO DUPLICATAS GARANTIDO)
- **Status Canônico**: Todas as 103 páginas de produtos foram 100% auditadas com verificação estrita (`scripts/check_all_reviews_strict.py`), confirmando **0 imagens duplicadas de unboxing** no DOM em produção.
- **Script Obrigatório Pré-Deploy**: É terminantemente proibido subir deploy sem a aprovação limpa de `scripts/check_all_reviews_strict.py`.

#### 7.11 REGRAS CRÍTICAS INEGOCIÁVEIS: VOLUME MÍNIMO DE VÍDEOS, PLAY NA DESCRIÇÃO E 10+ FOTOS DE UNBOX
1. **PROIBIDO TER MENOS DE 10 VÍDEOS DE CRIADORES NO CARROSSEL**:
   - É terminantemente PROIBIDO qualquer produto exibir contador ou carrossel com menos de 10 vídeos (ex: "Vídeos de criadores (2)" ou "(4)").
   - O carrossel DEVE exibir SEMPRE no mínimo 10 a 30+ vídeos de criadores reais. Se o dataset nativo do produto possuir menos de 10 vídeos, ele DEVE ser OBRIGATORIAMENTE complementado com o pool de criadores do mesmo nicho até atingir 10+ ou 30+ vídeos, sem deixar o feed pobre ou solitário.
2. **VÍDEO DA DESCRIÇÃO OBRIGATORIAMENTE FUNCIONAL (PLAY GARANTIDO)**:
   - É terminantemente PROIBIDO o vídeo demonstrativo da descrição (`#tt-product-video` / `.product-video-block`) falhar ao dar play!
   - O player de vídeo da descrição DEVE responder instantaneamente ao clique/toque do usuário, com toggle de Play/Pause, controles visíveis, fallback de áudio sem erro de autoplay e tratamento resiliente de formato MP4/WebM compatível com mobile e desktop.
3. **MÍNIMO DE 10 IMAGENS REAIS DE UNBOXING NAS AVALIAÇÕES**:
   - É expressamente PROIBIDO um produto ter somente 3 ou 4 avaliações e ter apenas 3 imagens de unbox!
   - Todo produto anunciado no TikTok Shop da Stone Shop DEVE conter pelo menos 10 cards com fotos reais de unboxing enviadas por compradores autênticos demonstrando o produto físico desembalado, recebido em mãos, sobre a mesa/chão ou em uso doméstico real, mantendo zero repetição de imagem.

#### 7.12 PROIBIÇÃO ABSOLUTA DE USAR IMAGENS DE VÍDEOS DE CRIADORES NO SLIDER E NAS AVALIAÇÕES (REGRA PRODUTO 121 E GERAL)
1. **PROIBIÇÃO DE PRINTS/FRAMES DE VÍDEOS NO SLIDER DE PRODUTOS**:
   - É expressamente e terminantemente PROIBIDO fatiar vídeos de criadores ou capturar prints de vídeos para usar como fotos nos slides do produto (o carrossel principal de fotos de catálogo `[1/X]`).
   - O slider principal DEVE conter OBRIGATORIAMENTE imagens oficiais de catálogo com fundo branco, nítidas, em alta definição.
   - **Protocolo de Busca (TikTok Shop First -> Mercado Livre Fallback)**:
     - 1º: Puxar as fotos oficiais de catálogo do anúncio do TikTok Shop via Playwright MCP.
     - 2º: Se o anúncio do TikTok Shop não tiver fotos suficientes ou de boa qualidade, é OBRIGATÓRIO pesquisar o anúncio do mesmo produto no **Mercado Livre** e extrair as fotos oficiais de catálogo de lá!
2. **PROIBIÇÃO DE PRINTS/FRAMES DE VÍDEOS NAS AVALIAÇÕES DE CLIENTES**:
   - É terminantemente PROIBIDO fatiar vídeos de criadores para colocar nos cards de avaliações de clientes fingindo que são fotos de unboxing!
   - As fotos de avaliações DEVEM ser OBRIGATORIAMENTE fotos reais de clientes de unboxing (o produto recebido desembalado, na caixa, na mão ou na bancada).
   - **Protocolo de Busca de Unboxing (TikTok Shop First -> Mercado Livre Fallback)**:
     - 1º: Extrair as fotos reais de compradores nas avaliações do TikTok Shop via Playwright MCP.
     - 2º: Se o TikTok Shop não tiver fotos de unboxing suficientes, é OBRIGATÓRIO buscar as fotos reais enviadas pelos compradores nas avaliações do mesmo produto no **Mercado Livre**!
3. **CASO MANDATÓRIO DO PRODUTO 121 (`pages/produto-121.html` - Travesseiro Cervical Ortopédico)**:
   - Fica formalmente proibido manter os arquivos `../img/travesseiro-slide-*.webp` (que vieram de cortes de vídeos de criadores) no slider do Produto 121.
   - Devem ser substituídos por fotos oficiais de catálogo de travesseiro cervical ortopédico extraídas do Mercado Livre.
   - As fotos de avaliação `../img/reviews/review-121-*.webp` devem ser substituídas por fotos reais de compradores do Mercado Livre desembalando o travesseiro em casa.

#### 7.13 MATRIZ DE AUDITORIA E FILA DE EXTRAÇÃO VIA PLAYWRIGHT MCP (94 PRODUTOS)
- **Status Geral do Catálogo (103 Produtos)**:
  - **Zero Contaminação de Slider**: 100% dos 103 produtos possuem sliders limpos de catálogo oficial.
  - **Zero Falha no Player de Vídeo da Descrição**: 100% dos produtos com vídeo funcional e responsivo.
  - **Fila Prioritária de Extração (Unboxing < 10 fotos)**: Os 94 produtos listados em uditoria_geral_nao_conformidades.md devem ter suas fotos de unboxing expandidas progressivamente via extração oficial do TikTok Shop / Mercado Livre pelo MCP Playwright no Profile 42 (Max Digital) até atingirem o piso de 10 fotos reais de unboxing.

#### 7.14 OBRIGATORIEDADE DE VERIFICAÇÃO E AUDITORIA 1 POR 1 EM TODOS OS PRODUTOS DO CATÁLOGO
1. **PROIBIDO AMOSTRAGEM OU AUDITORIA SUPERFICIAL**:
   - É expressamente e terminantemente OBRIGATÓRIO verificar e auditar **1 por 1**, de forma individual, exaustiva e nominal, cada um dos **103 produtos** do catálogo (pages/produto-1.html até produto-124.html).
   - Proibido assumir que produtos irmãos ou da mesma categoria estão corretos sem inspecionar individualmente o arquivo HTML de cada um.
2. **CHECKLIST INDIVIDUAL OBRIGATÓRIO POR PRODUTO**:
   - **Slider Principal**: Confirmar 1 por 1 que todas as fotos são de catálogo com fundo branco do produto exato (zero frames cortados de vídeo, zero produto de outro nicho como fogão atlas em mesa/sofá/travesseiro/etc).
   - **Vídeo da Descrição**: Confirmar 1 por 1 que o vídeo pertence estritamente ao produto anunciado (expurgar o vídeo genérico de iPad 3rtr42.mp4 ou vídeos trocados).
   - **Vídeos de Criadores**: Confirmar 1 por 1 que o carrossel exibe no mínimo 10 vídeos reais do nicho.
   - **Avaliações com Foto de Unboxing**: Confirmar 1 por 1 a contagem de fotos reais de unboxing e auditar individualmente cada página para atingir o piso de 10 fotos reais sem duplicatas.


#### 7.15 DIRETRIZ MANDATÓRIA DO CTO BRUNO //goal //boost: DIAGNÓSTICO NOMINAL 1 POR 1 E TABELA OFICIAL
1. **RESULTADO DA AUDITORIA NOMINAL EXAUSTIVA (103 PRODUTOS AUDITADOS 1 POR 1)**:
   - **Total de Páginas Auditadas**: 103 arquivos (`pages/produto-4.html` a `pages/produto-124.html`).
   - **Imagens Locais Quebradas no Slider**: **0 páginas** (P17 e P18 corrigidos com expurgo de `shopee-asset` para `stone-asset`).
   - **Imagens Locais Quebradas em Avaliações**: **0 páginas** com erro de 404 local.
   - **Contaminação de Fogão Atlas (`55n8uo.mp4`)**: **0 páginas contaminadas** (apenas P117 mantém o vídeo pois É o Fogão Atlas).
   - **Vídeos da Descrição com iPad Genérico (`3rtr42.mp4`)**: Identificados nominalmente nos produtos:
     - `P32` (Chuveiro Acqua Duo Lorenzetti)
     - `P39` (Secador de Cabelos Philco PSC3500)
     - `P45` (Prancha Pro 480 Turbo MQ Professional)
     - `P47` (Extratora Higienizadora Portátil)
     - `P49` (Detergente Limpador Wap)
     - `P50` (Lava e Seca Midea Master Clean)
     - `P54` (Purificador Eletrônico PE11X)
     - `P56` (Cadeira de Praia Alta Mor - **CORRIGIDO** para `jechqr.mp4`)
     - `P68` (Jogo de Panelas Cerâmica)
     *(P52 é o iPad Genérico 11", mantido contextualmente)*.
2. **FILA OBRIGATÓRIA DE DESACOPLAMENTO DE VÍDEO**:
   - Os produtos P32, P39, P45, P47, P49, P50, P54 e P68 DEVEM ter seus vídeos da descrição substituídos por vídeos do nicho exato extraídos via MCP Playwright no Profile 42 (Max Digital) ou mapeados de seus respectivos produtos.
3. **FILA OBRIGATÓRIA DE PISO 10 FOTOS DE UNBOXING (92 PRODUTOS)**:
   - Cada uma das 92 páginas identificadas com menos de 10 avaliações com fotos reais de unboxing deve receber fotos adicionais extraídas via Playwright MCP direto das avaliações do TikTok Shop ou Mercado Livre.
4. **COMPROMISSO DOS SUBAGENTES**:
   - É terminantemente proibido aos subagents inventar dados, usar ffmpeg para fatiar vídeos de criadores fingindo que são fotos de unboxing, ou gerar imagens por IA.
   - Toda verificação e edição deve ser nominal, arquivo por arquivo.


#### 7.16 PROIBIÇÃO ABSOLUTA DE FOTOS/AVATARES DE HOMENS EM PRODUTOS FEMININOS
1. **REGRA SOBERANA DE GÊNERO FEMININO**:
   - É **EXTREMAMENTE PROIBIDO** utilizar fotos, avatares ou nomes de homens em produtos femininos (calçados femininos, vestidos, saias, moda íntima, body modelador lipo, calças femininas, secadores, modeladores de cachos, pranchas, perfumes femininos e mochilas femininas).
   - Produtos impactados: P28, P38, P39, P45, P87, P88, P103, P104, P106, P108, P109.
2. **COERÊNCIA 100% MULHER**:
   - 100% dos avatares devem ser exclusivamente mulheres reais do banco oficial do TikTok CDN (números pares: `tt_avatar_2.jpg` a `tt_avatar_220.jpg`).
   - 100% dos nomes mascarados devem ser femininos (`M**a S**a`, `J**e F**s`, etc.).
   - 100% dos vídeos de criadores devem ser de criadoras mulheres autênticas testando o produto no TikTok.


#### 7.17 DIRETRIZ SOBERANA DE AVATARES REAIS BRASILEIROS DO TIKTOK SHOP (PROIBIÇÃO DE GRINGOS, STOCK PHOTOS E GÊNERO INVERTIDO)
1. **PROIBIÇÃO ABSOLUTA DE ROSTOS GRINGOS / ESTRANGEIROS / ESTADOS UNIDOS / STOCK PHOTOS**:
   - É terminantemente PROIBIDO utilizar fotos de bancos de imagens gratuitos (Unsplash, Pexels, UI Faces, ThisPersonDoesNotExist) ou fotos de pessoas que aparentem ser de fora do Brasil (homens ou mulheres com estética gringa dos Estados Unidos, Europa ou cenários estrangeiros como estatueta do Oscar, casacos pesados de inverno americano, etc.).
   - 100% dos avatares devem ser OBRIGATORIAMENTE de pessoas físicas reais do Brasil, com perfil e estética autêntica de compradores e criadores do TikTok / TikTok Shop Brasil!
2. **PROIBIÇÃO ABSOLUTA DE HOMENS EM PRODUTOS DE MULHER**:
   - Em todo e qualquer produto do nicho feminino (vestidos, saias, moda íntima, body modelador lipo, calças mom jeans, chinelos femininos de strass, secadores de cabelo, pranchas térmicas, modeladores de cachos, perfumes femininos e bolsas/mochilas juvenis femininas), é TERMINANTEMENTE PROIBIDO exibir fotos, avatares ou nomes de homens!
   - 100% das avaliações e 100% dos criadores nesses produtos DEVEM ser mulheres brasileiras reais.
3. **OBRIGATORIEDADE DE VERIFICAÇÃO VISUAL NOMINAL DOS AVATARES**:
   - Fica terminantemente proibido qualquer script que classifique avatares por atalhos matemáticos cegos (como deduzir gênero por par/ímpar de arquivo).
   - Todo avatar DEVE ser inspecionado visualmente e categorizado nominalmente entre homem brasileiro real e mulher brasileira real, expurgando sumariamente logos de lojas, robôs, desenhos e rostos gringos.


#### 7.18 OBRIGATORIEDADE INEGOCIÁVEL: AVATARES EXCLUSIVOS DO TIKTOK CDN OFICIAL BRASIL
1. **FONTE EXCLUSIVA E OBRIGATÓRIA: CDN OFICIAL DO TIKTOK**:
   - 100% dos avatares de avaliações e criadores DEVEM ser puxados única e exclusivamente dos servidores de mídia oficiais do TikTok CDN (`p16-common-sign.tiktokcdn.com`, `p19-common-sign.tiktokcdn-us.com`, `tos-alisg-avt-*`, etc.), extraídos com o Chrome no Profile 42 (Max Digital) de compradores e criadores do TikTok Shop Brasil.
   - **Tolerância Zero para Fontes Externas**: Proibido qualquer avatar de banco de imagens da internet, fotos de IA, robôs ou desenhos.
2. **FILTRO OBRIGATÓRIO DE BRASILIDADE (PROIBIDO ROSTO GRINGO / ESTADOS UNIDOS)**:
   - Todo avatar deve refletir pessoas físicas reais do Brasil. Proibido colocar rostos de estrangeiros, norte-americanos, europeus ou cenários de outros países.
3. **BLINDAGEM TOTAL DE GÊNERO EM PRODUTOS FEMININOS**:
   - Em qualquer produto voltado ao público feminino (calçados femininos, vestidos, moda íntima, body modelador, calças femininas, secadores, modeladores de cachos, pranchas, perfumes femininos), 100% dos avatares e nomes DEVEM ser mulheres brasileiras reais do TikTok. Proibição absoluta de fotos masculinas nesses produtos.
