<template>
  <div class="store-profile" :class="{ compact }">
    <button type="button" class="btn-ghost btn-sm back-btn" @click="emit('back')">
      <AppIcon name="arrow-left" :size="16" />
      {{ backLabel }}
    </button>

    <div v-if="carregando && !perfil" class="profile-loading" role="status">Carregando loja…</div>
    <p v-else-if="erro" class="profile-error" role="alert">{{ erro }}</p>

    <template v-else-if="perfil">
      <!-- Cabeçalho da loja -->
      <header class="profile-header">
        <div class="profile-cover" aria-hidden="true"></div>
        <div class="profile-identity">
          <span class="profile-avatar" aria-hidden="true">
            <AppIcon :name="iconeCategoria(loja.categoria)" :size="compact ? 26 : 30" />
          </span>
          <div class="profile-title">
            <span class="eyebrow">{{ loja.categoria }}</span>
            <h2>{{ loja.nome }}</h2>
            <p class="profile-location">
              <AppIcon name="map-pin" :size="14" />
              {{ loja.pavimento }} · {{ loja.localizacao }}
            </p>
          </div>
        </div>
        <p v-if="loja.descricao" class="profile-desc">{{ loja.descricao }}</p>

        <dl class="profile-stats">
          <div>
            <dt>Produtos</dt>
            <dd class="num">{{ loja.total_produtos }}</dd>
          </div>
          <div>
            <dt>Em promoção</dt>
            <dd class="num">{{ loja.total_promocoes }}</dd>
          </div>
          <div>
            <dt>Maior desconto</dt>
            <dd class="num">{{ loja.maior_desconto ? `${loja.maior_desconto}%` : '—' }}</dd>
          </div>
        </dl>

        <div class="profile-actions">
          <button type="button" class="btn-gold" :class="{ 'btn-lg': !compact }" @click="irParaLocalizacao">
            <AppIcon name="navigation" :size="17" />
            Como chegar
          </button>
          <span v-if="perfil.rota" class="profile-walk">
            <AppIcon name="clock" :size="15" />
            {{ perfil.rota.tempo_estimado_min }} min a pé {{ origemLabel }}
          </span>
        </div>
        <p v-if="loja.atualizado_em" class="profile-updated">
          <AppIcon name="refresh" :size="13" />
          Produtos atualizados pela loja hoje às {{ horario(loja.atualizado_em) }}
        </p>
      </header>

      <!-- Promoções em destaque -->
      <section v-if="perfil.destaques.length" class="profile-section" aria-labelledby="destaques-title">
        <div class="section-head">
          <h3 id="destaques-title">
            <AppIcon name="percent" :size="18" />
            Promoções em destaque
          </h3>
          <button type="button" class="link-action" @click="filtroPromo = 'com'; rolarParaProdutos()">
            Ver todas
          </button>
        </div>
        <div class="destaques-row">
          <ProductCard
            v-for="prod in perfil.destaques"
            :key="prod.id"
            :produto="prod"
            class="destaque-card"
            @select="emit('select', $event)"
            @route="emit('route', $event)"
          />
        </div>
      </section>

      <!-- Todos os produtos -->
      <section ref="produtosRef" class="profile-section" aria-labelledby="produtos-title">
        <div class="section-head">
          <h3 id="produtos-title">
            <AppIcon name="package" :size="18" />
            Produtos da loja
          </h3>
          <span class="badge badge-neutral num">{{ produtosFiltrados.length }}</span>
        </div>

        <div class="search-field store-search">
          <AppIcon name="search" :size="17" />
          <input
            v-model="buscaLocal"
            type="search"
            :aria-label="`Buscar produtos na ${loja.nome}`"
            :placeholder="`Buscar na ${loja.nome}`"
          />
        </div>

        <div class="segmented" role="radiogroup" aria-label="Filtrar por desconto">
          <button
            v-for="op in opcoesPromo"
            :key="op.valor"
            type="button"
            role="radio"
            class="segmented-btn"
            :class="{ active: filtroPromo === op.valor }"
            :aria-checked="filtroPromo === op.valor"
            @click="filtroPromo = op.valor"
          >
            {{ compact ? op.curto : op.label }}
            <span class="segmented-count num">{{ contagemLocal[op.valor] }}</span>
          </button>
        </div>

        <div v-if="loja.categorias_produtos.length > 1" class="cat-scroll">
          <button type="button" class="chip" :class="{ active: !categoriaLocal }" @click="categoriaLocal = ''">
            Todas
          </button>
          <button
            v-for="c in loja.categorias_produtos"
            :key="c"
            type="button"
            class="chip"
            :class="{ active: categoriaLocal === c }"
            @click="categoriaLocal = categoriaLocal === c ? '' : c"
          >
            <AppIcon :name="iconeCategoria(c)" :size="14" />
            {{ c }}
          </button>
        </div>

        <div v-if="produtosFiltrados.length" :class="compact ? 'products-list' : 'products-grid'">
          <ProductCard
            v-for="prod in produtosFiltrados"
            :key="prod.id"
            :produto="prod"
            :layout="compact ? 'horizontal' : 'vertical'"
            @select="emit('select', $event)"
            @route="emit('route', $event)"
          />
        </div>
        <div v-else class="empty-state">
          <AppIcon name="search-x" :size="28" />
          <p>Nenhum produto encontrado com esses filtros.</p>
        </div>
      </section>

      <!-- Localização -->
      <section ref="localRef" class="profile-section" aria-labelledby="local-title">
        <div class="section-head">
          <h3 id="local-title">
            <AppIcon name="map-pin" :size="18" />
            Localização
          </h3>
        </div>
        <MappedinViewer
          :height="mapHeight"
          :totem-label="origemNome"
          :loja-destino="loja"
          :rota="perfil.rota"
        >
          <template #actions>
            <slot name="map-actions"></slot>
          </template>
        </MappedinViewer>
      </section>
    </template>
  </div>
