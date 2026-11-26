# Stone Shop — Manual Mestre de Arquitetura, Regras e Protocolos (Bruno CTO - Modo ZIKA Blindado)

> **Gatilho de Ativação:** Sempre ativo em qualquer sessão na pasta `c:\Users\Dell\Downloads\ds`.
> **Objetivo Deste Arquivo:** Ser a ÚNICA fonte de verdade para qualquer agente ou engenheiro entender como o projeto funciona, o que é estritamente proibido, o que é obrigatório, e como cadastrar, validar e subir produtos sem nunca se perder.

---

## 1. VISÃO GERAL & ARQUITETURA DO PROJETO (COMO TUDO FUNCIONA)

A **Stone Shop** é uma plataforma e-commerce de ultra-alta conversão inspirada na interface nativa do **TikTok Shop Brasil**, hospedada na **Vercel** com domínio oficial e CDN global HTTPS (`https://stoneshopclone.vercel.app`), com repositório no GitHub (`main`).

### 1.1 Doutrina do Modelo Único Permanente (Single Source of Truth)
- **PROIBIDO CRIAR ARQUIVOS HTML ESTÁTICOS EM `pages/`**: NUNCA crie `pages/produto-*.html`. Esse padrão antigo foi 100% extinto!
- **Cada Produto é um JSON**: Todos os produtos moram exclusivamente em `data/produtos/produto-[id].json`.
- **Índice Central de Registro**: Todo produto DEVE ser registrado em `data/produtos/index.js` via lazy require estático (`'126': () => require('./produto-126.json'),`).
- **Renderizador Oficial Dinâmico**: A Vercel Serverless Function `api/_lib/render-produto.js` recebe o ID do produto, lê o respectivo JSON e injeta os dados dinamicamente no template mestre `templates/produto-modelo.html`.
- **Roteamento Unificado (`vercel.json`)**:
  - `/produto-126` -> Renderiza dinamicamente via `api/serve?slug=produto-126`
  - `/produto/126` -> Renderiza dinamicamente via `api/serve?slug=produto-126`
  - `/pages/produto-126` -> Compatibilidade legada garantida
  - `/` -> Vitrine oficial da loja (`index.html`)

---

## 2. DOUTRINA DE ENGENHARIA: PERMITIDO VS PROIBIDO (TOLERÂNCIA ZERO A JÚNIORICE)

### ❌ O que é TERMINANTEMENTE PROIBIDO:
1. **Proibição de Fatiar Vídeos para Reviews**: NUNCA use `ffmpeg` para tirar prints de vídeos de criadores e fingir que são fotos de clientes. Review falsa desse tipo quebra a credibilidade.
2. **Proibição de Fundo Branco em Avaliações**: Foto de review é de cliente físico em ambiente doméstico real (sala, chão, cozinha, desembalando o pacote dos Correios). Zero foto de estúdio nos cards de depoimento.
3. **Proibição de Avatares Falsos / Gringos / IA**: Proibido fotos de banco gratuito (Unsplash, Pexels), rostos gerados por IA ou pessoas com estética gringa (inverno americano, etc.). Avatares DEVEM ser 100% pessoas físicas reais brasileiras do CDN do TikTok (`img/reviews-avatars/tiktok_real/`).
4. **Proibição de Incoerência de Gênero**:
   - Nome feminino (`Maria`, `Camila`, `Juliana`) DEVE ter avatar de mulher real.
   - Nome masculino (`Rodrigo`, `Carlos`, `Felipe`) DEVE ter avatar de homem real.
   - Em produtos femininos (vestidos, lingerie, modeladores, secadores), 100% dos nomes e avatares DEVEM ser mulheres.
5. **Proibição de Contaminação de Nicho**: Nunca misture mídias de produtos diferentes (ex: vídeo de ar-condicionado em patinete ou churrasqueira em tênis).
6. **Proibição de Lixo na Codebase**: Proibido arquivos `*_backup.js`, `*_old.html`, `test*.png` soltos na raiz. Arquivos temporários de scripts DEVEM ser apagados imediatamente após o uso.
7. **Proibição de Excesso de Vídeos (Bloatware)**: Não use 30+ vídeos pesados. O padrão oficial são **entre 8 e 15 vídeos de criadores reais** de alta qualidade.
8. **Proibição de Redirecionar Celulares Reais**: Nunca redirecione celulares legítimos para `/loja` ou páginas de erro.

