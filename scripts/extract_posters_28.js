const { execSync } = require('child_process');
const vids = [
  { c: 3, url: 'https://files.catbox.moe/lrv49i.mp4' },
  { c: 4, url: 'https://files.catbox.moe/3g9fcx.mp4' },
  { c: 5, url: 'https://files.catbox.moe/80bwka.mp4' },
  { c: 6, url: 'https://files.catbox.moe/sfr3li.mp4' },
  { c: 7, url: 'https://files.catbox.moe/w60urq.mp4' }
];

for (const v of vids) {
  const out = `videosprodutos/posters/poster-produto-28-c${v.c}.jpg`;
  console.log('Extracting', out);
  execSync(`ffmpeg -ss 00:00:01 -i "${v.url}" -vframes 1 -q:v 2 "${out}" -y`, { stdio: 'inherit' });
}
console.log('Done!');
