const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

const targetUrl = 'https://www.tiktok.com/view/product/1738069213963388745?_d=f35d27e862e8cg&_svg=1&chain_key=%7B%22t%22%3A1%2C%22k%22%3A%22000000000000000007703069033205384961%22%2C%22sc%22%3A%22copy%22%7D&checksum=685a0a1678364be0bbab68eab4e00042f15a1f1b7af725522ff541c836327855&share_region=BR';

(async () => {
  console.log('Iniciando navegador com Chrome real...');
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

  const apiResponses = [];

  page.on('response', async res => {
    const url = res.url();
    if (url.includes('api') || url.includes('pdp') || url.includes('shop') || url.includes('review') || url.includes('item')) {
      try {
        const text = await res.text();
        apiResponses.push({ url, text });
      } catch (e) {}
    }
  });

  console.log('Navegando para URL:', targetUrl);
  try {
    await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 30000 });
  } catch (e) {
    console.log('Goto timeout/erro, continuando...', e.message);
  }

  await new Promise(r => setTimeout(r, 4000));

  const pageTitle = await page.title();
  console.log('Título da página:', pageTitle);

  const html = await page.content();
  fs.writeFileSync('product_dump.html', html);
  fs.writeFileSync('product_apis.json', JSON.stringify(apiResponses, null, 2));

  await page.screenshot({ path: 'product_screenshot.png', fullPage: false });
  console.log('Salvo product_dump.html, product_apis.json, product_screenshot.png');

  await browser.close();
})();
