<template>
  <div class="mobile-view-wrap">
    <!-- Conteúdo rolável da aba ativa -->
    <div class="mobile-scroll-body">
      <!-- Banner de Continuidade Herdada do Totem (RN02 / RN10 - Fiel ao 2º frame do Print 03) -->
      <div v-if="inheritedFromTotem" class="totem-inherited-banner">
        <span>✓ Pesquisa, comparação e rota do totem salvas</span>
        <button type="button" class="close-banner-btn" @click="inheritedFromTotem = false">✕</button>
      </div>

      <!-- ABA 1: INÍCIO (Frame 1 do Print 03) -->
      <section v-if="activeTab === 'inicio'" class="m-section">
        <h1 class="m-hero-title">
          Seu próximo achado<br />
          está aqui.
        </h1>

        <div class="m-search-box">
          <span>🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="O que você está procurando?"
            @keyup.enter="irParaOfertas()"
          />
        </div>

        <!-- Card de Campanha Mobile ("Explore mais. Gaste menos.") -->
        <div class="m-promo-banner" @click="aplicarChipMobile('tênis de corrida até R$ 350')">
          <div class="m-promo-text">
            <span class="m-eyebrow">OFERTAS DA SEMANA</span>
            <h3>Explore mais.<br />Gaste menos.</h3>
            <p>Achadinhos até 25% OFF</p>
          </div>
          <img
            src="/assets/products/tenis-sprint.svg"
            alt="Ofertas da Semana"
            class="m-promo-img"
          />
        </div>

        <!-- Chips rápidos -->
        <div class="m-chips-row">
          <button
            type="button"
            class="m-chip"
            @click="aplicarChipMobile('tênis de corrida até R$ 350')"
          >
            Tênis até R$ 350
          </button>
          <button
            type="button"
            class="m-chip"
            @click="aplicarChipMobile('presente para mãe')"
          >
            Presente para mãe
          </button>
        </div>

        <h2 class="m-section-subtitle">Ofertas em destaque</h2>

        <div class="m-list-vertical">
          <ProductCard
            v-for="prod in produtos"
            :key="prod.id"
            :produto="prod"
            layout="horizontal"
            @select="abrirDetalheMobile"
            @route="abrirRotaMobile"
          />
        </div>
      </section>

      <!-- ABA 2: OFERTAS / BUSCA HERDADA DO TOTEM (Frame 2 do Print 03) -->
      <section v-else-if="activeTab === 'ofertas'" class="m-section">
        <div class="m-search-box">
          <span>🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="tênis de corrida até R$ 350"
          />
        </div>

        <div class="m-chips-row">
          <span class="m-chip active">Calçados ✕</span>
          <span class="m-chip active">Até R$ 350 ✕</span>
        </div>

        <div class="m-results-header">
          <h2>{{ produtosOfertas.length }} ofertas para você</h2>
          <div class="m-sub-filters">
            <span>Filtros ▾</span>
            <span>Menor preço ▾</span>
          </div>
        </div>

        <div class="m-list-vertical">
          <ProductCard
            v-for="prod in produtosOfertas"
            :key="prod.id"
            :produto="prod"
            layout="horizontal"
            @select="abrirDetalheMobile"
            @route="abrirRotaMobile"
          />
        </div>

        <button
          type="button"
          class="btn-gold full-width"
          @click="activeTab = 'comparar'"
        >
          Comparar {{ produtosOfertas.length }} ofertas
        </button>
      </section>

      <!-- ABA 2.1: COMPARAR SUAS ESCOLHAS (Frame 3 do Print 03) -->
      <section v-else-if="activeTab === 'comparar'" class="m-section">
        <h2 class="m-hero-title">Compare suas escolhas</h2>

        <button type="button" class="btn-cream full-width" @click="activeTab = 'ofertas'">
          ← Voltar à busca
        </button>

        <div class="m-compare-2col">
          <div
            v-for="prod in produtosOfertas.slice(0, 2)"
            :key="prod.id"
            class="m-compare-card"
          >
            <img :src="prod.imagem_url" :alt="prod.nome" class="m-compare-img" />
            <h4>{{ prod.nome.replace('Tênis ', '') }}</h4>
            <p class="m-compare-store">{{ prod.loja?.nome }}</p>
            <strong class="m-compare-price">{{ formatCurrency(prod.preco_final) }}</strong>
            <span class="m-compare-meta">
              {{ prod.loja?.pavimento }} • Hoje, 10:42
            </span>
            <button type="button" class="btn-gold full-width btn-sm" @click="abrirRotaMobile(prod)">
              Como chegar
            </button>
          </div>
        </div>

        <div v-if="produtosOfertas[2]" class="m-compare-extra">
          <strong>
            {{ produtosOfertas[2].nome.replace('Tênis ', '') }} •
            {{ formatCurrency(produtosOfertas[2].preco_final) }} •
            {{ produtosOfertas[2].loja?.pavimento }}
          </strong>
          <p>Mais uma oferta da pesquisa salva</p>
        </div>
      </section>

      <!-- ABA 2.2: DETALHES DO PRODUTO NO MOBILE (Frames 4, 6, 8, 10 do Print 03) -->
      <section v-else-if="activeTab === 'detalhe' && selectedProduct" class="m-section">
        <button type="button" class="m-back-link" @click="activeTab = 'ofertas'">
          ← Voltar à busca
        </button>

        <div class="m-detail-img-wrap">
          <img :src="selectedProduct.imagem_url" :alt="selectedProduct.nome" />
        </div>

        <span class="m-eyebrow">{{ selectedProduct.categoria.toUpperCase() }}</span>
        <h2 class="m-detail-title">{{ selectedProduct.nome }}</h2>
        <p class="m-detail-desc">{{ selectedProduct.descricao }}</p>

        <div class="m-detail-price-box">
          <span v-if="selectedProduct.preco_promocional" class="m-old-price">
            {{ formatCurrency(selectedProduct.preco_original) }}
          </span>
          <strong class="m-big-price">{{ formatCurrency(selectedProduct.preco_final) }}</strong>
          <span class="m-updated">✓ {{ selectedProduct.atualizado_formatado }}</span>
        </div>

        <p class="m-store-line">
          <strong>{{ selectedProduct.loja?.nome }} • {{ selectedProduct.loja?.pavimento }}</strong>
          <span v-if="selectedProduct.loja?.localizacao"> • {{ selectedProduct.loja.localizacao }}</span>
        </p>

        <button type="button" class="btn-gold full-width" @click="abrirRotaMobile(selectedProduct)">
          Como chegar ↗
        </button>
      </section>

      <!-- ABA 3: MAPA 3D + ROTA PRONTA NO CELULAR (Frames 5, 7, 9 do Print 03) -->
      <section v-else-if="activeTab === 'mapa'" class="m-section">
        <h2 class="m-hero-title">Sua rota está pronta</h2>

        <!-- Seletor de loja destino no mobile -->
        <div class="m-store-select-row">
          <select
            class="m-store-select"
            :value="selectedStore?.id"
            @change="onSelectStoreChange($event)"
          >
            <option v-for="l in lojas" :key="l.id" :value="l.id">
              📍 {{ l.nome }} ({{ l.pavimento }})
            </option>
          </select>
        </div>

        <MappedinViewer
          :height="360"
          :totem-label="`Totem Piso ${totemOrigemId}`"
          :loja-destino="selectedStore"
          :rota="currentRoute"
          :produto-nome="selectedProduct?.nome || ''"
        />
      </section>

      <!-- ABA 4: RECOMPENSAS SIMULADAS (RN12) -->
      <section v-else-if="activeTab === 'recompensas'" class="m-section">
        <h2 class="m-hero-title">Recompensas & Vouchers</h2>
        <div class="m-demo-card">
          <strong>Preços e prêmios demonstrativos (RN12)</strong>
          <p>
            Na versão demonstrativa do HACKARUN 2026, validações de notas fiscais (NFC-e) e
            sorteios de vouchers na roleta são simulados para apresentação da jornada física no
            Capim Dourado Shopping.
          </p>
          <button
            type="button"
            class="btn-gold full-width"
            style="margin-top: 12px"
            @click="voucherMessage = '🎉 Voucher demonstrativo: 10% OFF extra na loja física apresentado no caixa!'"
          >
            Simular validação de visita na loja
          </button>
          <p v-if="voucherMessage" class="m-voucher-alert">{{ voucherMessage }}</p>
        </div>
      </section>

      <!-- ABA 5: PERFIL / AJUDA SEM LOGIN (RN02) -->
      <section v-else-if="activeTab === 'perfil'" class="m-section">
        <h2 class="m-hero-title">Acesso Livre • Sem Cadastro</h2>
        <div class="m-demo-card">
          <strong>Privacidade e Agilidade (RN02 / RN10)</strong>
          <p>
            O TemAqui não exige criação de conta nem login para pesquisar ofertas, comparar preços
            ou continuar no celular a rota iniciada no Totem.
          </p>
          <p style="margin-top: 8px">
            <strong>Nenhuma compra ou pagamento online (RN01):</strong> toda a experiência é
            voltada a levar você até a loja física do Capim Dourado Shopping.
          </p>
        </div>
      </section>
    </div>

    <!-- Bottom Navigation Bar (Fiel ao Print 03: Início, Ofertas, Mapa, Recompensas, Perfil) -->
    <nav class="mobile-bottom-nav">
      <button
        type="button"
        class="m-nav-item"
        :class="{ active: activeTab === 'inicio' }"
        @click="activeTab = 'inicio'"
      >
        <span class="m-nav-icon">🏠</span>
        <span>Início</span>
      </button>
      <button
        type="button"
        class="m-nav-item"
        :class="{ active: ['ofertas', 'comparar', 'detalhe'].includes(activeTab) }"
        @click="activeTab = 'ofertas'"
      >
        <span class="m-nav-icon">🏷️</span>
        <span>Ofertas</span>
      </button>
      <button
        type="button"
        class="m-nav-item"
        :class="{ active: activeTab === 'mapa' }"
        @click="activeTab = 'mapa'"
      >
        <span class="m-nav-icon">🗺️</span>
        <span>Mapa</span>
      </button>
      <button
        type="button"
        class="m-nav-item"
        :class="{ active: activeTab === 'recompensas' }"
        @click="activeTab = 'recompensas'"
      >
        <span class="m-nav-icon">🎁</span>
        <span>Recompensas</span>
      </button>
      <button
        type="button"
        class="m-nav-item"
        :class="{ active: activeTab === 'perfil' }"
        @click="activeTab = 'perfil'"
      >
        <span class="m-nav-icon">👤</span>
        <span>Perfil</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { api, formatCurrency } from '@/services/api'