</template>

<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { api } from '@/services/api'
import { iconeCategoria } from '@/utils/categorias'
import { normalizar } from '@/utils/texto'
import MappedinViewer from '@/components/common/MappedinViewer.vue'
import ProductCard from '@/components/common/ProductCard.vue'

const props = defineProps({
  lojaId: { type: Number, required: true },
  totemId: { type: Number, default: 1 },
  compact: { type: Boolean, default: false },
  mapHeight: { type: Number, default: 540 },
  backLabel: { type: String, default: 'Todas as lojas' },
  origemNome: { type: String, default: 'Totem Piso 1' },
  // Rota 100% acessível (só elevador)
  acessivel: { type: Boolean, default: false }
})

const emit = defineEmits(['back', 'select', 'route'])

const perfil = ref(null)
const carregando = ref(false)
const erro = ref('')
const buscaLocal = ref('')
const filtroPromo = ref('todas')
const categoriaLocal = ref('')
const produtosRef = ref(null)
const localRef = ref(null)

const loja = computed(() => perfil.value?.loja)
const origemLabel = computed(() => `a partir do ${props.origemNome}`)

const opcoesPromo = [
  { valor: 'todas', label: 'Todos', curto: 'Todos' },
  { valor: 'com', label: 'Em promoção', curto: 'Promoção' },
  { valor: 'sem', label: 'Preço normal', curto: 'Sem desconto' }
]

const baseFiltrada = computed(() => {
  const termo = normalizar(buscaLocal.value.trim())
  return (perfil.value?.produtos || []).filter((p) => {
    if (categoriaLocal.value && p.categoria !== categoriaLocal.value) return false
    if (!termo) return true
    return normalizar(`${p.nome} ${p.descricao} ${p.categoria}`).includes(termo)
  })
})

const contagemLocal = computed(() => {
  const com = baseFiltrada.value.filter((p) => p.percentual_desconto > 0).length
  return { todas: baseFiltrada.value.length, com, sem: baseFiltrada.value.length - com }
})

const produtosFiltrados = computed(() => {
  if (filtroPromo.value === 'com') return baseFiltrada.value.filter((p) => p.percentual_desconto > 0)
  if (filtroPromo.value === 'sem') return baseFiltrada.value.filter((p) => p.percentual_desconto === 0)
  return baseFiltrada.value
})

