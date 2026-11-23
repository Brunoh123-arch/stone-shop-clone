# 🛍️ Stone Shop - Clone Completo & Extração Integral

Site original: `https://lojastoneshop.vercel.app`

Extração integral realizada com padrão de engenharia profissional: vitrine mobile-first estilo TikTok Shop / Shopee, 87 páginas de produtos dinâmicas, todos os vídeos VSL locais e reels de criadores, animações de checkout, scripts de catálogo, eventos do TikTok Pixel, sistema de cupons, carrinho reativo, funil de checkout, resumo de pedido e gateway simulado de pagamento Pix.

---

## 📦 Estrutura do Projeto Clonado

```
stone_shop_clone/
├── index.html                   # Vitrine Principal com Header, Tabs, Cupons e Grids de Produtos
├── server.js                    # Servidor local Node.js com suporte a Range Streaming de vídeos (206)
├── vercel.json                  # Configuração para deploy instantâneo na Vercel
├── package.json                 # Manifesto Node.js com scripts 'start' e 'dev'
├── iniciar_loja.bat             # Atalho executável para subir o site localmente no Windows
├── css/
│   ├── style.css                # Folha de estilo base do layout responsivo
│   └── original_index.css       # Estilos específicos dos cards e carrosséis
├── js/
│   ├── app.js                   # Lógica central da loja, carrinho, modais e transições
│   ├── catalogo.js              # Base de dados de produtos e indexação
│   ├── tiktok-events.js         # Rastreamento de eventos do TikTok Pixel
│   ├── videos-criadores.js      # Player reels estilo TikTok com drawer de comentários e likes
│   ├── avaliacoes-iphone.js     # Avaliações com fotos e depoimentos de iPhone
│   ├── avaliacoes-pirelli.js    # Avaliações de pneus Pirelli com carrossel
│   └── avaliacoes-scooter.js    # Depoimentos e dados da Scooter Elétrica
├── pages/
│   ├── carrinho.html            # Tela de carrinho com cálculo de frete e cupom
│   ├── checkout.html            # Funil de checkout com dados de entrega e validação
│   ├── resumo.html              # Resumo do pedido e confirmação
│   ├── pix.html                 # Tela de pagamento Pix com QR Code e Copia-e-Cola
│   └── produto-[4..102].html    # 87 páginas individuais completas de produtos
├── videosprodutos/              # 41 vídeos MP4 completos de demonstração dos produtos (149 MB)
├── videoscooterintroducao/
│   └── scooter-preta.mp4        # Vídeo VSL de introdução da scooter (8.6 MB)
├── videosdoscriadorespneu/      # 13 vídeos MP4 completos dos criadores/reviews (>85 MB)
├── decalque/
│   └── decalque-oferta.jpg      # Background banner de oferta da loja
├── botoesdecarrinhioechat/
│   └── image.png                # Botões de carrinho e chat
├── img/
│   ├── tiktok-anim-v5.mp4       # Vídeo de animação TikTok no carrinho (2.2 MB)
│   ├── share-arrow.png          # Ícone de compartilhamento
│   └── ...                      # Imagens de produtos, logos e selos
├── logo.png                     # Logotipo oficial da loja
├── logoorderbumps/              # Fotos dos order bumps (películas, capinhas, adaptadores)
├── logopix/                     # Selo e layout de pagamento Pix
├── FOTOSDEPERFIL/               # Fotos reais de perfil dos clientes avaliadores
├── AVALIACOESFOTOS/             # Fotos anexadas nas avaliações
├── imagemscooterpreta/          # Fotos da Scooter preta
├── imagemscootervermelho/       # Fotos da Scooter vermelha
├── imagemscooterbronze/         # Fotos da Scooter bronze
├── imagemscooterrosa/           # Fotos da Scooter rosa
├── esteirafotos/                # Galeria de fotos da esteira ergométrica
└── avaliacoesesteira/           # Fotos de avaliações da esteira ergométrica
```

---

## 🚀 Como Executar Localmente

### Opção 1: Atalho Rápido (.bat)
Dê um duplo clique no arquivo:
- `INICIAR_STONE_SHOP.bat` (na raiz do projeto) ou
- `iniciar_loja.bat` (dentro da pasta `stone_shop_clone`)

O navegador abrirá automaticamente em `http://localhost:3333`.

### Opção 2: Terminal Node.js
```bash
cd stone_shop_clone
npm start
```
Acesse `http://localhost:3333` no navegador.

---

## 🌐 Como Fazer Deploy na Vercel

Dentro da pasta `stone_shop_clone`, execute:
```bash
npx vercel --prod
```
O arquivo `vercel.json` já está configurado para servir todos os arquivos estáticos e páginas com URLs limpas (`cleanUrls: true`).

---

## 🎯 Destaques Técnicos

1. **Extração 100% Completa & Autossuficiente**: Mais de 710 arquivos baixados e verificados, totalizando ~350 MB de páginas, imagens, folhas de estilo e vídeos locais.
2. **56 Vídeos MP4 Locais (Zero Dependência Externa de CDN)**:
   - 41 vídeos completos de demonstração dos produtos em `videosprodutos/` (149.2 MB).
   - `scooter-preta.mp4` (vídeo VSL de demonstração em alta resolução, 8.6 MB).
   - 13 vídeos MP4 completos de criadores e reels de reviews em `videosdoscriadorespneu/` (>85 MB).
   - `tiktok-anim-v5.mp4` com animação nativa na tela de carrinho e resumo (2.2 MB).
3. **Player Interativo de Vídeos de Criadores (`js/videos-criadores.js`)**:
   - Drawer de comentários com contagem, curtidas e botão de seguir.
   - Buffering simulado e reprodução instantânea.
4. **Resiliência e Zero Links Quebrados**:
   - Auditoria automatizada executada em todas as 92 páginas HTML: **0 referências locais ou de mídia quebradas**.
   - Servidor com suporte nativo a **HTTP Range Requests (RFC 7233)** para buffering e streaming suave de vídeo nos navegadores mobile e desktop.