import MappedinViewer from '@/components/common/MappedinViewer.vue'
import ProductCard from '@/components/common/ProductCard.vue'

const route = useRoute()

const activeTab = ref('inicio') // 'inicio' | 'ofertas' | 'comparar' | 'detalhe' | 'mapa' | 'recompensas' | 'perfil'
const inheritedFromTotem = ref(false)
const totemOrigemId = ref(1)
const searchQuery = ref('')
const voucherMessage = ref('')

const produtos = ref([])
const lojas = ref([])
const selectedProduct = ref(null)
const selectedStore = ref(null)
const currentRoute = ref(null)

const produtosOfertas = computed(() => {
  const q = searchQuery.value.toLowerCase()
  if (q.includes('350') || q.includes('tênis') || q.includes('tenis') || !q) {
    const calcados = produtos.value
      .filter((p) => p.categoria === 'Calçados' && p.preco_final <= 350)
      .sort((a, b) => a.preco_final - b.preco_final)
    return calcados.length ? calcados : produtos.value
  }
  return produtos.value.filter(
    (p) =>
      p.nome.toLowerCase().includes(q) ||
      p.categoria.toLowerCase().includes(q) ||
      p.loja?.nome.toLowerCase().includes(q)
  )
})

async function inicializarMobile() {
  try {
    const [pData, lData] = await Promise.all([
      api.listarProdutos({ totem_id: totemOrigemId.value }),
      api.listarLojas()
    ])
    produtos.value = pData
    lojas.value = lData
    selectedProduct.value = pData[0] || null
    selectedStore.value = selectedProduct.value?.loja || lData[0] || null

    // Verifica parâmetros vindos do QR Code do Totem (RN10)
    if (route.query.fromTotem) {
      inheritedFromTotem.value = true
      totemOrigemId.value = Number(route.query.fromTotem) || 1
      searchQuery.value = String(route.query.q || 'tênis de corrida até R$ 350')

      if (route.query.produtoId) {
        const foundProd = pData.find((p) => p.id === Number(route.query.produtoId))
        if (foundProd) {
          selectedProduct.value = foundProd
          selectedStore.value = foundProd.loja
        }
      }
      if (route.query.lojaId) {
        const foundLoja = lData.find((l) => l.id === Number(route.query.lojaId))
        if (foundLoja) selectedStore.value = foundLoja
      }
      activeTab.value = 'ofertas'
    }

    if (selectedStore.value) {
      currentRoute.value = await api.obterRota(totemOrigemId.value, selectedStore.value.id)
    }
  } catch (err) {
    console.error('Erro ao inicializar Mobile:', err)
  }
}

