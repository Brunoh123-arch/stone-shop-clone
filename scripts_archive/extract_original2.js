const fs = require('fs');
const readline = require('readline');

async function findInTranscript() {
  const transcriptPath = 'C:\\Users\\Dell\\.gemini\\antigravity\\brain\\40253795-724e-4836-a8ee-923b78213fd5\\.system_generated\\logs\\transcript_full.jsonl';
  const fileStream = fs.createReadStream(transcriptPath);
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

  for await (const line of rl) {
    if (line.includes('paint0_linear_886_9176_gold') && line.includes('Jogo de Jantar Canyon')) {
      const idx = line.indexOf('principais-produtos-section');
      const start = line.lastIndexOf('<div', idx);
      const end = line.indexOf('<!-- PRODUTOS RECOMENDADOS -->', idx);
      console.log('start:', start, 'end:', end);
      if (start !== -1 && end !== -1) {
        let chunk = line.slice(start, end);
        // Desescapa se tiver barras
        chunk = chunk.replace(/\\n/g, '\n').replace(/\\"/g, '"');
        fs.writeFileSync('original_principais.html', chunk, 'utf8');
        console.log('✅ original_principais.html salvo! Tamanho:', chunk.length);
        return;
      }
    }
  }
}

findInTranscript();
