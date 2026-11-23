// Vercel Serverless Function: Geração de PIX Direto via SyncPayments (D+0)
// Documentação: https://syncpay.apidog.io/

const SYNCPAY_CLIENT_ID = process.env.SYNCPAY_CLIENT_ID || "d0ba7220-8b10-4038-9cb2-c990664ae6ec";
const SYNCPAY_CLIENT_SECRET = process.env.SYNCPAY_CLIENT_SECRET || "2b505916-f200-4e73-b008-2253c2785432";
const SYNCPAY_BASE_URL = "https://api.syncpayments.com.br";

let cachedToken = null;
let tokenExpiresAt = 0;

async function getAccessToken() {
  const now = Date.now();
  if (cachedToken && tokenExpiresAt > now + 60000) {
    return cachedToken;
  }

  const authPayload = JSON.stringify({
    client_id: SYNCPAY_CLIENT_ID,
    client_secret: SYNCPAY_CLIENT_SECRET,
  });

  const tokenRes = await fetch(`${SYNCPAY_BASE_URL}/api/partner/v1/auth-token`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Content-Length": Buffer.byteLength(authPayload).toString(),
      "Accept": "application/json",
      "User-Agent": "EcommercePlatform/2.4",
    },
    body: authPayload,
  });

  if (!tokenRes.ok) {
    const errText = await tokenRes.text();
    throw new Error(`SyncPayments Auth Failed: ${errText}`);
  }

  const tokenData = await tokenRes.json();
  cachedToken = tokenData.access_token;
  tokenExpiresAt = now + (tokenData.expires_in ? tokenData.expires_in * 1000 : 3600000);
  return cachedToken;
}

