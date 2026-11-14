<template>
  <!-- Rota em texto, fora do iframe do mapa: funciona com TalkBack, VoiceOver e leitura por voz -->
  <section class="rota-passos" :aria-labelledby="idTitulo">
    <div class="rota-passos-head">
      <h3 :id="idTitulo">Rota em texto, passo a passo</h3>
      <span v-if="rota.acessivel" class="rota-acessivel-tag">
        <AppIcon name="elevator" :size="14" />
        Rota acessível · só elevador
      </span>
    </div>

    <ol class="rota-lista">
      <li v-for="(passo, i) in passosVisiveis" :key="i">
        <span class="rota-num num" aria-hidden="true">{{ i + 1 }}</span>
        <span>{{ passo }}</span>
      </li>
    </ol>

    <p v-if="rota.banheiro_acessivel" class="rota-wc">
      <span class="rota-wc-icon"><AppIcon name="accessibility" :size="18" /></span>
      <span><strong>WC PCD</strong> {{ rota.banheiro_acessivel.replace(/^WC PCD\s*/, '') }}</span>
    </p>

    <button v-if="suportaFala" type="button" class="btn-cream btn-sm rota-ouvir" @click="ouvirRota">
      <AppIcon name="volume-2" :size="16" />
      Ouvir a rota
    </button>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { falar, suportaFala } from '@/composables/useVoz'
import { textoDaRota } from '@/utils/leitura'

const props = defineProps({
  rota: { type: Object, required: true }
})

const idTitulo = `rota-passos-${Math.random().toString(36).slice(2, 8)}`

// O banheiro acessível aparece em destaque logo abaixo da lista (na voz, ele continua nos passos)
const passosVisiveis = computed(() =>
  props.rota.banheiro_acessivel
    ? props.rota.passos.filter((p) => !p.startsWith('Banheiro acessível'))
    : props.rota.passos
)

function ouvirRota() {
  falar(textoDaRota(props.rota))
}
</script>

<style scoped>
.rota-passos {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 14px 16px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border);
  background: var(--color-surface);
}

.rota-passos-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}

.rota-passos-head h3 {
  font-size: 15px;
  font-weight: 700;
}

.rota-acessivel-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  background: var(--color-graphite);
  color: var(--color-white);
  font-size: 12px;
  font-weight: 700;
}

.rota-lista {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.rota-lista li {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 14px;
  line-height: 1.45;
}

.rota-num {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--color-gold);
  color: var(--color-graphite);
  font-size: 12px;
  font-weight: 700;
}

.rota-wc {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  border: 2px solid var(--color-graphite);
  background: var(--color-white);
  font-size: 14px;
}

.rota-wc-icon {
  width: 32px;
  height: 32px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  background: #1565C0;
  color: #FFFFFF;
}

.rota-ouvir {
  align-self: flex-start;
}
</style>
