const puppeteer = require('../ttk/node_modules/puppeteer-core');
const fs = require('fs');

(async () => {
  console.log('Iniciando Chrome isolado...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });

  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
  });

  const targetUrl = 'https://shop.tiktok.com/br/pdp/escova-alisadora-5-em-1-alisa-seca-hidrata-modela-anti-frizz/1733725427997246564';
  console.log('Navegando para:', targetUrl);

  const capturedApis = [];
  page.on('response', async res => {
    const u = res.url();
    if (u.includes('api') || u.includes('review') || u.includes('pdp') || u.includes('oec') || u.includes('item')) {
      try {
        const text = await res.text();
        capturedApis.push({ url: u, text });
      } catch (e) {}
    }
  });

  try {
    await page.goto(targetUrl, { waitUntil: 'networkidle2', timeout: 35000 });
  } catch (e) {
    console.log('Goto err/timeout:', e.message);
  }

  await new Promise(r => setTimeout(r, 4000));

  const title = await page.title();
  console.log('Page Title:', title);
  console.log('Captured APIs count:', capturedApis.length);

  // Check review elements or json in page
  const pageData = await page.evaluate(() => {
    const scripts = Array.from(document.querySelectorAll('script')).map(s => s.innerText);
    const candidateData = scripts.filter(s => s.includes('product_reviews') || s.includes('review_info') || s.includes('review_rating'));
    return {
      title: document.title,
      candidateScriptsCount: candidateData.length,
      candidateSamples: candidateData.map(s => s.substring(0, 300))
    };
  });

  console.log('Candidate scripts:', pageData.candidateScriptsCount);
  fs.writeFileSync('scripts/captured_108_apis.json', JSON.stringify(capturedApis, null, 2), 'utf-8');

  await browser.close();
  console.log('Pronto!');
})();
