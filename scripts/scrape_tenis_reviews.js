const puppeteer = require('../ttk/node_modules/puppeteer-core');
const fs = require('fs');

(async () => {
  console.log('Iniciando navegador com perfil stealth...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--window-size=430,932',
      '--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 430, height: 932, isMobile: true, hasTouch: true });

  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt', 'en-US', 'en'] });
  });

  const targetUrl = 'https://www.netshoes.com.br/p/tenis-kappa-pulse-branco+preto-D24-6911-028';
  console.log('Navegando para:', targetUrl);
  try {
    await page.goto(targetUrl, { waitUntil: 'domcontentloaded', timeout: 25000 });
    await new Promise(r => setTimeout(r, 4000));
    const title = await page.title();
    console.log('Page Title:', title);

    const reviews = await page.evaluate(() => {
      // Look for reviews container or comments
      const items = [];
      const reviewEls = document.querySelectorAll('.review, .customer-review, [class*="review"], [class*="comment"], [class*="avaliacao"]');
      return {
        elementsCount: reviewEls.length,
        bodyTextSnippet: document.body.innerText.slice(0, 500)
      };
    });
    console.log('Result:', reviews);
  } catch (e) {
    console.log('Erro ao navegar:', e.message);
  }

  await browser.close();
})();
