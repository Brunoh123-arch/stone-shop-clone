const fs = require('fs');
const readline = require('readline');

const fileStream = fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/.system_generated/logs/transcript_full.jsonl');
const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

rl.on('line', (line) => {
  if (line.includes('ranking-top1.webp') && (line.includes('top-products-grid') || line.includes('top-product-card'))) {
    try {
      const step = JSON.parse(line);
      console.log('FOUND AT STEP:', step.step_index);
      if (step.tool_calls) {
        step.tool_calls.forEach(tc => {
          if (tc.args.TargetContent && tc.args.TargetContent.includes('ranking-top1.webp')) {
            console.log('TARGET_CONTENT:\n', tc.args.TargetContent);
          }
          if (tc.args.ReplacementContent && tc.args.ReplacementContent.includes('ranking-top1.webp')) {
            console.log('REPLACEMENT_CONTENT:\n', tc.args.ReplacementContent);
          }
        });
      }
    } catch (e) {}
  }
});