### ✅ O que é OBRIGATÓRIO & PERMITIDO:
1. **Navegador Chrome Oficial (Profile 42)**: Toda extração via Playwright DEVE rodar no Chrome oficial conectado ao perfil **Profile 42** (`kaiobrunocastro12@gmail.com`), com sessão real para evitar bloqueios de bot.
2. **Janela Minimizada & Som Mutado**: Quando rodar Playwright no PC do usuário, mantenha a janela minimizada (`bounds: { windowState: 'minimized' }`) e o áudio forçado em `volume = 0` para não atrapalhar o usuário assistindo Netflix/vídeos.
3. **Fotos Oficiais de Catálogo (5 a 8 Fotos)**: Fotos de alta resolução em formato WebP com fundo branco, cobrindo todos os ângulos, detalhes e dimensões.
4. **Grade de Variações 1:1**: Cada opção de cor/modelo deve ter sua miniatura exata correspondente e trocar no slider ao ser clicada.
5. **Autoplay no Carrossel de Criadores**: Cards de criadores devem rodar vídeos MP4 leves com `autoplay`, `muted`, `loop` e `playsinline`.
6. **Avaliações com Unboxing Real (5+ fotos)**: No topo das avaliações, exibir depoimentos autênticos com fotos de unboxing recebidas no Brasil.
7. **Validação Obrigatória**: Antes de qualquer commit, rodar compulsoriamente `node scripts/validar-modelo-unico.js` (deve passar com ZERO erros).

---

## 3. PROTOCOLO PASSO A PASSO PARA CADASTRAR UM NOVO PRODUTO

Sempre que o usuário pedir para subir ou puxar um novo produto (ex: `produto-125`), siga rigorosamente este fluxo:

```
[1. Extração no Chrome Profile 42]
  ↓ (Puxar fotos de catálogo + unboxings reais + especificações via Playwright no ML / TikTok Shop)
[2. Download & Otimização de Mídias]
  ↓ (Salvar slides em img/produto-[id]-slide-*.webp e unboxings em img/review-[id]-real-*.webp)
[3. Criar JSON Canônico]
  ↓ (Escrever data/produtos/produto-[id].json com preço calibrado, reviews, variações e specs)
[4. Registrar no Índice]
  ↓ (Adicionar 'id': () => require('./produto-[id].json') em data/produtos/index.js)
[5. Mapear Vídeos de Criadores]
  ↓ (Configurar CREATORS_[PROD]_[ID] e adicionar o case [id] em js/videos-criadores.js)
[6. Validação do Modelo Único]
  ↓ (Atualizar contagem esperada e rodar node scripts/validar-modelo-unico.js)
[7. Deploy & Sincronização Git]
  ↓ (Commit limpo, push origin main e npx vercel --prod --yes com alias stoneshopclone.vercel.app)
```

---

## 4. ESTRUTURA DO JSON DO PRODUTO (`data/produtos/produto-[id].json`)

Todo produto deve seguir exatamente esta estrutura de campos:

```json
{
  "id": 126,
  "title": "Título Completo com SEO - Stone Shop",
  "meta_description": "Descrição persuasiva com preço PIX e frete grátis.",
  "product_title": "Título Limpo para Exibição no Topo da Página",
  "slider_imgs": [
    { "src": "../img/produto-126-slide-1.webp", "alt": "Vista Frontal" },
    { "src": "../img/produto-126-slide-2.webp", "alt": "Detalhes" }
  ],
  "discount_badge": "-75%",
  "price_int": "97",
  "price_cents": ",00",
  "price_original": "R$ 389,90",
  "installment_text": "3x de R$ 32,33 sem juros",
  "installment_highlight": "sem juros",
  "coupon_main": "Cupom R$ 50 OFF aplicado",
  "coupon_bonus": "Final R$ 97,00 no Pix ou Cartão",
  "rating_score": "4,9",
  "rating_count": "(386)",
  "sold_count": "3.8K vendido(s)",
  "frete_original": "R$ 24,90",
  "reviews_header": "Avaliações dos clientes (15)",
  "reviews_avg": "4,9",
  "reviews": [
    {
      "name": "P**a S**s",
      "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_57.jpg",
      "stars": 5,
      "date": "24/11",
      "variation": "Azul Turbo",
      "date_line": "24/11 · Azul Turbo",
      "comment": "Texto humanizado em português de cliente real elogiando entrega e qualidade.",
      "photos": ["../img/review-126-real-1.webp"]
    }
  ],
  "description_html": "<div class=\"product-description-content\">...especificações e tabela...</div>",
  "produto_atual": {
    "id": 126,
    "nome": "Título do Produto",
    "preco_original": 389.9,
    "preco_avista": 97.0,
    "parcelas": 3,
    "valor_parcela": 32.33,
    "categoria": "Brinquedos",
    "imagem": "../img/produto-126-slide-1.webp",
    "fotos": ["../img/produto-126-slide-1.webp"],
    "variacoes": {
      "cor": {
        "label": "Cor",
        "opcoes": [
          { "nome": "Preto", "imagem": "../img/var-preto.webp", "preco": 97.0 }
        ]
      }
    }
  },
  "creator_context": "patinete126",
  "creators": [
    {
      "name": "Criador Real",
      "username": "usuario_tiktok",
      "avatar": "../img/reviews-avatars/tiktok_real/tt_avatar_30.jpg",
      "poster": "../videosprodutos/posters/poster-produto-c1.jpg",
      "video": "https://files.catbox.moe/64aksn.mp4#prod=126",
      "catbox_id": "64aksn.mp4",
      "startTime": 0.2,
      "likes": 32400,
      "commentsCount": 380,
      "saves": 3890,
      "shares": 210,
      "description": "Legenda real do vídeo com hashtags #tiktokshop #review"
    }
  ]
}
```

