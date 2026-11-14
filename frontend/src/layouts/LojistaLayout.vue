<template>
  <div class="lojista-stage">
    <div class="lojista-shell">
      <router-view />
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.lojista-stage {
  min-height: calc(100vh - 38px);
  background: var(--color-cream);
  padding: 20px;
  display: flex;
  justify-content: center;
}

.lojista-shell {
  width: 100%;
  max-width: 1440px;
  min-height: 860px;
  background: var(--color-white);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  box-shadow: 0 12px 36px var(--color-shadow);
  overflow: hidden;
  display: flex;
}
</style>
