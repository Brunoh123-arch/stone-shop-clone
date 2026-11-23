const fs = require('fs');
const path = require('path');

const dsDir = 'C:/Users/Dell/Downloads/ds';
const cloneDir = 'C:/Users/Dell/Downloads/stone_shop_clone';

const template = fs.readFileSync(path.join(dsDir, 'pages', 'produto-104.html'), 'utf8');

// Build customized produto-105.html
let html = template;

// 1. Title and description
html = html.replace(
  /<title>.*?<\/title>/i,
  '<title>Projetor HY300 Original Portátil Smart Android 11 4K Ultra HD HDMI Wifi Bluetooth Alto - Stone Shop</title>'
);

html = html.replace(
  /<meta name="description" content=".*?">/i,
  '<meta name="description" content="Projetor HY300 Original Portátil Smart Android 11 4K Ultra HD com 90% OFF no Festival 11.11. Apenas R$ 39,90 com Frete Grátis.">'
);

// 2. Slider track images
const sliderImages = `
        <img class="slider-img" src="https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/81525a24b6074e6c87b673c8cc37d237~tplv-aphluv4xwc-resize-webp:800:800.webp" alt="Projetor HY300 4K Smart - 1" onerror="this.style.display='none'">
        <img class="slider-img" src="../img/poster-projetor-1.jpg" alt="Projetor HY300 no Teto - 2" onerror="this.style.display='none'">
        <img class="slider-img" src="../img/poster-projetor-2.jpg" alt="Projetor HY300 Rotação 180 Graus - 3" onerror="this.style.display='none'">
        <img class="slider-img" src="../img/poster-projetor-3.jpg" alt="Projetor HY300 Tela Gigante 130 Pol - 4" onerror="this.style.display='none'">
`;

html = html.replace(/<div class="slider-track">[\s\S]*?<\/div>\s*<div class="slider-counter">.*?<\/div>/i, 
  `<div class="slider-track">${sliderImages}      </div>\n      <div class="slider-counter">1 / 4</div>`
);

// 3. Price section
html = html.replace(/<div class="discount-badge-white">.*?<\/div>/i, '<div class="discount-badge-white">-90%</div>');
html = html.replace(/<div class="price-current">.*?<\/div>/i, '<div class="price-current">39<span class="price-cents">,90</span></div>');
html = html.replace(/<div class="price-original">.*?<\/div>/i, '<div class="price-original">R$ 399,90</div>');

// 4. Discount ticket
html = html.replace(/Desconto de R\$ \d+/i, 'Desconto de R$ 360');
html = html.replace(/Economize \d+% com bônus/i, 'Economize 90% com bônus');

// 5. Installments
html = html.replace(/2x R\$ [\d,]+ <span style="color: #fe2c55; font-weight: 600;">sem juros<\/span>/i, '2x R$ 22,94 <span style="color: #fe2c55; font-weight: 600;">sem juros</span>');

// 6. Product title
html = html.replace(/<h1 class="product-title"[^>]*>[\s\S]*?<\/h1>/i, 
  `<h1 class="product-title" style="font-size: 16px; font-weight: 700; color: #161823; line-height: 1.35; margin: 0; flex: 1;">
          Projetor HY300 Original Portátil Smart Android 11 4K Ultra HD HDMI Wifi Bluetooth Alto
        </h1>`
);

// 7. Ratings and sold count
html = html.replace(/<span style="font-size: 13px; font-weight: 700; color: #161823;">.*?<\/span>/i, '<span style="font-size: 13px; font-weight: 700; color: #161823;">4.9</span>');
html = html.replace(/<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document\.querySelector\('\.reviews-section'\)\?\.scrollIntoView\(\{behavior:'smooth'\}\)">\(.*?\)<\/span>/i, 
  '<span style="font-size: 13px; font-weight: 500; color: #4364db; cursor: pointer;" onclick="document.querySelector(\'.reviews-section\')?.scrollIntoView({behavior:\'smooth\'})">(5)</span>'
);
html = html.replace(/<div class="sold-count"[^>]*>.*?<\/div>/i, '<div class="sold-count" style="font-size: 13px; color: #757575; font-weight: 400;">14.8K vendidos</div>');

