<template>
  <div class="totem-container">
    <!-- Top Header do Totem (Presente em todas as telas do Print 02) -->
    <header class="totem-topbar">
      <div class="brand-logo totem-brand" @click="screen = 'welcome'">
        <span class="brand-pin"></span>
        <span>TemAqui</span>
      </div>
      <div class="totem-location-meta">
        <strong>CAPIM DOURADO SHOPPING</strong>
        <span>{{ totemInfo.identificacao }} • {{ totemInfo.posicao_referencia }}</span>
      </div>
    </header>

    <!-- 1. TELA DE DESCANSO / BOAS-VINDAS (Com a 5ª imagem enviada!) -->
    <section v-if="screen === 'welcome'" class="welcome-screen">
      <div class="hero-image-card" @click="irParaVitrine()">
        <img
          src="/assets/capim-dourado-hero.webp"
          alt="Capim Dourado Shopping - Palmas TO"
          class="hero-photo"
        />
        <span class="hero-badge">EXPERIMENTE NOVAS DESCOBERTAS</span>
      </div>

      <div class="welcome-copy">
        <h1 class="welcome-title">
          Bem-vindo<br />
          ao TemAqui!
        </h1>
        <p class="welcome-lead">O que você procura, tem aqui!</p>
        <p class="welcome-desc">
          Ofertas, lojas e o melhor caminho.<br />
          Tudo a um toque de você.
        </p>
      </div>

      <div class="welcome-cta-area">
        <button type="button" class="btn-gold btn-totem-hero" @click="irParaVitrine()">
          Toque para explorar →
        </button>
        <p class="welcome-footnote">
          Sem baixar aplicativo. Sem cadastro para explorar.
        </p>
      </div>
    </section>

    <!-- DEMAIS TELAS DO TOTEM (Vitrine, Busca, Comparar, Detalhes, Mapa, QR, Ajuda) -->
    <template v-else>
      <!-- Navegação de Abas do Totem -->
      <nav class="totem-tabs">
        <button
          type="button"
          class="totem-tab"
          :class="{ active: screen === 'vitrine' && !activeQuickMode }"
          @click="resetVitrine()"
        >
          Início
        </button>
        <button
          type="button"
          class="totem-tab"
          :class="{ active: screen === 'vitrine' && !!activeQuickMode || screen === 'compare' }"
          @click="aplicarBuscaOrcamento()"
        >
          Ofertas
        </button>
        <button
          type="button"
          class="totem-tab"
          :class="{ active: screen === 'lojas' }"
          @click="screen = 'lojas'"
        >
          Lojas
        </button>
        <button
          type="button"
          class="totem-tab"
          :class="{ active: screen === 'map' }"
          @click="abrirMapaGeral()"
        >
          Mapa
        </button>
        <button
          type="button"
          class="totem-tab"
          :class="{ active: screen === 'ajuda' }"
          @click="screen = 'ajuda'"
        >
          Ajuda
        </button>
      </nav>

      <!-- 2. VITRINE DE OFERTAS / BUSCA POR ORÇAMENTO / BUSCA POR OCASIÃO -->
      <section v-if="screen === 'vitrine'" class="totem-content">
        <!-- Barra de Busca -->
        <div class="search-box-row">
          <span class="search-icon">🔍</span>
          <input
            v-model="searchQuery"
            type="text"
            class="totem-search-input"
            placeholder="O que você está procurando?"
            @keyup.enter="executarBusca()"
          />
          <button v-if="searchQuery" type="button" class="clear-btn" @click="resetVitrine()">
            ✕
          </button>
        </div>

        <!-- Sugestões Rápidas (Orcamento e Ocasião - Fiéis ao Print 02) -->
        <div v-if="!activeQuickMode" class="quick-suggestions-row">
          <span class="sug-label">Sugestões:</span>
          <button type="button" class="sug-chip" @click="aplicarBuscaOrcamento()">
            Tênis até R$ 350
          </button>
          <button type="button" class="sug-chip" @click="aplicarBuscaOcasiao()">
            Presente para minha mãe
          </button>
        </div>

        <!-- MODO: VITRINE PADRÃO -->
        <template v-if="!activeQuickMode">
          <CampaignBanner @action="onCampaignAction" />

          <!-- Ícones de Categorias e Serviços do Shopping -->
          <div class="category-icons-grid">
            <button
              v-for="cat in categoryShortcuts"
              :key="cat.label"
              type="button"
              class="cat-icon-btn"
              @click="filtrarPorCategoria(cat.filter)"
            >
              <span class="cat-emoji">{{ cat.icon }}</span>
              <span class="cat-name">{{ cat.label }}</span>
            </button>
          </div>

          <div class="section-header-row">
            <h2>Ofertas em destaque</h2>
            <button type="button" class="text-action-btn" @click="aplicarBuscaOrcamento()">
              Ver todas →
            </button>
          </div>

          <div class="products-grid-3">
            <ProductCard
              v-for="prod in produtosDestaque"
              :key="prod.id"
              :produto="prod"
              @select="abrirDetalhe"
              @route="abrirRotaProduto"
            />
          </div>

          <div class="explore-stores-block">
            <h3>Explore nossas lojas</h3>
            <div class="store-pills-row">
              <button
                v-for="loja in lojas.slice(0, 5)"
                :key="loja.id"
                type="button"
                class="store-pill-btn"
                @click="abrirRotaLoja(loja)"
              >
                {{ loja.nome }}
              </button>
            </div>
          </div>
        </template>

        <!-- MODO: BUSCA POR ORÇAMENTO ("Seu tênis. Dentro do orçamento.") -->
        <template v-else-if="activeQuickMode === 'orcamento'">
          <div class="mode-header">
            <h2>Seu tênis. Dentro do orçamento.</h2>
            <p>Encontre e compare ofertas de lojas participantes.</p>
          </div>

          <div class="active-filter-chips">
            <span class="filter-chip active">Categoria: Calçados</span>
            <span class="filter-chip active">Até R$ 350</span>
            <span class="filter-chip">1º e 2º piso</span>
          </div>
          <p class="ai-interpretation-line">
            ✓ Entendemos seu orçamento e selecionamos {{ produtosFiltrados.length }} opções.
          </p>

          <div class="results-toolbar">
            <strong>{{ produtosFiltrados.length }} ofertas encontradas</strong>
            <span class="sort-pill">Menor preço ▾</span>
          </div>

          <div class="products-grid-3">
            <ProductCard
              v-for="prod in produtosFiltrados"
              :key="prod.id"
              :produto="prod"
              @select="abrirDetalhe"
              @route="abrirRotaProduto"
            />
          </div>

          <button type="button" class="btn-gold full-width" @click="screen = 'compare'">
            Comparar ofertas
          </button>

          <div class="info-disclaimer-box">
            <strong>Preços informados pelas próprias lojas</strong>
            <p>Confirme disponibilidade, tamanhos e condições na loja física (RN06).</p>
          </div>
        </template>

        <!-- MODO: BUSCA POR OCASIÃO ("Um presente com a cara dela.") -->
        <template v-else-if="activeQuickMode === 'ocasiao'">
          <div class="mode-header">
            <h2>Um presente com a cara dela.</h2>
            <p>Selecionamos ideias de diferentes lojas para você.</p>
          </div>

          <div class="active-filter-chips">
            <span class="filter-chip active">Perfumaria</span>
            <span class="filter-chip active">Moda Feminina</span>
            <span class="filter-chip active">Acessórios</span>
          </div>
          <p class="ai-interpretation-line">
            Sugestões para você: Perfumaria, Moda Feminina, Acessórios, Calçados
          </p>

          <div class="results-toolbar">
            <strong>{{ produtosFiltrados.length }} ofertas encontradas</strong>
            <span class="sort-pill">Mais próximas ▾</span>
          </div>

          <div class="products-grid-3">
            <ProductCard
              v-for="prod in produtosFiltrados"
              :key="prod.id"
              :produto="prod"
              @select="abrirDetalhe"
              @route="abrirRotaProduto"
            />
          </div>

          <button type="button" class="btn-gold full-width" @click="screen = 'compare'">
            Comparar ofertas
          </button>

          <div class="info-disclaimer-box">
            <strong>Preços informados pelas próprias lojas</strong>
            <p>Confirme disponibilidade, tamanhos e condições na loja física (RN06).</p>
          </div>
        </template>
      </section>

      <!-- 3. COMPARAR OFERTAS ("Compare e escolha seu caminho") -->
      <section v-else-if="screen === 'compare'" class="totem-content">
        <div>
          <button type="button" class="btn-cream btn-sm" @click="screen = 'vitrine'">
            ← Voltar
          </button>
        </div>

        <div class="mode-header">
          <h2>Compare e escolha seu caminho</h2>
          <p>Mesma categoria. Diferentes possibilidades.</p>
        </div>

        <div class="compare-grid">
          <div v-for="prod in produtosComparacao" :key="prod.id" class="compare-col-card">
            <img :src="prod.imagem_url" :alt="prod.nome" class="compare-img" />
            <h3 class="compare-prod-name">{{ prod.nome }}</h3>
            <p class="compare-store">{{ prod.loja?.nome }}</p>

            <div class="compare-price-box">
              <strong class="compare-price">{{ formatCurrency(prod.preco_final) }}</strong>
              <span v-if="prod.percentual_desconto > 0" class="compare-off">
                {{ prod.percentual_desconto }}% OFF
              </span>
            </div>

            <div class="compare-meta-list">
              <span>{{ prod.atualizado_formatado }}</span>
              <strong>{{ prod.loja?.pavimento }}</strong>
              <span>{{ prod.tempo_estimado_min || 2 }} min a pé</span>
            </div>

            <button type="button" class="btn-cream full-width" @click="abrirDetalhe(prod)">
              Ver detalhes
            </button>
            <button type="button" class="btn-gold full-width" @click="abrirRotaProduto(prod)">
              Como chegar
            </button>
          </div>
        </div>

        <button type="button" class="btn-cream full-width" @click="screen = 'qr'">
          Continuar no celular (QR Code)
        </button>
      </section>

      <!-- 4. DETALHES DO PRODUTO ("Seu próximo achado está aqui.") -->
      <section v-else-if="screen === 'detail' && selectedProduct" class="totem-content">
        <div>
          <button type="button" class="btn-cream btn-sm" @click="screen = 'vitrine'">
            ← Voltar
          </button>
        </div>

        <h2 class="section-main-title">Seu próximo achado está aqui.</h2>

        <div class="detail-hero-card">
          <img
            :src="selectedProduct.imagem_url"
            :alt="selectedProduct.nome"
            class="detail-hero-img"
          />
        </div>

        <div class="detail-info-block">
          <span class="detail-cat-eyebrow">
            {{ selectedProduct.categoria.toUpperCase() }} • OFERTA VERIFICADA
          </span>
          <h3 class="detail-prod-title">{{ selectedProduct.nome }}</h3>
          <p class="detail-prod-desc">{{ selectedProduct.descricao }}</p>

          <div class="detail-price-row">
            <div>
              <span
                v-if="selectedProduct.preco_promocional"
                class="detail-old-price"
              >
                {{ formatCurrency(selectedProduct.preco_original) }}
              </span>
              <strong class="detail-final-price">
                {{ formatCurrency(selectedProduct.preco_final) }}
              </strong>
            </div>
            <span v-if="selectedProduct.percentual_desconto > 0" class="detail-discount-pill">
              {{ selectedProduct.percentual_desconto }}% OFF
            </span>
          </div>

          <p class="detail-updated-stamp">
            ✓ Preço informado em {{ selectedProduct.atualizado_formatado }}
          </p>

          <div class="detail-store-box">
            <strong>{{ selectedProduct.loja?.nome }} • {{ selectedProduct.loja?.pavimento }}</strong>
            <p>
              Promoção demonstrativa válida enquanto durar o estoque •
              {{ selectedProduct.loja?.localizacao }}
            </p>
          </div>
        </div>

        <div class="detail-actions">
          <button
            type="button"
            class="btn-gold full-width"
            @click="abrirRotaProduto(selectedProduct)"
          >
            Como chegar ↗
          </button>
          <button type="button" class="btn-cream full-width" @click="screen = 'qr'">
            Continuar no celular
          </button>
        </div>
      </section>

      <!-- 5. MAPA 3D + ROTA ("Seu caminho, sem complicação.") -->
      <section v-else-if="screen === 'map'" class="totem-content">
        <div>
          <button type="button" class="btn-cream btn-sm" @click="screen = 'vitrine'">
            ← Voltar
          </button>
        </div>

        <h2 class="section-main-title">Seu caminho, sem complicação.</h2>

        <!-- Seletor rápido de loja destino caso queira alternar no mapa -->
        <div class="map-store-selector">
          <button
            v-for="loja in lojas"
            :key="loja.id"
            type="button"
            class="store-pill-btn"
            :class="{ active: selectedStore?.id === loja.id }"
            @click="abrirRotaLoja(loja)"
          >
            {{ loja.nome }} ({{ loja.pavimento }})
          </button>
        </div>

        <!-- Componente Reutilizável MappedinViewer.vue (Iframe Oficial 3D) -->
        <MappedinViewer
          :height="540"
          :totem-label="totemInfo.identificacao"
          :loja-destino="selectedStore"
          :rota="currentRoute"
          :produto-nome="selectedProduct?.nome || ''"
        >
          <template #actions>
            <button
              type="button"
              class="btn-gold full-width"
              style="margin-top: 8px"
              @click="screen = 'qr'"
            >
              Levar rota no celular (QR Code)
            </button>
          </template>
        </MappedinViewer>
      </section>

      <!-- 6. MODAL / TELA DE QR CODE ("Continue sua busca e rota no celular") -->
      <section v-else-if="screen === 'qr'" class="totem-content">
        <QrCodeModal
          :totem-id="totemId"
          :search-query="searchQuery || 'Tênis até R$ 350'"
          :produto="selectedProduct"
          :loja="selectedStore || selectedProduct?.loja"
          @close="screen = 'map'"
        />
      </section>

      <!-- 7. LISTA DE LOJAS DO SHOPPING -->
      <section v-else-if="screen === 'lojas'" class="totem-content">
        <div class="mode-header">
          <h2>Lojas e Serviços do Capim Dourado</h2>
          <p>Toque em qualquer loja para visualizar sua localização e rota no Mapa 3D.</p>
        </div>
        <div class="stores-list-grid">
          <div v-for="loja in lojas" :key="loja.id" class="store-card-item">
            <div>
              <strong>{{ loja.nome }}</strong>
              <p>{{ loja.categoria }} • {{ loja.pavimento }} ({{ loja.localizacao }})</p>
            </div>
            <button type="button" class="btn-gold" @click="abrirRotaLoja(loja)">
              Como chegar ↗
            </button>
          </div>
        </div>
      </section>

      <!-- 8. TELA DE AJUDA -->
      <section v-else-if="screen === 'ajuda'" class="totem-content">
        <div class="mode-header">
          <h2>Como funciona o TemAqui?</h2>
          <p>Encontre produtos, compare preços e chegue rápido à loja física.</p>
        </div>
        <div class="help-steps">
          <div class="help-step-card">
            <strong>1. Encontre</strong>
            <p>Busque por produto, orçamento ("tênis até R$ 350") ou ocasião ("presente para mãe").</p>
          </div>
          <div class="help-step-card">
            <strong>2. Compare</strong>
            <p>Veja preços e descontos atualizados diretamente pelos lojistas do shopping.</p>
          </div>
          <div class="help-step-card">
            <strong>3. Vá até a loja</strong>
            <p>Siga o mapa 3D a partir deste totem ou escaneie o QR Code para levar a rota no celular.</p>
          </div>
        </div>
      </section>

      <!-- Rodapé institucional do Totem -->
      <footer class="totem-footer">
        <span>Palmas, TO • Mapa e ofertas demonstrativas (RN01 / RN11)</span>
        <button type="button" class="help-pill-btn" @click="screen = 'ajuda'">
          ? Ajuda
        </button>
      </footer>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api, formatCurrency } from '@/services/api'
