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
        Aponte a câmera do seu celular para o código. Sem baixar aplicativo e sem criar conta.
      </p>
    </div>

    <!-- QR Code ilustrativo (no protótipo, o toque simula a leitura e abre a experiência Mobile) -->
    <button
      type="button"
      class="qr-box-wrapper"
      aria-label="QR Code. No protótipo, toque para simular a leitura no celular"
      @click="abrirNoCelular"
    >
      <QrGlyph class="qr-svg" :valor="urlQr" />
      <span class="qr-hint">
        <AppIcon name="touch" :size="14" />
        Aponte a câmera do celular · {{ dominio }}/celular
      </span>
    </button>

    <div class="qr-context-summary">
      <span class="eyebrow">O que vai para o celular</span>
      <strong>{{ resumoTitulo }}</strong>
      <p>{{ resumoDetalhe }}</p>
    </div>

    <div class="qr-actions">
      <button type="button" class="btn-gold btn-lg full-width" @click="abrirNoCelular">
        Simular leitura no celular
        <AppIcon name="arrow-right" :size="18" />
      </button>
      <button type="button" class="btn-cream full-width" @click="$emit('close')">
        Retornar ao totem
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import QrGlyph from '@/components/common/QrGlyph.vue'
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

// URL que o celular abre ao ler o QR: somente o layout mobile (/celular) + contexto do totem
const urlQr = computed(() =>
  urlCelular({
    fromTotem: props.totemId || 1,
    q: props.searchQuery,
    produtoId: props.produto?.id,
    lojaId: props.loja?.id || props.produto?.loja_id
  })
)

const dominio = computed(() => urlPublicaDoSite().replace(/^https?:\/\//, ''))

// Demonstração: abre em outra aba exatamente o que o celular veria
function abrirNoCelular() {
  window.open(urlQr.value, '_blank', 'noopener')
}
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
  width: 220px;
  height: 220px;
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

.qr-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
