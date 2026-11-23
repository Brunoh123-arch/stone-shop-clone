const puppeteer = require('../ttk/node_modules/puppeteer-core');
const fs = require('fs');

(async () => {
  console.log('Testing TikTok Shop PDP direct load...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ]
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });

  const apiResponses = [];
  page.on('response', async res => {
    const url = res.url();
    if (url.includes('api') || url.includes('pdp') || url.includes('review') || url.includes('item')) {
      try {
        const text = await res.text();
        apiResponses.push({ url, text });
      } catch (e) {}
    }
  });

  const url = 'https://shop.tiktok.com/br/pdp/modelador-de-cachos-automatico-ceramica-360-bivolt/1733112053728118755';
  console.log('Navigating to:', url);
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 4000));

  const pageTitle = await page.title();
  const currentUrl = page.url();
  console.log('Page title:', pageTitle);
  console.log('Current URL:', currentUrl);

  fs.writeFileSync('scripts/pdp_109_direct_apis.json', JSON.stringify(apiResponses, null, 2));
  console.log(`Saved ${apiResponses.length} API responses to scripts/pdp_109_direct_apis.json`);

  const bodySnippet = await page.evaluate(() => document.body.innerText.slice(0, 1000));
  console.log('Body snippet:\n', bodySnippet);

  await browser.close();
})();
