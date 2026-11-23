const fs = require('fs');
const d = JSON.parse(fs.readFileSync('./chinelo_details.json', 'utf8'));
console.log('Top keys:', Object.keys(d));

const jsonStr = JSON.stringify(d);
const matches = jsonStr.match(/https:\/\/[^"'\s]+\.mp4[^"'\s]*/g);
console.log('MP4 matches count:', matches ? matches.length : 0);
if (matches) {
  matches.forEach((m, i) => console.log(`[${i}] ${m.substring(0, 100)}...`));
}

// Check review videos
function searchForVideos(obj, path = '') {
  if (!obj) return;
  if (typeof obj === 'object') {
    for (const k of Object.keys(obj)) {
      if (k.toLowerCase().includes('video')) {
        console.log('Video key found at:', path + '.' + k, typeof obj[k]);
      }
      searchForVideos(obj[k], path + '.' + k);
    }
  }
}
searchForVideos(d);
