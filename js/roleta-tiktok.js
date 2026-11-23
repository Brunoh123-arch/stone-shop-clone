/**
 * ROLETA OFICIAL TIKTOK SHOP - MODO ZIKA BLINDADO
 * 1. Abre ao entrar no site com animação suave.
 * 2. Dedo indicador 3D animado simulando o clique contínuo no botão rosa.
 * 3. Seleção automática regressiva (5s, 4s, 3s...).
 * 4. Ao girar, dá 5 voltas completas e desacelera caindo com precisão cirúrgica no R$ 10,00 OFF + Frete Grátis.
 * 5. Ao cair, faz transição para a tela "Ofertas para novos clientes" com cupons e cronômetro em tempo real.
 * 6. Ao clicar no botão "Comprar" ou no "X", fecha o modal e volta para o site com cupom ativado.
 */
(function () {
  'use strict';

  // Evita carregar duas vezes
  if (window.__roletaTikTokLoaded) return;
  window.__roletaTikTokLoaded = true;

  // Injeção de Estilos CSS Blindados
  var styles = `
    /* OVERLAY GLOBAL */
    .roleta-backdrop {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.78);
      backdrop-filter: blur(5px);
      -webkit-backdrop-filter: blur(5px);
      z-index: 999999;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 16px;
      box-sizing: border-box;
      opacity: 0;
      visibility: hidden;
      transition: opacity 0.35s ease, visibility 0.35s ease;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      user-select: none;
      -webkit-tap-highlight-color: transparent;
    }

    .roleta-backdrop.roleta-visible {
      opacity: 1;
      visibility: visible;
    }

    /* CONTAINER DO CONTEÚDO */
    .roleta-container {
      width: 100%;
      max-width: 330px;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
    }

    /* PASSO 1: A ROLETA */
    .roleta-step-wheel {
      width: 100%;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      transition: transform 0.35s ease, opacity 0.35s ease;
    }

    .roleta-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.28;
      margin-bottom: 22px;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
      position: relative;
    }

    .roleta-sparkle {
      position: absolute;
      width: 14px;
      height: 14px;
      pointer-events: none;
      animation: roletaTwinkle 1.8s infinite ease-in-out;
    }

    @keyframes roletaTwinkle {
      0%, 100% { opacity: 0.3; transform: scale(0.8) rotate(0deg); }
      50% { opacity: 1; transform: scale(1.2) rotate(45deg); }
    }

    /* ÁREA DA RODA */
    .roleta-wheel-box {
      position: relative;
      width: 250px;
      height: 250px;
      margin-bottom: 22px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* CONFETES DECORATIVOS NAS LATERAIS */
    .roleta-confetti-piece {
      position: absolute;
      border-radius: 2px;
      pointer-events: none;
      z-index: 5;
    }

    .roleta-disc-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: contain;
      display: block;
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.45);
      transform: rotate(0deg);
      will-change: transform;
    }

    /* CENTRO DO GO + PONTEIRO */
    .roleta-center-btn {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 68px;
      height: 78px;
      z-index: 10;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      margin-top: -6px;
      transition: transform 0.15s ease;
      outline: none;
      border: none;
      background: transparent;
      padding: 0;
    }

    .roleta-center-btn:active {
      transform: translate(-50%, -50%) scale(0.95);
    }

    .roleta-center-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }

    /* BOTÃO GIRAR */
    .roleta-btn-wrap {
      position: relative;
      width: 210px;
      margin-bottom: 14px;
    }

    .roleta-spin-button {
      width: 100%;
      height: 44px;
      background: linear-gradient(90deg, #ff2b56, #fe3e6a);
      border: none;
      border-radius: 22px;
      color: #ffffff;
      font-size: 16px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(254, 44, 85, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      outline: none;
      transition: transform 0.15s ease, filter 0.15s ease;
      animation: roletaBtnPulse 1.6s infinite ease-in-out;
    }

    .roleta-spin-button:active {
      transform: scale(0.96);
    }

    @keyframes roletaBtnPulse {
      0%, 100% {
        transform: scale(1);
        box-shadow: 0 4px 16px rgba(254, 44, 85, 0.5);
      }
      30% {
        transform: scale(0.98);
        box-shadow: 0 2px 8px rgba(254, 44, 85, 0.7);
      }
      50% {
        transform: scale(1);
        box-shadow: 0 4px 16px rgba(254, 44, 85, 0.5);
      }
    }

    /* DEDO ANIMADO CLICANDO */
    .roleta-finger-tap {
      position: absolute;
      right: -8px;
      bottom: -16px;
      width: 44px;
      height: 46px;
      pointer-events: none;
      z-index: 15;
      animation: roletaFingerTapAnim 1.6s infinite ease-in-out;
      transform-origin: top left;
      filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.4));
    }

    @keyframes roletaFingerTapAnim {
      0%, 100% {
        transform: translate(0, 0) scale(1);
      }
      30% {
        transform: translate(-4px, -4px) scale(0.88);
      }
      50% {
        transform: translate(0, 0) scale(1);
      }
      70% {
        transform: translate(-3px, -3px) scale(0.93);
      }
      85% {
        transform: translate(0, 0) scale(1);
      }
    }

    /* TEXTO DO TIMER E TERMOS */
    .roleta-auto-timer {
      font-size: 13.5px;
      color: #ffffff;
      font-weight: 600;
      margin-bottom: 6px;
      letter-spacing: -0.2px;
      text-shadow: 0 1px 4px rgba(0, 0, 0, 0.5);
    }

    .roleta-terms-link {
      font-size: 11.5px;
      color: #b5b5b5;
      text-decoration: underline;
      cursor: pointer;
      margin-bottom: 16px;
      opacity: 0.85;
    }

    /* BOTÃO FECHAR (X) REDONDO */
    .roleta-close-circle {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(0, 0, 0, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.25);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      outline: none;
      transition: background 0.2s ease, transform 0.15s ease;
      margin-top: 6px;
    }

    .roleta-close-circle:hover {
      background: rgba(0, 0, 0, 0.85);
      transform: scale(1.08);
    }

    /* ========================================================== */
    /* PASSO 2: RESULTADO (OFERTAS PARA NOVOS CLIENTES)           */
    /* ========================================================== */
    .roleta-step-result {
      width: 100%;
      display: none;
      flex-direction: column;
      align-items: center;
      text-align: center;
      animation: roletaPopIn 0.4s cubic-bezier(0.18, 0.89, 0.32, 1.28);
    }

    @keyframes roletaPopIn {
      0% {
        opacity: 0;
        transform: scale(0.85) translateY(20px);
      }
      100% {
        opacity: 1;
        transform: scale(1) translateY(0);
      }
    }

    .roleta-result-title {
      font-size: 20px;
      font-weight: 800;
      color: #ffffff;
      line-height: 1.2;
      margin-bottom: 14px;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
    }

    .roleta-result-card {
      width: 100%;
      background: #ffffff;
      border-radius: 18px;
      overflow: hidden;
      box-shadow: 0 12px 35px rgba(0, 0, 0, 0.45);
      display: flex;
      flex-direction: column;
    }

    .roleta-card-header {
      padding: 20px 16px 12px;
      text-align: center;
      background: #ffffff;
    }

    .roleta-card-title {
      font-size: 23px;
      font-weight: 800;
      color: #111111;
      letter-spacing: -0.5px;
      margin: 0;
      line-height: 1.2;
    }

    .roleta-card-sub {
      font-size: 12.5px;
      color: #777777;
      margin-top: 3px;
      font-weight: 500;
    }

    /* CUPONS LISTA */
    .roleta-coupons-body {
      padding: 0 14px 14px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      background: #ffffff;
    }

    /* CUPOM 1 (FRETE GRÁTIS CIANO) */
    .roleta-coupon-item {
      position: relative;
      border-radius: 10px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      box-sizing: border-box;
      border: 1px dashed;
    }

    .roleta-coupon-cyan {
      background: #f2fbf9;
      border-color: #8be4d2;
    }

    .roleta-coupon-pink {
      background: #fff5f7;
      border-color: #ffb8c5;
    }

    .roleta-coupon-title-cyan {
      font-size: 17.5px;
      font-weight: 800;
      color: #00bfa5;
      line-height: 1.2;
      margin: 0;
    }

    .roleta-coupon-title-pink {
      font-size: 17.5px;
      font-weight: 800;
      color: #fe2c55;
      line-height: 1.2;
      margin: 0;
    }

    .roleta-coupon-desc {
      font-size: 12px;
      color: #444444;
      margin-top: 3px;
      font-weight: 500;
    }

    .roleta-coupon-terms {
      font-size: 10.5px;
      color: #999999;
      margin-top: 2px;
    }

    /* DENTES RECORTADOS NAS LATERAIS DO TICKET */
    .roleta-coupon-item::before,
    .roleta-coupon-item::after {
      content: '';
      position: absolute;
      top: 50%;
      transform: translateY(-50%);
      width: 10px;
      height: 10px;
      background: #ffffff;
      border-radius: 50%;
      box-sizing: border-box;
    }

    .roleta-coupon-item::before {
      left: -6px;
      border-right: 1px solid #8be4d2;
    }
    .roleta-coupon-item::after {
      right: -6px;
      border-left: 1px solid #8be4d2;
    }

    .roleta-coupon-pink::before {
      border-right: 1px solid #ffb8c5;
    }
    .roleta-coupon-pink::after {
      border-left: 1px solid #ffb8c5;
    }

    /* RODAPÉ DO CARD VERMELHO/ROSA */
    .roleta-card-footer {
      background: linear-gradient(180deg, #ff2950 0%, #fe3b64 100%);
      padding: 16px 16px 18px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }

    .roleta-timer-row {
      display: flex;
      align-items: center;
      gap: 4px;
      color: #ffffff;
      font-size: 14px;
      font-weight: 700;
    }

    .roleta-time-box {
      background: rgba(0, 0, 0, 0.28);
      color: #ffffff;
      font-size: 13.5px;
      font-weight: 800;
      padding: 3px 6px;
      border-radius: 4px;
      min-width: 20px;
      text-align: center;
      line-height: 1.2;
    }

    .roleta-time-colon {
      color: #ffffff;
      font-weight: 800;
      font-size: 14px;
    }

    .roleta-buy-btn {
      width: 100%;
      height: 44px;
      background: #ffffff;
      color: #fe2c55;
      font-size: 16px;
      font-weight: 800;
      border: none;
      border-radius: 22px;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
      display: flex;
      align-items: center;
      justify-content: center;
      outline: none;
      transition: transform 0.15s ease, background 0.15s ease;
    }

    .roleta-buy-btn:active {
      transform: scale(0.97);
      background: #fafafa;
    }
  `;

  var styleEl = document.createElement('style');
  styleEl.id = 'roleta-tiktok-styles';
  styleEl.innerHTML = styles;
  document.head.appendChild(styleEl);

  // Markup dos Modais
  var backdrop = document.createElement('div');
  backdrop.id = 'roleta-backdrop';
  backdrop.className = 'roleta-backdrop';

  backdrop.innerHTML = `
    <div class="roleta-container">
      
      <!-- PASSO 1: ROLETA -->
      <div class="roleta-step-wheel" id="roleta-step-wheel">
        
        <div class="roleta-title">
          <svg class="roleta-sparkle" style="top: -6px; left: 10px;" viewBox="0 0 24 24" fill="#ffffff"><polygon points="12,2 14.5,9.5 22,12 14.5,14.5 12,22 9.5,14.5 2,12 9.5,9.5"/></svg>
          <svg class="roleta-sparkle" style="top: 22px; right: 8px;" viewBox="0 0 24 24" fill="#ffd700"><polygon points="12,2 14.5,9.5 22,12 14.5,14.5 12,22 9.5,14.5 2,12 9.5,9.5"/></svg>
          <div>Gire para desbloquear</div>
          <div>uma oferta especial ✨</div>
        </div>

        <div class="roleta-wheel-box">
          <!-- Confetes Decorativos -->
          <div class="roleta-confetti-piece" style="left: -12px; top: 38%; width: 9px; height: 16px; background: #9c27b0; transform: rotate(-25deg);"></div>
          <div class="roleta-confetti-piece" style="left: -8px; bottom: 15%; width: 14px; height: 9px; background: #4caf50; transform: rotate(15deg);"></div>
          <div class="roleta-confetti-piece" style="right: -10px; top: 40%; width: 12px; height: 12px; background: #ffc107; transform: rotate(45deg);"></div>
          <div class="roleta-confetti-piece" style="right: 8px; bottom: 8%; width: 10px; height: 14px; background: #ffeb3b; transform: rotate(-35deg);"></div>
          
          <!-- Brilhos na borda -->
          <svg class="roleta-sparkle" style="top: 14px; right: 28px;" viewBox="0 0 24 24" fill="#ffffff"><polygon points="12,2 14.5,9.5 22,12 14.5,14.5 12,22 9.5,14.5 2,12 9.5,9.5"/></svg>
          <svg class="roleta-sparkle" style="bottom: 40px; left: 16px;" viewBox="0 0 24 24" fill="#ffffff"><polygon points="12,2 14.5,9.5 22,12 14.5,14.5 12,22 9.5,14.5 2,12 9.5,9.5"/></svg>
          
          <!-- DISCO DA ROLETA -->
          <img src="/img/roleta-disco.png" id="roleta-wheel-disc" class="roleta-disc-img" alt="Roleta Oficial" onerror="this.src='../img/roleta-disco.png'">

          <!-- BOTÃO GO CENTRAL COM PONTEIRO -->
          <button type="button" class="roleta-center-btn" id="roleta-center-btn" aria-label="Girar no GO">
            <img src="/img/roleta-centro-go.png" class="roleta-center-img" alt="GO" onerror="this.src='../img/roleta-centro-go.png'">
          </button>
        </div>

        <!-- BOTÃO GIRAR COM DEDO ANIMADO -->
        <div class="roleta-btn-wrap">
          <button type="button" class="roleta-spin-button" id="roleta-spin-btn">Girar</button>
          
          <!-- DEDO INDICADOR SIMULANDO O CLIQUE -->
          <img src="/img/dedo-clique.png" id="roleta-finger-tap" class="roleta-finger-tap" alt="Dedo animado" onerror="this.src='../img/dedo-clique.png'">
        </div>

        <div class="roleta-auto-timer" id="roleta-auto-timer">Seleção automática em <span id="roleta-timer-sec">5</span> s</div>
        <div class="roleta-terms-link" onclick="window.roletaFecharModal()">Aplicam-se os termos</div>

        <!-- BOTÃO FECHAR X -->
        <button type="button" class="roleta-close-circle" id="roleta-close-wheel-btn" aria-label="Fechar" onclick="window.roletaFecharModal()">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

      <!-- PASSO 2: RESULTADO (OFERTAS PARA NOVOS CLIENTES) -->
      <div class="roleta-step-result" id="roleta-step-result">
        <div class="roleta-result-title">
          <span>✨</span>
          <span>Ofertas para novos clientes</span>
          <span>✨</span>
        </div>

        <div class="roleta-result-card">
          <div class="roleta-card-header">
            <h3 class="roleta-card-title">R$ 10,00 OFF</h3>
            <div class="roleta-card-sub">Pacote de cupons</div>
          </div>

          <div class="roleta-coupons-body">
            <!-- Cupom 1: Frete Grátis -->
            <div class="roleta-coupon-item roleta-coupon-cyan">
              <div class="roleta-coupon-title-cyan">Frete grátis</div>
              <div class="roleta-coupon-desc">Sem gasto mínimo</div>
              <div class="roleta-coupon-terms">Aplicam-se os termos</div>
            </div>

            <!-- Cupom 2: Desconto de R$ 10 -->
            <div class="roleta-coupon-item roleta-coupon-pink">
              <div class="roleta-coupon-title-pink">Desconto de R$ 10</div>
              <div class="roleta-coupon-desc">nos pedidos acima de R$ 19</div>
              <div class="roleta-coupon-terms">Aplicam-se os termos</div>
            </div>
          </div>

          <!-- Rodapé do Card com Contador e Botão Comprar -->
          <div class="roleta-card-footer">
            <div class="roleta-timer-row">
              <span>Termina em</span>
              <span class="roleta-time-box" id="roleta-box-hh">20</span>
              <span class="roleta-time-colon">:</span>
              <span class="roleta-time-box" id="roleta-box-mm">26</span>
              <span class="roleta-time-colon">:</span>
              <span class="roleta-time-box" id="roleta-box-ss">43</span>
            </div>

            <button type="button" class="roleta-buy-btn" id="roleta-buy-now-btn">Comprar</button>
          </div>
        </div>

        <!-- BOTÃO FECHAR X RESULTADO -->
        <button type="button" class="roleta-close-circle" style="margin-top: 14px;" id="roleta-close-result-btn" aria-label="Fechar" onclick="window.roletaFecharModal()">
          <svg viewBox="0 0 24 24" width="16" height="16" stroke="#ffffff" stroke-width="2.5" fill="none" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
        </button>
      </div>

    </div>
  `;

  document.body.appendChild(backdrop);

  // Estados e Variáveis de Controle
  var isSpinning = false;
  var hasSpun = false;
  var autoCountdownSeconds = 5;
  var countdownInterval = null;
  var offerTimerInterval = null;

  // Mostra a Roleta
  function abrirRoleta() {
    try {
      sessionStorage.setItem('tiktok_roleta_vista', 'true');
    } catch (e) {}
    backdrop.classList.add('roleta-visible');
    iniciarContagemRegressiva();
  }

  // Fecha o Modal e Volta pro Site
  window.roletaFecharModal = function () {
    try {
      sessionStorage.setItem('tiktok_roleta_vista', 'true');
    } catch (e) {}
    backdrop.classList.remove('roleta-visible');
    if (countdownInterval) clearInterval(countdownInterval);
    if (offerTimerInterval) clearInterval(offerTimerInterval);
  };

  // Contagem regressiva da seleção automática (5s -> 0s)
  function iniciarContagemRegressiva() {
    var timerSecEl = document.getElementById('roleta-timer-sec');
    if (!timerSecEl) return;
    autoCountdownSeconds = 5;
    timerSecEl.textContent = autoCountdownSeconds;

    if (countdownInterval) clearInterval(countdownInterval);
    countdownInterval = setInterval(function () {
      if (isSpinning || hasSpun) {
        clearInterval(countdownInterval);
        return;
      }
      autoCountdownSeconds--;
      if (timerSecEl) timerSecEl.textContent = autoCountdownSeconds;

      if (autoCountdownSeconds <= 0) {
        clearInterval(countdownInterval);
        dispararGiroRoleta();
      }
    }, 1000);
  }

  // Disparo do Giro da Roleta
  function dispararGiroRoleta() {
    if (isSpinning || hasSpun) return;
    isSpinning = true;
    hasSpun = true;

    if (countdownInterval) clearInterval(countdownInterval);

    // Ocultar dedo animado e timer
    var finger = document.getElementById('roleta-finger-tap');
    if (finger) finger.style.display = 'none';

    var autoTimer = document.getElementById('roleta-auto-timer');
    if (autoTimer) autoTimer.style.opacity = '0';

    var spinBtn = document.getElementById('roleta-spin-btn');
    if (spinBtn) {
      spinBtn.style.animation = 'none';
      spinBtn.style.opacity = '0.85';
      spinBtn.textContent = 'Girando...';
    }

    // A Roleta dá 5 voltas completas = 1800 graus e para cravado no "R$ 10,00 OFF + frete grátis" (setor de cima!)
    var disc = document.getElementById('roleta-wheel-disc');
    var grausGiro = 1800; // 5 voltas completas (360 * 5)
    
    disc.style.transition = 'transform 3.8s cubic-bezier(0.12, 0.8, 0.3, 1)';
    disc.style.transform = 'rotate(' + grausGiro + 'deg)';

    // Quando o giro terminar
    setTimeout(function () {
      isSpinning = false;

      // Pausa triunfante de 500ms no 10 OFF e troca de tela
      setTimeout(function () {
        var stepWheel = document.getElementById('roleta-step-wheel');
        var stepResult = document.getElementById('roleta-step-result');

        if (stepWheel && stepResult) {
          stepWheel.style.display = 'none';
          stepResult.style.display = 'flex';
          iniciarCronometroOferta();

          // Salva no localStorage que o cliente ganhou os cupons
          try {
            localStorage.setItem('tiktok_cupom_10_off', 'true');
            localStorage.setItem('tiktok_cupom_frete_gratis', 'true');
            localStorage.setItem('tiktok_roleta_concluida', 'true');
            sessionStorage.setItem('tiktok_roleta_vista', 'true');
          } catch (e) {}
        }
      }, 500);

    }, 3900);
  }

  // Cronômetro dinâmico regressivo no modal de resultado
  function iniciarCronometroOferta() {
    var hhEl = document.getElementById('roleta-box-hh');
    var mmEl = document.getElementById('roleta-box-mm');
    var ssEl = document.getElementById('roleta-box-ss');

    var totalSegundos = 20 * 3600 + 26 * 60 + 43; // Começa em 20:26:43

    if (offerTimerInterval) clearInterval(offerTimerInterval);
    offerTimerInterval = setInterval(function () {
      totalSegundos--;
      if (totalSegundos < 0) totalSegundos = 0;

      var h = Math.floor(totalSegundos / 3600);
      var m = Math.floor((totalSegundos % 3600) / 60);
      var s = totalSegundos % 60;

      if (hhEl) hhEl.textContent = (h < 10 ? '0' : '') + h;
      if (mmEl) mmEl.textContent = (m < 10 ? '0' : '') + m;
      if (ssEl) ssEl.textContent = (s < 10 ? '0' : '') + s;
    }, 1000);
  }

  // Eventos de clique
  var spinBtn = document.getElementById('roleta-spin-btn');
  if (spinBtn) {
    spinBtn.addEventListener('click', dispararGiroRoleta);
  }

  var centerBtn = document.getElementById('roleta-center-btn');
  if (centerBtn) {
    centerBtn.addEventListener('click', dispararGiroRoleta);
  }

  var buyBtn = document.getElementById('roleta-buy-now-btn');
  if (buyBtn) {
    buyBtn.addEventListener('click', function () {
      window.roletaFecharModal();
      if (typeof window.showToast === 'function') {
        window.showToast('🎉 Cupons de R$ 10 OFF e Frete Grátis ativados!', 3000);
      }
    });
  }

  // Verificação estrita: deve abrir apenas 1x por sessão e nunca se já concluiu/ganhou cupons
  function deveAutoAbrir() {
    try {
      if (localStorage.getItem('tiktok_roleta_concluida') === 'true' || localStorage.getItem('tiktok_cupom_10_off') === 'true') {
        return false;
      }
      if (sessionStorage.getItem('tiktok_roleta_vista') === 'true') {
        return false;
      }
      var path = window.location.pathname || '';
      if (path.indexOf('produto-') !== -1 || path.indexOf('resumo.html') !== -1 || path.indexOf('carrinho.html') !== -1) {
        return false;
      }
    } catch (e) {
      return false;
    }
    return true;
  }

  // Abre automaticamente ao carregar a página apenas se permitido
  setTimeout(function () {
    if (deveAutoAbrir()) {
      abrirRoleta();
    }
  }, 450);

  // Expõe API global para reabrir caso necessário
  window.abrirRoletaTikTok = function () {
    var stepWheel = document.getElementById('roleta-step-wheel');
    var stepResult = document.getElementById('roleta-step-result');
    var disc = document.getElementById('roleta-wheel-disc');
    var finger = document.getElementById('roleta-finger-tap');
    var autoTimer = document.getElementById('roleta-auto-timer');
    var spinBtn = document.getElementById('roleta-spin-btn');

    isSpinning = false;
    hasSpun = false;

    if (stepWheel) stepWheel.style.display = 'flex';
    if (stepResult) stepResult.style.display = 'none';
    if (disc) {
      disc.style.transition = 'none';
      disc.style.transform = 'rotate(0deg)';
    }
    if (finger) finger.style.display = 'block';
    if (autoTimer) autoTimer.style.opacity = '1';
    if (spinBtn) {
      spinBtn.style.animation = 'roletaBtnPulse 1.6s infinite ease-in-out';
      spinBtn.style.opacity = '1';
      spinBtn.textContent = 'Girar';
    }

    abrirRoleta();
  };

})();
