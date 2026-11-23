const fs = require('fs');

const requests = JSON.parse(fs.readFileSync('requests.json', 'utf8'));
const responses = JSON.parse(fs.readFileSync('api_responses.json', 'utf8'));

// Map of url to status / body
const resMap = {};
responses.forEach(r => {
  resMap[r.url] = r;
});

// Group requests by categories
const apis = [];
const scripts = [];
const monitors = [];
const others = [];

requests.forEach((r, idx) => {
  const url = r.url;
  const res = resMap[url] || {};
  const status = res.status || (url.startsWith('https://sf16') ? 200 : '-');
  const u = new URL(url);

  const item = {
    id: idx + 1,
    method: r.method,
    status: status,
    host: u.hostname,
    pathname: u.pathname,
    search: u.search,
    type: r.resourceType,
    fullUrl: url,
    bodyPreview: res.body ? res.body.substring(0, 300) : null
  };

  if (url.includes('/api/') || url.includes('/wallet_api') || url.includes('/tiktok/pns/') || url.includes('/popup/') || url.includes('/ttwid/')) {
    apis.push(item);
  } else if (r.resourceType === 'script' || u.pathname.endsWith('.js')) {
    scripts.push(item);
  } else if (u.hostname.includes('mon') || u.hostname.includes('mcs') || u.hostname.includes('mssdk') || url.includes('collect')) {
    monitors.push(item);
  } else {
    others.push(item);
  }
});

fs.writeFileSync('detailed_tables.json', JSON.stringify({ apis, scripts, monitors, others }, null, 2), 'utf8');
console.log('Saved detailed_tables.json');
console.log(`APIs: ${apis.length}, Scripts: ${scripts.length}, Monitors: ${monitors.length}, Others: ${others.length}`);
