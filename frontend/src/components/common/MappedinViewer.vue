<template>
  <div class="mappedin-wrapper">
    <!-- Controles de Pavimento e Origem Fixa (RN04, RN05) -->
    <div class="map-controls-row">
      <div class="floor-pills">
        <button
          type="button"
          class="floor-btn"
          :class="{ active: selectedFloor === '1º Piso' }"
          @click="selectedFloor = '1º Piso'"
        >
          1º Piso
        </button>
        <button
          type="button"
          class="floor-btn"
          :class="{ active: selectedFloor === '2º Piso' }"
          @click="selectedFloor = '2º Piso'"
        >
          2º Piso
        </button>
      </div>
      <div class="origin-tag">
        Origem fixa • {{ totemLabel }}
      </div>
    </div>

    <!-- Container do Mapa 3D Interativo Mappedin (RF08-RF12) -->
    <div class="mappedin-iframe-card">
      <iframe
        href="https://www.mappedin.com/"
        title="Mappedin Map"
        name="Mappedin Map"
        allow="clipboard-write 'self' https://app.mappedin.com; web-share 'self' https://app.mappedin.com"
        scrolling="no"
        width="100%"
        :height="height"
        frameborder="0"
        style="border:0"
        :src="computedSrc"
      ></iframe>

      <!-- Barra de POIs Rápidos sobreposta no rodapé do mapa (conforme Prints 02 e 03) -->
      <div class="poi-overlay-bar">
        <span class="poi-origin">● Você está aqui ({{ totemLabel }})</span>
        <span class="poi-chip">↗ Rota</span>
        <span class="poi-chip">⇅ Elevador / escada</span>
        <span class="poi-chip">WC</span>
      </div>
    </div>

    <!-- Card de Instruções de Rota Passo a Passo (quando houver loja selecionada) -->
    <div v-if="lojaDestino || rota" class="route-summary-card">
      <div class="route-summary-header">
        <div>
          <h4 class="route-store-title">
            {{ rota?.loja_nome || lojaDestino?.nome || 'Centauro' }} •
            {{ rota?.loja_pavimento || lojaDestino?.pavimento || selectedFloor }}
          </h4>
          <p class="route-sub">
            <span v-if="produtoNome">{{ produtoNome }} • </span>
            <strong>{{ rota?.tempo_estimado_min || 2 }} min a pé</strong>
            <span v-if="lojaDestino?.localizacao"> • {{ lojaDestino.localizacao }}</span>
          </p>
        </div>
        <span class="route-badge">{{ rota?.tempo_estimado_min || 2 }} min a pé</span>
      </div>

      <p class="route-instructions">
        {{
          rota?.instrucoes ||
          'Siga pelo corredor principal e vire à direita até a loja.'
        }}
      </p>
      <p class="route-disclaimer">
        Origem fixa no totem, sem GPS indoor (RN05 / RN11).
      </p>

      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const DEFAULT_EMBED_URL = 'https://app.mappedin.com/map/6af749be2250b6000c4fe524?embedded=true'

const props = defineProps({
  mapUrl: {
    type: String,
    default: DEFAULT_EMBED_URL
  },
  height: {
    type: [Number, String],
    default: 650
  },
  pavimentoInicial: {
    type: String,
    default: '1º Piso'
  },
  totemLabel: {
    type: String,
    default: 'Totem Piso 1'
  },
  lojaDestino: {
    type: Object,
    default: null
  },
  rota: {
    type: Object,
    default: null
  },
  produtoNome: {
    type: String,
    default: ''
  }
})

const selectedFloor = ref(props.lojaDestino?.pavimento || props.rota?.loja_pavimento || props.pavimentoInicial)

watch(
  () => [props.lojaDestino, props.rota],
  () => {
    const targetFloor = props.lojaDestino?.pavimento || props.rota?.loja_pavimento
    if (targetFloor) selectedFloor.value = targetFloor
  },
  { immediate: true }
)

const computedSrc = computed(() => {
  const base = props.rota?.url_rota || props.lojaDestino?.mappedin_url || props.mapUrl || DEFAULT_EMBED_URL
  if (base.startsWith('https://app.mappedin.com/map/6af749be2250b6000c4fe524')) {
    return DEFAULT_EMBED_URL
  }
  return base
})
</script>

<style scoped>
.mappedin-wrapper {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.map-controls-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
}

.floor-pills {
  display: flex;
  gap: 8px;
}

.floor-btn {
  padding: 10px 22px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: var(--color-cream);
  color: var(--color-graphite);
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.floor-btn.active {
  background: var(--color-gold);
  border-color: var(--color-gold);
  color: var(--color-graphite);
}

.origin-tag {
  font-size: 12px;
  color: var(--color-graphite-muted);
  background: var(--color-cream);
  padding: 6px 12px;
  border-radius: 999px;
}

.mappedin-iframe-card {
  position: relative;
  background: var(--color-white);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
  box-shadow: 0 4px 18px var(--color-shadow);
}

.poi-overlay-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  padding: 10px 14px;
  background: var(--color-white);
  border-top: 1px solid var(--color-border);
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.poi-origin {
  font-weight: 700;
  color: var(--color-graphite);
}

.poi-chip {
  background: var(--color-cream);
  padding: 4px 10px;
  border-radius: 999px;
  font-weight: 600;
}

.route-summary-card {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.route-summary-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.route-store-title {
  font-size: 18px;
  font-weight: 800;
  color: var(--color-graphite);
}

.route-sub {
  font-size: 13px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.route-badge {
  background: var(--color-gold-soft);
  color: var(--color-graphite);
  font-weight: 700;
  font-size: 12px;
  padding: 5px 10px;
  border-radius: 999px;
  white-space: nowrap;
}

.route-instructions {
  font-size: 14px;
  color: var(--color-graphite);
  line-height: 1.45;
}

.route-disclaimer {
  font-size: 11px;
  color: var(--color-graphite-muted);
}
</style>
