<template>
  <div class="mobile-stage">
    <div class="mobile-shell">
      <!-- Barra de status simulada do iPhone (9:41) conforme Print 03 -->
      <div class="mobile-statusbar">
        <span>9:41</span>
        <div class="status-icons">
          <span>ll</span>
          <span>Wi-Fi</span>
          <span>🔋</span>
        </div>
      </div>

      <!-- Header TemAqui + Capim Dourado -->
      <header class="mobile-header">
        <router-link to="/" class="brand-logo">
          <span class="brand-pin"></span>
          <span>TemAqui</span>
        </router-link>
        <span class="mall-tag">Capim Dourado</span>
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
  padding: 20px 12px;
  background: var(--color-cream);
}

.mobile-shell {
  width: 100%;
  max-width: 412px;
  min-height: 844px;
  background: var(--color-white);
  border-radius: 34px;
  border: 6px solid #292929;
  box-shadow: 0 20px 50px rgba(41, 41, 41, 0.16);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.mobile-statusbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 22px 4px;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-graphite);
}

.status-icons {
  display: flex;
  gap: 6px;
  font-size: 11px;
}

.mobile-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px 12px;
  border-bottom: 1px solid var(--color-border);
}

.mall-tag {
  font-size: 12px;
  font-weight: 700;
  color: var(--color-graphite);
}

.mobile-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

@media (max-width: 480px) {
  .mobile-stage {
    padding: 0;
  }
  .mobile-shell {
    max-width: 100%;
    min-height: 100vh;
    border-radius: 0;
    border: none;
  }
}
</style>
