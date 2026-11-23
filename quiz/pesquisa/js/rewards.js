/**
 * Handles the reward distribution and display
 */

// Total reward to distribute across all questions
const TOTAL_REWARD = 559.51;
const NUM_QUESTIONS = 6;

// Áudio oficial e original de moedas do Quiz (spikebet original limpo)
const originalAudio = new Audio('media/dinheiro.mp3');

function playMoneyCoinSound() {
  try {
    originalAudio.currentTime = 0;
    const playPromise = originalAudio.play();
    if (playPromise !== undefined) {
      playPromise.catch(function(err) {
        // Fallback imediato com nova instância
        try {
          const fallback = new Audio('media/dinheiro.wav');
          fallback.play().catch(function(){});
        } catch(_) {}
      });
    }
  } catch(e) {
    try {
      const fallback = new Audio('media/dinheiro.wav');
      fallback.play().catch(function(){});
    } catch(_) {}
  }
}

// Recompensas pré-calibradas com dopamina crescente (soma exata de R$ 559.51 em 6 rodadas)
function generateRewards() {
  return [78.20, 89.40, 94.30, 96.10, 98.50, 103.01];
}

// Reward modal handling
const rewardModal = document.getElementById('reward-modal');
const rewardValue = document.getElementById('reward-value');
const continueRewardBtn = document.getElementById('continue-reward-btn');
const currentBalance = document.getElementById('current-balance');
const finalModal = document.getElementById('final-modal');
const totalReward = document.getElementById('total-reward');
const restartBtn = document.getElementById('restart-btn');

// Initialize rewards
let rewards = generateRewards();
let totalEarned = 0;

// Animate number counting
function animateValue(element, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    const current = progress * (end - start) + start;
    element.textContent = formatCurrency(current);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

// Show the reward modal with animation and confetti
function showReward(questionIndex) {
  const reward = rewards[questionIndex];
  totalEarned += reward;
  
  // Update the current balance with animation
  animateValue(currentBalance, totalEarned - reward, totalEarned, 1000);
  
  // Update the reward value in the modal with animation
  rewardValue.textContent = "0.00";
  
  // Show the modal with animation
  rewardModal.classList.add('active');
  setTimeout(() => {
    // Start confetti animation and play money sound
    startConfetti();
    playMoneyCoinSound();
    // Animate the reward value counting up
    animateValue(rewardValue, 0, reward, 1000);
  }, 100);
  
  // Add bounce animation to the reward amount
  animateElement(document.querySelector('.reward-amount'), 'bounce');
}

// Hide the reward modal
function hideReward() {
  rewardModal.classList.remove('active');
  stopConfetti();
}

// Show the final modal
function showFinalReward() {
  // Ensure the total reward displayed is exactly the TOTAL_REWARD
  totalReward.textContent = "0.00";
  
  finalModal.classList.add('active');
  setTimeout(() => {
    // Start confetti animation and play money sound
    startConfetti();
    playMoneyCoinSound();
    // Animate the final reward value counting up
    animateValue(totalReward, 0, TOTAL_REWARD, 2000);
  }, 100);
  
  // Add bounce animation to the final reward amount
  animateElement(document.querySelector('.final-content .reward-amount'), 'bounce');
}

// Hide the final modal
function hideFinalReward() {
  finalModal.classList.remove('active');
  stopConfetti();
}

// Event listeners
continueRewardBtn.addEventListener('click', () => {
  hideReward();
  nextQuestion();
});

restartBtn.addEventListener('click', () => {
  hideFinalReward();
  showPage('withdraw');
});