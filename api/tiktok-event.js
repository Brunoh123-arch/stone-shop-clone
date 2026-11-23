// API OFICIAL SERVER-SIDE TIKTOK EVENTS API (BRUNO CTO)
const https = require('https');
const crypto = require('crypto');

const PIXEL_ID = process.env.TIKTOK_PIXEL_ID || 'DBD7ASBC77UF91061F1G';
const ACCESS_TOKEN = process.env.TIKTOK_ACCESS_TOKEN || '4e975b3b1cb7cb54a147e102cd7cc7e5a0da10bc';

function sha256(val) {
  if (!val) return undefined;
  const clean = String(val).trim().toLowerCase();
  return crypto.createHash('sha256').update(clean).digest('hex');
}

function sha256Phone(phone) {
  if (!phone) return undefined;
  let p = String(phone).replace(/\D/g, '');
  if (!p) return undefined;
  if (p.length <= 11) p = '+55' + p;
  else if (!p.startsWith('+')) p = '+' + p;
  return crypto.createHash('sha256').update(p).digest('hex');
}

function sendTikTokServerEvent({ event, event_id, event_time, user = {}, page = {}, properties = {} }) {
  return new Promise((resolve) => {
    try {
      const userData = {};

      if (user.ip) userData.ip = user.ip;
      if (user.user_agent) userData.user_agent = user.user_agent;
      if (user.ttclid) userData.ttclid = user.ttclid;
      if (user.ttp) userData.ttp = user.ttp;

      if (user.email) {
        userData.email = user.email.length === 64 ? user.email : sha256(user.email);
      }
      if (user.phone) {
        userData.phone = user.phone.length === 64 ? user.phone : sha256Phone(user.phone);
      }

      const payload = JSON.stringify({
        event_source: 'web',
        event_source_id: PIXEL_ID,
        data: [
          {
            event: event,
            event_time: event_time || Math.floor(Date.now() / 1000),
            event_id: String(event_id || 'evt_' + Date.now() + '_' + Math.random().toString(36).substring(2, 7)),
            user: userData,
            page: {
              url: page.url || 'https://stoneshopclone.vercel.app/'
            },
            properties: properties
          }
        ]
      });

      const req = https.request('https://business-api.tiktok.com/open_api/v1.3/event/track/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Access-Token': ACCESS_TOKEN,
          'Content-Length': Buffer.byteLength(payload)
        },
        timeout: 4000
      }, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          try {
            resolve({ statusCode: res.statusCode, data: JSON.parse(body) });
          } catch(e) {
            resolve({ statusCode: res.statusCode, body });
          }
        });
      });

      req.on('error', (err) => {
        console.error('[TikTok CAPI] Erro de rede:', err.message);
        resolve({ error: err.message });
      });

      req.on('timeout', () => {
        req.destroy();
        resolve({ error: 'timeout' });
      });

      req.write(payload);
      req.end();
    } catch(err) {
      console.error('[TikTok CAPI] Falha de execucao:', err.message);
      resolve({ error: err.message });
    }
  });
}

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Access-Token');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const body = req.body || {};
    const clientIp = req.headers['x-forwarded-for'] ? req.headers['x-forwarded-for'].split(',')[0].trim() : (req.headers['x-real-ip'] || req.socket.remoteAddress || '');
    const clientUa = req.headers['user-agent'] || '';

    const user = Object.assign({}, body.user || {}, {
      ip: (body.user && body.user.ip) || clientIp,
      user_agent: (body.user && body.user.user_agent) || clientUa
    });

    const result = await sendTikTokServerEvent({
      event: body.event || 'PageView',
      event_id: body.event_id,
      event_time: body.event_time,
      user: user,
      page: body.page || { url: req.headers.referer || 'https://stoneshopclone.vercel.app/' },
      properties: body.properties || {}
    });

    return res.status(200).json({ ok: true, result });
  } catch(err) {
    return res.status(500).json({ error: err.message });
  }
};

module.exports.sendTikTokServerEvent = sendTikTokServerEvent;
