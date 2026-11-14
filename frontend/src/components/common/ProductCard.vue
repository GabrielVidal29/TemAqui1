<template>
  <article class="product-card" :class="{ horizontal: layout === 'horizontal' }">
    <div class="product-thumb-wrap">
      <img :src="produto.imagem_url" alt="" class="product-thumb" loading="lazy" />
      <span v-if="produto.percentual_desconto > 0" class="discount-badge num">
        -{{ produto.percentual_desconto }}%
      </span>
    </div>

    <div class="product-body">
      <p class="product-store-line">
        <span class="store-name">{{ produto.loja?.nome }}</span>
        <span class="dot" aria-hidden="true">·</span>
        <span>{{ produto.loja?.pavimento }}</span>
      </p>

      <h3 class="product-title">
        <button type="button" class="title-btn" @click="$emit('select', produto)">
          {{ produto.nome }}
        </button>
      </h3>

      <div class="price-block">
        <span
          v-if="produto.preco_promocional && produto.preco_promocional < produto.preco_original"
          class="price-old num"
        >
          <span class="sr-only">De</span>
          {{ formatCurrency(produto.preco_original) }}
        </span>
        <strong class="price-current num">
          <span class="sr-only">Por</span>
          {{ formatCurrency(produto.preco_final) }}
        </strong>
      </div>

      <p class="product-updated-line">
        <AppIcon name="check-circle" :size="13" />
        {{ produto.atualizado_formatado || 'Atualizado hoje, 10:42' }}
      </p>

      <div class="card-links">
        <button type="button" class="link-action" @click="$emit('select', produto)">
          Detalhes
        </button>
        <button type="button" class="link-action route-link" @click="$emit('route', produto)">
          <AppIcon name="navigation" :size="13" />
          Como chegar
        </button>
      </div>
    </div>
  </article>
</template>

<script setup>
import { formatCurrency } from '@/services/api'

defineProps({
  produto: {
    type: Object,
    required: true
  },
  layout: {
    type: String,
    default: 'vertical' // 'vertical' | 'horizontal'
  }
})

defineEmits(['select', 'route'])
</script>

<style scoped>
.product-card {
  position: relative;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: var(--shadow-xs);
  transition: transform 0.18s var(--ease), box-shadow 0.18s var(--ease),
    border-color 0.18s var(--ease);
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
  border-color: var(--color-border-strong);
}

.product-card.horizontal {
  flex-direction: row;
  align-items: stretch;
  gap: 14px;
}

.product-thumb-wrap {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: var(--color-cream);
  aspect-ratio: 4 / 3;
}

.product-card.horizontal .product-thumb-wrap {
  width: 104px;
  aspect-ratio: auto;
  flex-shrink: 0;
}

.product-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s var(--ease);
}

.product-card:hover .product-thumb {
  transform: scale(1.03);
}

.discount-badge {
  position: absolute;
  top: 8px;
  left: 8px;
  background: var(--color-graphite);
  color: var(--color-white);
  font-size: 12px;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: var(--radius-xs);
}

.product-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  min-width: 0;
  padding: 0 4px 2px;
}

.product-card.horizontal .product-body {
  padding: 2px 4px 2px 0;
}

.product-store-line {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.store-name {
  font-weight: 600;
  color: var(--color-graphite);
}

.product-title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.3;
  letter-spacing: -0.01em;
}

.title-btn {
  background: none;
  border: none;
  padding: 0;
  font: inherit;
  text-align: left;
  color: var(--color-graphite);
  cursor: pointer;
}

/* Torna o card inteiro clicável a partir do título, mantendo um único alvo semântico */
.title-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: var(--radius-md);
}

.price-block {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 2px 8px;
  margin-top: 2px;
}

.price-old {
  order: 2;
  font-size: 13px;
  color: var(--color-graphite-muted);
  text-decoration: line-through;
}

.price-current {
  font-size: 19px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--color-graphite);
}

.product-updated-line {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-success-text);
}

.card-links {
  position: relative; /* fica acima da área clicável do título */
  z-index: 1;
  margin-top: auto;
  padding-top: 8px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  border-top: 1px solid var(--color-border);
}

.card-links .link-action {
  font-size: 13px;
  min-height: 32px;
  white-space: nowrap;
}

.route-link {
  color: var(--color-gold-deep);
}

.route-link:hover {
  color: var(--color-graphite);
}
</style>