// 8. EXACT STANDARD REVIEWS SECTION MATCHING PRODUTO-104 & PRODUTO-103
const exactReviewsSection = `      <!-- AVALIAÇÕES -->
      <div class="reviews-section">
        <h3 class="reviews-header">Avaliações dos clientes (5)</h3>
        <div class="reviews-summary">
          <span class="review-avg">4,9</span><span class="review-avg-total">/5</span>
          <div class="review-stars">
            ⭐⭐⭐⭐⭐
          </div>
        </div>

        <!-- Avaliação 1 (Juliana Ferreira) -->
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <div class="review-avatar-placeholder">J</div>
              </div>
              <div class="review-user-info">
                <div class="review-user-name">Juliana Ferreira</div>
                <div class="review-user-stars">⭐⭐⭐⭐⭐</div>
                <div class="review-date">24/10/2026 | Variação: SMART WI-FI 4K, BIVOLT</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou super rápido em 3 dias bem embalado! A imagem na parede do quarto no escuro é surpreendente, bem nítida. O som interno quebra um galho mas conectei na caixinha bluetooth e virou um cinema de verdade. Super fácil regular o foco na rodinha.</p>
          <div class="review-photos">
            <video class="review-video" src="../img/review-vid-1.mp4" playsinline muted onclick="openPhotoModal(this.src)"></video>
            <img class="review-photo" src="../img/review-projetor-1.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="../img/review-projetor-2.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="../img/review-projetor-3.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 2 (Carlos Eduardo Rocha) -->
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <div class="review-avatar-placeholder">C</div>
              </div>
              <div class="review-user-info">
                <div class="review-user-name">Carlos Eduardo Rocha</div>
                <div class="review-user-stars">⭐⭐⭐⭐⭐</div>
                <div class="review-date">19/10/2026 | Variação: SMART WI-FI 4K, BIVOLT</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Comprei pras crianças assistirem desenho no teto do quarto e elas adoraram! O Android é bem fluido, já veio com YouTube e Netflix funcionando no Wi-Fi 5G. O ajuste automático de ângulo ajuda demais quando coloca ele de lado na mesinha.</p>
          <div class="review-photos">
            <img class="review-photo" src="../img/review-projetor-4.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="../img/review-projetor-5.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="../img/review-projetor-6.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 3 (Marcos Vinicius Ramos) -->
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar">
                <div class="review-avatar-placeholder">M</div>
              </div>
              <div class="review-user-info">
                <div class="review-user-name">Marcos Vinicius Ramos</div>
                <div class="review-user-stars">⭐⭐⭐⭐⭐</div>
                <div class="review-date">14/10/2026 | Variação: COMBO CINEMA VIP, BIVOLT</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Melhor compra que fiz pro meu quarto! Imagem enorme de umas 100 polegadas na parede branca. Espelhei a tela do celular sem cabo nenhum e assisti futebol no fim de semana, a qualidade no escuro é top.</p>
          <div class="review-photos">
            <video class="review-video" src="../img/review-vid-2.mp4" playsinline muted onclick="openPhotoModal(this.src)"></video>
            <img class="review-photo" src="../img/review-projetor-7.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="../img/review-projetor-8.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="../img/review-projetor-9.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 4 (Amanda Lima) -->
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar"><div class="review-avatar-placeholder">A</div></div>
              <div class="review-user-info">
                <div class="review-user-name">Amanda Lima</div>
                <div class="review-user-stars">⭐⭐⭐⭐⭐</div>
                <div class="review-date">09/10/2026 | Variação: SMART WI-FI 4K, BIVOLT</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Excelente produto! Muito compacto e leve, levo pra sala e pro quarto tranquilo. Ajuste de 180 graus no teto funciona perfeitamente. Entrega muito rápida!</p>
          <div class="review-photos">
            <img class="review-photo" src="../img/review-projetor-2.jpg" alt="Foto da cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="../img/review-projetor-5.jpg" alt="Foto da cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>

        <!-- Avaliação 5 (Thiago Alcantara) -->
        <div class="review-card">
          <div class="review-header">
            <div class="review-user">
              <div class="review-avatar"><div class="review-avatar-placeholder">T</div></div>
              <div class="review-user-info">
                <div class="review-user-name">Thiago Alcantara</div>
                <div class="review-user-stars">⭐⭐⭐⭐⭐</div>
                <div class="review-date">02/10/2026 | Variação: SMART WI-FI 4K, BIVOLT</div>
              </div>
            </div>
          </div>
          <p class="review-comment">Chegou tudo certinho com o controle e cabo de energia. Recomendo usar com a luz apagada pra ter a melhor experiência. Valeu super a pena, nota 10!</p>
          <div class="review-photos">
            <img class="review-photo" src="../img/review-projetor-8.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
            <img class="review-photo" src="../img/review-projetor-3.jpg" alt="Foto do cliente" onclick="openPhotoModal(this.src)">
          </div>
        </div>

      </div>`;