function horario(iso) {
  return new Date(iso).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

function rolarParaProdutos() {
  nextTick(() => produtosRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
}

function irParaLocalizacao() {
  localRef.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

async function carregar() {
  carregando.value = true
  erro.value = ''
  buscaLocal.value = ''
  filtroPromo.value = 'todas'
  categoriaLocal.value = ''
  try {
    perfil.value = await api.obterPerfilLoja(props.lojaId, props.totemId, props.acessivel)
  } catch {
    erro.value = 'Não foi possível carregar o perfil da loja.'
  } finally {
    carregando.value = false
  }
}

watch(() => [props.lojaId, props.totemId, props.acessivel], carregar, { immediate: true })

defineExpose({ irParaLocalizacao })
</script>

<style scoped>
.store-profile {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.back-btn {
  align-self: flex-start;
  margin: 0 0 -10px -10px;
}

.profile-loading,
.profile-error {
  padding: 40px 0;
  text-align: center;
  color: var(--color-graphite-muted);
}

.profile-error {
  color: var(--color-danger-text);
}

/* Cabeçalho */
.profile-header {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 0 20px 20px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  overflow: hidden;
}

.profile-cover {
  height: 84px;
  margin: 0 -20px;
  background:
    radial-gradient(circle at 85% 20%, rgba(201, 163, 74, 0.45), transparent 50%),
    linear-gradient(120deg, var(--color-graphite) 0%, #3A3631 100%);
}

.profile-identity {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  margin-top: -38px;
}

.profile-avatar {
  width: 76px;
  height: 76px;
  border-radius: 20px;
  background: var(--color-white);
  border: 4px solid var(--color-white);
  box-shadow: var(--shadow-md);
  color: var(--color-gold-deep);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background-image: linear-gradient(140deg, var(--color-gold-soft), var(--color-cream));
}

.profile-title {
  min-width: 0;
  padding-top: 46px; /* começa abaixo da capa escura */
}

.profile-title .eyebrow {
  color: var(--color-gold-deep);
}

.profile-title h2 {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.profile-location {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--color-graphite-muted);
  margin-top: 4px;
}

.profile-desc {
  font-size: 15px;
  line-height: 1.5;
  color: var(--color-graphite-muted);
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.profile-stats div {
  padding: 12px 14px;
  background: var(--color-surface);
}

.profile-stats div + div {
  border-left: 1px solid var(--color-border);
}

.profile-stats dt {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.profile-stats dd {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin-top: 2px;
}

.profile-actions {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px 16px;
}

.profile-walk {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: var(--color-graphite-muted);
}

.profile-updated {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--color-success-text);
}

/* Seções */
.profile-section {
  display: flex;
  flex-direction: column;
  gap: 14px;
  scroll-margin-top: 16px;
}

.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.section-head h3 {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 19px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.section-head h3 .app-icon {
  color: var(--color-gold-deep);
}

.destaques-row {
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: calc((100% - 24px) / 3);
  gap: 12px;
  overflow-x: auto;
  padding: 2px 2px 8px;
  scroll-snap-type: x mandatory;
  scrollbar-width: thin;
}

.destaque-card {
  scroll-snap-align: start;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.products-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.store-search {
  min-height: 44px;
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
  min-height: 38px;
  border: none;
  border-radius: 9px;
  background: transparent;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-graphite-muted);
  cursor: pointer;
}

.segmented-btn.active {
  background: var(--color-white);
  color: var(--color-graphite);
  box-shadow: var(--shadow-sm);
}

.segmented-count {
  padding: 1px 6px;
  border-radius: var(--radius-pill);
  background: var(--color-cream-dark);
  font-size: 12px;
}

.segmented-btn.active .segmented-count {
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
}

.cat-scroll {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  scrollbar-width: none;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 28px 16px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  color: var(--color-graphite-muted);
  font-size: 14px;
}

/* Mobile */
.compact .profile-header {
  padding: 0 16px 16px;
  border-radius: var(--radius-md);
}

.compact .profile-cover {
  height: 64px;
  margin: 0 -16px;
}

.compact .profile-identity {
  margin-top: -30px;
}

.compact .profile-title {
  padding-top: 36px;
}

.compact .profile-avatar {
  width: 62px;
  height: 62px;
  border-radius: 16px;
}

.compact .profile-title h2 {
  font-size: 22px;
}

.compact .profile-desc {
  font-size: 14px;
}

.compact .profile-stats dd {
  font-size: 18px;
}

.compact .profile-stats div {
  padding: 10px;
}

.compact .destaques-row {
  grid-auto-columns: 72%;
}

.compact .section-head h3 {
  font-size: 17px;
}

.compact .segmented-btn {
  font-size: 12px;
  gap: 4px;
}
</style>
