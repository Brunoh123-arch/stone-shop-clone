const https = require('https');

const candidates = [
  "https://www.tiktok.com/@raysscalazans/video/7537080199381388600",
  "https://www.tiktok.com/@danny.d4ily/video/7508127820397169926",
  "https://www.tiktok.com/@dg_tudo/video/7705556265266679060",
  "https://www.tiktok.com/@amoreamoras/video/7557401811271814412",
  "https://www.tiktok.com/@ricardomartinsbrk/video/7697987109696703765",
  "https://www.tiktok.com/@myllyrecomenda/video/7703298396236320008",
  "https://www.tiktok.com/@paula.raysa/video/7646535609242176776",
  "https://www.tiktok.com/@jesiel.farias/video/7681882056850197767"
];

function fetchTikwm(url) {
  return new Promise((resolve, reject) => {
    https.get(`https://www.tikwm.com/api/?url=${encodeURIComponent(url)}`, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.code === 0 && json.data) {
            resolve(json.data);
          } else {
            resolve({ error: json.msg || 'Erro' });
          }
        } catch (e) {
          resolve({ error: e.message });
        }
      });
    }).on('error', err => resolve({ error: err.message }));
  });
}

async function run() {
  for (const url of candidates) {
    console.log(`Checking: ${url}`);
    const data = await fetchTikwm(url);
    if (data.error) {
      console.log(`  Error: ${data.error}`);
    } else {
      console.log(`  Title: ${data.title}`);
      console.log(`  Author: ${data.author ? data.author.nickname : 'n/a'} (@${data.author ? data.author.unique_id : 'n/a'})`);
      console.log(`  Duration: ${data.duration}s | Play: ${data.play ? 'OK' : 'NO'}`);
      console.log(`  Cover: ${data.cover}`);
    }
  }
}

run();
