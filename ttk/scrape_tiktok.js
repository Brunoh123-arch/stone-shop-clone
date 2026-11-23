const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: false, // Running with head or headless - let's check with standard headless or headed. TikTok often detects headless, but headless: 'new' or headed might work. Let's try headless: 'new' first.
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--window-size=1920,1080',
      '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    window.chrome = { runtime: {} };
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['pt-BR', 'pt', 'en-US', 'en'] });
  });

  const recordedRequests = [];

  page.on('request', req => {
    recordedRequests.push({
      time: new Date().toISOString(),
      url: req.url(),
      method: req.method(),
      resourceType: req.resourceType(),
      headers: req.headers(),
      postData: req.postData()
    });
  });

  const apiResponses = [];

  page.on('response', async res => {
    const req = res.request();
    const type = req.resourceType();
    const url = res.url();
    if (['xhr', 'fetch', 'document'].includes(type) || url.includes('api') || url.includes('shop') || url.includes('feed') || url.includes('item_list') || url.includes('detail')) {
      let bodyText = null;
      try {
        const ct = res.headers()['content-type'] || '';
        if (ct.includes('json') || ct.includes('text') || ct.includes('javascript')) {
          bodyText = await res.text();
        }
      } catch (e) {
        // body could not be retrieved
      }
      apiResponses.push({
        url: url,
        status: res.status(),
        type: type,
        headers: res.headers(),
        body: bodyText ? (bodyText.length > 50000 ? bodyText.substring(0, 50000) + '...[truncated]' : bodyText) : null
      });
    }
  });

  console.log('Navigating to https://www.tiktok.com/@nandaa1332 ...');
  try {
    await page.goto('https://www.tiktok.com/@nandaa1332', {
      waitUntil: 'networkidle2',
      timeout: 30000
    });
  } catch (err) {
    console.log('Navigation warning/timeout:', err.message);
  }

  console.log('Page loaded, waiting 5 seconds...');
  await new Promise(r => setTimeout(r, 5000));

  await page.screenshot({ path: 'screenshot_profile.png' });
  console.log('Screenshot taken: screenshot_profile.png');

  // Get page title and basic info
  const title = await page.title();
  console.log('Page title:', title);

  // Look for tabs on the profile (e.g. Videos, Shop, Vitrine, Showcase)
  const tabs = await page.evaluate(() => {
    const tabEls = Array.from(document.querySelectorAll('p, span, div, a, button'))
      .filter(el => {
        const text = el.innerText ? el.innerText.trim() : '';
        return ['Shop', 'Loja', 'Vitrine', 'Showcase', 'Vídeos', 'Videos', 'Favoritos', 'Curtidas', 'Reposts'].includes(text);
      })
      .map(el => ({
        tag: el.tagName,
        text: el.innerText.trim(),
        className: el.className,
        role: el.getAttribute('role'),
        href: el.getAttribute('href')
      }));
    return tabEls;
  });
  console.log('Detected tabs/buttons:', JSON.stringify(tabs, null, 2));

  // Check if there is a shop tab to click
  const shopTabFound = await page.evaluate(() => {
    const targets = Array.from(document.querySelectorAll('*')).filter(el => {
      const text = (el.innerText || '').trim().toLowerCase();
      return (text === 'shop' || text === 'vitrine' || text === 'loja' || text === 'showcase') && el.children.length === 0;
    });
    if (targets.length > 0) {
      targets[0].click();
      return true;
    }
    return false;
  });

  if (shopTabFound) {
    console.log('Clicked shop/vitrine tab! Waiting for requests...');
    await new Promise(r => setTimeout(r, 6000));
    await page.screenshot({ path: 'screenshot_shop.png' });
  } else {
    console.log('No direct shop tab click target found.');
  }

  // Scroll down a bit to trigger lazy loading
  console.log('Scrolling down...');
  await page.evaluate(() => window.scrollBy(0, 1000));
  await new Promise(r => setTimeout(r, 3000));

  // Extract rehydration data / scripts from HTML
  const pageData = await page.evaluate(() => {
    const sigiState = window.SIGI_STATE || null;
    const universalData = window.__UNIVERSAL_DATA_FOR_REHYDRATION__ || null;
    const scripts = Array.from(document.querySelectorAll('script')).map(s => ({
      id: s.id,
      src: s.src,
      type: s.type,
      textLength: s.innerText ? s.innerText.length : 0
    }));
    return {
      sigiState,
      universalData,
      scriptsCount: scripts.length,
      scripts: scripts.filter(s => s.src || s.id)
    };
  });

  // Save results
  fs.writeFileSync('requests.json', JSON.stringify(recordedRequests, null, 2));
  fs.writeFileSync('api_responses.json', JSON.stringify(apiResponses, null, 2));
  fs.writeFileSync('page_data.json', JSON.stringify(pageData, null, 2));

  console.log(`Finished! Total requests: ${recordedRequests.length}, API/XHR responses: ${apiResponses.length}`);
  await browser.close();
})();
