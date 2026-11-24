/**
 * REPOSITÓRIO CENTRAL DE ESTADO SERVER-SIDE (STONE SHOP)
 * Centraliza:
 *  1. Overrides de produtos salvos no /admin (preço, preço riscado, ativo, bump individual)
 *  2. Pedidos Pix gerados + Fila de Recuperação Automática + Controle Idempotente de CompletePayment
 *  3. Cálculo / Validação Server-Side de Preço Oficial a partir de data/produtos/index.js
 */
const produtosRegistry = require('../../data/produtos/index');

const state = global.__STONE_SERVER_STATE__ || {
  productOverrides: {},
  orders: [],
  ordersByTx: new Map(),
};
global.__STONE_SERVER_STATE__ = state;

function getOfficialProduct(id) {
  const key = String(id || '').replace(/[^0-9]/g, '');
  if (!key || !produtosRegistry[key]) return null;
  try {
    const base = produtosRegistry[key]();
    if (!base || base.redirect) return base;
    const ov = state.productOverrides[key];
    if (!ov) return base;

    const merged = JSON.parse(JSON.stringify(base));
    if (typeof ov.preco === 'number' && ov.preco > 0) {
      const pStr = ov.preco.toFixed(2).replace('.', ',');
      const [pInt, pCents] = pStr.split(',');
      merged.price_int = pInt;
      merged.price_cents = ',' + pCents;
      if (merged.produto_atual) merged.produto_atual.preco = ov.preco;
    }
    if (ov.precoOrig) {
      const origClean = String(ov.precoOrig).startsWith('R$') ? String(ov.precoOrig) : `R$ ${ov.precoOrig}`;
      merged.price_original = origClean;
      const numOrig = parseFloat(String(ov.precoOrig).replace(/[^\d.,]/g, '').replace(',', '.'));
      if (!isNaN(numOrig) && numOrig > 0 && merged.produto_atual) {
        merged.produto_atual.preco_antigo = numOrig;
        if (merged.produto_atual.preco && numOrig > merged.produto_atual.preco) {
          const pct = Math.round(((numOrig - merged.produto_atual.preco) / numOrig) * 100);
          if (pct > 0 && pct < 99) merged.discount_badge = `-${pct}%`;
        }
      }
    }
    if (ov.order_bump !== undefined) {
      merged.order_bump = ov.order_bump;
    }
    if (ov.ativo !== undefined) {
      merged.ativo = ov.ativo;
    }
    return merged;
  } catch (e) {
    return null;
  }
}

function setProductOverride(id, patch) {
  const key = String(id || '').replace(/[^0-9]/g, '');
  if (!key) return null;
  state.productOverrides[key] = {
    ...(state.productOverrides[key] || {}),
    ...(patch || {}),
    updatedAt: new Date().toISOString(),
  };
  return state.productOverrides[key];
}

function getAllProductOverrides() {
  return state.productOverrides;
}

/**
 * Valida o valor cobrado no Pix contra a tabela oficial de produtos no servidor.
 * Impede adulteração via DevTools (ex: enviar R$ 1,00 num produto de R$ 149,00),
 * preservando compatibilidade com cupons legítimos e bumps do checkout.
 */
