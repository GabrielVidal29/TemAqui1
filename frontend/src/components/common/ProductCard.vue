<template>
  <article class="product-card" :class="{ horizontal: layout === 'horizontal' }">
    <div class="product-thumb-wrap" @click="$emit('select', produto)">
      <img :src="produto.imagem_url" :alt="produto.nome" class="product-thumb" />
      <span v-if="produto.percentual_desconto > 0" class="discount-badge">
        -{{ produto.percentual_desconto }}%
      </span>
    </div>

    <div class="product-body">
      <h3 class="product-title" @click="$emit('select', produto)">
        {{ produto.nome }}
      </h3>

      <p class="product-store-line">
        {{ produto.loja?.nome }} • {{ produto.loja?.pavimento }}
      </p>
      <p class="product-updated-line">
        ✓ {{ produto.atualizado_formatado || 'Atualizado hoje, 10:42' }}
      </p>

      <div class="price-block">
        <span
          v-if="produto.preco_promocional && produto.preco_promocional < produto.preco_original"
          class="price-old"
        >
          {{ formatCurrency(produto.preco_original) }}
        </span>
        <strong class="price-current">
          {{ formatCurrency(produto.preco_final) }}
        </strong>
      </div>

      <div class="card-links">
        <button type="button" class="link-btn" @click="$emit('select', produto)">
          Ver detalhes →
        </button>
        <button type="button" class="link-btn route-link" @click="$emit('route', produto)">
          Como chegar ↗
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
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px var(--color-shadow);
}

.product-card.horizontal {
  flex-direction: row;
  align-items: center;
}

.product-thumb-wrap {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: var(--color-cream);
  aspect-ratio: 4 / 3;
  cursor: pointer;
}

.product-card.horizontal .product-thumb-wrap {
  width: 100px;
  height: 92px;
  aspect-ratio: auto;
  flex-shrink: 0;
}

.product-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.discount-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: var(--color-white);
  color: var(--color-graphite);
  font-size: 11px;
  font-weight: 800;
  padding: 4px 8px;
  border-radius: 999px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.product-body {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.product-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--color-graphite);
  line-height: 1.25;
  cursor: pointer;
}

.product-store-line {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.product-updated-line {
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.price-block {
  margin-top: 4px;
  display: flex;
  flex-direction: column;
}

.price-old {
  font-size: 11px;
  color: var(--color-graphite-muted);
  text-decoration: line-through;
}

.price-current {
  font-size: 18px;
  font-weight: 800;
  color: var(--color-graphite);
}

.card-links {
  margin-top: 6px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.link-btn {
  background: none;
  border: none;
  padding: 2px 0;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-graphite);
  cursor: pointer;
}

.link-btn.route-link {
  color: #8A6B20;
}

.link-btn:hover {
  text-decoration: underline;
}
</style>
