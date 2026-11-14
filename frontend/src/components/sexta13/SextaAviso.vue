<template>
  <!-- Faixa do modo sexta-feira 13 -->
  <div v-if="ativo" class="sexta-banner" :class="{ compact }" role="note">
    <span class="sexta-moon" aria-hidden="true"><AppIcon name="moon" :size="16" /></span>
    <span class="sexta-text">
      <strong>Sexta-feira 13.</strong>
      Tem um gato preto andando entre as ofertas. Encontre-o e ganhe um cupom.
    </span>
    <button type="button" class="sexta-off" @click="definirModo(false)">Desativar</button>
  </div>
</template>

<script setup>
import { useSexta13 } from '@/composables/useSexta13'

defineProps({
  compact: { type: Boolean, default: false }
})

const { ativo, definirModo } = useSexta13()
</script>

<style scoped>
.sexta-banner {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px 10px 14px;
  border-radius: var(--radius-md);
  background: linear-gradient(120deg, #1A1A1A 0%, #2E2A25 100%);
  color: #E8E2D3;
  font-size: 14px;
  line-height: 1.4;
}

.sexta-banner strong {
  color: var(--color-gold);
  font-weight: 700;
}

.sexta-moon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(201, 163, 74, 0.16);
  color: var(--color-gold);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.sexta-text {
  flex: 1;
}

.sexta-off {
  border: 1px solid rgba(232, 226, 211, 0.3);
  background: transparent;
  color: #E8E2D3;
  border-radius: var(--radius-sm);
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.sexta-off:hover {
  background: rgba(255, 255, 255, 0.08);
}

.compact {
  font-size: 12px;
  gap: 10px;
  padding: 8px 8px 8px 10px;
}

.compact .sexta-moon {
  width: 28px;
  height: 28px;
}
</style>
