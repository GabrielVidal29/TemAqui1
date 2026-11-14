<template>
  <div class="search-filters" :class="{ compact }">
    <!-- Com / sem desconto -->
    <div class="segmented" role="radiogroup" aria-label="Filtrar por desconto">
      <button
        v-for="op in opcoesPromocao"
        :key="op.valor"
        type="button"
        role="radio"
        class="segmented-btn"
        :class="{ active: filtros.promocao === op.valor }"
        :aria-checked="filtros.promocao === op.valor"
        @click="emit('change', { promocao: op.valor })"
      >
        <AppIcon v-if="op.icone" :name="op.icone" :size="15" />
        {{ compact ? op.curto : op.label }}
        <span class="segmented-count num">{{ contagem[op.valor] }}</span>
      </button>
    </div>

    <!-- Categorias -->
    <div class="cat-scroll" role="group" aria-label="Categorias">
      <button
        type="button"
        class="chip"
        :class="{ active: !filtros.categoria }"
        :aria-pressed="!filtros.categoria"
        @click="emit('change', { categoria: '' })"
      >
        <AppIcon name="grid" :size="14" />
        Todas
      </button>
      <button
        v-for="cat in categorias"
        :key="cat.categoria"
        type="button"
        class="chip"
        :class="{ active: filtros.categoria === cat.categoria }"
        :aria-pressed="filtros.categoria === cat.categoria"
        @click="emit('change', { categoria: filtros.categoria === cat.categoria ? '' : cat.categoria })"
      >
        <AppIcon :name="iconeCategoria(cat.categoria)" :size="14" />
        {{ cat.categoria }}
      </button>
    </div>

    <!-- Piso, faixa de preço e ordenação -->
    <div class="select-row">
      <label class="select-wrap">
        <span class="sr-only">Piso</span>
        <AppIcon name="layers" :size="15" class="select-icon" />
        <select :value="filtros.pavimento" @change="emit('change', { pavimento: $event.target.value })">
          <option v-for="p in PISOS" :key="p.valor" :value="p.valor">{{ p.label }}</option>
        </select>
        <AppIcon name="chevron-down" :size="14" class="select-chevron" />
      </label>
      <label class="select-wrap">
        <span class="sr-only">Faixa de preço</span>
        <AppIcon name="tag" :size="15" class="select-icon" />
        <select
          :value="filtros.preco_max ?? ''"
          @change="emit('change', { preco_max: $event.target.value ? Number($event.target.value) : null })"
        >
          <option v-for="f in faixas" :key="String(f.valor)" :value="f.valor ?? ''">{{ f.label }}</option>
        </select>
        <AppIcon name="chevron-down" :size="14" class="select-chevron" />
      </label>
      <label class="select-wrap">
        <span class="sr-only">Ordenar por</span>
        <AppIcon name="arrow-up-down" :size="15" class="select-icon" />
        <select :value="filtros.ordenar_por" @change="emit('change', { ordenar_por: $event.target.value })">
          <option v-for="o in ORDENACOES" :key="o.valor" :value="o.valor">{{ o.label }}</option>
        </select>
        <AppIcon name="chevron-down" :size="14" class="select-chevron" />
      </label>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { FAIXAS_PRECO, ORDENACOES, PISOS, iconeCategoria } from '@/utils/categorias'

const props = defineProps({
  filtros: { type: Object, required: true },
  contagem: { type: Object, default: () => ({ todas: 0, com: 0, sem: 0 }) },
  categorias: { type: Array, default: () => [] },
  compact: { type: Boolean, default: false }
})

const emit = defineEmits(['change'])

const opcoesPromocao = [
  { valor: 'todas', label: 'Todos', curto: 'Todos' },
  { valor: 'com', label: 'Em promoção', curto: 'Promoção', icone: 'percent' },
  { valor: 'sem', label: 'Preço normal', curto: 'Sem desconto' }
]

// Garante que uma faixa vinda da busca (ex.: "até R$ 350") apareça no seletor
const faixas = computed(() => {
  const v = props.filtros.preco_max
  if (v === null || v === undefined || FAIXAS_PRECO.some((f) => f.valor === v)) return FAIXAS_PRECO
  return [...FAIXAS_PRECO, { valor: v, label: `Até R$ ${v}` }]
})
</script>

<style scoped>
.search-filters {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.segmented {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 4px;
  padding: 4px;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 12px;
}

.segmented-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  min-height: 40px;
  padding: 6px 8px;
  border: none;
  border-radius: 9px;
  background: transparent;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-graphite-muted);
  cursor: pointer;
  transition: background-color 0.15s var(--ease), color 0.15s var(--ease);
}

.segmented-btn.active {
  background: var(--color-white);
  color: var(--color-graphite);
  box-shadow: var(--shadow-sm);
}

.segmented-btn.active .app-icon {
  color: var(--color-gold-deep);
}

.segmented-count {
  min-width: 22px;
  padding: 1px 6px;
  border-radius: var(--radius-pill);
  background: var(--color-cream-dark);
  font-size: 12px;
  font-weight: 600;
}

.segmented-btn.active .segmented-count {
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
}

.cat-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 2px;
  scrollbar-width: none;
}

.cat-scroll::-webkit-scrollbar {
  display: none;
}

.select-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}

.select-wrap {
  position: relative;
  display: block;
}

.select-wrap select {
  width: 100%;
  appearance: none;
  min-height: 40px;
  padding: 8px 30px 8px 34px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-strong);
  background: var(--color-white);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-graphite);
  cursor: pointer;
}

.select-wrap select:focus-visible {
  outline: 3px solid var(--color-graphite);
  outline-offset: 1px;
}

.select-icon,
.select-chevron {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-graphite-muted);
  pointer-events: none;
}

.select-icon {
  left: 12px;
}

.select-chevron {
  right: 10px;
}

/* Mobile */
.compact .segmented-btn {
  font-size: 13px;
  gap: 4px;
  padding: 6px 4px;
}

.compact .segmented-btn .app-icon {
  display: none;
}

.compact .select-row {
  grid-template-columns: 1fr 1fr;
}

.compact .select-row .select-wrap:last-child {
  grid-column: 1 / -1;
}
</style>
