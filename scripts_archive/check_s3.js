const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');

const scripts = html.match(/<script[\s\S]*?<\/script>/gi) || [];
// Script inline 3:
const inlineScripts = scripts.filter(s => !s.includes('src='));
console.log('Total inline scripts:', inlineScripts.length);

const s3 = inlineScripts[2];
console.log('Script 3 (primeiros e últimos 500 chars):');
console.log(s3.slice(0, 300));
console.log('...');
console.log(s3.slice(s3.length - 300));
