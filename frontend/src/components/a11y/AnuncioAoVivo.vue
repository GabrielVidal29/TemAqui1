<template>
  <!-- Região lida pelos leitores de tela (TalkBack, VoiceOver, NVDA) sempre que o TemAqui anuncia algo -->
  <div class="sr-only" role="status" aria-live="polite" aria-atomic="true">{{ mensagemAoVivo }}</div>
</template>

<script setup>
import { mensagemAoVivo } from '@/composables/useVoz'
</script>
