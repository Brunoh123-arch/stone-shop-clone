// API SERVERLESS DE RASTREAMENTO & ABANDONO (BRUNO CTO)
const https = require('https');

const CLOUD_OBJECT_URL = 'https://api.restful-api.dev/objects/ff808181a09d98f701a131c5b10f4d67';

// Buffer em memória local da instância Lambda
let sessionsCache = {};

function syncCloud(sessionsArray) {
  return new Promise((resolve) => {
    const payload = JSON.stringify({
      data: {
        sessions: sessionsArray.slice(-80),
        atualizado_em: new Date().toISOString()
      }
    });

    const req = https.request(CLOUD_OBJECT_URL, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      },
      timeout: 3000
    }, (res) => {
      resolve();
    });
    req.on('error', () => resolve());
    req.write(payload);
    req.end();
  });
}

function fetchCloud() {
  return new Promise((resolve) => {
    https.get(CLOUD_OBJECT_URL, { timeout: 3000 }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json?.data?.sessions || []);
        } catch (e) {
          resolve([]);
        }
      });
    }).on('error', () => resolve([]));
  });
}

module.exports = async function handler(req, res) {
  // CORS agressivo
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, DELETE');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  // DELETE: Limpar histórico se o admin quiser resetar
  if (req.method === 'DELETE') {
    sessionsCache = {};
    await syncCloud([]);
    return res.status(200).json({ ok: true, message: 'Histórico resetado!' });
  }

  // POST: Receber telemetria do tracker.js
  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch(e) {}
    }

    if (!body || !body.sessionId) {
      return res.status(200).json({ ok: false, error: 'Sem sessionId' });
    }

    const sid = body.sessionId;
    const existing = sessionsCache[sid] || {};

    const updated = {
      sessionId: sid,
      timestamp: body.timestamp || Date.now(),
      horaFormatada: new Date().toLocaleTimeString('pt-BR', { timeZone: 'America/Sao_Paulo' }),
      isMobile: !!body.isMobile,
      isTikTok: !!body.isTikTok,
      maxScroll: Math.max(existing.maxScroll || 0, body.maxScroll || 0),
      duracaoSegundos: Math.max(existing.duracaoSegundos || 0, body.duracaoSegundos || 0),
      etapa: body.etapa || existing.etapa || '1_visualizou_loja',
      pontoAbandono: body.pontoAbandono || existing.pontoAbandono || 'Topo da Loja'
    };

    sessionsCache[sid] = updated;

    // Sincroniza em background
    const arr = Object.values(sessionsCache);
    if (arr.length % 3 === 0) {
      syncCloud(arr).catch(() => {});
    }

    return res.status(200).json({ ok: true });
  }

  // GET: Retornar métricas e diagnóstico consolidado para o Admin
  if (req.method === 'GET') {
    // Mescla com a nuvem para não perder dados se a lambda reiniciar
    const cloudSessions = await fetchCloud();
    cloudSessions.forEach(s => {
      if (s && s.sessionId && (!sessionsCache[s.sessionId] || sessionsCache[s.sessionId].timestamp < s.timestamp)) {
        sessionsCache[s.sessionId] = s;
      }
    });

    const lista = Object.values(sessionsCache).sort((a, b) => b.timestamp - a.timestamp);
    const total = lista.length;

    if (total === 0) {
      return res.status(200).json({
        total: 0,
        tiktok_total: 0,
        scroll_medio: 0,
        tempo_medio: 0,
        funil: {
          visualizou_loja: 0,
          rolou_produto: 0,
          clicou_comprar: 0,
          abriu_carrinho: 0,
          digitou_endereco: 0,
          gerou_pix: 0
        },
        motivos_abandono: {},
        sessoes: []
      });
    }

    let somaScroll = 0;
    let somaTempo = 0;
    let tiktokTotal = 0;
    const motivos = {};

    const funil = {
      visualizou_loja: 0,
      rolou_produto: 0,
      clicou_comprar: 0,
      abriu_carrinho: 0,
      digitou_endereco: 0,
      gerou_pix: 0
    };

    lista.forEach(s => {
      somaScroll += (s.maxScroll || 0);
      somaTempo += (s.duracaoSegundos || 0);
      if (s.isTikTok) tiktokTotal++;

      // Funil cumulativo
      funil.visualizou_loja++;
      if (s.maxScroll >= 30 || s.etapa !== '1_visualizou_loja') funil.rolou_produto++;
      if (['3_clicou_comprar', '4_abriu_carrinho', '5_digitou_endereco', '6_gerou_pix'].includes(s.etapa)) funil.clicou_comprar++;
      if (['4_abriu_carrinho', '5_digitou_endereco', '6_gerou_pix'].includes(s.etapa)) funil.abriu_carrinho++;
      if (['5_digitou_endereco', '6_gerou_pix'].includes(s.etapa)) funil.digitou_endereco++;
      if (s.etapa === '6_gerou_pix') funil.gerou_pix++;

      // Motivos
      const mot = s.pontoAbandono || 'Desconhecido';
      motivos[mot] = (motivos[mot] || 0) + 1;
    });

    return res.status(200).json({
      total: total,
      tiktok_total: tiktokTotal,
      scroll_medio: Math.round(somaScroll / total),
      tempo_medio: Math.round(somaTempo / total),
      funil: funil,
      motivos_abandono: motivos,
      sessoes: lista.slice(0, 50)
    });
  }

  return res.status(405).json({ error: 'Método não permitido' });
};
