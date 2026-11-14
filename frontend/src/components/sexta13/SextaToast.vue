<template>
  <!-- Aviso rápido ao ligar/desligar o modo sexta-feira 13 (13 toques no logo) -->
  <Teleport to="body">
    <div v-if="aviso" class="sexta-toast" role="status">
      <AppIcon name="moon" :size="16" />
      {{ aviso }}
    </div>
  </Teleport>
</template>

<script setup>
import { useSexta13 } from '@/composables/useSexta13'

const { aviso } = useSexta13()
</script>

<style scoped>
.sexta-toast {
  position: fixed;
  left: 50%;
  bottom: 28px;
  translate: -50% 0;
  z-index: 2100;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 18px;
  border-radius: var(--radius-pill);
  background: var(--color-graphite);
  color: var(--color-gold);
  font-size: 14px;
  font-weight: 600;
  box-shadow: var(--shadow-lg);
  animation: toast 0.25s var(--ease);
}

@keyframes toast {
  from { opacity: 0; transform: translateY(8px); }
  to { opacity: 1; transform: none; }
}
</style>
