const fs = require('fs');

async function testKernel() {
  const url = 'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/js/biz.shared.kernel.init.a5248099.js';
  const res = await fetch(url);
  const text = await res.text();
  const idx = text.indexOf('shouldShowShop');
  if (idx !== -1) {
    console.log('Snippet around shouldShowShop:');
    console.log(text.substring(Math.max(0, idx - 200), Math.min(text.length, idx + 400)));
  }
}

testKernel();
