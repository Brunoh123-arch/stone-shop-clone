const fs = require('fs');
const path = require('path');

const candidates = [
  'C:/Users/Dell/Downloads/ds/.playwright-mcp',
  'C:/Users/Dell/Downloads/ds',
  'C:/Users/Dell/Downloads/stone_shop_clone/.playwright-mcp',
  'C:/Users/Dell/.playwright-mcp'
];

for (const c of candidates) {
  if (fs.existsSync(c)) {
    console.log('Dir exists:', c);
    const files = fs.readdirSync(c);
    const matched = files.filter(f => f.includes('produto') || f.includes('chinelo') || f.endsWith('.json'));
    console.log('Matches in', c, ':', matched);
  }
}