html = html.replace(/<!-- AVALIAÇÕES -->[\s\S]*?<!-- DESCRIÇÃO DO PRODUTO -->/i, `${exactReviewsSection}\n\n      <!-- DESCRIÇÃO DO PRODUTO -->`);

// 9. Description section
const descHtml = `      <!-- DESCRIÇÃO DO PRODUTO -->
      <div class="description-section">
        <h3 class="section-title">Descrição</h3>
        <div class="description-text">
          <strong>🍿 Cinema Portátil 4K no Teto do seu Quarto 🍿</strong><br><br>
          O <strong>Mini Projetor HY300 Original Smart</strong> é a revolução do entretenimento portátil. Equipado com <strong>Android 11 integrado</strong>, ele permite baixar seus aplicativos favoritos como <strong>Netflix, YouTube, Prime Video, Disney+ e Globoplay</strong> diretamente no aparelho, sem precisar de computador ou TV Box externa.<br><br>
          Com seu inovador <strong>suporte com rotação flexível de 180°</strong>, você pode posicionar o projetor na mesinha de cabeceira e projetar suas séries e filmes favoritos <strong>diretamente no teto enquanto fica deitado confortavelmente na cama</strong>, ou em qualquer parede criando uma tela gigante de <strong>até 130 polegadas</strong> com foco cristalino.<br><br>
          <strong>Destaques e Especificações Técnicas:</strong><br>
          • <strong>Sistema Android 11.0 Smart:</strong> Acesso direto à Google Play Store para baixar apps e jogos.<br>
          • <strong>Suporte 4K Ultra HD & Resolução Nativa HD:</strong> Decodificação inteligente para imagens nítidas, cores vibrantes e alto contraste.<br>
          • <strong>Conexão Wi-Fi 6 Dual Band (2.4G / 5G):</strong> Transmissão ultra rápida sem atraso (lag) para streaming e espelhamento de celular (iOS e Android).<br>
          • <strong>Bluetooth 5.0 Bidirecional:</strong> Conecte facilmente caixas de som sem fio (JBL, fones Bluetooth ou soundbars) para som de cinema imersivo.<br>
          • <strong>Ajuste de Foco Manual & Correção Keystone Automática:</strong> Alinha a imagem retangular perfeitamente mesmo em ângulos inclinados.<br>
          • <strong>Entradas Múltiplas:</strong> Conexão HDMI (para PS5, Xbox, PC, Notebook), USB (pendrives e periféricos) e saída de áudio P2 (3.5mm).<br>
          • <strong>Alto-Falante Hi-Fi Integrado:</strong> Áudio nítido embutido para usar onde você quiser sem precisar de caixas externas.<br>
          • <strong>Super Silencioso e Compacto:</strong> Sistema de resfriamento avançado com baixíssimo ruído de ventoinha.<br><br>
          <strong>Conteúdo da Embalagem:</strong><br>
          • 1x Projetor HY300 Original Smart 4K<br>
          • 1x Controle Remoto Inteligente<br>
          • 1x Cabo de Energia Bivolt (110V - 220V)<br>
          • 1x Manual de Instruções em Português<br><br>
          <strong>Garantia Oficial:</strong> 12 meses de garantia de fábrica com troca imediata e suporte técnico no Brasil. Envio prioritário com rastreamento e entrega rápida!
        </div>
      </div>`;

html = html.replace(/<!-- DESCRIÇÃO DO PRODUTO -->[\s\S]*?<!-- PRODUTOS RELACIONADOS -->/i, `${descHtml}\n\n      <!-- PRODUTOS RELACIONADOS -->`);

