import { computed, reactive } from 'vue'

/**
 * EASTER EGG — Sexta-feira 13 (HACKARUN 2026)
 *
 * Modo especial em que um gato preto passeia entre os cards de ofertas.
 * Quem toca nele ganha o cupom SEXTA13 (com QR Code para levar no celular).
 *
 * Como ativar:
 *  - automaticamente em qualquer sexta-feira 13 real;
 *  - tocando 13 vezes seguidas no logo do TemAqui (totem ou celular);
 *  - abrindo a URL com ?sexta13 (atalho para a apresentação).
 */

export const CUPOM_SEXTA13 = Object.freeze({
  codigo: 'SEXTA13',
  titulo: '13% OFF de sexta-feira 13',
  regra: 'Válido em lojas participantes, hoje até 23:59. Apresente o código no caixa.'
})

const CHAVE_MODO = 'temaqui_sexta13_modo'
const CHAVE_CUPONS = 'temaqui_cupons'
const TOQUES_PARA_ATIVAR = 13
const JANELA_TOQUES_MS = 1500

function lerCupons() {
  try {
    return JSON.parse(localStorage.getItem(CHAVE_CUPONS) || '[]')
  } catch {
    return []
  }
}

// Estado compartilhado entre totem, celular e layouts
const estado = reactive({
  forcado: sessionStorage.getItem(CHAVE_MODO), // '1' ligado, '0' desligado, null = automático
  toques: 0,
  ultimoToque: 0,
  aviso: '',
  cupons: lerCupons()
})

export function ehSextaFeira13(data = new Date()) {
  return data.getDay() === 5 && data.getDate() === 13
}

const ativo = computed(() => {
  if (estado.forcado === '1') return true
  if (estado.forcado === '0') return false
  return ehSextaFeira13() || new URLSearchParams(window.location.search).has('sexta13')
})

function definirModo(ligado) {
  estado.forcado = ligado ? '1' : '0'
  sessionStorage.setItem(CHAVE_MODO, estado.forcado)
  estado.aviso = ligado
    ? 'Sexta-feira 13 ativada: um gato preto está andando pela vitrine.'
    : 'Modo sexta-feira 13 desativado.'
  setTimeout(() => (estado.aviso = ''), 3500)
}

/** Conta toques no logo; no 13º toque seguido, liga/desliga o modo. Retorna o total de toques. */
function registrarToqueLogo() {
  const agora = Date.now()
  if (agora - estado.ultimoToque > JANELA_TOQUES_MS) estado.toques = 0
  estado.ultimoToque = agora
  estado.toques += 1
  if (estado.toques >= TOQUES_PARA_ATIVAR) {
    estado.toques = 0
    definirModo(!ativo.value)
  }
  return estado.toques
}

function salvarCupom(codigo = CUPOM_SEXTA13.codigo) {
  if (!estado.cupons.includes(codigo)) {
    estado.cupons.push(codigo)
    localStorage.setItem(CHAVE_CUPONS, JSON.stringify(estado.cupons))
  }
}

function removerCupom(codigo = CUPOM_SEXTA13.codigo) {
  estado.cupons = estado.cupons.filter((c) => c !== codigo)
  localStorage.setItem(CHAVE_CUPONS, JSON.stringify(estado.cupons))
}

export function useSexta13() {
  return {
    ativo,
    aviso: computed(() => estado.aviso),
    toques: computed(() => estado.toques),
    temCupom: computed(() => estado.cupons.includes(CUPOM_SEXTA13.codigo)),
    registrarToqueLogo,
    definirModo,
    salvarCupom,
    removerCupom
  }
}
