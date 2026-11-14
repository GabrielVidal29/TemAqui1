<template>
  <div class="totem-stage">
    <div class="totem-shell">
      <router-view />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.totem-stage {
  min-height: calc(100vh - 38px);
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 20px 16px;
  background: #DFD9C9;
}

.totem-shell {
  width: 100%;
  max-width: 680px; /* Proporção vertical de Totem 9:16 confortável em monitores desktop e 1080x1920 */
  min-height: 1120px;
  background: var(--color-white);
  border-radius: 28px;
  border: 8px solid var(--color-graphite);
  box-shadow: 0 24px 60px rgba(41, 41, 41, 0.22);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

@media (min-width: 1080px) and (min-height: 1600px) {
  .totem-shell {
    max-width: 1080px;
    min-height: 1860px;
  }
}
</style>
