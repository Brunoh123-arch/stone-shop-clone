const fs = require('fs');

async function findSvg() {
  const url = 'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/js/cache.tux.1abe1f5f.js';
  const res = await fetch(url);
  const text = await res.text();
  const idx = text.indexOf('TUXLoading-greenhole');
  if (idx !== -1) {
    console.log('Found SVG definition:');
    console.log(text.substring(Math.max(0, idx - 300), Math.min(text.length, idx + 600)));
  }
}

findSvg();
