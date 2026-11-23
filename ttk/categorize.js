const fs = require('fs');

const requests = JSON.parse(fs.readFileSync('requests.json', 'utf8'));

console.log('Total requests captured:', requests.length);

const categories = {
  api: [],
  shop_or_commerce: [],
  security_antibot: [],
  telemetry_monitoring: [],
  scripts_bundles: [],
  media_static: [],
  other: []
};

requests.forEach(r => {
  const url = r.url;
  const u = new URL(url);
  const path = u.pathname;
  const host = u.hostname;

  if (url.includes('shop') || url.includes('commerce') || url.includes('showcase') || url.includes('seller') || url.includes('wallet') || url.includes('recharge')) {
    categories.shop_or_commerce.push({ method: r.method, host, path, url: r.url });
  } else if (url.includes('/api/') || url.includes('/tiktok/pns/') || url.includes('/popup/')) {
    categories.api.push({ method: r.method, host, path, url: r.url });
  } else if (host.includes('mon') || host.includes('mcs') || host.includes('vcs') || url.includes('collect') || url.includes('report') || url.includes('log')) {
    categories.telemetry_monitoring.push({ method: r.method, host, path, url: r.url });
  } else if (url.includes('slardar') || url.includes('mssdk') || url.includes('waf') || url.includes('turing') || url.includes('pumbaa') || url.includes('ttwid')) {
    categories.security_antibot.push({ method: r.method, host, path, url: r.url });
  } else if (r.resourceType === 'script' || path.endsWith('.js')) {
    categories.scripts_bundles.push({ method: r.method, host, path, url: r.url });
  } else if (['image', 'media', 'font', 'stylesheet'].includes(r.resourceType) || path.endsWith('.css') || path.endsWith('.png') || path.endsWith('.jpg') || path.endsWith('.woff2')) {
    categories.media_static.push({ method: r.method, host, path, url: r.url });
  } else {
    categories.other.push({ method: r.method, host, path, resourceType: r.resourceType, url: r.url });
  }
});

console.log('--- SUMMARY OF CATEGORIES ---');
console.log('Shop / Commerce / Wallet:', categories.shop_or_commerce.length);
console.log('APIs:', categories.api.length);
console.log('Security & Anti-bot (WAF / MSSDK / Turing):', categories.security_antibot.length);
console.log('Telemetry & Monitoring (Slardar / Mon / MCS):', categories.telemetry_monitoring.length);
console.log('Scripts & Bundles (JS Webpack/Vite):', categories.scripts_bundles.length);
console.log('Media & Static (CSS, Images, Fonts):', categories.media_static.length);
console.log('Other:', categories.other.length);

fs.writeFileSync('categorized_requests.json', JSON.stringify(categories, null, 2), 'utf8');
