<template>
  <div class="mobile-stage" :class="{ standalone }">
    <div class="mobile-shell">
      <!-- Barra de status simulada do iPhone (moldura do protótipo) -->
      <div v-if="!standalone" class="mobile-statusbar" aria-hidden="true">
        <span>9:41</span>
        <div class="status-icons">
          <AppIcon name="signal" :size="14" :stroke-width="2.4" />
          <AppIcon name="wifi" :size="14" :stroke-width="2.4" />
          <AppIcon name="battery" :size="18" :stroke-width="2" />
        </div>
      </div>

      <!-- Header TemAqui + Capim Dourado -->
      <header class="mobile-header">
        <router-link
          :to="standalone ? '/celular' : '/'"
          class="brand-logo"
          aria-label="TemAqui, página inicial"
          @click="sexta13.registrarToqueLogo()"
        >
          <span class="brand-pin"></span>
          <span>TemAqui</span>
        </router-link>
        <div class="header-right">
          <span class="mall-tag">
            <AppIcon name="map-pin" :size="14" />
            Capim Dourado
          </span>
          <button
            type="button"
            class="a11y-header-btn"
            :class="{ ativo: a11y.temAlgumAtivo.value }"
            aria-label="Acessibilidade"
            :aria-expanded="painelA11y"
            @click="painelA11y = true"
          >
            <AppIcon name="accessibility" :size="20" />
          </button>
        </div>
      </header>

      <!-- Conteúdo principal da rota Mobile -->
      <main class="mobile-main">
        <router-view />
      </main>
    </div>

    <PainelAcessibilidade v-if="painelA11y" contexto="mobile" compacto @fechar="painelA11y = false" />
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSexta13 } from '@/composables/useSexta13'
import { useAcessibilidade } from '@/composables/useAcessibilidade'
import PainelAcessibilidade from '@/components/a11y/PainelAcessibilidade.vue'

// /celular (aberto pelo QR Code): só o app mobile, em tela cheia, sem a moldura de demonstração
const route = useRoute()
const standalone = computed(() => !!route.meta.standalone)

// Easter egg: 13 toques seguidos no logo ligam/desligam o modo sexta-feira 13
const sexta13 = useSexta13()

// Acessibilidade no celular: painel compacto + opções vindas do totem pelo QR Code/NFC (?a11y=)
const a11y = useAcessibilidade('mobile')
a11y.aplicarNoDocumento()
const painelA11y = ref(false)
watch(
  () => route.query.a11y,
  (valor) => {
    if (valor) a11y.aplicarParametro(valor)
  },
  { immediate: true }
)
</script>

<style scoped>
.mobile-stage {
  min-height: calc(100vh - 38px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 24px 12px;
  background: var(--color-cream);
}

.mobile-shell {
  width: 100%;
  max-width: 412px;
  height: 844px;
  background: var(--color-white);
  border-radius: 44px;
  border: 8px solid #1F1F1F;
  box-shadow: var(--shadow-lg), 0 0 0 1px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.mobile-statusbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 26px 4px;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-graphite);
}

.status-icons {
  display: flex;
  align-items: center;
  gap: 6px;
}

.mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px 12px;
  border-bottom: 1px solid var(--color-border);
  font-size: 20px;
}

.mall-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-graphite-muted);
}

.mobile-main {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}

/* Modo celular real (/celular): ocupa a tela inteira, sem moldura */
.mobile-stage.standalone {
  min-height: 100dvh;
  padding: 0;
  background: var(--color-white);
}

.mobile-stage.standalone .mobile-shell {
  max-width: 520px;
  height: 100dvh;
  border: none;
  border-radius: 0;
  box-shadow: none;
}

.mobile-stage.standalone .mobile-header {
  padding-top: max(12px, env(safe-area-inset-top));
}

@media (max-width: 480px) {
  .mobile-stage {
    padding: 0;
  }
  .mobile-shell {
    max-width: 100%;
    height: calc(100vh - 38px);
    border-radius: 0;
    border: none;
  }
  .mobile-statusbar {
    display: none;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.a11y-header-btn {
  width: 44px;
  height: 44px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  border: 1px solid var(--color-border-strong);
  background: var(--color-white);
  color: var(--color-graphite);
  cursor: pointer;
}

.a11y-header-btn.ativo {
  background: var(--color-graphite);
  color: var(--color-white);
  border-color: var(--color-graphite);
}
</style>
