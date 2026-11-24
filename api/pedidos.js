const { registerPixOrder, listOrdersWithRecovery, markOrderPaid } = require('./_lib/store-state');

module.exports = function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');

  if (req.method === 'OPTIONS') return res.status(200).end();

  if (req.method === 'POST') {
    let body = req.body;
    if (typeof body === 'string') {
      try { body = JSON.parse(body); } catch (e) { body = {}; }
    }
    if (body && body.action === 'mark_paid' && body.txid) {
      markOrderPaid(body.txid);
      return res.status(200).json({ ok: true });
    }
    if (body && typeof body === 'object') {
      registerPixOrder({
        txid: body.txid || body.id || `ord_${Date.now()}`,
        orderNum: body.orderNum || body.numero,
        status: body.status || 'pending',
        amount: body.valor || body.amount || body.total || 0,
        pixCode: body.pix_code || body.pixCode || '',
        customer: {
          name: body.cliente || body.nome || body.name || 'Cliente',
          phone: body.telefone || body.whatsapp || body.phone || '',
          email: body.email || '',
          cpf: body.cpf || '',
        },
        items: body.itens || body.items || (body.produto ? [{ nome: body.produto, qty: 1, preco: body.valor }] : []),
      });
    }
    return res.status(200).json({ ok: true });
  }

  const pedidos = listOrdersWithRecovery();
  const stats = {
    total: pedidos.length,
    paid: pedidos.filter((p) => p.status === 'paid').length,
    pending: pedidos.filter((p) => p.status === 'pending').length,
    recoveryReady: pedidos.filter((p) => p.recoveryReady).length,
  };
  return res.status(200).json({ pedidos: pedidos.slice(0, 100), stats });
};
