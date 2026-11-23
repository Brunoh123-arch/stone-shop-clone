const fs = require('fs');

let html = fs.readFileSync('pages/produto-104.html', 'utf8');

// 1. Injetar CSS do Tooltip
const shareCss = `
    /* === TOOLTIP CIANO COMPARTILHE OFICIAL TIKTOK SHOP === */
    .header-share-btn {
      position: relative !important;
    }
    .share-dot {
      position: absolute;
      top: 1px;
      right: 1px;
      width: 7px;
      height: 7px;
      background: #fe2c55;
      border-radius: 50%;
      border: 1.5px solid #fff;
    }
    .share-tooltip-bubble {
      position: fixed;
      top: 50px;
      right: 12px;
      background: #00a8b5;
      color: #ffffff;
      padding: 9px 12px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 500;
      line-height: 1.35;
      max-width: 230px;
      box-shadow: 0 4px 16px rgba(0, 168, 181, 0.4);
      z-index: 10005;
      cursor: pointer;
      opacity: 0;
      transform: translateY(-8px);
      transition: opacity 0.35s ease, transform 0.35s ease;
      pointer-events: auto;
      text-align: left;
    }
    .share-tooltip-bubble.visible {
      opacity: 1;
      transform: translateY(0);
    }
    .share-tooltip-arrow {
      position: absolute;
      top: -7px;
      right: 48px;
      width: 0;
      height: 0;
      border-left: 6px solid transparent;
      border-right: 6px solid transparent;
      border-bottom: 7px solid #00a8b5;
    }
`;

if (!html.includes('share-tooltip-bubble')) {
  html = html.replace('</style>', `${shareCss}\n</style>`);
}

// 2. Atualizar o botão de share com a dot vermelha
html = html.replace(
  '<button class="header-share-btn" onclick="shareProduct()" aria-label="Compartilhar"><img src="../img/share-arrow.png" alt="Compartilhar" style="width: 22px; height: 22px; object-fit: contain;"></button>',
  `<button class="header-share-btn" onclick="shareProduct()" aria-label="Compartilhar">
      <img src="../img/share-arrow.png" alt="Compartilhar" style="width: 22px; height: 22px; object-fit: contain;">
      <span class="share-dot"></span>
    </button>`
);

// 3. Injetar o elemento HTML do tooltip
if (!html.includes('id="share-tooltip-bubble"')) {
  const tooltipHtml = `
  <!-- TOOLTIP CIANO OFICIAL TIKTOK SHOP -->
  <div id="share-tooltip-bubble" class="share-tooltip-bubble" onclick="closeShareTooltip()">
    <div class="share-tooltip-arrow"></div>
    Compartilhe isso com amigos para ganhar comissões nas compras deles
  </div>
  `;
  html = html.replace('</header>', `</header>\n${tooltipHtml}`);
}

// 4. Injetar o script de ativação do tooltip
const tooltipScript = `
  // Tooltip de Compartilhamento TikTok Shop
  function initShareTooltip() {
    const tooltip = document.getElementById('share-tooltip-bubble');
    if (!tooltip) return;
    setTimeout(() => {
      tooltip.classList.add('visible');
    }, 400);

    setTimeout(() => {
      closeShareTooltip();
    }, 4800);
  }

  function closeShareTooltip() {
    const tooltip = document.getElementById('share-tooltip-bubble');
    if (tooltip) {
      tooltip.classList.remove('visible');
      setTimeout(() => {
        if (tooltip && tooltip.parentNode) tooltip.style.display = 'none';
      }, 400);
    }
  }

  document.addEventListener('DOMContentLoaded', () => {
    initShareTooltip();
  });
`;

if (!html.includes('function initShareTooltip()')) {
  html = html.replace('</body>', `<script>${tooltipScript}</script>\n</body>`);
}

fs.writeFileSync('pages/produto-104.html', html, 'utf8');
console.log('✅ pages/produto-104.html atualizado com tooltip de compartilhamento!');
