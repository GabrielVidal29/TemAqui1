<template>
  <section class="campaign-banner" aria-roledescription="carrossel" aria-label="Campanhas do shopping">
    <div class="campaign-content">
      <span class="eyebrow campaign-eyebrow">{{ activeSlide.eyebrow }}</span>
      <h3 class="campaign-title">{{ activeSlide.title }}</h3>
      <p class="campaign-subtitle">{{ activeSlide.subtitle }}</p>

      <div class="campaign-footer">
        <button type="button" class="btn-gold btn-sm" @click="$emit('action', activeSlide)">
          Ver ofertas
          <AppIcon name="arrow-right" :size="16" />
        </button>

        <div class="campaign-dots">
          <button
            v-for="(slide, idx) in slides"
            :key="idx"
            type="button"
            class="dot-btn"
            :class="{ active: idx === currentIndex }"
            :aria-label="`Campanha ${idx + 1} de ${slides.length}`"
            :aria-current="idx === currentIndex ? 'true' : undefined"
            @click="currentIndex = idx"
          ></button>
        </div>
      </div>
    </div>
    <div class="campaign-img-wrap">
      <img :src="activeSlide.image" alt="" class="campaign-img" />
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const slides = [
  {
    eyebrow: 'Achadinhos do shopping',
    title: 'Seu próximo achado está mais perto.',
    subtitle: 'Até 25% de desconto em produtos selecionados.',
    image: '/assets/products/fotos/tenis-sprint-run.jpg',
    filter: { q: 'tênis de corrida até R$ 350', preco_max: 350 }
  },
  {
    eyebrow: 'Ofertas da semana',
    title: 'Novas ofertas, novos encontros.',
    subtitle: 'Moda, beleza e acessórios para o seu dia.',
    image: '/assets/products/fotos/bolsa-couro-caramelo.jpg',
    filter: { q: 'presente para minha mãe' }
  },
  {
    eyebrow: 'Descontos especiais',
    title: 'Mais descoberta. Menos no preço.',
    subtitle: 'Compare ofertas e siga até a loja.',
    image: '/assets/products/fotos/perfume-essencial-100-ml.jpg',
    filter: { apenas_promocao: true }
  }
]

const currentIndex = ref(0)
const activeSlide = computed(() => slides[currentIndex.value])

defineEmits(['action'])
</script>

<style scoped>
.campaign-banner {
  position: relative;
  background: linear-gradient(120deg, var(--color-cream) 0%, var(--color-gold-soft) 100%);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 22px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  overflow: hidden;
}

.campaign-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
  min-width: 0;
}

.campaign-eyebrow {
  color: var(--color-gold-deep);
}

.campaign-title {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  color: var(--color-graphite);
}

.campaign-subtitle {
  font-size: 14px;
  color: var(--color-graphite-muted);
}

.campaign-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 10px;
}

.campaign-dots {
  display: flex;
  gap: 4px;
}

.dot-btn {
  width: 24px;
  height: 24px;
  border: none;
  background: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.dot-btn::before {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: var(--radius-pill);
  background: var(--color-border-strong);
  transition: width 0.2s var(--ease), background-color 0.2s var(--ease);
}

.dot-btn.active::before {
  width: 20px;
  background: var(--color-graphite);
}

.campaign-img-wrap {
  width: 132px;
  height: 108px;
  border-radius: 14px;
  overflow: hidden;
  flex-shrink: 0;
  background: var(--color-white);
  box-shadow: var(--shadow-md);
}

.campaign-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
</style>