import MappedinViewer from '@/components/common/MappedinViewer.vue'
import ProductCard from '@/components/common/ProductCard.vue'
import CampaignBanner from '@/components/common/CampaignBanner.vue'
import QrCodeModal from '@/components/common/QrCodeModal.vue'

const route = useRoute()
const totemId = computed(() => Number(route.params.totemId || 1))

const screen = ref('welcome') // 'welcome' | 'vitrine' | 'compare' | 'detail' | 'map' | 'qr' | 'lojas' | 'ajuda'
const activeQuickMode = ref('') // '' | 'orcamento' | 'ocasiao'
const searchQuery = ref('')

const totemInfo = ref({
  id: 1,
  identificacao: 'Totem Piso 1',
  pavimento: '1º Piso',
  posicao_referencia: 'Entrada Principal'
})

const produtos = ref([])
const lojas = ref([])
const selectedProduct = ref(null)
const selectedStore = ref(null)
const currentRoute = ref(null)

const categoryShortcuts = [
  { icon: '👕', label: 'Moda', filter: 'Calçados' },
  { icon: '👟', label: 'Calçados', filter: 'Calçados' },
  { icon: '✨', label: 'Beleza', filter: 'Perfumaria' },
  { icon: '👜', label: 'Acessórios', filter: 'Acessórios' },
  { icon: '🍽️', label: 'Restaurantes', filter: 'Restaurantes' },
  { icon: '🎬', label: 'Cinema', filter: 'Lazer' },
  { icon: '🚻', label: 'Serviços', filter: 'mapa' }
]

