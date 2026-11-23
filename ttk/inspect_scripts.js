const fs = require('fs');
const html = fs.readFileSync('hydrated_page.html', 'utf8');

const regex = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
let match;
let count = 0;
while ((match = regex.exec(html)) !== null) {
  count++;
  const attrs = match[1];
  const content = match[2];
  console.log(`Script ${count}: attrs=[${attrs.trim()}] content-len=${content.length}`);
  if (content.length > 50 && content.length < 500) {
    console.log(`Preview: ${content.substring(0, 150)}...\n`);
  } else if (content.length >= 500) {
    console.log(`Preview (large): ${content.substring(0, 150)}...\n`);
  }
}
