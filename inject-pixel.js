const fs = require('fs');

const pixelSnippet = `<!-- TikTok Pixel Code Start -->
<script>
!function (w, d, t) {
  w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie","holdConsent","revokeConsent","grantConsent"],ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){for(
var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e},ttq.load=function(e,n){var r="https://analytics.tiktok.com/i18n/pixel/events.js",o=n&&n.partner;ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=r,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};n=document.createElement("script")
;n.type="text/javascript",n.async=!0,n.src=r+"?sdkid="+e+"&lib="+t;e=document.getElementsByTagName("script")[0];e.parentNode.insertBefore(n,e)};

  ttq.load('DB31ROJC77U04C8M50Q0');
  ttq.page();
}(window, document, 'ttq');
</script>
<!-- TikTok Pixel Code End -->
`;

function injectPixel(filePath) {
  if (!fs.existsSync(filePath)) return;
  let html = fs.readFileSync(filePath, 'utf8');
  if (html.includes('DB31ROJC77U04C8M50Q0')) {
    console.log('Ja possui pixel:', filePath);
    return;
  }
  if (html.includes('<head>')) {
    html = html.replace('<head>', '<head>\n' + pixelSnippet);
  } else if (html.includes('<head ')) {
    html = html.replace(/<head[^>]*>/, '$&\n' + pixelSnippet);
  } else {
    html = pixelSnippet + '\n' + html;
  }
  fs.writeFileSync(filePath, html, 'utf8');
  console.log('Pixel injetado em:', filePath);
}

const files = [
  'c:/Users/Dell/Downloads/ds/index.html',
  'c:/Users/Dell/Downloads/ds/confirmar-saque.html',
  'c:/Users/Dell/Downloads/ds/quiz/pesquisa/index.html',
  'c:/Users/Dell/Downloads/ds-quiz/index.html',
  'c:/Users/Dell/Downloads/ds-quiz/confirmar-saque-quiz.html',
  'c:/Users/Dell/Downloads/ds-quiz/quiz/pesquisa/index.html'
];

files.forEach(injectPixel);
console.log('Finalizado com sucesso!');
