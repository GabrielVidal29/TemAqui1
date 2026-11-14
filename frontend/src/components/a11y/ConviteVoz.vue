<template>
  <div class="convite-overlay">
    <section
      class="convite-card"
      role="dialog"
      aria-modal="true"
      aria-labelledby="convite-titulo"
      aria-describedby="convite-texto"
    >
      <span class="convite-icon"><AppIcon name="volume-2" :size="30" /></span>
      <h2 id="convite-titulo">Deseja ativar o Modo Leitura por Voz?</h2>
      <p id="convite-texto">
        O totem lê em voz alta as ofertas, os resultados da busca e o caminho até a loja.
      </p>

      <!-- Situação da fala e do microfone -->
      <div class="convite-status" :class="`st-${status}`" role="status" aria-live="polite">
        <template v-if="status === 'falando'">
          <AppIcon name="volume-2" :size="18" />
          <span>Falando…</span>
        </template>
        <template v-else-if="status === 'ouvindo'">
          <span class="mic-dot" aria-hidden="true"><AppIcon name="mic" :size="18" /></span>
          <span>Microfone aberto: diga <strong>“sim”</strong> para ativar</span>
          <span class="mic-bars" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
        </template>
        <template v-else>
          <AppIcon name="info" :size="18" />
          <span>{{ MENSAGENS[status] }}</span>
        </template>
      </div>
      <p v-if="ouvido" class="convite-ouvido">Ouvi: “{{ ouvido }}”</p>

      <div class="convite-acoes">
        <button ref="btnSim" type="button" class="btn-gold btn-lg" @click="aceitar">
          <AppIcon name="volume-2" :size="20" />
          Sim, ativar leitura por voz
        </button>
        <button type="button" class="btn-cream btn-lg" @click="continuarSemAudio">
          Continuar sem áudio
          <AppIcon name="arrow-right" :size="20" />
        </button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { falar, ouvir, pararEscuta, pararFala, suportaFala, suportaMicrofone } from '@/composables/useVoz'
import { normalizar } from '@/utils/texto'

const emit = defineEmits(['aceitar', 'recusar'])

const PERGUNTA =
  'Olá! Deseja ativar o modo de leitura por voz? Diga sim para ativar, ou toque em continuar sem áudio.'

const MENSAGENS = {
  'nao-entendi': 'Não entendi. Toque em uma das opções abaixo.',
  'sem-microfone': 'Este navegador não tem microfone para comandos de voz. Toque em uma opção.',
  negado: 'O microfone não foi liberado. Toque em uma das opções abaixo.',
  'sem-rede': 'O reconhecimento de voz precisa de internet. Toque em uma opção.',
  pronto: 'Toque em uma das opções abaixo.'
}

const status = ref(suportaFala ? 'falando' : 'pronto')
const ouvido = ref('')
const btnSim = ref(null)

let fechado = false
let tentativas = 0
let seguranca = null

// "não quero" contém "quero": a recusa é conferida primeiro
const RECUSA = /\b(nao|sem audio|continuar|dispenso|agora nao)\b/
const ACEITE = /\b(sim|aceito|quero|ativar|ativa|ative|pode|claro|ok)\b/

function interpretar(texto, final) {
  const t = normalizar(texto)
  ouvido.value = texto.split(' | ')[0]
  if (RECUSA.test(t)) {
    if (final) continuarSemAudio()
    return
  }
  if (ACEITE.test(t)) aceitar()
}

function abrirMicrofone() {
  if (fechado || status.value === 'ouvindo') return
  clearTimeout(seguranca)
  if (!suportaMicrofone) {
    status.value = 'sem-microfone'
    return
  }
  status.value = 'ouvindo'
  ouvir({
    aoOuvir: interpretar,
    aoErro: (codigo) => {
      if (codigo === 'not-allowed' || codigo === 'service-not-allowed') status.value = 'negado'
      else if (codigo === 'network') status.value = 'sem-rede'
    },
    aoTerminar: () => {
      if (fechado || status.value === 'negado' || status.value === 'sem-rede') return
      // O navegador fecha o microfone após alguns segundos de silêncio: tenta de novo duas vezes
      tentativas += 1
      status.value = 'pronto'
      if (tentativas < 3) abrirMicrofone()
      else status.value = 'nao-entendi'
    }
  })
}

function encerrar() {
  fechado = true
  clearTimeout(seguranca)
  pararEscuta()
}

function aceitar() {
  if (fechado) return
  encerrar()
  pararFala()
  emit('aceitar')
}

// Disponível desde o primeiro instante: interrompe a fala e fecha o microfone na hora
function continuarSemAudio() {
  if (fechado) return
  encerrar()
  pararFala()
  emit('recusar')
}

onMounted(async () => {
  await nextTick()
  btnSim.value?.focus()
  if (suportaFala) {
    falar(PERGUNTA, { aoTerminar: abrirMicrofone })
    // Se o navegador não avisar o fim da fala, abre o microfone mesmo assim
    seguranca = setTimeout(abrirMicrofone, 9000)
  } else {
    abrirMicrofone()
  }
})

onBeforeUnmount(encerrar)
</script>

<style scoped>
.convite-overlay {
  position: fixed;
  inset: 0;
  z-index: 70;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 24px 16px;
  background: rgba(20, 20, 20, 0.55);
}

.convite-card {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding: 32px 28px 28px;
  border-radius: var(--radius-lg);
  background: var(--color-white);
  color: var(--color-graphite);
  text-align: center;
  box-shadow: var(--shadow-lg);
}

.convite-icon {
  width: 64px;
  height: 64px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
}

.convite-card h2 {
  font-size: 26px;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.convite-card > p {
  font-size: 16px;
  line-height: 1.5;
  color: var(--color-graphite-muted);
  max-width: 460px;
}

.convite-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 44px;
  padding: 10px 16px;
  border-radius: var(--radius-pill);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  font-size: 15px;
  font-weight: 500;
}

.convite-status.st-ouvindo {
  background: var(--color-success-bg);
  border-color: var(--color-success-border);
  color: var(--color-success-text);
}

.mic-dot {
  display: inline-flex;
  animation: pulso 1.2s ease-in-out infinite;
}

.mic-bars {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  height: 18px;
}

.mic-bars i {
  width: 3px;
  height: 6px;
  border-radius: 2px;
  background: currentColor;
  animation: barra 0.9s ease-in-out infinite;
}

.mic-bars i:nth-child(2) { animation-delay: 0.15s; }
.mic-bars i:nth-child(3) { animation-delay: 0.3s; }
.mic-bars i:nth-child(4) { animation-delay: 0.45s; }

@keyframes barra {
  0%, 100% { height: 5px; }
  50% { height: 18px; }
}

@keyframes pulso {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.45; }
}

@media (prefers-reduced-motion: reduce) {
  .mic-dot,
  .mic-bars i {
    animation: none;
  }
}

.convite-ouvido {
  font-size: 14px;
  color: var(--color-graphite-muted);
}

.convite-acoes {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 6px;
}

.convite-acoes .btn-lg {
  width: 100%;
  min-height: 60px;
  font-size: 17px;
}
</style>
