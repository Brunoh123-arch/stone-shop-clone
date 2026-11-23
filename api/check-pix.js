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

export default async function handler(req, res) {
  // CORS Headers
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS,POST");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version"
  );

  if (req.method === "OPTIONS") {
    return res.status(200).end();
  }

  try {
    let identifier = null;

    if (req.method === "GET") {
      identifier = req.query.identifier || req.query.id;
    } else if (req.method === "POST") {
      let body = req.body;
      if (typeof body === "string") {
        try {
          body = JSON.parse(body);
        } catch (_) {
          body = {};
        }
      }
      identifier = body.identifier || body.id;
    }

    if (!identifier) {
      return res.status(400).json({ error: "Parâmetro 'identifier' é obrigatório" });
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

    return res.status(200).json({
      success: true,
      identifier: tx.reference_id || identifier,
      status: rawStatus,
      paid: isPaid,
      amount: tx.amount,
    });
  } catch (error) {
    console.error("Erro no handler /api/check-pix:", error);
    return res.status(500).json({ error: error.message || "Erro interno do servidor" });
  }
}
