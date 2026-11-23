const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

console.log('>>> [BRUNO CTO] APLICANDO TIPOGRAFIA OFICIAL TIKTOK IOS EM TODO O SITE <<<');

// 1. IMPORTAR FONTE COM PROPORÇÕES IDÊNTICAS AO SAN FRANCISCO DO IOS NO HEAD
const fontLink = `<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">`;

if (!html.includes('Plus+Jakarta+Sans')) {
  html = html.replace('<head>', `<head>\n${fontLink}`);
}

// 2. CSS DE TIPOGRAFIA PURA TIKTOK IOS
const iosTypographyCss = `
    /* === TIPOGRAFIA OFICIAL TIKTOK IOS (SAN FRANCISCO / TIKTOK SANS) === */
    :root {
      --font-tiktok: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Plus Jakarta Sans", "Inter", "TikTok Sans", sans-serif;
    }

    body, button, input, select, textarea, h1, h2, h3, h4, h5, h6, p, span, div, a {
      font-family: var(--font-tiktok) !important;
      -webkit-font-smoothing: antialiased !important;
      -moz-osx-font-smoothing: grayscale !important;
      text-rendering: optimizeLegibility !important;
    }

    /* Títulos dos produtos estilo iOS TikTok */
    .product-name, .principais-prod-title {
      font-family: var(--font-tiktok) !important;
      font-size: 13.5px !important;
      font-weight: 500 !important;
      color: #161823 !important;
      line-height: 1.34 !important;
      letter-spacing: -0.2px !important;
      margin: 0 0 4px 0 !important;
    }

    /* Abas estilo iOS TikTok */
    .nav-tab {
      font-family: var(--font-tiktok) !important;
      letter-spacing: -0.3px !important;
      font-size: 16px !important;
    }

    .nav-tab.active {
      color: #161823 !important;
      font-weight: 700 !important;
    }

    /* Título "Principais produtos" */
    #principais-produtos-section h2 {
      font-family: var(--font-tiktok) !important;
      font-size: 19px !important;
      font-weight: 700 !important;
      color: #161823 !important;
      letter-spacing: -0.4px !important;
    }

    /* Preços estilo iOS TikTok */
    .price-current-txt, .principais-price-cur {
      font-family: var(--font-tiktok) !important;
      font-weight: 700 !important;
      letter-spacing: -0.3px !important;
      font-feature-settings: "tnum" !important;
      color: #fe2c55 !important;
    }

    .price-old-txt, .principais-price-old {
      font-family: var(--font-tiktok) !important;
      font-weight: 400 !important;
      letter-spacing: -0.1px !important;
      color: #8a8b91 !important;
    }

    /* Vendas e Avaliações estilo iOS */
    .sales-count-txt, .principais-sales-txt, .card-rating-row {
      font-family: var(--font-tiktok) !important;
      font-weight: 400 !important;
      letter-spacing: -0.15px !important;
      color: #8a8b91 !important;
    }

    /* Badge Frete Grátis iOS */
    .badge-frete-gratis {
      font-family: var(--font-tiktok) !important;
      letter-spacing: -0.1px !important;
    }

    /* Como as fotos recortadas já contêm os selos TOP 1, 2, 3 em alta resolução, ocultar a tag html duplicada */
    .top-ranking-badge {
      display: none !important;
    }
`;

html = html.replace('</head>', `<style>\n${iosTypographyCss}\n</style>\n</head>`);

// 3. REMOVER O SELO HTML DUPLICADO DENTRO DOS CARDS DOS PRINCIPAIS PRODUTOS
html = html.replace(/<div class="top-ranking-badge[^"]*">[^<]*<\/div>/g, '');

fs.writeFileSync('index.html', html, 'utf8');
console.log('✅ Tipografia TikTok iOS injetada com sucesso no index.html!');
