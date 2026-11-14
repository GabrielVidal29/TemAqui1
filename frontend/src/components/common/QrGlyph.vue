<template>
  <svg class="qr-glyph" :width="size" :height="size" viewBox="0 0 220 220" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <rect width="220" height="220" rx="16" fill="#FFFFFF" />
    <!-- Cantos de leitura padrão QR -->
    <rect x="20" y="20" width="54" height="54" rx="6" fill="none" stroke="#292929" stroke-width="8" />
    <rect x="34" y="34" width="26" height="26" rx="3" fill="#292929" />

    <rect x="146" y="20" width="54" height="54" rx="6" fill="none" stroke="#292929" stroke-width="8" />
    <rect x="160" y="34" width="26" height="26" rx="3" fill="#292929" />

    <rect x="20" y="146" width="54" height="54" rx="6" fill="none" stroke="#292929" stroke-width="8" />
    <rect x="34" y="160" width="26" height="26" rx="3" fill="#292929" />

    <!-- Padrão de módulos de dados -->
    <g fill="#292929">
      <rect x="88" y="22" width="12" height="12" />
      <rect x="112" y="22" width="12" height="24" />
      <rect x="88" y="46" width="24" height="12" />
      <rect x="100" y="70" width="12" height="24" />
      <rect x="22" y="88" width="24" height="12" />
      <rect x="58" y="88" width="18" height="12" />
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
    <!-- Selo central: pin TemAqui ou gato (cupom) -->
    <rect x="88" y="96" width="30" height="30" rx="8" :fill="centro === 'gato' ? '#1A1A1A' : '#C9A34A'" />
    <circle v-if="centro !== 'gato'" cx="103" cy="111" r="5" fill="#FFFFFF" />
    <g v-else>
      <path d="M93 104 L95 98 L99 103 M113 104 L111 98 L107 103" fill="#1A1A1A" stroke="#1A1A1A" stroke-width="2" stroke-linejoin="round" />
      <circle cx="99" cy="111" r="2.4" fill="#C9A34A" />
      <circle cx="107" cy="111" r="2.4" fill="#C9A34A" />
    </g>
  </svg>
</template>

<script setup>
// Desenho do QR Code do protótipo (o toque simula a leitura no celular)
defineProps({
  size: { type: Number, default: 220 },
  centro: { type: String, default: 'pin' } // 'pin' | 'gato'
})
</script>

<style scoped>
.qr-glyph {
  display: block;
}
</style>
