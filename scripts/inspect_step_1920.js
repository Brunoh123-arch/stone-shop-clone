const fs = require('fs');
const readline = require('readline');

async function getStep() {
  const fileStream = fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/b18f76ca-784b-46cc-a262-b96b1682f455/.system_generated/logs/transcript_full.jsonl');
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });
  
  for await (const line of rl) {
    if (!line) continue;
    try {
      const obj = JSON.parse(line);
      if (obj.step_index >= 1918 && obj.step_index <= 1923) {
        console.log('[Step ' + obj.step_index + '] ' + obj.source + ': ' + (typeof obj.content === 'string' ? obj.content.slice(0, 600) : obj.type));
        if (obj.thinking) {
          console.log('THINKING:', obj.thinking.slice(0, 600));
        }
      }
    } catch(e) {}
  }
}
getStep();