// 10. Related products
const relatedHtml = `      <!-- PRODUTOS RELACIONADOS -->
      <div class="related-section">
        <h3 class="related-title">Você também pode gostar</h3>
        <div class="related-grid">
          <a class="related-card" href="produto-104.html">
            <img class="related-img" src="https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/937eda3788b14961af3dc12028a4c886~tplv-aphluv4xwc-resize-webp:800:800.webp" alt="Chinelo Strass Luxo">
            <div class="related-info">
              <div class="related-name">Chinelo Feminino Luxo Strass Brilhante Macio Leve</div>
              <div class="related-price-row">
                <span class="related-price">R$ 19,90</span>
                <span class="related-price-original">R$ 59,90</span>
              </div>
              <div class="related-badges">
                <span class="related-discount">67% OFF</span>
                <span class="badge-frete">· Frete grátis</span>
              </div>
              <div class="related-sold">21.3K vendido(s)</div>
            </div>
          </a>
          <a class="related-card" href="produto-35.html">
            <img class="related-img" src="https://down-br.img.susercontent.com/file/sg-11134201-824i8-mdyu6aqj7g1td8" alt="Caixa JBL Boombox">
            <div class="related-info">
              <div class="related-name">Caixa de Som JBL Boombox 4 Bluetooth 210W Preta</div>
              <div class="related-price-row">
                <span class="related-price">R$ 67,43</span>
                <span class="related-price-original">R$ 497,90</span>
              </div>
              <div class="related-badges">
                <span class="related-discount">81% OFF</span>
                <span class="badge-frete">· Frete grátis</span>
              </div>
              <div class="related-sold">8.5K vendido(s)</div>
            </div>
          </a>
        </div>
      </div>`;

html = html.replace(/<!-- PRODUTOS RELACIONADOS -->[\s\S]*?<\/div><!-- fim product-info -->/i, `${relatedHtml}\n    </div><!-- fim product-info -->`);

// 11. PRODUTO_ATUAL in script
const produtoAtualJs = `const PRODUTO_ATUAL = {
  id: 105,
  nome: "Projetor HY300 Original Portátil Smart Android 11 4K Ultra HD HDMI Wifi Bluetooth Alto",
  preco: 39.90,
  preco_antigo: 399.90,
  img: "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/81525a24b6074e6c87b673c8cc37d237~tplv-aphluv4xwc-resize-webp:800:800.webp",
  imagens: [
    "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/81525a24b6074e6c87b673c8cc37d237~tplv-aphluv4xwc-resize-webp:800:800.webp",
    "../img/poster-projetor-1.jpg",
    "../img/poster-projetor-2.jpg",
    "../img/poster-projetor-3.jpg"
  ],
  variacoes: {
    "modelo": {
      "com_imagem": true,
      "label": "Modelo / Versão",
      "opcoes": [
        {
          "nome": "Modelo Básico (Cabo HDMI / AV)",
          "preco": 39.90,
          "imagem": "https://p16-oec-sg.ibyteimg.com/tos-alisg-i-aphluv4xwc-sg/81525a24b6074e6c87b673c8cc37d237~tplv-aphluv4xwc-resize-webp:800:800.webp"
        },
        {
          "nome": "⭐ Smart Wi-Fi 4K (Android + Netflix/YouTube)",
          "preco": 59.90,
          "imagem": "../img/poster-projetor-2.jpg"
        },
        {
          "nome": "Combo Cinema VIP (Tripé 360° + Tela 100\\\")",
          "preco": 89.90,
          "imagem": "../img/poster-projetor-3.jpg"
        }
      ]
    },
    "voltagem": {
      "label": "Voltagem",
      "opcoes": ["Bivolt Automático (110V/220V)"]
    }
  }
};`;

html = html.replace(/const PRODUTO_ATUAL = \{[\s\S]*?\n\};/i, produtoAtualJs);

// Write to both ds and stone_shop_clone
fs.writeFileSync(path.join(dsDir, 'pages', 'produto-105.html'), html, 'utf8');
fs.writeFileSync(path.join(cloneDir, 'pages', 'produto-105.html'), html, 'utf8');

console.log('produto-105.html regenerated with EXACT standard reviews layout in both repositories!');
