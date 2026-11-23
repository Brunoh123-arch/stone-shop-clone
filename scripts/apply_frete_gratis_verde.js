const fs = require('fs');
const path = require('path');

function updateWorkspace(wsDir) {
  const cssPath = path.join(wsDir, 'css', 'style.css');
  if (!fs.existsSync(cssPath)) return;

  let css = fs.readFileSync(cssPath, 'utf8');

  // Adiciona / substitui a regra do badge-frete-gratis, badge-frete e related-discount
  const badgeCss = `
/* ==========================================================================
   BADGES OFICIAIS DOS CARDS DE PRODUTOS ("VOCÊ TAMBÉM PODE GOSTAR")
   ========================================================================== */
.badge-frete-gratis,
.badge-frete {
  display: inline-flex !important;
  align-items: center !important;
  background: #e6f9f6 !important;
  color: #00a699 !important;
  font-size: 10.5px !important;
  font-weight: 700 !important;
  padding: 1.5px 5.5px !important;
  border-radius: 3px !important;
  border: none !important;
  line-height: 1.3 !important;
  white-space: nowrap !important;
}

.related-discount {
  display: inline-flex !important;
  align-items: center !important;
  background: #ffebee !important;
  color: #fe2c55 !important;
  font-size: 10.5px !important;
  font-weight: 700 !important;
  padding: 1.5px 5.5px !important;
  border-radius: 3px !important;
  border: none !important;
  line-height: 1.3 !important;
  white-space: nowrap !important;
}
`;

  if (css.includes('.badge-frete-gratis {')) {
    css = css.replace(/\.badge-frete-gratis\s*\{[^}]*\}/g, '');
  }
  css += badgeCss;

  fs.writeFileSync(cssPath, css, 'utf8');
  console.log(`[OK] style.css atualizado com badges padronizados em ${wsDir}`);
}

updateWorkspace('c:\\Users\\Dell\\Downloads\\ds');
updateWorkspace('c:\\Users\\Dell\\Downloads\\stone_shop_clone');