function validateServerSideAmount(requestedAmount, items) {
  let reqVal = Number(requestedAmount) || 0;
  if (reqVal > 500 && (!Array.isArray(items) || items.length === 0)) {
    reqVal = Number((reqVal / 100).toFixed(2));
  }

  if (Array.isArray(items) && items.length > 0) {
    let officialSubtotal = 0;
    let matchedOfficialItems = 0;

    for (const item of items) {
      const pid = item && (item.id || item.product_id || item.prodId);
      const qty = Math.max(1, Math.min(50, parseInt(item && (item.qty || item.quantidade || item.quantity), 10) || 1));
      const official = pid ? getOfficialProduct(pid) : null;

      if (official && official.produto_atual && Number(official.produto_atual.preco) > 0) {
        officialSubtotal += Number(official.produto_atual.preco) * qty;
        matchedOfficialItems++;
      } else if (item && Number(item.preco) > 0) {
        officialSubtotal += Number(item.preco) * qty;
      }
    }

    if (matchedOfficialItems > 0 && officialSubtotal > 0) {
      // Permite até 35% de desconto legítimo de cupom/primeira compra, mas bloqueia valores fraudados abaixo disso
      const minAllowed = Number((officialSubtotal * 0.65).toFixed(2));
      if (reqVal < minAllowed) {
        return Number(officialSubtotal.toFixed(2));
      }
      // Se enviou em centavos por engano (ex: 1990 em vez de 19.90)
      if (reqVal > officialSubtotal * 20 && Math.abs(reqVal / 100 - officialSubtotal) < officialSubtotal * 0.5) {
        return Number((reqVal / 100).toFixed(2));
      }
      return Number(reqVal.toFixed(2));
    }
  }

  if (reqVal > 500) reqVal = Number((reqVal / 100).toFixed(2));
  if (reqVal < 5) reqVal = 29.90;
  return Number(reqVal.toFixed(2));
}

function registerPixOrder(order) {
  const txid = String(order.txid || order.identifier || `ord_${Date.now()}`);
  const record = {
    txid,
    orderNum: order.orderNum || Math.floor(10000 + Math.random() * 90000),
    status: order.status || 'pending',
    amount: Number(order.amount) || 0,
    pixCode: order.pixCode || '',
    customer: order.customer || {},
    items: Array.isArray(order.items) ? order.items : [],
    tracking: order.tracking || {},
    pageUrl: order.pageUrl || 'https://stoneshopclone.vercel.app/pages/pix',
    capiCompleteSent: false,
    createdAt: new Date().toISOString(),
    paidAt: null,
  };
  state.ordersByTx.set(txid, record);
  state.orders.unshift(record);
  if (state.orders.length > 300) state.orders.length = 300;
  return record;
}

function markOrderPaid(txid) {
  const key = String(txid || '');
  const rec = state.ordersByTx.get(key);
  if (!rec) return { record: null, firstTimePaid: false };
  const firstTimePaid = rec.status !== 'paid';
  rec.status = 'paid';
  if (!rec.paidAt) rec.paidAt = new Date().toISOString();
  return { record: rec, firstTimePaid };
}

function listOrdersWithRecovery() {
  const now = Date.now();
  return state.orders.map((o) => {
    const ageMs = now - new Date(o.createdAt).getTime();
    const recoveryReady = o.status === 'pending' && ageMs >= 5 * 60 * 1000;
    const phoneDigits = String((o.customer && o.customer.phone) || '').replace(/\D/g, '');
    const waPhone = phoneDigits.startsWith('55') ? phoneDigits : (phoneDigits ? `55${phoneDigits}` : '');
    const firstItem = (o.items && o.items[0] && (o.items[0].nome || o.items[0].title)) || 'seu pedido na Stone Shop';
    const waMsg = `Olá ${(o.customer && o.customer.name) || ''}! Notamos que o seu PIX de R$ ${Number(o.amount || 0).toFixed(2).replace('.', ',')} referente a *${firstItem}* ainda está aguardando confirmação. Posso te enviar o código Copia e Cola por aqui para garantir o envio hoje com Frete Grátis?`;
    return {
      ...o,
      ageMinutes: Math.floor(ageMs / 60000),
      recoveryReady,
      whatsappRecoveryUrl: waPhone ? `https://wa.me/${waPhone}?text=${encodeURIComponent(waMsg)}` : '',
    };
  });
}

module.exports = {
  getOfficialProduct,
  setProductOverride,
  getAllProductOverrides,
  validateServerSideAmount,
  registerPixOrder,
  markOrderPaid,
  listOrdersWithRecovery,
};
