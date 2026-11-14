<template>
  <div class="campaign-banner" @click="$emit('action', activeSlide)">
    <div class="campaign-content">
      <span class="campaign-eyebrow">{{ activeSlide.eyebrow }}</span>
      <h3 class="campaign-title">{{ activeSlide.title }}</h3>
      <p class="campaign-subtitle">{{ activeSlide.subtitle }}</p>
      <div class="campaign-dots">
        <button
          v-for="(slide, idx) in slides"
          :key="idx"
          type="button"
          class="dot-btn"
          :class="{ active: idx === currentIndex }"
          @click.stop="currentIndex = idx"
        >
          0{{ idx + 1 }}
        </button>
      </div>
    </div>
    <div class="campaign-img-wrap">
      <img :src="activeSlide.image" :alt="activeSlide.title" class="campaign-img" />
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const slides = [
  {
    eyebrow: 'ACHADINHOS DO SHOPPING',
    title: 'Seu próximo achado está mais perto.',
    subtitle: 'Até 25% de desconto em produtos selecionados.',
    image: '/assets/products/tenis-sprint.svg',
    filter: { q: 'tênis de corrida até R$ 350', preco_max: 350 }
  },
  {
    eyebrow: 'OFERTAS DA SEMANA',
    title: 'Novas ofertas, novos encontros.',
    subtitle: 'Moda, beleza e acessórios para o seu dia.',
    image: '/assets/products/bolsa-caramelo.svg',
    filter: { q: 'presente para minha mãe' }
  },
  {
    eyebrow: 'DESCONTOS ESPECIAIS',
    title: 'Mais descoberta. Menos no preço.',
    subtitle: 'Compare ofertas e siga até a loja.',
    image: '/assets/products/perfume-essencial.svg',
    filter: { apenas_promocao: true }
  }
]

const currentIndex = ref(0)
const activeSlide = computed(() => slides[currentIndex.value])

defineEmits(['action'])
</script>

<style scoped>
.campaign-banner {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 18px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  cursor: pointer;
}

.campaign-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.campaign-eyebrow {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-graphite-muted);
}

.campaign-title {
  font-size: 20px;
  font-weight: 800;
  line-height: 1.2;
  color: var(--color-graphite);
}

.campaign-subtitle {
  font-size: 13px;
  color: var(--color-graphite-muted);
}

.campaign-dots {
  display: flex;
  gap: 8px;
  margin-top: 6px;
}

.dot-btn {
  background: none;
  border: none;
  font-size: 11px;
  font-weight: 700;
  color: var(--color-graphite-muted);
  cursor: pointer;
  padding: 2px 4px;
}

.dot-btn.active {
  color: var(--color-graphite);
  border-bottom: 2px solid var(--color-gold);
}

.campaign-img-wrap {
  width: 118px;
  height: 92px;
  border-radius: 12px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--color-white);
}

.campaign-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
