const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
  input: fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/.system_generated/logs/transcript.jsonl'),
  crlfDelay: Infinity
});

rl.on('line', (line) => {
  if (line.includes('vt.tiktok') || line.includes('shop.tiktok.com')) {
    const data = JSON.parse(line);
    console.log(`Step ${data.step_index} (${data.source}):`, (data.content || JSON.stringify(data.tool_calls) || '').substring(0, 300));
  }
});
