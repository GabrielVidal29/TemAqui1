import { ref } from 'vue'

/*
 * Voz do TemAqui (Web Speech API, pt-BR).
 *
 * - Fala: window.speechSynthesis. Funciona nos navegadores modernos.
 * - Microfone: SpeechRecognition / webkitSpeechRecognition. Só no Chrome e no Edge,
 *   com internet, em HTTPS ou localhost, e o navegador pede permissão na primeira vez.
 *
 * Tudo o que é falado também vai para uma região aria-live (AnuncioAoVivo.vue),
 * para quem usa leitor de tela (TalkBack, VoiceOver, NVDA).
 */

const sintese = typeof window !== 'undefined' ? window.speechSynthesis : null
const Reconhecimento =
  typeof window !== 'undefined' ? window.SpeechRecognition || window.webkitSpeechRecognition : null

export const suportaFala = !!sintese
export const suportaMicrofone = !!Reconhecimento

// Estado compartilhado
const falando = ref(false)
const ouvindo = ref(false)
export const mensagemAoVivo = ref('')

let reconhecimentoAtual = null
let filaId = 0

function vozPortugues() {
  const vozes = sintese?.getVoices() || []
  return (
    vozes.find((v) => v.lang === 'pt-BR' && /google|microsoft|francisca|luciana/i.test(v.name)) ||
    vozes.find((v) => v.lang === 'pt-BR') ||
    vozes.find((v) => v.lang?.toLowerCase().startsWith('pt')) ||
    null
  )
}

// Alguns navegadores carregam a lista de vozes depois
if (sintese && typeof sintese.addEventListener === 'function') {
  sintese.addEventListener('voiceschanged', () => vozPortugues())
}

// Textos longos são divididos em frases: o Chrome corta falas muito longas
function emFrases(texto) {
  return String(texto)
    .replace(/\s+/g, ' ')
    .split(/(?<=[.!?;:])\s+/)
    .map((f) => f.trim())
    .filter(Boolean)
}

/** Atualiza a região aria-live (leitores de tela), mesmo sem a leitura por voz ligada. */
export function anunciar(texto) {
  mensagemAoVivo.value = ''
  // Pequeno atraso para o leitor de tela perceber a mudança mesmo com texto repetido
  setTimeout(() => {
    mensagemAoVivo.value = texto
  }, 60)
}

/**
 * Fala um texto em pt-BR.
 * @param {string} texto
 * @param {{ interromper?: boolean, aoTerminar?: () => void, velocidade?: number }} opcoes
 */
export function falar(texto, { interromper = true, aoTerminar, velocidade = 1 } = {}) {
  if (!texto) return
  anunciar(texto)
  if (!sintese) {
    aoTerminar?.()
    return
  }
  if (interromper) {
    sintese.cancel()
    filaId++
  }
  const meuId = filaId
  const frases = emFrases(texto)
  const voz = vozPortugues()
  frases.forEach((frase, i) => {
    const fala = new SpeechSynthesisUtterance(frase)
    fala.lang = 'pt-BR'
    fala.rate = velocidade
    if (voz) fala.voice = voz
    if (i === 0) fala.onstart = () => (falando.value = true)
    if (i === frases.length - 1) {
      const fim = () => {
        if (meuId !== filaId) return // foi interrompida por outra fala
        falando.value = false
        aoTerminar?.()
      }
      fala.onend = fim
      fala.onerror = fim
    }
    sintese.speak(fala)
  })
}

/** Interrompe a fala na hora. */
export function pararFala() {
  filaId++
  falando.value = false
  sintese?.cancel()
}

/**
 * Abre o microfone (pt-BR) e devolve o que a pessoa disse.
 * @param {{ aoOuvir: (texto: string, final: boolean) => void, aoTerminar?: () => void, aoErro?: (codigo: string) => void }} opcoes
 * @returns {() => void} função para fechar o microfone
 */
export function ouvir({ aoOuvir, aoTerminar, aoErro } = {}) {
  if (!Reconhecimento) {
    aoErro?.('nao-suportado')
    return () => {}
  }
  pararEscuta()
  const rec = new Reconhecimento()
  rec.lang = 'pt-BR'
  rec.interimResults = true
  rec.continuous = false
  rec.maxAlternatives = 3
  rec.onresult = (evento) => {
    for (let i = evento.resultIndex; i < evento.results.length; i++) {
      const resultado = evento.results[i]
      const textos = [...resultado].map((alt) => alt.transcript)
      aoOuvir?.(textos.join(' | '), resultado.isFinal)
    }
  }
  rec.onerror = (evento) => aoErro?.(evento.error)
  rec.onend = () => {
    if (reconhecimentoAtual === rec) {
      reconhecimentoAtual = null
      ouvindo.value = false
    }
    aoTerminar?.()
  }
  reconhecimentoAtual = rec
  try {
    rec.start()
    ouvindo.value = true
  } catch {
    aoErro?.('falha-ao-iniciar')
  }
  return () => {
    if (reconhecimentoAtual === rec) pararEscuta()
  }
}

/** Fecha o microfone na hora, sem esperar a pessoa terminar de falar. */
export function pararEscuta() {
  const rec = reconhecimentoAtual
  reconhecimentoAtual = null
  ouvindo.value = false
  if (rec) {
    rec.onresult = null
    rec.onerror = null
    rec.onend = null
    try {
      rec.abort()
    } catch {
      // já estava fechado
    }
  }
}

export function useVoz() {
  return { falando, ouvindo, suportaFala, suportaMicrofone, falar, pararFala, ouvir, pararEscuta, anunciar }
}
