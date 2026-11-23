const fs = require('fs');
const readline = require('readline');

const fileStream = fs.createReadStream('C:/Users/Dell/.gemini/antigravity/brain/40253795-724e-4836-a8ee-923b78213fd5/.system_generated/logs/transcript_full.jsonl');
const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

rl.on('line', (line) => {
  if (line.includes('"step_index":930') || line.includes('"step_index\":844') || line.includes('\"step_index\":1106')) {
    try {
      const step = JSON.parse(line);
      console.log('STEP:', step.step_index);
      if (step.tool_calls) {
        step.tool_calls.forEach(tc => {
          if (tc.name === 'replace_file_content' || tc.name === 'write_to_file') {
            console.log('Tool:', tc.name, tc.args.TargetFile);
            if (tc.args.TargetContent && tc.args.TargetContent.includes('top-products')) {
              console.log('TARGET_CONTENT:\n', tc.args.TargetContent.slice(0, 1500));
            }
            if (tc.args.ReplacementContent && tc.args.ReplacementContent.includes('top-products')) {
              console.log('REPLACEMENT_CONTENT:\n', tc.args.ReplacementContent.slice(0, 1500));
            }
          }
        });
      }
    } catch (e) {}
  }
});