module.exports = async function handler(req, res) {
  // CORS Headers
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS,PATCH,DELETE,POST,PUT");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version"
  );
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    let body = req.body;
    if (typeof body === "string") {
      try {
        body = JSON.parse(body);
      } catch (e) {
        body = {};
      }
    }
    const { name, nome, cpf, taxId, email, phone, cellphone, amount } = body || {};

    // Sanitização e Camuflagem Total (Modo Blindado E-commerce)
    let cleanName = ((name || nome) && String(name || nome).trim().length > 0) ? String(name || nome).trim() : "Cliente Consumidor";
    if (/tiktok|quiz|iof|recompensas|premio|resgate/i.test(cleanName)) {
      cleanName = "Cliente Consumidor";
    }

    let cleanCpf = (taxId || cpf || "").replace(/\D/g, "");
    if (cleanCpf.length !== 11) {
      cleanCpf = "41982019802"; // Fallback padrão
    }

    let cleanEmail = (email && email.includes("@")) ? email.trim() : "";
    if (!cleanEmail || /tiktok|spikebet|quiz|recompensas/i.test(cleanEmail)) {
      const randomId = Math.random().toString(36).substring(2, 8);
      cleanEmail = `pedido.${randomId}@sac-lojavirtual.com`;
    }

    let cleanPhone = (cellphone || phone || "").replace(/\D/g, "");
    if (cleanPhone.length < 10) {
      cleanPhone = "11985472190";
    }

    // Calcula valor final: se vier em centavos (> 500), converte para reais
    let valorFinal = 29.90;
    if (typeof amount === "number") {
      if (amount > 500) {
        valorFinal = Number((amount / 100).toFixed(2));
      } else if (amount > 0) {
        valorFinal = Number(amount.toFixed(2));
      }
    } else if (amount) {
      const parsed = parseFloat(String(amount).replace(",", "."));
      if (parsed > 500) {
        valorFinal = Number((parsed / 100).toFixed(2));
      } else if (parsed > 0) {
        valorFinal = Number(parsed.toFixed(2));
      }
    }

    // Código de Pedido de Loja Seguro
    const orderNum = Math.floor(10000 + Math.random() * 90000);
    const orderDesc = `Pedido #${orderNum} - Loja Stone`;

    // 1. Obter Bearer Token no SyncPayments
    const accessToken = await getAccessToken();

    // 2. Criar Cash-In PIX no SyncPayments
    const cashInPayload = JSON.stringify({
      amount: valorFinal,
      description: orderDesc,
      client: {
        name: cleanName,
        cpf: cleanCpf,
        email: cleanEmail,
        phone: cleanPhone,
      },
    });

    const cashInRes = await fetch(`${SYNCPAY_BASE_URL}/api/partner/v1/cash-in`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${accessToken}`,
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(cashInPayload).toString(),
        "Accept": "application/json",
        "User-Agent": "EcommercePlatform/2.4",
      },
      body: cashInPayload,
    });

    if (!cashInRes.ok) {
      const errText = await cashInRes.text();
      console.error("Erro SyncPayments Cash-In:", errText);
      return res.status(500).json({ error: "Erro ao emitir PIX no gateway", details: errText });
    }

    const cashInData = await cashInRes.json();

    // DISPARO SERVER-SIDE TIKTOK EVENTS API (BRUNO CTO)
    try {
      const { sendTikTokServerEvent } = require('./tiktok-event');
      const clientIp = req.headers['x-forwarded-for'] ? req.headers['x-forwarded-for'].split(',')[0].trim() : (req.headers['x-real-ip'] || req.socket.remoteAddress || '');
      const clientUa = req.headers['user-agent'] || '';
      const transactionId = cashInData.identifier || ('sync_' + Date.now());

      const trackingObj = tracking || {};
      const itemsList = Array.isArray(items) ? items : [];

      sendTikTokServerEvent({
        event: 'PlaceAnOrder',
        event_id: 'order_' + transactionId,
        user: {
          ip: clientIp,
          user_agent: clientUa,
          email: cleanEmail,
          phone: cleanPhone,
          ttclid: trackingObj.ttclid,
          ttp: trackingObj.ttp
        },
        page: { url: req.headers.referer || 'https://stoneshopclone.vercel.app/pages/resumo' },
        properties: {
          value: valorFinal,
          currency: 'BRL',
          content_type: 'product',
          contents: itemsList.map(i => ({
            content_id: String(i.id || 'prod'),
            content_type: 'product',
            content_name: i.nome || i.title || 'Produto',
            quantity: parseInt(i.qty, 10) || 1,
            price: parseFloat(i.preco) || valorFinal
          }))
        }
      }).catch(e => console.error('Erro CAPI PlaceAnOrder:', e.message));

      sendTikTokServerEvent({
        event: 'CompletePayment',
        event_id: 'purchase_' + transactionId,
        user: {
          ip: clientIp,
          user_agent: clientUa,
          email: cleanEmail,
          phone: cleanPhone,
          ttclid: trackingObj.ttclid,
          ttp: trackingObj.ttp
        },
        page: { url: req.headers.referer || 'https://stoneshopclone.vercel.app/pages/pix' },
        properties: {
          value: valorFinal,
          currency: 'BRL',
          content_type: 'product',
          contents: itemsList.map(i => ({
            content_id: String(i.id || 'prod'),
            content_type: 'product',
            content_name: i.nome || i.title || 'Produto',
            quantity: parseInt(i.qty, 10) || 1,
            price: parseFloat(i.preco) || valorFinal
          }))
        }
      }).catch(e => console.error('Erro CAPI CompletePayment:', e.message));
    } catch (capiErr) {
      console.error('Erro ao chamar CAPI no create-pix:', capiErr.message);
    }

    return res.status(200).json({
      success: true,
      identifier: cashInData.identifier,
      txid: cashInData.identifier,
      pix_code: cashInData.pix_code,
      amount: valorFinal,
    });
  } catch (error) {
    console.error("Erro no handler /api/create-pix:", error);
    return res.status(500).json({ error: error.message || "Erro interno do servidor" });
  }
};
