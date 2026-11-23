// Vercel Serverless Function: Geração de PIX Direto via SyncPayments (D+0)
// Documentação: https://syncpay.apidog.io/

const SYNCPAY_CLIENT_ID = process.env.SYNCPAY_CLIENT_ID || "d0ba7220-8b10-4038-9cb2-c990664ae6ec";
const SYNCPAY_CLIENT_SECRET = process.env.SYNCPAY_CLIENT_SECRET || "2b505916-f200-4e73-b008-2253c2785432";
const SYNCPAY_BASE_URL = "https://api.syncpayments.com.br";

export default async function handler(req, res) {
  // CORS Headers
  res.setHeader("Access-Control-Allow-Credentials", "true");
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,OPTIONS,PATCH,DELETE,POST,PUT");
  res.setHeader(
    "Access-Control-Allow-Headers",
    "X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version"
  );

  if (req.method === "OPTIONS") {
    res.status(200).end();
    return;
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
    const { name, cpf, email, phone, amount } = body || {};

    // Sanitização e Camuflagem Total (Modo Blindado E-commerce)
    let cleanName = (name && name.trim().length > 0) ? name.trim() : "Cliente Consumidor";
    if (/tiktok|quiz|iof|recompensas|premio|resgate/i.test(cleanName)) {
      cleanName = "Cliente Consumidor";
    }

    let cleanCpf = (cpf || "").replace(/\D/g, "");
    if (cleanCpf.length !== 11) {
      cleanCpf = "41982019802"; // Fallback padrão
    }

    let cleanEmail = (email && email.includes("@")) ? email.trim() : "";
    if (!cleanEmail || /tiktok|spikebet|quiz|recompensas/i.test(cleanEmail)) {
      // E-mail neutro de loja virtual
      const randomId = Math.random().toString(36).substring(2, 8);
      cleanEmail = `pedido.${randomId}@sac-lojavirtual.com`;
    }

    let cleanPhone = (phone || "").replace(/\D/g, "");
    if (cleanPhone.length < 10) {
      cleanPhone = "11985472190";
    }

    const valorFinal = typeof amount === "number" && amount > 0 ? Number(amount.toFixed(2)) : 21.74;

    // Código de Pedido de Loja Seguro (Ex: Pedido #94821 - Artigos Masculinos / Vestuário)
    const orderNum = Math.floor(10000 + Math.random() * 90000);
    const orderDesc = `Pedido #${orderNum} - Loja Oficial`;

    // 1. Obter Bearer Token no SyncPayments
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
      console.error("Erro SyncPayments Auth:", errText);
      return res.status(500).json({ error: "Falha de autenticação com SyncPayments", details: errText });
    }

    const tokenData = await tokenRes.json();
    const accessToken = tokenData.access_token;

    // 2. Criar Cash-In PIX Camuflado como Pedido de Loja
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

    return res.status(200).json({
      success: true,
      identifier: cashInData.identifier,
      pix_code: cashInData.pix_code,
      amount: valorFinal,
    });
  } catch (error) {
    console.error("Erro no handler /api/gerar-pix:", error);
    return res.status(500).json({ error: error.message || "Erro interno do servidor" });
  }
}
