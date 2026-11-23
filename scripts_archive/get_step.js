const fs = require('fs');
const readline = require('readline');

const rl = readline.createInterface({
  input: fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/.system_generated/logs/transcript_full.jsonl'),
  crlfDelay: Infinity
});

rl.on('line', (line) => {
  try {
    const data = JSON.parse(line);
    if (data.step_index >= 384 && data.step_index <= 395) {
      console.log(`Step ${data.step_index}: source=${data.source}`);
      if (data.content && data.content.includes('.mp4')) {
        console.log('Found .mp4 in content at step', data.step_index);
      }
    }
  } catch (e) {}
});
