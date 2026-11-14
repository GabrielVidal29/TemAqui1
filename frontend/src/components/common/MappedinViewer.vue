<template>
  <div class="mappedin-wrapper">
    <!-- Controles de Pavimento e Origem Fixa (RN04, RN05) -->
    <div class="map-controls-row">
      <div class="floor-pills" role="group" aria-label="Pavimento">
        <button
          v-for="piso in ['1º Piso', '2º Piso']"
          :key="piso"
          type="button"
          class="floor-btn"
          :class="{ active: selectedFloor === piso }"
          :aria-pressed="selectedFloor === piso"
          @click="selectedFloor = piso"
        >
          <AppIcon name="layers" :size="15" />
          {{ piso }}
        </button>
      </div>
      <div class="origin-tag">
        <AppIcon name="circle-dot" :size="14" />
        Origem: {{ totemLabel }}
      </div>
    </div>

    <!-- Container do Mapa 3D Interativo Mappedin (RF08-RF12) -->
    <div class="mappedin-iframe-card" :class="{ expanded }">
      <div v-if="allowFullscreen" class="map-toolbar">
        <span class="map-hint">
          <AppIcon name="search" :size="13" />
          Use a busca do mapa para encontrar lojas e serviços
        </span>
        <button
          type="button"
          class="map-expand-btn"
          :aria-label="expanded ? 'Fechar mapa em tela cheia' : 'Abrir mapa em tela cheia'"
          @click="expanded = !expanded"
        >
          <AppIcon :name="expanded ? 'x' : 'maximize'" :size="16" />
          {{ expanded ? 'Fechar' : 'Tela cheia' }}
        </button>
      </div>
      <!--
        Importante: abaixo de ~500px de altura o embed do Mappedin entra em modo compacto
        e esconde a barra de busca. Por isso a altura mínima no celular é maior.
      -->
      <iframe
        title="Mapa interativo do Capim Dourado Shopping com a rota até a loja"
        name="Mappedin Map"
        allow="clipboard-write 'self' https://app.mappedin.com; web-share 'self' https://app.mappedin.com"
        scrolling="no"
        width="100%"
        :height="expanded ? '100%' : height"
        frameborder="0"
        class="map-iframe"
        :src="computedSrc"
      ></iframe>

      <!-- Legenda de POIs no rodapé do mapa -->
      <div class="poi-overlay-bar">
        <span class="poi-origin">
          <span class="pulse-dot" aria-hidden="true"></span>
          Você está aqui · {{ totemLabel }}
        </span>
        <div class="poi-legend">
          <span class="poi-chip"><AppIcon name="route" :size="13" /> Rota</span>
          <span class="poi-chip"><AppIcon name="arrow-up-down" :size="13" /> Elevador / escada</span>
          <span class="poi-chip"><AppIcon name="info" :size="13" /> Banheiros</span>
        </div>
      </div>
    </div>

    <!-- Card de Instruções de Rota (quando houver loja selecionada) -->
    <div v-if="lojaDestino || rota" class="route-summary-card">
      <div class="route-summary-header">
        <span class="route-icon">
          <AppIcon name="store" :size="20" />
        </span>
        <div class="route-heading">
          <span class="eyebrow">Destino</span>
          <h4 class="route-store-title">
            {{ rota?.loja_nome || lojaDestino?.nome || 'Centauro' }}
          </h4>
          <p class="route-sub">
            {{ rota?.loja_pavimento || lojaDestino?.pavimento || selectedFloor }}
            <span v-if="lojaDestino?.localizacao"> · {{ lojaDestino.localizacao }}</span>
            <span v-if="produtoNome"> · {{ produtoNome }}</span>
          </p>
        </div>
        <span class="route-badge num">
          <AppIcon name="clock" :size="14" />
          {{ rota?.tempo_estimado_min || 2 }} min a pé
        </span>
      </div>

      <div class="route-instructions">
        <AppIcon name="navigation" :size="16" />
        <p>
          {{
            rota?.instrucoes ||
            'Siga pelo corredor principal e vire à direita até a loja.'
          }}
        </p>
      </div>
      <p class="route-disclaimer">
        Rota calculada a partir deste totem. Não usamos GPS ou localização do seu aparelho.
      </p>

      <slot name="actions"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'

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
  },
  allowFullscreen: {
    type: Boolean,
    default: false
  }
})

const expanded = ref(false)

// Esc fecha o mapa em tela cheia
function onKeydown(e) {
  if (e.key === 'Escape') expanded.value = false
}
watch(expanded, (aberto) => {
  if (aberto) window.addEventListener('keydown', onKeydown)
  else window.removeEventListener('keydown', onKeydown)
})
onBeforeUnmount(() => window.removeEventListener('keydown', onKeydown))

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
  gap: 14px;
}

.map-controls-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
}

.floor-pills {
  display: inline-flex;
  padding: 4px;
  gap: 4px;
  background: var(--color-cream);
  border-radius: 12px;
  border: 1px solid var(--color-border);
}

.floor-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 38px;
  padding: 8px 16px;
  border-radius: 9px;
  border: none;
  background: transparent;
  color: var(--color-graphite-muted);
  font-weight: 600;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.15s var(--ease), color 0.15s var(--ease);
}

.floor-btn.active {
  background: var(--color-white);
  color: var(--color-graphite);
  box-shadow: var(--shadow-sm);
}

.origin-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-graphite-muted);
}

.mappedin-iframe-card {
  position: relative;
  background: var(--color-white);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
}

.map-iframe {
  border: 0;
  display: block;
}

.map-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 8px 8px 12px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-surface);
}

.map-hint {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.map-expand-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-height: 34px;
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-strong);
  background: var(--color-white);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-graphite);
  cursor: pointer;
  white-space: nowrap;
}

/* Mapa em tela cheia (celular) */
.mappedin-iframe-card.expanded {
  position: fixed;
  inset: 0;
  z-index: 1000;
  border-radius: 0;
  border: none;
  display: flex;
  flex-direction: column;
}

.mappedin-iframe-card.expanded .map-iframe {
  flex: 1;
}

.mappedin-iframe-card.expanded .poi-overlay-bar {
  display: none;
}

.poi-overlay-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px 12px;
  padding: 12px 14px;
  background: var(--color-white);
  border-top: 1px solid var(--color-border);
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.poi-origin {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 13px;
  color: var(--color-graphite);
}

.pulse-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--color-gold);
  box-shadow: 0 0 0 4px rgba(201, 163, 74, 0.25);
}

.poi-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.poi-chip {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--color-cream);
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  font-weight: 500;
}

.route-summary-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: var(--shadow-sm);
}

.route-summary-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.route-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.route-heading {
  flex: 1;
  min-width: 0;
}

.route-store-title {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.015em;
  color: var(--color-graphite);
  margin-top: 2px;
}

.route-sub {
  font-size: 13px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.route-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: var(--color-graphite);
  color: var(--color-white);
  font-weight: 600;
  font-size: 13px;
  padding: 6px 12px;
  border-radius: var(--radius-pill);
  white-space: nowrap;
}

.route-instructions {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  font-size: 14px;
  line-height: 1.5;
  color: var(--color-graphite);
}

.route-instructions .app-icon {
  margin-top: 2px;
  color: var(--color-gold-deep);
}

.route-disclaimer {
  font-size: 12px;
  color: var(--color-graphite-muted);
}
</style>
