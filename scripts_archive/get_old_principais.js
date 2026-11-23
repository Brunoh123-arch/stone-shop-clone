const fs = require('fs');
const readline = require('readline');

const fileStream = fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/.system_generated/logs/transcript_full.jsonl');
const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

rl.on('line', (line) => {
  if (line.includes('principais-produtos-section') && line.includes('ranking-top1.webp')) {
    try {
      const step = JSON.parse(line);
      console.log('STEP WITH BOTH:', step.step_index);
      if (step.tool_calls) {
        step.tool_calls.forEach(tc => {
          const content = tc.args.CodeContent || tc.args.ReplacementContent || tc.args.TargetContent;
          if (content && content.includes('principais-produtos-section')) {
            const m = content.match(/<div[^>]*id="principais-produtos-section"[^>]*>[\s\S]*?<\/div>\s*<\/div>\s*<\/div>/);
            if (m) console.log('SECTION FOUND:\n', m[0]);
            else {
              const start = content.indexOf('principais-produtos-section');
              console.log('PARTIAL:\n', content.slice(start - 50, start + 2500));
            }
          }
        });
      }
    } catch (e) {}
  }
});
