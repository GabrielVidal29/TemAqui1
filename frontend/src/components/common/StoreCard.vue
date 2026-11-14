<template>
  <article class="store-card" :class="{ compact }">
    <span class="store-avatar" aria-hidden="true">
      <AppIcon :name="iconeCategoria(loja.categoria)" :size="compact ? 20 : 22" />
    </span>

    <div class="store-info">
      <h3 class="store-name">
        <button type="button" class="store-name-btn" @click="emit('open', loja)">
          {{ loja.nome }}
        </button>
      </h3>
      <p class="store-meta">
        {{ loja.categoria }} · {{ loja.pavimento }}
        <span v-if="!compact && loja.localizacao"> · {{ loja.localizacao }}</span>
      </p>
      <div class="store-stats">
        <span class="badge badge-neutral num">
          <AppIcon name="package" :size="12" />
          {{ loja.total_produtos }} {{ loja.total_produtos === 1 ? 'produto' : 'produtos' }}
        </span>
        <span v-if="loja.total_promocoes" class="badge badge-gold num">
          <AppIcon name="percent" :size="12" />
          {{ loja.total_promocoes }} em promoção
        </span>
        <span v-if="loja.maior_desconto && !compact" class="badge badge-success num">
          até {{ loja.maior_desconto }}% OFF
        </span>
      </div>
    </div>

    <span class="store-chevron" aria-hidden="true">
      <AppIcon name="chevron-right" :size="18" />
    </span>
  </article>
</template>

<script setup>
import { iconeCategoria } from '@/utils/categorias'

defineProps({
  loja: { type: Object, required: true },
  compact: { type: Boolean, default: false }
})

const emit = defineEmits(['open'])
</script>

<style scoped>
.store-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 16px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-xs);
  transition: border-color 0.15s var(--ease), box-shadow 0.15s var(--ease), transform 0.15s var(--ease);
}

.store-card:hover {
  border-color: var(--color-gold);
  box-shadow: var(--shadow-md);
  transform: translateY(-1px);
}

.store-card.compact {
  padding: 12px;
  gap: 12px;
}

.store-avatar {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: var(--color-graphite);
  color: var(--color-gold);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.compact .store-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
}

.store-info {
  flex: 1;
  min-width: 0;
}

.store-name {
  font-size: 17px;
  font-weight: 700;
  letter-spacing: -0.015em;
}

.compact .store-name {
  font-size: 15px;
}

.store-name-btn {
  background: none;
  border: none;
  padding: 0;
  font: inherit;
  color: var(--color-graphite);
  text-align: left;
  cursor: pointer;
}

/* O cartão inteiro abre o perfil */
.store-name-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-md);
}

.store-meta {
  font-size: 13px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.store-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 8px;
}

.store-chevron {
  color: var(--color-graphite-muted);
}
</style>
