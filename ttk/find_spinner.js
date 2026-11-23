const fs = require('fs');

async function searchSpinner() {
  const cssUrls = [
    'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/assets/index.b5f3c689.css',
    'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/assets/styles.814f3d15.css',
    'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/assets/all.871b7edc.css'
  ];

  for (const url of cssUrls) {
    try {
      const res = await fetch(url);
      const text = await res.text();
      // Search for keyframe or loading animation
      const matches = text.match(/@keyframes[^{]+{[^}]+}/gi);
      if (matches) {
        console.log(`Keyframes in ${url.split('/').pop()}:`, matches.slice(0, 10));
      }
    } catch (e) {
      console.log('Error:', e.message);
    }
  }
}

searchSpinner();