function irParaOfertas() {
  activeTab.value = 'ofertas'
}

function aplicarChipMobile(texto) {
  searchQuery.value = texto
  activeTab.value = 'ofertas'
}

function abrirDetalheMobile(prod) {
  selectedProduct.value = prod
  selectedStore.value = prod.loja
  activeTab.value = 'detalhe'
}

async function abrirRotaMobile(prod) {
  selectedProduct.value = prod
  selectedStore.value = prod.loja
  try {
    currentRoute.value = await api.obterRota(totemOrigemId.value, prod.loja_id)
  } catch {
    currentRoute.value = null
  }
  activeTab.value = 'mapa'
}

async function onSelectStoreChange(event) {
  const id = Number(event.target.value)
  const loja = lojas.value.find((l) => l.id === id)
  if (loja) {
    selectedStore.value = loja
    currentRoute.value = await api.obterRota(totemOrigemId.value, loja.id)
  }
}

onMounted(() => {
  inicializarMobile()
})
</script>

<style scoped>
.mobile-view-wrap {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 100%;
  justify-content: space-between;
}

.mobile-scroll-body {
  flex: 1;
  padding: 16px 18px 24px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.totem-inherited-banner {
  background: var(--color-cream);
  border: 1px solid var(--color-gold);
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-graphite);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}

