<template>
  <div class="qr-card-view">
    <div class="qr-header">
      <button type="button" class="btn-ghost btn-sm" @click="$emit('close')">
        <AppIcon name="arrow-left" :size="16" />
        Voltar
      </button>
    </div>

    <div class="qr-intro">
      <span class="qr-icon-circle">
        <AppIcon name="smartphone" :size="22" />
      </span>
      <h2 class="qr-title">Continue sua busca e rota no celular</h2>
      <p class="qr-subtitle">
        Sem baixar aplicativo e sem criar conta.
      </p>
    </div>

    <div class="qr-context-summary">
      <span class="eyebrow">O que vai para o celular</span>
      <strong>{{ resumoTitulo }}</strong>
      <p>{{ resumoDetalhe }}</p>
      <p v-if="a11y" class="qr-a11y-note">
        <AppIcon name="accessibility" :size="14" />
        Suas opções de acessibilidade também vão para o celular.
      </p>
    </div>

    <!-- QR Code e leitor NFC na parte de baixo da tela: ao alcance de quem está sentado -->
    <div class="qr-bottom">
      <p class="nfc-aviso" role="note">
        <AppIcon name="nfc" :size="22" />
        <strong>{{ AVISO_NFC }}</strong>
      </p>

      <button
        type="button"
        class="qr-box-wrapper"
        aria-label="QR Code para abrir no celular. No protótipo, toque para simular a leitura"
        @click="abrirNoCelular"
      >
        <QrGlyph class="qr-svg" :valor="urlQr" />
        <span class="qr-hint">
          <AppIcon name="touch" :size="14" />
          Toque no código para simular · {{ dominio }}/celular
        </span>
      </button>

      <!-- Indicador do leitor NFC (simulação: o hardware ficaria abaixo da tela, no centro) -->
      <div class="nfc-reader" :class="`nfc-${estadoNfc}`">
        <span class="nfc-pad" aria-hidden="true">
          <span class="nfc-ring"></span>
          <span class="nfc-ring r2"></span>
          <AppIcon :name="estadoNfc === 'ok' ? 'check' : 'nfc'" :size="30" />
        </span>
        <span class="nfc-label">Leitor NFC · centro, abaixo da tela</span>
        <button
          type="button"
          class="btn-gold btn-lg nfc-btn"
          :disabled="estadoNfc === 'lendo'"
          @click="simularNfc"
        >
          <AppIcon name="smartphone" :size="18" />
          {{ estadoNfc === 'lendo' ? 'Lendo o celular…' : 'Simular aproximação NFC' }}
        </button>
        <p class="nfc-status" role="status" aria-live="polite">{{ mensagemNfc }}</p>
        <span class="nfc-seta" aria-hidden="true"><AppIcon name="arrow-down-to-line" :size="22" /></span>
      </div>

      <button type="button" class="btn-cream full-width" @click="$emit('close')">
        Retornar ao totem
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import QrGlyph from '@/components/common/QrGlyph.vue'
import { falar } from '@/composables/useVoz'
import { AVISO_NFC } from '@/utils/leitura'
import { urlCelular, urlPublicaDoSite } from '@/utils/qr'

const props = defineProps({
  totemId: {
    type: [Number, String],
    default: 1
  },
  searchQuery: {
    type: String,
    default: 'Tênis até R$ 350'
  },
  produto: {
    type: Object,
    default: null
  },
  loja: {
    type: Object,
    default: null
  },
  // Preferências de acessibilidade ativas (?a11y=...), levadas para o celular
  a11y: {
    type: String,
    default: ''
  },
  leituraVoz: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])

const resumoTitulo = computed(() => {
  if (props.searchQuery) return `Pesquisa “${props.searchQuery}”`
  if (props.produto) return `Oferta selecionada: ${props.produto.nome}`
  return 'Pesquisa e rota do Totem'
})

const resumoDetalhe = computed(() => {
  const nomeProd = props.produto?.nome || 'Tênis Move Comfort'
  const nomeLoja = props.loja?.nome || props.produto?.loja?.nome || 'Riachuelo'
  const piso = props.loja?.pavimento || props.produto?.loja?.pavimento || '1º Piso'
  return `${nomeProd} · Rota até ${nomeLoja} · ${piso}`
})