const produtosDestaque = computed(() => {
  // Exibe na capa Tênis Sprint Run, Perfume Essencial e Bolsa Couro Caramelo (como no Print 02)
  const idsCapa = [1, 4, 5]
  const escolhidos = idsCapa
    .map((id) => produtos.value.find((p) => p.id === id))
    .filter(Boolean)
  return escolhidos.length ? escolhidos : produtos.value.slice(0, 3)
})

const produtosFiltrados = computed(() => {
  if (activeQuickMode.value === 'orcamento') {
    return produtos.value
      .filter((p) => p.categoria === 'Calçados' && p.preco_final <= 350)
      .sort((a, b) => a.preco_final - b.preco_final)
  }
  if (activeQuickMode.value === 'ocasiao') {
    const idsPresente = [1, 4, 5]
    return idsPresente
      .map((id) => produtos.value.find((p) => p.id === id))
      .filter(Boolean)
  }
  if (!searchQuery.value.trim()) return produtos.value
  const q = searchQuery.value.toLowerCase()
  return produtos.value.filter(
    (p) =>
      p.nome.toLowerCase().includes(q) ||
      p.categoria.toLowerCase().includes(q) ||
      p.loja?.nome.toLowerCase().includes(q)
  )
})

const produtosComparacao = computed(() => {
  const base = produtosFiltrados.value.length
    ? produtosFiltrados.value
    : produtos.value.filter((p) => p.categoria === 'Calçados')
  return base.slice(0, 3)
})