.close-banner-btn {
  background: none;
  border: none;
  font-size: 12px;
  cursor: pointer;
}

.m-section {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.m-hero-title {
  font-size: 24px;
  font-weight: 800;
  line-height: 1.15;
  color: var(--color-graphite);
}

.m-search-box {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 10px 14px;
}

.m-search-box input {
  flex: 1;
  border: none;
  background: transparent;
  outline: none;
  font-size: 13px;
}

.m-promo-banner {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  cursor: pointer;
}

.m-eyebrow {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: var(--color-graphite-muted);
}

.m-promo-text h3 {
  font-size: 17px;
  font-weight: 800;
  margin: 4px 0;
}

.m-promo-text p {
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.m-promo-img {
  width: 96px;
  height: 76px;
  object-fit: cover;
  border-radius: 10px;
  background: var(--color-white);
}

.m-chips-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.m-chip {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  padding: 7px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

.m-chip.active {
  background: var(--color-gold-soft);
  border-color: var(--color-gold);
}

.m-section-subtitle {
  font-size: 16px;
  font-weight: 800;
}

.m-list-vertical {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.m-results-header h2 {
  font-size: 18px;
  font-weight: 800;
}

.m-sub-filters {
  display: flex;
  gap: 14px;
  font-size: 12px;
  color: var(--color-graphite-muted);
  margin-top: 4px;
}

.m-compare-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.m-compare-card {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.m-compare-img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 8px;
}

.m-compare-store,
.m-compare-meta {
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.m-compare-price {
  font-size: 17px;
  font-weight: 800;
}

.m-compare-extra {
  background: var(--color-cream);
  border-radius: 12px;
  padding: 12px;
  font-size: 12px;
}

.m-back-link {
  align-self: flex-start;
  background: none;
  border: none;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.m-detail-img-wrap {
  border-radius: 16px;
  overflow: hidden;
  background: var(--color-cream);
}

.m-detail-img-wrap img {
  width: 100%;
  height: 210px;
  object-fit: cover;
}

.m-detail-title {
  font-size: 22px;
  font-weight: 800;
}

.m-detail-desc {
  font-size: 13px;
  color: var(--color-graphite-muted);
  line-height: 1.45;
}

.m-detail-price-box {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.m-old-price {
  font-size: 12px;
  color: var(--color-graphite-muted);
  text-decoration: line-through;
}

.m-big-price {
  font-size: 28px;
  font-weight: 800;
}

.m-updated {
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.m-store-line {
  font-size: 13px;
}

.m-store-select {
  width: 100%;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: var(--color-cream);
  font-size: 13px;
  font-weight: 600;
}

.m-demo-card {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 16px;
  font-size: 13px;
  line-height: 1.45;
}

.m-voucher-alert {
  margin-top: 10px;
  padding: 10px;
  border-radius: 8px;
  background: var(--color-success-bg);
  color: var(--color-success-text);
  font-weight: 700;
  font-size: 12px;
}

.full-width {
  width: 100%;
}

/* Barra de Navegação Inferior */
.mobile-bottom-nav {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  border-top: 1px solid var(--color-border);
  background: var(--color-white);
  padding: 8px 4px 12px;
}

.m-nav-item {
  background: none;
  border: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  font-size: 10px;
  font-weight: 600;
  color: var(--color-graphite-muted);
  cursor: pointer;
}

.m-nav-item.active {
  color: var(--color-graphite);
  font-weight: 800;
}

.m-nav-icon {
  font-size: 16px;
}
</style>
