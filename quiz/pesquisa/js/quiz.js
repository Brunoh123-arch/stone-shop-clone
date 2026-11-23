/**
 * Quiz questions and logic
 */

// Quiz questions (Configurado com 6 perguntas estratégicas de alta retenção)
const quizQuestions = [
  {
    id: 1,
    question: "Como você avalia sua experiência geral no TikTok?",
    options: [
      { emoji: "😍", text: "Excelente" },
      { emoji: "😊", text: "Boa" },
      { emoji: "😐", text: "Regular" },
      { emoji: "😒", text: "Ruim" }
    ]
  },
  {
    id: 2,
    question: "Quantas horas por dia você passa no TikTok?",
    options: [
      { emoji: "⚡", text: "Menos de 1 hora" },
      { emoji: "📱", text: "1 a 2 horas" },
      { emoji: "🔥", text: "2 a 4 horas" },
      { emoji: "👑", text: "Mais de 4 horas" }
    ]
  },
  {
    id: 3,
    question: "Qual formato de conteúdo você mais assiste no feed?",
    options: [
      { emoji: "🎥", text: "Vídeos curtos rápidos" },
      { emoji: "😂", text: "Comédia e entretenimento" },
      { emoji: "ℹ️", text: "Dicas e tutoriais" },
      { emoji: "📺", text: "Lives de criadores" }
    ]
  },
  {
    id: 4,
    question: "Qual horário do dia você mais costuma abrir o TikTok?",
    options: [
      { emoji: "🌅", text: "Pela manhã" },
      { emoji: "🌞", text: "Durante a tarde" },
      { emoji: "🌜", text: "À noite" },
      { emoji: "🌙", text: "De madrugada" }
    ]
  },
  {
    id: 5,
    question: "Qual seção do aplicativo você mais gosta de explorar?",
    options: [
      { emoji: "🎯", text: "Feed Para Você" },
      { emoji: "👥", text: "Aba Seguindo" },
      { emoji: "🔍", text: "Pesquisa e Tendências" },
      { emoji: "💬", text: "Comentários e Vídeos Salvos" }
    ]
  },
  {
    id: 6,
    question: "Qual é a sua faixa etária para validação do saque?",
    options: [
      { emoji: "🎉", text: "18 a 24 anos" },
      { emoji: "💼", text: "25 a 34 anos" },
      { emoji: "🌟", text: "35 a 44 anos" },
      { emoji: "✨", text: "45 anos ou mais" }
    ]
  }
];

// Quiz state
let currentQuestionIndex = 0;
let selectedOption = null;
const quizContainer = document.getElementById('quiz-container');

// Render a question
function renderQuestion(questionIndex) {
  const question = quizQuestions[questionIndex];
  
  // Update progress
  updateProgressBar(questionIndex, quizQuestions.length);
  
  // Create the question HTML
  const questionHTML = `
    <div class="quiz-title">${question.question}</div>
    <div class="quiz-subtitle">Selecione uma opção para continuar:</div>
    <div class="options-container">
      ${question.options.map((option, index) => `
        <div class="option" data-index="${index}">
          <div class="option-content">
            <div class="option-emoji">${option.emoji}</div>
            <div class="option-text">${option.text}</div>
          </div>
          <div class="custom-checkbox"></div>
        </div>
      `).join('')}
    </div>
    <button id="continue-btn" class="continue-btn" disabled>Continuar</button>
    <div class="bonus-text">Concorra a um bônus adicional</div>
    <div class="divider"></div>
  `;
  
  // Set the HTML
  quizContainer.innerHTML = questionHTML;
  
  // Add event listeners to options
  const options = document.querySelectorAll('.option');
  options.forEach(option => {
    option.addEventListener('click', () => {
      // Remove selection from all options
      options.forEach(opt => opt.classList.remove('selected'));
      
      // Select this option
      option.classList.add('selected');
      
      // Enable the continue button
      document.getElementById('continue-btn').disabled = false;
      
      // Store the selected option
      selectedOption = parseInt(option.dataset.index);
    });
  });
  
  // Add event listener to continue button
  document.getElementById('continue-btn').addEventListener('click', () => {
    if (selectedOption !== null) {
      // Show reward
      showReward(currentQuestionIndex);
    }
  });
  
  // Animate the new question in
  animateElement(quizContainer, 'fade-in');
}

// Move to the next question
function nextQuestion() {
  currentQuestionIndex++;
  selectedOption = null;
  
  if (currentQuestionIndex < quizQuestions.length) {
    renderQuestion(currentQuestionIndex);
  } else {
    // Show final reward
    showFinalReward();
  }
}

// Reset the quiz
function resetQuiz() {
  currentQuestionIndex = 0;
  selectedOption = null;
  totalEarned = 0;
  rewards = generateRewards();
  currentBalance.textContent = "0";
  renderQuestion(currentQuestionIndex);
}