const fs = require('fs');

async function inspectSpinnerCSS() {
  const url = 'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/assets/styles.814f3d15.css';
  const res = await fetch(url);
  const text = await res.text();

  const idx1 = text.indexOf('@keyframes greenAnimation');
  const idx2 = text.indexOf('@keyframes redAnimation');

  console.log('--- greenAnimation ---');
  console.log(text.substring(idx1, idx1 + 600));

  console.log('\n--- redAnimation ---');
  console.log(text.substring(idx2, idx2 + 600));

  // Find classes using these animations
  const idx3 = text.indexOf('greenAnimation');
  console.log('\n--- Usage context ---');
  console.log(text.substring(Math.max(0, idx1 - 400), idx1));
}

inspectSpinnerCSS();
