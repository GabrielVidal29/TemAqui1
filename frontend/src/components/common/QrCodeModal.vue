<template>
  <div class="qr-card-view">
    <div class="qr-header">
      <button type="button" class="btn-cream btn-sm" @click="$emit('close')">
        ← Voltar
      </button>
    </div>

    <h2 class="qr-title">Continue sua busca e rota no celular</h2>
    <p class="qr-subtitle">
      Aponte a câmera do seu celular para o QR Code — sem baixar app e sem criar conta (RN02 / RN10).
    </p>

    <!-- QR Code Interativo SVG (No protótipo, toque abre diretamente a experiência Mobile herdada) -->
    <div class="qr-box-wrapper" @click="abrirNoCelular">
      <svg class="qr-svg" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg">
        <rect width="220" height="220" rx="16" fill="#FFFFFF" />
        <!-- Cantos de leitura padrão QR -->
        <rect x="20" y="20" width="54" height="54" fill="none" stroke="#292929" stroke-width="8" />
        <rect x="34" y="34" width="26" height="26" fill="#292929" />

        <rect x="146" y="20" width="54" height="54" fill="none" stroke="#292929" stroke-width="8" />
        <rect x="160" y="34" width="26" height="26" fill="#292929" />

        <rect x="20" y="146" width="54" height="54" fill="none" stroke="#292929" stroke-width="8" />
        <rect x="34" y="160" width="26" height="26" fill="#292929" />

        <!-- Padrão de módulos de dados -->
        <g fill="#292929">
          <rect x="88" y="22" width="12" height="12" />
          <rect x="112" y="22" width="12" height="24" />
          <rect x="88" y="46" width="24" height="12" />
          <rect x="100" y="70" width="12" height="24" />
          <rect x="22" y="88" width="24" height="12" />
          <rect x="58" y="88" width="18" height="12" />
          <rect x="88" y="96" width="28" height="28" fill="#C9A34A" rx="4" />
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
      </svg>
      <p class="qr-hint">No protótipo, toque no QR para abrir no celular.</p>
    </div>

    <div class="qr-context-summary">
      <strong>{{ resumoTitulo }}</strong>
      <p>{{ resumoDetalhe }}</p>
    </div>

    <div class="qr-actions">
      <button type="button" class="btn-gold full-width" @click="abrirNoCelular">
        Simular leitura no Celular agora →
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
  if (props.searchQuery) return `Pesquisa "${props.searchQuery}"`
  if (props.produto) return `Oferta selecionada: ${props.produto.nome}`
  return 'Pesquisa e rota do Totem'
})

const resumoDetalhe = computed(() => {
  const nomeProd = props.produto?.nome || 'Tênis Move Comfort'
  const nomeLoja = props.loja?.nome || props.produto?.loja?.nome || 'Riachuelo'
  const piso = props.loja?.pavimento || props.produto?.loja?.pavimento || '1º Piso'
  return `${nomeProd} • Rota até ${nomeLoja} • ${piso}`
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
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.qr-title {
  font-size: 26px;
  font-weight: 800;
  color: var(--color-graphite);
  line-height: 1.2;
}

.qr-subtitle {
  font-size: 14px;
  color: var(--color-graphite-muted);
}

.qr-box-wrapper {
  align-self: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px;
  background: var(--color-cream);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: transform 0.15s ease;
}

.qr-box-wrapper:hover {
  transform: scale(1.02);
}

.qr-svg {
  width: 210px;
  height: 210px;
}

.qr-hint {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-graphite);
}

.qr-context-summary {
  background: var(--color-cream);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.qr-context-summary strong {
  font-size: 14px;
  color: var(--color-graphite);
}

.qr-context-summary p {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.qr-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.full-width {
  width: 100%;
}
</style>
