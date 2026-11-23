const fs = require('fs');
const readline = require('readline');

async function findInTranscript() {
  const transcriptPath = 'C:\\Users\\Dell\\.gemini\\antigravity\\brain\\40253795-724e-4836-a8ee-923b78213fd5\\.system_generated\\logs\\transcript_full.jsonl';
  if (!fs.existsSync(transcriptPath)) {
    console.log('Transcript full não existe');
    return;
  }

  const fileStream = fs.createReadStream(transcriptPath);
  const rl = readline.createInterface({ input: fileStream, crlfDelay: Infinity });

  for await (const line of rl) {
    if (line.includes('paint0_linear_886_9176_gold') && line.includes('Jogo de Jantar Canyon')) {
      const parsed = JSON.parse(line);
      const content = parsed.content || '';
      console.log('--- ENCONTRADO NO TRANSCRIPT! ---');
      const start = content.indexOf('<div style="background: white; padding: 16px; margin-bottom: 8px;" id="principais-produtos-section">');
      const end = content.indexOf('<!-- PRODUTOS RECOMENDADOS -->', start);
      if (start !== -1 && end !== -1) {
        fs.writeFileSync('original_principais.html', content.slice(start, end), 'utf8');
        console.log('✅ original_principais.html salvo com sucesso!');
        return;
      }
    }
  }
  console.log('Não encontrou o trecho exato');
}

findInTranscript();
