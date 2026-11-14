<template>
  <!-- QR Code real (lido pela câmera do celular) com o selo do TemAqui no centro -->
  <svg
    class="qr-glyph"
    :width="size"
    :height="size"
    :viewBox="`0 0 ${total} ${total}`"
    xmlns="http://www.w3.org/2000/svg"
    shape-rendering="crispEdges"
    role="img"
    :aria-label="`QR Code para abrir no celular: ${valor}`"
  >
    <rect :width="total" :height="total" rx="2" fill="#FFFFFF" />
    <path :d="caminho" fill="#292929" />

    <!-- Selo central: pin TemAqui ou gato (cupom de sexta-feira 13) -->
    <g :transform="`translate(${selo.x} ${selo.y})`" shape-rendering="geometricPrecision">
      <rect
        :x="-0.6"
        :y="-0.6"
        :width="selo.lado + 1.2"
        :height="selo.lado + 1.2"
        rx="1.4"
        fill="#FFFFFF"
      />
      <rect :width="selo.lado" :height="selo.lado" rx="1.2" :fill="centro === 'gato' ? '#1A1A1A' : '#C9A34A'" />
      <circle
        v-if="centro !== 'gato'"
        :cx="selo.lado / 2"
        :cy="selo.lado / 2"
        :r="selo.lado * 0.18"
        fill="#FFFFFF"
      />
      <g v-else :transform="`scale(${selo.lado / 10})`">
        <path d="M2 4 L2.8 1.6 L4.4 3.4 M8 4 L7.2 1.6 L5.6 3.4" fill="#1A1A1A" stroke="#C9A34A" stroke-width="0.5" stroke-linejoin="round" />
        <circle cx="3.7" cy="6" r="0.9" fill="#C9A34A" />
        <circle cx="6.3" cy="6" r="0.9" fill="#C9A34A" />
      </g>
    </g>
  </svg>
</template>

<script setup>
import { computed } from 'vue'
import { matrizQr } from '@/utils/qr'

const props = defineProps({
  // Texto/URL codificado no QR Code
  valor: { type: String, required: true },
  size: { type: Number, default: 220 },
  centro: { type: String, default: 'pin' } // 'pin' | 'gato'
})

const MARGEM = 3 // zona de silêncio (em módulos) exigida pelos leitores

const matriz = computed(() => matrizQr(props.valor))
const n = computed(() => matriz.value.length)
const total = computed(() => n.value + MARGEM * 2)

// Um quadrado por módulo escuro, num único <path> (leve para renderizar)
const caminho = computed(() => {
  let d = ''
  matriz.value.forEach((linha, r) => {
    linha.forEach((escuro, c) => {
      if (escuro) d += `M${c + MARGEM},${r + MARGEM}h1v1h-1z`
    })
  })
  return d
})

// Selo ocupa ~17% da largura: bem abaixo do limite da correção de erro Q
const selo = computed(() => {
  const lado = Math.max(5, Math.round(n.value * 0.17))
  const pos = MARGEM + (n.value - lado) / 2
  return { lado, x: pos, y: pos }
})
</script>

<style scoped>
.qr-glyph {
  display: block;
}
</style>
