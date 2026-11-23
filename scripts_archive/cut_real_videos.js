const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const baseImg = path.join(__dirname, 'img');
const sourceVideo = path.join(baseImg, 'video-chinelo-oficial.mp4');

console.log('Source video:', sourceVideo, 'exists?', fs.existsSync(sourceVideo));

const cuts = [
  {
    name: 'video-chinelo-completo.mp4',
    poster: 'poster-chinelo-completo.jpg',
    ss: '00:00:00',
    t: '20',
    desc: 'Gente, chocada com o brilho desse chinelo de strass! Super macio, parece que tô pisando em nuvem. Chegou em 3 dias! 🌸'
  },
  {
    name: 'video-chinelo-take1.mp4',
    poster: 'poster-chinelo-take1.jpg',
    ss: '00:00:00',
    t: '6',
    desc: 'Olha que lindeza esse modelo nos pés! O acabamento é impecável e muito delicado. Amei! ✨'
  },
  {
    name: 'video-chinelo-take2.mp4',
    poster: 'poster-chinelo-take2.jpg',
    ss: '00:00:05',
    t: '6',
    desc: 'A sola é super macia e flexível, dá pra dobrar inteira! Não cansa o pé de jeito nenhum. 👡'
  },
  {
    name: 'video-chinelo-take3.mp4',
    poster: 'poster-chinelo-take3.jpg',
    ss: '00:00:10',
    t: '6',
    desc: 'O nó cravejado de strass brilha demais na luz do sol! Muito bem colado, nota 10! 💎'
  },
  {
    name: 'video-chinelo-take4.mp4',
    poster: 'poster-chinelo-take4.jpg',
    ss: '00:00:15',
    t: '5',
    desc: 'O par completo é maravilhoso, combina com qualquer look de verão. Podem comprar sem medo! 💖'
  }
];

for (const cut of cuts) {
  const outVideo = path.join(baseImg, cut.name);
  const outPoster = path.join(baseImg, cut.poster);

  // 1. Cut video
  const cmdVideo = `ffmpeg -y -ss ${cut.ss} -i "${sourceVideo}" -t ${cut.t} -c:v libx264 -preset fast -crf 22 -c:a aac -b:a 128k -movflags +faststart "${outVideo}"`;
  console.log('Generating:', cut.name);
  execSync(cmdVideo, { stdio: 'pipe' });

  // 2. Extract exact 1st frame as poster
  const cmdPoster = `ffmpeg -y -ss 00:00:00.2 -i "${outVideo}" -vframes 1 -q:v 2 "${outPoster}"`;
  console.log('Generating poster:', cut.poster);
  execSync(cmdPoster, { stdio: 'pipe' });
}

console.log('✅ Todos os 5 takes reais gerados com sucesso!');
