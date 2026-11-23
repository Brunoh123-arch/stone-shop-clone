const fs = require('fs');
const path = require('path');
let versionsBundle = {};
try {
  versionsBundle = require('./_lib/versions_content');
} catch (e) {}

module.exports = async function handler(req, res) {
  try {
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate');

    const v = (req.query && (req.query.v || req.query.version)) || (req.body && req.body.version) || '';
    const cleanVer = String(v).trim().toLowerCase().replace(/[^a-z0-9_-]/g, '');

    // Se for listagem: /api/switch-version?action=list
    if (!cleanVer || req.query.action === 'list') {
      const list = (versionsBundle && versionsBundle.list) || [];
      const activeItem = list.find(item => item.ativo) || list[0];
      return res.status(200).json({
        success: true,
        current: activeItem ? activeItem.id : 'v4',
        versions: list
      });
    }

    // Se passou uma versão específica
    const content = versionsBundle && versionsBundle[cleanVer];
    if (!content) {
      return res.status(404).json({
        success: false,
        message: `Versão "${cleanVer}" não encontrada no registro.`
      });
    }

    // Tenta gravar em disco se estiver em ambiente local
    try {
      const indexPath = path.join(__dirname, '..', 'index.html');
      const stoneContentPath = path.join(__dirname, 'stone_content.js');
      if (fs.existsSync(indexPath)) {
        fs.writeFileSync(indexPath, content, 'utf8');
      }
      if (fs.existsSync(stoneContentPath)) {
        fs.writeFileSync(stoneContentPath, `module.exports = ${JSON.stringify(content)};\n`, 'utf8');
      }
    } catch (e) {}

    return res.status(200).json({
      success: true,
      message: `Versão ${cleanVer} selecionada com sucesso!`,
      version: cleanVer,
      previewUrl: `/?v=${cleanVer}`
    });
  } catch (err) {
    return res.status(500).json({
      success: false,
      error: err.message
    });
  }
};