async function carregarDadosTotem() {
  try {
    const [tData, pData, lData] = await Promise.all([
      api.obterTotem(totemId.value),
      api.listarProdutos({ totem_id: totemId.value }),
      api.listarLojas()
    ])
    totemInfo.value = tData
    produtos.value = pData
    lojas.value = lData
    selectedProduct.value = pData.find((p) => p.id === 2) || pData[0] || null
    selectedStore.value = selectedProduct.value?.loja || lData[0] || null
  } catch (err) {
    console.error('Erro ao carregar dados do totem:', err)
  }
}

function irParaVitrine() {
  screen.value = 'vitrine'
  activeQuickMode.value = ''
}

function resetVitrine() {
  screen.value = 'vitrine'
  activeQuickMode.value = ''
  searchQuery.value = ''
}

function aplicarBuscaOrcamento() {
  screen.value = 'vitrine'
  activeQuickMode.value = 'orcamento'
  searchQuery.value = 'tênis de corrida até R$ 350'
}

function aplicarBuscaOcasiao() {
  screen.value = 'vitrine'
  activeQuickMode.value = 'ocasiao'
  searchQuery.value = 'presente para minha mãe'
}

function executarBusca() {
  const q = searchQuery.value.toLowerCase()
  if (q.includes('350') || q.includes('tênis') || q.includes('tenis')) {
    activeQuickMode.value = 'orcamento'
  } else if (q.includes('mãe') || q.includes('mae') || q.includes('presente')) {
    activeQuickMode.value = 'ocasiao'
  } else {
    activeQuickMode.value = ''
  }
}

