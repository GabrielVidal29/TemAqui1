<template>
  <div class="app-root">
    <!-- Barra discreta de alternância rápida entre as 3 interfaces do Monorepo -->
    <nav v-if="!route.meta.standalone" class="env-switcher-bar" aria-label="Alternar interface de demonstração">
      <span class="env-switcher-title">
        <strong>TemAqui</strong>
        <span>Capim Dourado Shopping · HACKARUN 2026</span>
      </span>
      <div class="env-switcher-links">
        <router-link to="/totem/1" class="env-pill">
          <AppIcon name="monitor" :size="14" />
          Totem
        </router-link>
        <router-link to="/" exact-active-class="active" class="env-pill">
          <AppIcon name="smartphone" :size="14" />
          Mobile
        </router-link>
        <router-link to="/lojista" class="env-pill">
          <AppIcon name="store" :size="14" />
          Lojista
        </router-link>
      </div>
    </nav>

    <router-view />
    <SextaToast />
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import SextaToast from '@/components/sexta13/SextaToast.vue'

// Rotas "standalone" (ex.: /celular, aberta pelo QR Code) não mostram a barra de demonstração
const route = useRoute()
</script>
