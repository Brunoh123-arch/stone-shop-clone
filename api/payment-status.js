// Vercel Serverless Function: Consulta de Status de PIX Direto via SyncPayments (D+0)
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
  res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS,POST");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version"
  );
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate");

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  try {
    let identifier = null;

    // Pega identifier de query, body ou url path (ex: /api/payment-status/abc123xyz)
    if (req.query) {
      identifier = req.query.identifier || req.query.txid || req.query.id;
    }

    if (!identifier && req.url) {
      const match = req.url.match(/\/api\/payment-status\/([^?\/]+)/);
      if (match && match[1]) {
        identifier = match[1];
      }
    }

    if (!identifier && req.method === "POST") {
      let body = req.body;
      if (typeof body === "string") {
        try {
          body = JSON.parse(body);
        } catch (_) {
          body = {};
        }
      }
      identifier = body.identifier || body.txid || body.id;
    }

    if (!identifier) {
      return res.status(400).json({ error: "Parâmetro 'identifier' ou 'txid' é obrigatório" });
    }

    const token = await getAccessToken();

    const checkRes = await fetch(`${SYNCPAY_BASE_URL}/api/partner/v1/transaction/${encodeURIComponent(identifier)}`, {
      method: "GET",
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/json",
        "User-Agent": "EcommercePlatform/2.4",
      },
    });

    if (!checkRes.ok) {
      const errText = await checkRes.text();
      return res.status(checkRes.status).json({
        error: "Erro ao consultar transação no SyncPayments",
        details: errText
      });
    }

    const result = await checkRes.json();
    const tx = result.data || result;
    const rawStatus = (tx.status || "").toLowerCase();

    // Status de sucesso no SyncPayments
    const isPaid = (
      rawStatus === "paid" ||
      rawStatus === "approved" ||
      rawStatus === "completed" ||
      rawStatus === "confirmed" ||
      rawStatus === "liquidated"
    );

    // DISPARO IDEMPOTENTE DE CompletePayment APENAS QUANDO PAGO DE VERDADE!
    if (isPaid) {
      try {
        const { markOrderPaid } = require("./_lib/store-state");
        const { record, firstTimePaid } = markOrderPaid(tx.reference_id || identifier);
        if (firstTimePaid || (record && !record.capiCompleteSent)) {
          if (record) record.capiCompleteSent = true;
          const { sendTikTokServerEvent } = require("./tiktok-event");
          const cust = (record && record.customer) || {};
          const trk = (record && record.tracking) || {};
          const items = (record && record.items) || [];
          const paidVal = Number(tx.amount || (record && record.amount) || 29.90);
          sendTikTokServerEvent({
            event: "CompletePayment",
            event_id: "purchase_" + (tx.reference_id || identifier),
            user: {
              ip: trk.ip || (req.headers["x-forwarded-for"] ? req.headers["x-forwarded-for"].split(",")[0].trim() : ""),
              user_agent: trk.ua || req.headers["user-agent"] || "",
              email: cust.email || "",
              phone: cust.phone || "",
              ttclid: trk.ttclid || "",
              ttp: trk.ttp || "",
            },
            page: { url: (record && record.pageUrl) || "https://stoneshopclone.vercel.app/pages/pix" },
            properties: {
              value: paidVal,
              currency: "BRL",
              content_type: "product",
              contents: items.map((i) => ({
                content_id: String(i.id || "prod"),
                content_type: "product",
                content_name: i.nome || i.title || "Produto",
                quantity: parseInt(i.qty, 10) || 1,
                price: parseFloat(i.preco) || paidVal,
              })),
            },
          }).catch((err) => console.error("Erro CAPI CompletePayment real:", err.message));
        }
      } catch (hookErr) {
        console.error("Erro hook markOrderPaid:", hookErr.message);
      }
    }

    return res.status(200).json({
      success: true,
      identifier: tx.reference_id || identifier,
      txid: tx.reference_id || identifier,
      status: rawStatus,
      paid: isPaid,
      amount: tx.amount,
    });
  } catch (error) {
    console.error("Erro no handler /api/payment-status:", error);
    return res.status(500).json({ error: error.message || "Erro interno do servidor" });
  }
};