function onCampaignAction(slide) {
  if (slide.filter?.preco_max) {
    aplicarBuscaOrcamento()
  } else {
    aplicarBuscaOcasiao()
  }
}

function filtrarPorCategoria(filterVal) {
  if (filterVal === 'mapa') {
    abrirMapaGeral()
    return
  }
  searchQuery.value = filterVal
  activeQuickMode.value = ''
}

async function abrirDetalhe(prod) {
  selectedProduct.value = prod
  selectedStore.value = prod.loja
  screen.value = 'detail'
}

async function abrirRotaProduto(prod) {
  selectedProduct.value = prod
  selectedStore.value = prod.loja
  try {
    currentRoute.value = await api.obterRota(totemId.value, prod.loja_id)
  } catch {
    currentRoute.value = null
  }
  screen.value = 'map'
}

async function abrirRotaLoja(loja) {
  selectedStore.value = loja
  try {
    currentRoute.value = await api.obterRota(totemId.value, loja.id)
  } catch {
    currentRoute.value = null
  }
  screen.value = 'map'
}

async function abrirMapaGeral() {
  if (!selectedStore.value && lojas.value.length) {
    selectedStore.value = lojas.value[0]
  }
  if (selectedStore.value) {
    await abrirRotaLoja(selectedStore.value)
  } else {
    screen.value = 'map'
  }
}

