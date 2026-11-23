const fs = require('fs');
const path = require('path');

function processWorkspace(wsDir) {
  const appJsPath = path.join(wsDir, 'js', 'app.js');
  const styleCssPath = path.join(wsDir, 'css', 'style.css');

  if (fs.existsSync(appJsPath)) {
    let appJs = fs.readFileSync(appJsPath, 'utf8');
    appJs = appJs.replace(/aria-label="Fechar">[^<]*<\/div>/g, 'aria-label="Fechar">&times;</div>');
    appJs = appJs.replace(/aria-label="Anterior">[^<]*<\/button>/g, 'aria-label="Anterior">&#8249;</button>');
    appJs = appJs.replace(/aria-label="Pr[^"]*">[^<]*<\/button>/g, 'aria-label="Próxima">&#8250;</button>');
    fs.writeFileSync(appJsPath, appJs, 'utf8');
    console.log(`[OK] app.js atualizado em ${wsDir}`);
  }

  if (fs.existsSync(styleCssPath)) {
    let styleCss = fs.readFileSync(styleCssPath, 'utf8');
    if (!styleCss.includes('.photo-modal-thumbs-bar')) {
      const modalCss = `
/* ==========================================================================
   ESTILOS COMPLETOS DO PHOTO MODAL (GALERIA MULTI-FOTOS DE AVALIAÇÕES)
   ========================================================================== */
.photo-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.94);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  z-index: 10000000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
  overflow: hidden;
}
.photo-modal.open {
  opacity: 1 !important;
  pointer-events: auto !important;
}
.photo-modal-counter {
  position: absolute;
  top: 18px;
  left: 20px;
  color: #fff;
  font-size: 15px;
  font-weight: 700;
  background: rgba(0, 0, 0, 0.6);
  padding: 4px 12px;
  border-radius: 14px;
  z-index: 10000001;
  pointer-events: none;
  letter-spacing: 0.5px;
}
.photo-modal-close {
  position: absolute;
  top: 16px;
  right: 18px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
  z-index: 10000001;
  -webkit-tap-highlight-color: transparent;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5);
}
.photo-modal-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.65);
  border: 1.5px solid rgba(255, 255, 255, 0.35);
  color: #fff;
  font-size: 26px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10000001;
  outline: none;
  transition: background 0.2s ease, transform 0.15s ease;
  -webkit-tap-highlight-color: transparent;
  box-shadow: 0 4px 12px rgba(0,0,0,0.6);
}
.photo-modal-nav-btn:active {
  transform: translateY(-50%) scale(0.9);
  background: rgba(255, 255, 255, 0.4);
}
.photo-modal-nav-prev {
  left: 12px;
}
.photo-modal-nav-next {
  right: 12px;
}
#photo-modal-content {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 55px 12px 85px;
  box-sizing: border-box;
  touch-action: pan-y;
  position: relative;
}
#photo-modal-content img,
#photo-modal-content video {
  max-width: 96vw;
  max-height: 72vh;
  object-fit: contain;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8);
  display: block;
}
.photo-modal-thumbs-bar {
  position: absolute;
  bottom: 14px;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 4px 16px;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  z-index: 10000001;
  box-sizing: border-box;
}
.photo-modal-thumbs-bar::-webkit-scrollbar {
  display: none;
}
.photo-modal-thumb {
  width: 50px;
  height: 50px;
  min-width: 50px;
  border-radius: 6px;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.35);
  cursor: pointer;
  background: #222;
  transition: border-color 0.2s ease, transform 0.2s ease;
  -webkit-tap-highlight-color: transparent;
  box-sizing: border-box;
}
.photo-modal-thumb.active {
  border-color: #fe2c55 !important;
  transform: scale(1.1);
}
.photo-modal-thumb img,
.photo-modal-thumb video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  pointer-events: none;
}
`;
      fs.appendFileSync(styleCssPath, modalCss, 'utf8');
      console.log(`[OK] style.css atualizado com estilos do photo modal em ${wsDir}`);
    } else {
      console.log(`[OK] style.css já continha estilos do photo modal em ${wsDir}`);
    }
  }
}

processWorkspace('c:\\Users\\Dell\\Downloads\\ds');
processWorkspace('c:\\Users\\Dell\\Downloads\\stone_shop_clone');
