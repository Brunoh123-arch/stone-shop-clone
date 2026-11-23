const fs = require('fs');
const path = require('path');

function updateResumo(wsDir) {
  const filePath = path.join(wsDir, 'pages', 'resumo.html');
  if (!fs.existsSync(filePath)) return;

  let html = fs.readFileSync(filePath, 'utf8');

  // Substituir a função triggerTikTokBonusMoneyAnimation para usar o WebP animado oficial
  const animFunction = `    function triggerTikTokBonusMoneyAnimation() {
      const sw = document.getElementById('bonus-switch');
      if (!sw) return;

      const rect = sw.getBoundingClientRect();
      const animWidth = 72;
      const animHeight = 155;

      // Alinha a lateral direita com o switch do bônus
      const posX = rect.right - animWidth + 4;
      const posY = rect.bottom - 4;

      const animEl = document.createElement('img');
      animEl.src = '../img/tiktok-bonus-rain.webp?t=' + Date.now();
      animEl.alt = 'Bônus TikTok';
      animEl.style.cssText = 'position:fixed;left:' + posX + 'px;top:' + posY + 'px;width:' + animWidth + 'px;height:' + animHeight + 'px;object-fit:contain;pointer-events:none;z-index:9999999;';

      document.body.appendChild(animEl);

      setTimeout(function() {
        if (animEl && animEl.parentNode) {
          animEl.parentNode.removeChild(animEl);
        }
      }, 1000);
    }`;

  // Substitui a função antiga
  html = html.replace(/function triggerTikTokBonusMoneyAnimation\(\)[\s\S]*?setTimeout\(function\(\)[\s\S]*?1400\);\s*\}/, animFunction);

  fs.writeFileSync(filePath, html, 'utf8');
  console.log(`[OK] resumo.html atualizado com WebP animado em ${wsDir}`);
}

updateResumo('c:\\Users\\Dell\\Downloads\\ds');
updateResumo('c:\\Users\\Dell\\Downloads\\stone_shop_clone');