watch(totemId, () => {
  carregarDadosTotem()
})

onMounted(() => {
  carregarDadosTotem()
})
</script>

<style scoped>
.totem-container {
  display: flex;
  flex-direction: column;
  min-height: 100%;
  flex: 1;
  background: var(--color-white);
}

.totem-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 26px 14px;
  border-bottom: 1px solid var(--color-border);
}

.totem-brand {
  font-size: 22px;
  cursor: pointer;
}

.totem-location-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.totem-location-meta strong {
  color: var(--color-graphite);
  letter-spacing: 0.04em;
}

/* 1. TELA DE BOAS-VINDAS / DESCANSO */
.welcome-screen {
  flex: 1;
  padding: 26px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 24px;
}

.hero-image-card {
  position: relative;
  border-radius: 22px;
  overflow: hidden;
  height: 440px;
  box-shadow: 0 12px 32px rgba(41, 41, 41, 0.14);
  cursor: pointer;
}

.hero-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.hero-badge {
  position: absolute;
  left: 18px;
  bottom: 18px;
  background: var(--color-white);
  color: var(--color-graphite);
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.06em;
  padding: 8px 14px;
  border-radius: 999px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.18);
}

.welcome-copy {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.welcome-title {
  font-size: 46px;
  font-weight: 800;
  line-height: 1.08;
  letter-spacing: -0.03em;
  color: var(--color-graphite);
}

.welcome-lead {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-graphite);
}

.welcome-desc {
  font-size: 16px;
  line-height: 1.45;
  color: var(--color-graphite-muted);
}

.welcome-cta-area {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-totem-hero {
  width: 100%;
  padding: 20px;
  font-size: 18px;
  border-radius: 14px;
}

.welcome-footnote {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

/* ABAS DO TOTEM */
.totem-tabs {
  display: flex;
  gap: 22px;
  padding: 12px 26px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-white);
}

.totem-tab {
  background: none;
  border: none;
  font-size: 14px;
  font-weight: 600;
  color: var(--color-graphite-muted);
  padding: 6px 2px;
  cursor: pointer;
  border-bottom: 2px solid transparent;
}

.totem-tab.active {
  color: var(--color-graphite);
  font-weight: 800;
  border-bottom-color: var(--color-gold);
}

.totem-content {
  flex: 1;
  padding: 22px 26px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.search-box-row {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 12px 16px;
}

.totem-search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-size: 15px;
  color: var(--color-graphite);
}

.clear-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: var(--color-graphite-muted);
}