---

## 5. CLOAKER V6.6 & SEGURANÇA CONTRA SCRAPERS

O sistema conta com proteção em duas camadas:
1. **Camada Backend (`api/serve.js`)**:
   - Bloqueia na largada scrapers como SaveWeb2Zip, HTTrack, Scrapy, Wget, Puppeteer e Selenium entregando `fake.html`.
   - Permite 100% dos bots de aprovação de anúncios (TikTokBot, Googlebot, FacebookExternalHit) para aprovar campanhas instantaneamente.
2. **Camada Frontend (`js/tiktok-cloaker.js`)**:
   - Detecta emuladores de celular do PC (DevTools Device Toolbar), telas desktop sem touch e plataformas spoofed.
   - **LIBERAÇÃO TOTAL DE CELULARES REAIS**: Celulares físicos legítimos (Android e iPhone com touch e GPU móvel) têm acesso imediato liberado aos produtos da loja, mesmo quando acessados diretamente por links compartilhados no WhatsApp, Instagram ou navegador.
   - Bypass para o dono da loja via query string: `?preview=1` ou `?c=1` ou `?owner=1`.

---

## 6. LISTA OURO DE NATAL / 13º SALÁRIO (FOGUETES 125 A 131)

Produtos de alta viralidade calibrados no ponto cego de preço do mercado (sweet spot no PIX para conversão imediata de trabalhadores com 13º salário em mãos):

| ID | Produto | Nicho / Gancho | Preço PIX | Status Atual |
|:---:|:---|:---|:---:|:---:|
| **125** | Carrinho Rolimã Girocar / Super Car c/ LED (até 100kg) | Brinquedo Família / Pai e Filho | R$ 84,90 | ⏳ Na fila de extração |
| **126** | Patinete Elétrico Infantil Dobrável c/ LED e Som (Bivolt) | Brinquedos Elétricos / Sonho de Criança | R$ 97,00 | ✅ 100% Cadastrado e No Ar |
| **127** | Carrinho RC Drift 4x4 Alta Velocidade (Solta Fumaça) | Controle Remoto / Drift Real | R$ 74,90 | ⏳ Na fila de extração |
| **128** | Mesa Dobrável Maleta Portátil 1,80m em Polietileno | Casa / Ceia de Natal e Churrasco | R$ 89,90 | ⏳ Na fila de extração |
| **129** | Escova Elétrica Giratória 9 em 1 sem Fio c/ Extensor | Faxina Pesada de Fim de Ano | R$ 64,90 | ⏳ Na fila de extração |
| **130** | Colar Prata 925 na Caixa com Rosa Giratória Encantada | Presente Romântico de Natal | R$ 74,90 | ⏳ Na fila de extração |
| **131** | Kit 2 Jogos de Cama Casal 400 Fios Toque Acetinado Hotel | Cama e Banho / Renovação da Casa | R$ 69,90 | ⏳ Na fila de extração |

---

## 7. COMANDOS DE MANUTENÇÃO E VALIDAÇÃO OFICIAL

Sempre execute os comandos a partir da raiz `c:\Users\Dell\Downloads\ds`:

- **Validar integridade de todos os produtos:**
  ```powershell
  node scripts/validar-modelo-unico.js
  ```
- **Fazer deploy em produção na Vercel:**
  ```powershell
  npx vercel --prod --yes
  ```
- **Apontar o domínio de produção oficial:**
  ```powershell
  npx vercel alias set <deployment-url> stoneshopclone.vercel.app
  ```
- **Commit e sincronização no Git:**
  ```powershell
  git add -A; git commit -m "feat/fix: descricao das alteracoes"; git push origin main
  ```
