const fs = require('fs');
const path = require('path');

const cssPath = path.join(__dirname, '..', 'css', 'style.css');
const appJsPath = path.join(__dirname, '..', 'js', 'app.js');

// 1. Atualizar css/style.css
let css = fs.readFileSync(cssPath, 'utf8');
const bannerCss = `\n/* ========================================================================== */
/* BANNER 11.11 LIQUIDAÇÃO NO MODAL DE VARIAÇÕES (IMAGEM 1 / IMAGEM 3)        */
/* ========================================================================== */
.var-modal-banner-1111 {
  padding: 4px 16px 12px 16px !important;
  width: 100% !important;
  box-sizing: border-box !important;
}
.var-modal-banner-1111 img {
  width: 100% !important;
  max-width: 100% !important;
  height: auto !important;
  display: block !important;
  border-radius: 18px !important;
  object-fit: contain !important;
}
`;

if (!css.includes('.var-modal-banner-1111')) {
  css += bannerCss;
  fs.writeFileSync(cssPath, css, 'utf8');
  console.log('✅ css/style.css atualizado com classes do banner 11.11 no modal');
}

// 2. Atualizar js/app.js com inline styles blindados
let appJs = fs.readFileSync(appJsPath, 'utf8');
const oldBannerHtml = `<div class="var-modal-banner-1111">
        <img src="/img/banner-1111-modal.png" onerror="this.src='../img/banner-1111-modal.png'" alt="11.11 Liquidação">
      </div>`;

const newBannerHtml = `<div class="var-modal-banner-1111" style="padding: 4px 16px 12px 16px; width: 100%; box-sizing: border-box;">
        <img src="/img/banner-1111-modal.png" onerror="this.src='../img/banner-1111-modal.png'" alt="11.11 Liquidação" style="width: 100% !important; max-width: 100% !important; height: auto !important; display: block !important; border-radius: 18px !important; object-fit: contain !important;">
      </div>`;

if (appJs.includes(oldBannerHtml)) {
  appJs = appJs.replace(oldBannerHtml, newBannerHtml);
  fs.writeFileSync(appJsPath, appJs, 'utf8');
  console.log('✅ js/app.js atualizado com inline styles blindados para o banner');
}
