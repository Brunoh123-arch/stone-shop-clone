const fs = require('fs');
const categories = JSON.parse(fs.readFileSync('categorized_requests.json', 'utf8'));

console.log('=== SHOP / COMMERCE / WALLET ===');
categories.shop_or_commerce.forEach(x => console.log(`${x.method} ${x.host}${x.path}`));

console.log('\n=== API ENDPOINTS (DATA FETCHING) ===');
[...new Set(categories.api.map(x => `${x.method} ${x.host}${x.path}`))].forEach(x => console.log(x));

console.log('\n=== SECURITY & ANTI-BOT ===');
[...new Set(categories.security_antibot.map(x => `${x.method} ${x.host}${x.path}`))].forEach(x => console.log(x));

console.log('\n=== TELEMETRY / MONITORING (UNIQUE PATHS) ===');
[...new Set(categories.telemetry_monitoring.map(x => `${x.method} ${x.host}${x.path}`))].forEach(x => console.log(x));

console.log('\n=== OTHER REQUESTS ===');
categories.other.forEach(x => console.log(`${x.method} ${x.host}${x.path} [${x.resourceType}]`));
