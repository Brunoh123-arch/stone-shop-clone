const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: 460, height: 900 },
    deviceScaleFactor: 2
  });
  
  const targetPath = 'file:///' + path.resolve(__dirname, '../pages/produto-104.html').replace(/\\/g, '/');
  await page.goto(targetPath);
  await page.waitForTimeout(1000);
  
  const priceSec = await page.locator('.price-section').first();
  if (await priceSec.count() > 0) {
    const box = await priceSec.boundingBox();
    await page.screenshot({
      path: 'C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/our_crop_current.png',
      clip: {
        x: 0,
        y: Math.max(0, box.y - 10),
        width: 460,
        height: 320
      }
    });
    console.log('✅ Screenshot do nosso site atual capturado com sucesso!');
  } else {
    console.log('❌ .price-section não encontrado');
  }
  await browser.close();
})();
