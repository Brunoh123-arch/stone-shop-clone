const puppeteer = require('../ttk/node_modules/puppeteer-core');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

  // Let's search Google for site:shop.tiktok.com/br "tenis" "kappa"
  const url = 'https://www.google.com/search?q=site%3Ashop.tiktok.com%2Fbr+inurl%3Apdp+%22kappa%22';
  console.log('Navigating to:', url);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  await new Promise(r => setTimeout(r, 2000));

  const links = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('a')).map(a => ({ href: a.href, text: a.innerText })).filter(x => x.href.includes('shop.tiktok.com'));
  });

  console.log('Found TikTok Shop Kappa PDP links:', links);
  await browser.close();
})();
