// API Serverless: Configuração Global da Stone Shop
// Permite salvar e ler configurações da loja (Pix, WhatsApp, Timer, Cupons, etc.)

let configStore = {
  pix_mode: "manual", // "manual" ou "gateway"
  pix_key: "financeiro@stoneshop.com.br",
  pix_beneficiario: "STONE SHOP OFICIAL LTDA",
  pix_cidade: "SAO PAULO",
  gateway_provider: "syncpayments", // "syncpayments", "sealpay", "pushinpay"
  whatsapp_suporte: "5511987654321",
  oferta_timer_minutos: 30,
  pessoas_olhando_min: 34,
  pessoas_olhando_max: 68,
  cupom_texto: "Até 74% de desconto - Termina em 1 dia",
  cupom_valor: "R$ 30,00",
  cupom_porcentagem: 74,
  frete_gratis: true,
  prazo_entrega: "2 a 7 dias úteis",
  social_proof_popups: true,
  store_name: "Stone Shop",
  store_sales: "112.2K vendido(s)",
  store_response_rate: "95% responde em 24 horas",
  store_shipping_rate: "99% envios pontuais",
  tiktok_pixel_id: "DBD7ASBC77UF91061F1G",
  tiktok_access_token: "5d6d02037cf86209372b4d1748ed7eba24158030",
  tiktok_test_code: "TEST96518",
  meta_pixel_id: "",
  atualizado_em: new Date().toISOString()
};

module.exports = function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate");

  if (req.method === "OPTIONS") return res.status(200).end();

  if (req.method === "POST") {
    let body = req.body;
    if (typeof body === "string") {
      try { body = JSON.parse(body); } catch(e) {}
    }
    if (body && typeof body === "object") {
      configStore = {
        ...configStore,
        ...body,
        atualizado_em: new Date().toISOString()
      };
      return res.status(200).json({ success: true, config: configStore });
    }
    return res.status(400).json({ success: false, error: "Invalid body" });
  }

  return res.status(200).json({ success: true, config: configStore });
};
