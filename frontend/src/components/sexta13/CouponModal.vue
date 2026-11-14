<template>
  <Teleport to="body">
    <div class="coupon-overlay" @click.self="emit('fechar')">
      <div
        ref="dialogo"
        class="coupon-dialog"
        :class="{ compact: modo === 'mobile' }"
        role="dialog"
        aria-modal="true"
        aria-labelledby="cupom-titulo"
        tabindex="-1"
      >
        <button type="button" class="icon-btn coupon-close" aria-label="Fechar" @click="emit('fechar')">
          <AppIcon name="x" :size="18" />
        </button>

        <div class="coupon-hero">
          <span class="coupon-moon" aria-hidden="true">
            <AppIcon name="moon" :size="22" />
          </span>
          <span class="eyebrow coupon-eyebrow">Easter egg · Sexta-feira 13</span>
          <h2 id="cupom-titulo">{{ salvo ? 'Seu cupom de sexta-feira 13' : 'Você encontrou o gato preto!' }}</h2>
          <p>Dizem que gato preto dá azar. No TemAqui, ele dá desconto.</p>
        </div>

        <!-- Cupom -->
        <div class="coupon-ticket">
          <span class="ticket-label">Cupom</span>
          <strong class="ticket-code num">{{ CUPOM_SEXTA13.codigo }}</strong>
          <span class="ticket-title">{{ CUPOM_SEXTA13.titulo }}</span>
          <span class="ticket-rule">{{ CUPOM_SEXTA13.regra }}</span>
        </div>

        <!-- Totem: leva o cupom para o celular pelo QR Code -->
        <template v-if="modo === 'totem'">
          <button
            type="button"
            class="coupon-qr"
            aria-label="QR Code do cupom. No protótipo, toque para simular a leitura no celular"
            @click="levarNoCelular"
          >
            <QrGlyph :size="176" centro="gato" />
            <span class="coupon-qr-hint">
              <AppIcon name="smartphone" :size="14" />
              Aponte a câmera para levar o cupom no celular
            </span>
          </button>
          <div class="coupon-actions">
            <button type="button" class="btn-gold btn-lg full-width" @click="levarNoCelular">
              <AppIcon name="qr-code" :size="18" />
              Simular leitura no celular
            </button>
            <button type="button" class="btn-cream full-width" @click="emit('fechar')">Voltar às ofertas</button>
          </div>
        </template>

        <!-- Celular: guardar e copiar o código -->
        <template v-else>
          <div class="coupon-actions">
            <button
              type="button"
              class="btn-gold btn-lg full-width"
              :disabled="salvo"
              @click="emit('salvar')"
            >
              <AppIcon :name="salvo ? 'check' : 'ticket'" :size="18" />
              {{ salvo ? 'Cupom guardado no celular' : 'Guardar cupom' }}
            </button>
            <button type="button" class="btn-cream full-width" @click="copiar">
              <AppIcon :name="copiado ? 'check' : 'pencil'" :size="16" />
              {{ copiado ? 'Código copiado' : 'Copiar código' }}
            </button>
          </div>
          <p class="coupon-note">Mostre este código no caixa da loja participante.</p>
        </template>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import QrGlyph from '@/components/common/QrGlyph.vue'
import { CUPOM_SEXTA13 } from '@/composables/useSexta13'

const props = defineProps({
  modo: { type: String, default: 'totem' }, // 'totem' | 'mobile'
  totemId: { type: [Number, String], default: 1 },
  salvo: { type: Boolean, default: false }
})

const emit = defineEmits(['fechar', 'salvar'])
const router = useRouter()
const dialogo = ref(null)
const copiado = ref(false)

// Mesmo fluxo do QR Code do totem: abre o site mobile levando o cupom na URL
function levarNoCelular() {
  router.push({ path: '/', query: { fromTotem: String(props.totemId || 1), cupom: CUPOM_SEXTA13.codigo } })
}

async function copiar() {
  try {
    await navigator.clipboard.writeText(CUPOM_SEXTA13.codigo)
  } catch {
    // Sem permissão de área de transferência: o código continua visível na tela
  }
  copiado.value = true
  setTimeout(() => (copiado.value = false), 2000)
}

function onKeydown(e) {
  if (e.key === 'Escape') emit('fechar')
}

onMounted(() => {
  window.addEventListener('keydown', onKeydown)
  nextTick(() => dialogo.value?.focus())
})
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))
</script>

<style scoped>
.coupon-overlay {
  position: fixed;
  inset: 0;
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: rgba(20, 20, 20, 0.62);
  backdrop-filter: blur(3px);
  animation: aparecer 0.2s var(--ease);
}

@keyframes aparecer {
  from { opacity: 0; }
  to { opacity: 1; }
}

.coupon-dialog {
  position: relative;
  width: 100%;
  max-width: 460px;
  max-height: calc(100vh - 40px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding: 28px;
  border-radius: var(--radius-lg);
  background: var(--color-white);
  box-shadow: var(--shadow-lg);
  animation: subir 0.25s var(--ease);
}

.coupon-dialog:focus {
  outline: none;
}

@keyframes subir {
  from { transform: translateY(12px); opacity: 0; }
  to { transform: none; opacity: 1; }
}

.coupon-close {
  position: absolute;
  top: 12px;
  right: 12px;
}

.coupon-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 6px;
}

.coupon-moon {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  background: var(--color-graphite);
  color: var(--color-gold);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.coupon-eyebrow {
  color: var(--color-gold-deep);
}

.coupon-hero h2 {
  font-size: 24px;
  font-weight: 800;
  letter-spacing: -0.025em;
  line-height: 1.15;
}

.coupon-hero p {
  font-size: 14px;
  color: var(--color-graphite-muted);
}

/* Bilhete do cupom com recortes laterais */
.coupon-ticket {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  padding: 18px 20px;
  border-radius: var(--radius-md);
  background: linear-gradient(120deg, var(--color-graphite) 0%, #3A3631 100%);
  color: var(--color-white);
  text-align: center;
}

.coupon-ticket::before,
.coupon-ticket::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 22px;
  height: 22px;
  margin-top: -11px;
  border-radius: 50%;
  background: var(--color-white);
}

.coupon-ticket::before {
  left: -11px;
}

.coupon-ticket::after {
  right: -11px;
}

.ticket-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: #B8B0A0;
}

.ticket-code {
  font-size: 36px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: var(--color-gold);
  padding: 2px 16px;
  border: 2px dashed rgba(201, 163, 74, 0.6);
  border-radius: var(--radius-sm);
}

.ticket-title {
  font-size: 15px;
  font-weight: 600;
  margin-top: 4px;
}

.ticket-rule {
  font-size: 12px;
  color: #CFC8B8;
  max-width: 320px;
}

.coupon-qr {
  align-self: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 16px 16px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-white);
  box-shadow: var(--shadow-md);
  cursor: pointer;
}

.coupon-qr-hint {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.coupon-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.coupon-actions .btn-gold:disabled {
  background: var(--color-success-bg);
  border-color: var(--color-success-border);
  color: var(--color-success-text);
  cursor: default;
}

.coupon-note {
  text-align: center;
  font-size: 12px;
  color: var(--color-graphite-muted);
  margin-top: -6px;
}

.compact {
  padding: 22px 18px;
  gap: 14px;
}

.compact .coupon-hero h2 {
  font-size: 21px;
}

.compact .ticket-code {
  font-size: 30px;
}
</style>
