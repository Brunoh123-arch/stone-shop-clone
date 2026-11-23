const fs = require('fs');
const readline = require('readline');

const fileStream = fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/.system_generated/logs/transcript_full.jsonl');
const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

rl.on('line', (line) => {
  if (line.includes('ranking-top1.webp')) {
    const idx = line.indexOf('ranking-top1.webp');
    console.log('SNIPPET:\n', line.slice(Math.max(0, idx - 200), Math.min(line.length, idx + 400)));
    console.log('---');
  }
});
