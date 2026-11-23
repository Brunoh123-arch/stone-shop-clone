import re

with open('css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Substituir bloco Sobre este produto e Player de Vídeo no css/style.css
old_about_section = """/* ==========================================================================
   TIKTOK SHOP: SEÇÃO SOBRE ESTE PRODUTO OFICIAL (GLOBAL MULTI-PRODUTO)
   ========================================================================== */
.about-product-section {
  background: #ffffff !important;
  padding: 16px 16px 20px 16px !important;
  margin-top: 8px !important;
  box-sizing: border-box !important;
  width: 100% !important;
}

.about-section-title {
  font-size: 16px !important;
  font-weight: 700 !important;
  color: #161823 !important;
  margin: 0 0 16px 0 !important;
  line-height: 1.3 !important;
}

.about-subtitle {
  font-size: 14.5px !important;
  font-weight: 600 !important;
  color: #161823 !important;
  margin: 0 0 10px 0 !important;
}

/* Link azul Ver mais de Detalhes (alinhado à esquerda) */
.btn-detalhes-link {
  background: none !important;
  border: none !important;
  padding: 8px 0 4px 0 !important;
  color: #1e56a0 !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  cursor: pointer !important;
  text-align: left !important;
  display: inline-block !important;
  outline: none !important;
  -webkit-tap-highlight-color: transparent !important;
}

/* Player de Vídeo Oficial TikTok Shop */
.tiktok-video-card {
  position: relative !important;
  width: 100% !important;
  max-width: 480px !important;
  height: 260px !important;
  margin: 0 auto !important;
  background: #000000 !important;
  border-radius: 12px !important;
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  -webkit-tap-highlight-color: transparent !important;
}

.tiktok-video-card video {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;
  background: #000000 !important;
  display: block !important;
}

.tt-video-center-play {
  position: absolute !important;
  width: 56px !important;
  height: 56px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 2 !important;
  transition: opacity 0.2s ease, transform 0.2s ease !important;
  pointer-events: none !important;
}

.tt-video-center-play svg {
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.45)) !important;
}

.tiktok-video-card.is-playing .tt-video-center-play {
  opacity: 0 !important;
  transform: scale(0.8) !important;
}"""

new_about_section = """/* ==========================================================================
   TIKTOK SHOP: SEÇÃO SOBRE ESTE PRODUTO OFICIAL (GLOBAL MULTI-PRODUTO)
   ========================================================================== */
.about-product-section {
  background: #ffffff !important;
  padding: 14px 14px 18px 14px !important;
  margin-top: 8px !important;
  box-sizing: border-box !important;
  width: 100% !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.about-section-title {
  font-size: 15px !important;
  font-weight: 700 !important;
  color: #161823 !important;
  margin: 0 0 10px 0 !important;
  line-height: 1.25 !important;
  letter-spacing: -0.2px !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.about-subtitle {
  font-size: 14px !important;
  font-weight: 600 !important;
  color: #161823 !important;
  margin: 0 0 6px 0 !important;
  line-height: 1.3 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.product-details-block {
  margin-bottom: 14px !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.details-attributes-grid {
  display: flex !important;
  flex-direction: column !important;
  gap: 3px !important;
}

.detail-row {
  display: flex !important;
  align-items: flex-start !important;
  justify-content: flex-start !important;
  gap: 8px !important;
  font-size: 13px !important;
  line-height: 1.35 !important;
  padding: 1px 0 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.detail-row.is-hidden {
  display: none !important;
}

.detail-label {
  color: #73747b !important;
  width: 140px !important;
  min-width: 140px !important;
  flex-shrink: 0 !important;
  font-weight: 400 !important;
  font-size: 12.5px !important;
  word-break: break-word !important;
  line-height: 1.35 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

.detail-value {
  color: #161823 !important;
  flex: 1 !important;
  font-weight: 400 !important;
  font-size: 13px !important;
  word-break: break-word !important;
  line-height: 1.35 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

/* Link azul Ver mais de Detalhes (alinhado à esquerda) */
.btn-detalhes-link {
  background: none !important;
  border: none !important;
  padding: 4px 0 0 0 !important;
  margin-top: 2px !important;
  color: #2d68ff !important;
  font-size: 13px !important;
  font-weight: 400 !important;
  cursor: pointer !important;
  text-align: left !important;
  display: inline-block !important;
  outline: none !important;
  -webkit-tap-highlight-color: transparent !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
}

/* Player de Vídeo Oficial TikTok Shop (Paridade 1:1 com Imagem 3 - Altura 232px) */
.product-video-block {
  margin-top: 14px !important;
  margin-bottom: 14px !important;
}

.tiktok-video-card {
  position: relative !important;
  width: 100% !important;
  max-width: 480px !important;
  height: 232px !important;
  margin: 0 auto !important;
  background: #000000 !important;
  border-radius: 10px !important;
  overflow: hidden !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  cursor: pointer !important;
  -webkit-tap-highlight-color: transparent !important;
}

.tiktok-video-card video {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;
  background: #000000 !important;
  display: block !important;
}

.tt-video-center-play {
  position: absolute !important;
  width: 46px !important;
  height: 46px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  z-index: 2 !important;
  transition: opacity 0.2s ease, transform 0.2s ease !important;
  pointer-events: none !important;
}

.tt-video-center-play svg {
  filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.45)) !important;
}

.tiktok-video-card.is-playing .tt-video-center-play {
  opacity: 0 !important;
  transform: scale(0.8) !important;
}"""

if old_about_section in css:
    css = css.replace(old_about_section, new_about_section)
    print("✓ Substituído bloco old_about_section com sucesso!")
else:
    print("AVISO: old_about_section não bateu exato, tentando substituição cirúrgica...")

# Atualizar também a barra de controles (.tt-video-bar, .tt-video-time, etc.)
old_bar = """.tt-video-bar {
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 34px !important;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.85)) !important;
  display: flex !important;
  align-items: center !important;
  padding: 0 10px !important;
  gap: 8px !important;
  z-index: 3 !important;
  box-sizing: border-box !important;
}

.tt-video-time {
  font-size: 11px !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  color: #ffffff !important;
  font-weight: 500 !important;
  min-width: 30px !important;
}

.tt-video-progress-bg {
  flex: 1 !important;
  height: 2.5px !important;
  background: rgba(255, 255, 255, 0.35) !important;
  border-radius: 2px !important;
  cursor: pointer !important;
  position: relative !important;
  display: flex !important;
  align-items: center !important;
}

.tt-video-progress-fill {
  height: 100% !important;
  width: 0% !important;
  background: #ffffff !important;
  border-radius: 2px !important;
  transition: width 0.1s linear !important;
}"""

new_bar = """.tt-video-bar {
  position: absolute !important;
  bottom: 0 !important;
  left: 0 !important;
  width: 100% !important;
  height: 32px !important;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.75) 0%, rgba(0, 0, 0, 0.3) 60%, transparent 100%) !important;
  display: flex !important;
  align-items: center !important;
  padding: 0 10px !important;
  gap: 8px !important;
  z-index: 3 !important;
  box-sizing: border-box !important;
}

.tt-video-time {
  font-size: 11px !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
  color: #ffffff !important;
  font-weight: 400 !important;
  min-width: 28px !important;
  letter-spacing: 0.2px !important;
}

.tt-video-progress-bg {
  flex: 1 !important;
  height: 2px !important;
  background: rgba(255, 255, 255, 0.35) !important;
  border-radius: 1px !important;
  cursor: pointer !important;
  position: relative !important;
  display: flex !important;
  align-items: center !important;
}

.tt-video-progress-fill {
  height: 100% !important;
  width: 0% !important;
  background: #ffffff !important;
  border-radius: 1px !important;
  transition: width 0.1s linear !important;
}

.tt-video-btn-play, .tt-video-btn-fs {
  background: none !important;
  border: none !important;
  padding: 0 !important;
  cursor: pointer !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  outline: none !important;
  -webkit-tap-highlight-color: transparent !important;
}"""

if old_bar in css:
    css = css.replace(old_bar, new_bar)
    print("✓ Substituído bloco old_bar com sucesso!")
else:
    print("AVISO: old_bar não bateu exato!")

with open('css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("css/style.css atualizado com paridade 1:1 total!")
