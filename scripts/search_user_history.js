const fs = require('fs');
const readline = require('readline');

async function search() {
  const fileStream = fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/b18f76ca-784b-46cc-a262-b96b1682f455/.system_generated/logs/transcript.jsonl');
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });
  
  for await (const line of rl) {
    if (!line) continue;
    try {
      const obj = JSON.parse(line);
      if (obj.type === 'USER_INPUT') {
        const text = typeof obj.content === 'string' ? obj.content : JSON.stringify(obj.content);
        if (/juros|parcel|cupom|espa[cç]o|ticket|barra|pre[cç]o/i.test(text)) {
          console.log(`[Step ${obj.step_index}] USER:`, text);
        }
      }
    } catch(e) {}
  }
}
search();
