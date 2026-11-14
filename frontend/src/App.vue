<template>
  <div class="app-root">
    <!-- Barra discreta de alternância rápida entre as 3 interfaces do Monorepo -->
    <div class="env-switcher-bar">
      <span>
        <strong>TemAqui • Capim Dourado Shopping</strong> — HACKARUN 2026
      </span>
      <div class="env-switcher-links">
        <router-link to="/totem/1" class="env-pill">
          🖥️ Totem Interativo (/totem/1)
        </router-link>
        <router-link to="/" exact-active-class="active" class="env-pill">
          📱 Site Mobile (/)
        </router-link>
        <router-link to="/lojista" class="env-pill">
          🏪 Painel do Lojista (/lojista)
        </router-link>
      </div>
    </div>

    <router-view />
  </div>
</template>

<script setup>
</script>
