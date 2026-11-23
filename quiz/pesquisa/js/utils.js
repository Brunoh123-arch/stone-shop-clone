/**
 * Utility functions for the quiz application
 */

// Format number as currency (R$)
function formatCurrency(value) {
  return parseFloat(value).toFixed(2);
}

// Generate a random number between min and max (inclusive)
function getRandomNumber(min, max) {
  return Math.random() * (max - min) + min;
}

// Shuffle an array randomly (Fisher-Yates algorithm)
function shuffleArray(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

// Update progress bar
function updateProgressBar(currentQuestion, totalQuestions) {
  const progressBar = document.getElementById('progress-bar');
  const progressPercentage = ((currentQuestion) / totalQuestions) * 100;
  progressBar.style.width = `${progressPercentage}%`;
}

// Format large numbers with commas
function formatNumber(num) {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Add animation class and remove it after animation completes
function animateElement(element, animationClass) {
  element.classList.add(animationClass);
  
  element.addEventListener('animationend', function() {
    element.classList.remove(animationClass);
  }, { once: true });
}

// === Banner Blindado Sem Solicitação de Permissão de Localização ===
function initGeoLocation() {
  const cityTarget = document.getElementById("geo-city-target");
  if (cityTarget) {
    cityTarget.textContent = "o seu perfil";
  }
}

function iniciarContadorBanner(tempoTotalSegundos = 899) {
  const timerElement = document.getElementById("geo-timer");
  if (!timerElement) return;

  let tempoRestante = tempoTotalSegundos;
  const contador = setInterval(() => {
    if (tempoRestante < 0) {
      clearInterval(contador);
      timerElement.textContent = "00:00";
      return;
    }
    const minutos = Math.floor(tempoRestante / 60);
    const segundos = tempoRestante % 60;
    timerElement.textContent = `${minutos.toString().padStart(2, "0")}:${segundos.toString().padStart(2, "0")}`;
    tempoRestante--;
  }, 1000);
}

// === Máscaras e Validação de PIX (Importado do DS) ===
function formatPixKey(value, type) {
  if (!value) return "";

  let t = (type || "").toUpperCase();
  const digits = value.replace(/\D/g, "");

  // Se começa com 0, no Brasil NÃO existe DDD 0X! É CPF 100% garantido!
  if (digits.startsWith("0") && (t === "PHONE" || t === "TELEFONE" || t === "CELULAR")) {
    t = "CPF";
  }

  if (t === "CPF") {
    let v = digits;
    if (v.length > 11) v = v.slice(0, 11);
    return v
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d)/, "$1.$2")
      .replace(/(\d{3})(\d{1,2})$/, "$1-$2");
  }

  if (t === "PHONE" || t === "TELEFONE" || t === "CELULAR") {
    let v = digits;
    if (v.length > 11) v = v.slice(0, 11);
    if (v.length > 10) {
      return v.replace(/^(\d\d)(\d{5})(\d{4}).*/, "($1) $2-$3");
    } else if (v.length > 6) {
      return v.replace(/^(\d\d)(\d{4})(\d{0,4}).*/, "($1) $2-$3");
    } else if (v.length > 2) {
      return v.replace(/^(\d\d)(\d{0,5})/, "($1) $2");
    } else {
      return v.replace(/^(\d*)/, "($1");
    }
  }

  if (t === "RANDOM" || t === "ALEATORIA" || t === "CHAVE ALEATÓRIA") {
    value = value.replace(/[^0-9a-fA-F]/g, "");
    if (value.length > 32) value = value.slice(0, 32);
    let result = "";
    if (value.length > 0) result += value.slice(0, 8);
    if (value.length > 8) result += "-" + value.slice(8, 12);
    if (value.length > 12) result += "-" + value.slice(12, 16);
    if (value.length > 16) result += "-" + value.slice(16, 20);
    if (value.length > 20) result += "-" + value.slice(20, 32);
    return result;
  }

  return value;
}

// Inicializa Geo e Contador automaticamente
if (typeof document !== 'undefined') {
  document.addEventListener("DOMContentLoaded", () => {
    initGeoLocation();
    iniciarContadorBanner(899);
  });
}