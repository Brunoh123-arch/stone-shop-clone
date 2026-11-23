const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
  input: fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/.system_generated/logs/transcript_full.jsonl'),
  crlfDelay: Infinity
});

rl.on('line', (line) => {
  try {
    const data = JSON.parse(line);
    if (data.step_index === 388 || data.step_index === 389) {
      console.log(`=== STEP ${data.step_index} ===`);
      console.log('Tool calls:', JSON.stringify(data.tool_calls || []).substring(0, 500));
      console.log('Content:', (data.content || '').substring(0, 1000));
    }
  } catch (e) {}
});
