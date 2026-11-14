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
      <svg class="qr-svg" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <rect width="220" height="220" rx="16" fill="#FFFFFF" />
        <!-- Cantos de leitura padrão QR -->
        <rect x="20" y="20" width="54" height="54" rx="6" fill="none" stroke="#292929" stroke-width="8" />
        <rect x="34" y="34" width="26" height="26" rx="3" fill="#292929" />

        <rect x="146" y="20" width="54" height="54" rx="6" fill="none" stroke="#292929" stroke-width="8" />
        <rect x="160" y="34" width="26" height="26" rx="3" fill="#292929" />

        <rect x="20" y="146" width="54" height="54" rx="6" fill="none" stroke="#292929" stroke-width="8" />
        <rect x="34" y="160" width="26" height="26" rx="3" fill="#292929" />

        <!-- Padrão de módulos de dados -->
        <g fill="#292929">
          <rect x="88" y="22" width="12" height="12" />
          <rect x="112" y="22" width="12" height="24" />
          <rect x="88" y="46" width="24" height="12" />
          <rect x="100" y="70" width="12" height="24" />
          <rect x="22" y="88" width="24" height="12" />
          <rect x="58" y="88" width="18" height="12" />
          <rect x="128" y="88" width="12" height="24" />
          <rect x="152" y="88" width="24" height="12" />
          <rect x="184" y="100" width="14" height="24" />
          <rect x="24" y="114" width="14" height="18" />
          <rect x="52" y="116" width="24" height="12" />
          <rect x="88" y="136" width="14" height="14" />
          <rect x="114" y="128" width="24" height="14" />
          <rect x="148" y="132" width="14" height="26" />
          <rect x="174" y="142" width="24" height="14" />
          <rect x="90" y="164" width="26" height="12" />
          <rect x="126" y="162" width="14" height="28" />
          <rect x="152" y="174" width="24" height="12" />
          <rect x="184" y="170" width="14" height="26" />
        </g>
        <!-- Pin TemAqui no centro -->
        <rect x="88" y="96" width="30" height="30" rx="8" fill="#C9A34A" />
        <circle cx="103" cy="111" r="5" fill="#FFFFFF" />
      </svg>
      <span class="qr-hint">
        <AppIcon name="touch" :size="14" />
        Protótipo: toque no código para simular a leitura
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
import { useRouter } from 'vue-router'

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
const router = useRouter()

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

function abrirNoCelular() {
  const query = {
    fromTotem: String(props.totemId || 1),
    q: props.searchQuery || 'tênis de corrida até R$ 350'
  }
  if (props.produto?.id) query.produtoId = String(props.produto.id)
  if (props.loja?.id || props.produto?.loja_id) {
    query.lojaId = String(props.loja?.id || props.produto?.loja_id)
  }
  router.push({ path: '/', query })
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
