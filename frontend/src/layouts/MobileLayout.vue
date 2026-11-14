<template>
  <div class="mobile-stage">
    <div class="mobile-shell">
      <!-- Barra de status simulada do iPhone (moldura do protótipo) -->
      <div class="mobile-statusbar" aria-hidden="true">
        <span>9:41</span>
        <div class="status-icons">
          <AppIcon name="signal" :size="14" :stroke-width="2.4" />
          <AppIcon name="wifi" :size="14" :stroke-width="2.4" />
          <AppIcon name="battery" :size="18" :stroke-width="2" />
        </div>
      </div>

      <!-- Header TemAqui + Capim Dourado -->
      <header class="mobile-header">
        <router-link to="/" class="brand-logo" aria-label="TemAqui, página inicial">
          <span class="brand-pin"></span>
          <span>TemAqui</span>
        </router-link>
        <span class="mall-tag">
          <AppIcon name="map-pin" :size="14" />
          Capim Dourado
        </span>
      </header>

      <!-- Conteúdo principal da rota Mobile -->
      <main class="mobile-main">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
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
</style>
