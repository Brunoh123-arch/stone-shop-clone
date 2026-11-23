const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 375, height: 812 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true
  });
  const page = await context.newPage();
  
  const fileUrl = 'file:///' + path.resolve('index.html').replace(/\\/g, '/');
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  
  // 1. Screenshot Home
  await page.screenshot({ path: 'test_home.png', fullPage: false });
  console.log('✅ Screenshot Home gerado: test_home.png');
  
  // 2. Clicar na aba Produtos
  await page.evaluate(() => {
    const tabs = document.querySelectorAll('.nav-tab');
    if (tabs[1]) tabs[1].click();
  });
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'test_produtos.png', fullPage: false });
  console.log('✅ Screenshot Produtos gerado: test_produtos.png');
  
  // 3. Clicar na aba Categorias
  await page.evaluate(() => {
    const tabs = document.querySelectorAll('.nav-tab');
    if (tabs[2]) tabs[2].click();
  });
  await page.waitForTimeout(500);
  await page.screenshot({ path: 'test_categorias.png', fullPage: false });
  console.log('✅ Screenshot Categorias gerado: test_categorias.png');

  await browser.close();
})();
