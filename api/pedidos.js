let pedidosMem = [];

module.exports = function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') try { body = JSON.parse(body); } catch(e) {}
    if (body) pedidosMem.unshift(body);
    return res.status(200).json({ ok: true });
  }

  return res.status(200).json({ pedidos: pedidosMem.slice(0, 50) });
};
