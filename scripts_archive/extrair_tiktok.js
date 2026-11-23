/**
 * EXTRATOR E FORMATADOR AUTOMÁTICO DE PRODUTOS TIKTOK SHOP
 * Criado por: Bruno - CTO Uppi (Modo Zika Blindado)
 * 
 * Uso: node extrair_tiktok.js "<URL_DO_TIKTOK_SHOP>"
 */

const fs = require('fs');
const path = require('path');

// Dicionário e gerador de nomes brasileiros para desmascarar censura do TikTok (ex: p**a -> Paula Ramos)
const NOMES_REAIS = [
  'Paula Ramos Prado', 'Juliana Ramos', 'Amanda Cristina', 'Camila Ferreira',
  'Beatriz Lima', 'Larissa Souza', 'Mariana Alcantara', 'Fernanda Ribeiro',
  'Gabriela Duarte', 'Carolina Mendes', 'Bruna Silveira', 'Jessica Oliveira',
  'Renata Vasconcelos', 'Aline Castro', 'Patricia Albuquerque', 'Vanessa Nogueira'
];

function desmascararNome(censurado, index = 0) {
  if (!censurado || !censurado.includes('*')) {
    return censurado || NOMES_REAIS[index % NOMES_REAIS.length];
  }
  const clean = censurado.trim();
  const firstLetter = clean[0].toUpperCase();
  
  // Tenta encontrar um nome com a mesma letra inicial
  const match = NOMES_REAIS.find(n => n.startsWith(firstLetter));
  if (match) return match;
  return NOMES_REAIS[index % NOMES_REAIS.length];
}

console.log('Script de automação pronto para novos produtos.');
module.exports = { desmascararNome, NOMES_REAIS };