.quick-suggestions-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.sug-label {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.sug-chip {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  padding: 7px 14px;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-graphite);
  cursor: pointer;
}

.sug-chip:hover {
  background: var(--color-gold-soft);
}

.category-icons-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.cat-icon-btn {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 10px 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}

.cat-emoji {
  font-size: 18px;
}

.cat-name {
  font-size: 11px;
  font-weight: 600;
  color: var(--color-graphite);
}

.section-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-header-row h2 {
  font-size: 20px;
  font-weight: 800;
}

.text-action-btn {
  background: none;
  border: none;
  font-size: 13px;
  font-weight: 700;
  color: var(--color-graphite);
  cursor: pointer;
}

.products-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.explore-stores-block {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.explore-stores-block h3 {
  font-size: 15px;
  font-weight: 800;
}

.store-pills-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.store-pill-btn {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  padding: 10px 18px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
}

.store-pill-btn.active {
  background: var(--color-gold);
  border-color: var(--color-gold);
}

.mode-header h2 {
  font-size: 24px;
  font-weight: 800;
}

.mode-header p {
  font-size: 13px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.active-filter-chips {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.filter-chip {
  background: var(--color-cream);
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 700;
}

.filter-chip.active {
  background: var(--color-gold-soft);
  border: 1px solid var(--color-gold);
}

.ai-interpretation-line {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.results-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.sort-pill {
  background: var(--color-cream);
  padding: 6px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
}

.info-disclaimer-box {
  background: var(--color-cream);
  border-radius: 12px;
  padding: 14px 16px;
  font-size: 12px;
}

.info-disclaimer-box p {
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

/* COMPARADOR */
.compare-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.compare-col-card {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.compare-img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 10px;
  background: var(--color-white);
}

.compare-prod-name {
  font-size: 15px;
  font-weight: 800;
}

.compare-store {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.compare-price-box {
  display: flex;
   flex-direction: column;
}

.compare-price {
  font-size: 20px;
  font-weight: 800;
}

.compare-off {
  font-size: 11px;
  font-weight: 700;
  color: #8A6B20;
}

.compare-meta-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 11px;
  color: var(--color-graphite-muted);
  padding: 8px 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

/* DETALHES */
.section-main-title {
  font-size: 24px;
  font-weight: 800;
}

.detail-hero-card {
  border-radius: 18px;
  overflow: hidden;
  background: var(--color-cream);
  max-height: 310px;
}

.detail-hero-img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.detail-info-block {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-cat-eyebrow {
  font-size: 11px;
  font-weight: 700;
  color: var(--color-graphite-muted);
  letter-spacing: 0.05em;
}

.detail-prod-title {
  font-size: 28px;
  font-weight: 800;
}

.detail-prod-desc {
  font-size: 14px;
  color: var(--color-graphite-muted);
  line-height: 1.45;
}

.detail-price-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 6px;
}

.detail-old-price {
  display: block;
  font-size: 13px;
  color: var(--color-graphite-muted);
  text-decoration: line-through;
}

.detail-final-price {
  font-size: 32px;
  font-weight: 800;
}

.detail-discount-pill {
  background: var(--color-cream);
  padding: 6px 12px;
  border-radius: 999px;
  font-weight: 800;
  font-size: 13px;
}

.detail-updated-stamp {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.detail-store-box {
  background: var(--color-cream);
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 13px;
}

.detail-store-box p {
  font-size: 12px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.detail-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.map-store-selector {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.stores-list-grid,
.help-steps {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.store-card-item,
.help-step-card {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.help-step-card {
  flex-direction: column;
  align-items: flex-start;
}

.full-width {
  width: 100%;
}

.totem-footer {
  margin-top: auto;
  padding: 14px 26px;
  border-top: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.help-pill-btn {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}
</style>