// URL que o celular abre ao ler o QR/NFC: somente o layout mobile (/celular) + contexto do totem
const urlQr = computed(() =>
  urlCelular({
    fromTotem: props.totemId || 1,
    q: props.searchQuery,
    produtoId: props.produto?.id,
    lojaId: props.loja?.id || props.produto?.loja_id,
    a11y: props.a11y
  })
)

const dominio = computed(() => urlPublicaDoSite().replace(/^https?:\/\//, ''))

// Demonstração: abre em outra aba exatamente o que o celular veria
function abrirNoCelular() {
  window.open(urlQr.value, '_blank', 'noopener')
}

// Simulação do leitor NFC: no hardware real, aproximar o celular enviaria o mesmo link do QR Code
const estadoNfc = ref('aguardando') // 'aguardando' | 'lendo' | 'ok'
const mensagemNfc = ref('')
let timer = null

function simularNfc() {
  estadoNfc.value = 'lendo'
  mensagemNfc.value = 'Celular detectado. Enviando a busca…'
  abrirNoCelular() // abre já no toque, para o navegador não bloquear a nova aba
  clearTimeout(timer)
  timer = setTimeout(() => {
    estadoNfc.value = 'ok'
    mensagemNfc.value = 'Pronto! A busca e a rota abriram no seu celular.'
    if (props.leituraVoz) falar(mensagemNfc.value)
  }, 1200)
}

onMounted(() => {
  if (props.leituraVoz) falar(`Levar para o celular. ${AVISO_NFC}`)
})

onBeforeUnmount(() => clearTimeout(timer))
</script>

<style scoped>
.qr-card-view {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.qr-intro {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
}

.qr-icon-circle {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-pill);
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.qr-title {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.15;
  color: var(--color-graphite);
  max-width: 460px;
}

.qr-subtitle {
  font-size: 15px;
  color: var(--color-graphite-muted);
  max-width: 420px;
  line-height: 1.5;
}

.qr-box-wrapper {
  align-self: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding: 24px 24px 18px;
  background: var(--color-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
  cursor: pointer;
  transition: transform 0.18s var(--ease), box-shadow 0.18s var(--ease);
}

.qr-box-wrapper:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.qr-svg {
  width: 200px;
  height: 200px;
}

.qr-hint {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-graphite-muted);
}

.qr-context-summary {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.qr-context-summary strong {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-graphite);
  margin-top: 2px;
}

.qr-context-summary p {
  font-size: 13px;
  color: var(--color-graphite-muted);
}


/* Ocupa a altura da tela para o QR Code e o NFC ficarem embaixo */
.qr-card-view {
  flex: 1;
}

.qr-bottom {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
}

.qr-a11y-note {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 6px;
  font-weight: 600;
  color: var(--color-graphite) !important;
}

.nfc-aviso {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 14px 18px;
  border-radius: var(--radius-md);
  background: var(--color-graphite);
  color: var(--color-white);
  font-size: 16px;
  line-height: 1.4;
}

.nfc-aviso strong {
  font-weight: 600;
}

.nfc-reader {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 18px 16px 6px;
  border-radius: var(--radius-lg);
  border: 2px dashed var(--color-gold);
  background: var(--color-gold-soft);
  text-align: center;
}

.nfc-pad {
  position: relative;
  width: 76px;
  height: 76px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--color-white);
  color: var(--color-graphite);
  box-shadow: var(--shadow-md);
}

.nfc-ring {
  position: absolute;
  inset: -6px;
  border-radius: 50%;
  border: 2px solid var(--color-gold);
  opacity: 0;
  animation: nfc-onda 2s ease-out infinite;
}

.nfc-ring.r2 {
  animation-delay: 1s;
}

.nfc-lendo .nfc-ring {
  animation-duration: 0.8s;
}

.nfc-ok .nfc-pad {
  background: var(--color-success-text);
  color: #FFFFFF;
}

.nfc-ok .nfc-ring {
  animation: none;
}

@keyframes nfc-onda {
  0% { transform: scale(0.9); opacity: 0.9; }
  100% { transform: scale(1.5); opacity: 0; }
}

@media (prefers-reduced-motion: reduce) {
  .nfc-ring {
    animation: none;
  }
}

.nfc-label {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-graphite);
}

.nfc-btn {
  min-width: 280px;
}

.nfc-status {
  min-height: 20px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-success-text);
}

.nfc-seta {
  color: var(--color-gold-deep);
  animation: nfc-seta 1.4s ease-in-out infinite;
}

@keyframes nfc-seta {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(4px); }
}
</style>
