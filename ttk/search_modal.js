const fs = require('fs');

async function searchModalToast() {
  const url = 'https://sf16-website-login.neutral.ttwstatic.com/obj/tiktok_web_login_static/tiktok/webapp/main/react-v18/webapp-desktop/static/assets/styles.814f3d15.css';
  const res = await fetch(url);
  const text = await res.text();

  // Search for Toast, Modal, Dialog with Loading
  const matches = text.match(/\.[a-zA-Z0-9_\-]*(toast|Toast|dialog|Dialog|hud|HUD|card|Card)[a-zA-Z0-9_\-]*\s*\{[^}]+\}/g);
  if (matches) {
    console.log('Matches:', matches.slice(0, 15));
  }

  // Look for styles with rgba(0,0,0, or border-radius around loading
  const idx = text.indexOf('TUXLoading-container');
  if (idx !== -1) {
    console.log('Context of TUXLoading-container:');
    console.log(text.substring(Math.max(0, idx - 200), Math.min(text.length, idx + 400)));
  }
}

searchModalToast();
