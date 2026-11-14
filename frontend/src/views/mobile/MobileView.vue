<template>
  <div class="mobile-view-wrap">
    <div ref="scrollBody" class="mobile-scroll-body">
      <!-- Banner de continuidade herdada do Totem (RN02 / RN10) -->
      <div v-if="inheritedFromTotem" class="totem-inherited-banner" role="status">
        <span class="inherited-icon"><AppIcon name="check" :size="14" :stroke-width="2.6" /></span>
        <div class="inherited-text">
          <strong>Continuando do totem</strong>
          <span>Pesquisa, comparação e rota foram salvas.</span>
        </div>
        <button type="button" class="icon-btn" aria-label="Fechar aviso" @click="inheritedFromTotem = false">
          <AppIcon name="x" :size="16" />
        </button>
      </div>

      <!-- Aviso quando a API não responde (backend parado, desatualizado ou em outra porta) -->
      <div v-if="erroApi" class="api-error-banner" role="alert">
        <AppIcon name="info" :size="18" />
        <span>{{ erroApi }}</span>
        <button type="button" class="btn-cream btn-sm" @click="inicializarMobile()">Tentar de novo</button>
      </div>

      <!-- ABA: INÍCIO -->
      <section v-if="activeTab === 'inicio'" class="m-section">
        <SextaAviso compact />

        <!-- Cupom de sexta-feira 13 guardado no celular -->
        <button v-if="sexta13.temCupom.value" type="button" class="m-coupon-card" @click="mostrarCupom = true">
          <span class="m-coupon-icon" aria-hidden="true"><AppIcon name="ticket" :size="20" /></span>
          <span class="m-coupon-text">
            <strong>Cupom {{ CUPOM_SEXTA13.codigo }}</strong>
            <span>{{ CUPOM_SEXTA13.titulo }} · toque para mostrar no caixa</span>
          </span>
          <AppIcon name="chevron-right" :size="16" />
        </button>
        <div class="m-hero">
          <span class="eyebrow m-hero-eyebrow">Olá! Bem-vindo ao TemAqui</span>
          <h1 class="m-hero-title">Seu próximo achado está aqui.</h1>
        </div>

        <form class="search-field" role="search" @submit.prevent="buscarTexto(termoInicio)">
          <AppIcon name="search" :size="18" />
          <input
            v-model="termoInicio"
            type="search"
            enterkeyhint="search"
            aria-label="Buscar produtos ou lojas"
            placeholder="Produtos, lojas ou ocasiões"
          />
        </form>

        <div class="m-chips-row">
          <button type="button" class="chip" @click="aplicarOrcamento()">
            <AppIcon name="footprints" :size="14" />
            Tênis até R$ 350
          </button>
          <button type="button" class="chip" @click="buscarTexto('presente para mãe')">
            <AppIcon name="gift" :size="14" />
            Presente para mãe
          </button>
        </div>

        <button type="button" class="m-promo-banner" @click="abrirOfertas()">
          <div class="m-promo-text">
            <span class="eyebrow m-promo-eyebrow">Ofertas da semana</span>
            <span class="m-promo-title">Explore mais.<br />Gaste menos.</span>
            <span class="m-promo-cta num">
              {{ totalPromocoes }} produtos em promoção
              <AppIcon name="arrow-right" :size="14" />
            </span>
          </div>
          <img src="/assets/products/tenis-sprint.svg" alt="" class="m-promo-img" />
        </button>

        <div class="m-section-head">
          <h2 class="m-section-subtitle">Categorias</h2>
        </div>
        <div class="m-cat-scroll">
          <button
            v-for="cat in categorias"
            :key="cat.categoria"
            type="button"
            class="m-cat-btn"
            @click="search.aplicar({ categoria: cat.categoria }); activeTab = 'ofertas'"
          >
            <span class="m-cat-icon"><AppIcon :name="iconeCategoria(cat.categoria)" :size="20" /></span>
            <span>{{ cat.categoria }}</span>
          </button>
        </div>

        <div class="m-section-head">
          <h2 class="m-section-subtitle">Lojas em destaque</h2>
          <button type="button" class="link-action" @click="activeTab = 'lojas'">Ver todas</button>
        </div>
        <div class="m-store-scroll">
          <button
            v-for="loja in lojasDestaque"
            :key="loja.id"
            type="button"
            class="m-store-pill"
            @click="abrirPerfilLoja(loja.id)"
          >
            <span class="m-store-pill-icon"><AppIcon :name="iconeCategoria(loja.categoria)" :size="18" /></span>
            <span class="m-store-pill-name">{{ loja.nome }}</span>
            <span class="m-store-pill-meta num">até {{ loja.maior_desconto }}% OFF</span>
          </button>
        </div>

        <div class="m-section-head">
          <h2 class="m-section-subtitle">Maiores descontos</h2>
          <button type="button" class="link-action" @click="abrirOfertas()">Ver todas</button>
        </div>
        <div class="m-list-vertical cat-stage">
          <!-- Easter egg sexta-feira 13: o gato passeia entre os cards -->
          <BlackCat v-if="sexta13.ativo.value" top="calc(33% + 4px)" :duracao="20" @pegar="mostrarCupom = true" />
          <ProductCard
            v-for="prod in destaques"
            :key="prod.id"
            :produto="prod"
            layout="horizontal"
            @select="abrirDetalheMobile"
            @route="abrirRotaMobile"
          />
        </div>
      </section>

      <!-- ABA: BUSCA / OFERTAS -->
      <section v-else-if="activeTab === 'ofertas'" class="m-section">
        <SextaAviso compact />
        <div class="search-field">
          <AppIcon name="search" :size="18" />
          <input
            v-model="search.filtros.q"
            type="search"
            enterkeyhint="search"
            aria-label="Buscar produtos ou lojas"
            placeholder="O que você está procurando?"
          />
          <button
            v-if="search.filtros.q"
            type="button"
            class="icon-btn"
            aria-label="Limpar texto da busca"
            @click="search.filtros.q = ''"
          >
            <AppIcon name="x" :size="16" />
          </button>
        </div>

        <button
          type="button"
          class="m-filter-toggle"
          :aria-expanded="mostrarFiltros"
          @click="mostrarFiltros = !mostrarFiltros"
        >
          <AppIcon name="filter" :size="16" />
          Filtros
          <span v-if="search.temFiltroAtivo.value" class="m-filter-dot" aria-label="filtros ativos"></span>
          <AppIcon :name="mostrarFiltros ? 'chevron-down' : 'chevron-right'" :size="16" class="m-filter-chev" />
        </button>

        <SearchFilters
          v-show="mostrarFiltros"
          compact
          :filtros="search.filtros"
          :contagem="search.contagem.value"
          :categorias="categorias"
          @change="(patch) => Object.assign(search.filtros, patch)"
        />

        <div class="m-results-header">
          <h2 class="num" aria-live="polite">
            {{ search.carregando.value ? 'Buscando…' : `${search.resultados.value.length} produtos` }}
          </h2>
          <button v-if="search.temFiltroAtivo.value" type="button" class="link-action" @click="search.limpar()">
            Limpar
          </button>
        </div>

        <!-- Lojas com resultado: atalho para o perfil -->
        <div v-if="search.lojasEncontradas.value.length" class="m-found">
          <span class="m-found-label">Encontrado em:</span>
          <div class="m-found-row">
            <button
              v-for="item in search.lojasEncontradas.value"
              :key="item.loja.id"
              type="button"
              class="chip"
              @click="abrirPerfilLoja(item.loja.id)"
            >
              {{ item.loja.nome }}
              <span class="chip-meta num">{{ item.total }}</span>
            </button>
          </div>
        </div>

        <div v-if="search.resultados.value.length" class="m-list-vertical cat-stage" :class="{ loading: search.carregando.value }">
          <BlackCat
            v-if="sexta13.ativo.value && search.resultados.value.length > 2"
            top="calc(33% + 4px)"
            :duracao="20"
            @pegar="mostrarCupom = true"
          />
          <ProductCard
            v-for="prod in search.resultados.value"
            :key="prod.id"
            :produto="prod"
            layout="horizontal"
            @select="abrirDetalheMobile"
            @route="abrirRotaMobile"
          />
        </div>
        <div v-else-if="!search.carregando.value" class="m-empty">
          <AppIcon name="search-x" :size="28" />
          <strong>Nenhum produto encontrado</strong>
          <p>Tente outro termo ou remova filtros.</p>
          <button type="button" class="btn-cream btn-sm" @click="search.limpar()">Limpar filtros</button>
        </div>

        <button
          v-if="search.resultados.value.length > 1"
          type="button"
          class="btn-gold btn-lg full-width m-sticky-cta"
          @click="activeTab = 'comparar'"
        >
          <AppIcon name="bar-chart" :size="18" />
          Comparar melhores preços
        </button>
      </section>

      <!-- SUB: COMPARAR -->
      <section v-else-if="activeTab === 'comparar'" class="m-section">
        <button type="button" class="btn-ghost btn-sm m-back" @click="activeTab = 'ofertas'">
          <AppIcon name="arrow-left" :size="16" />
          Voltar à busca
        </button>

        <h2 class="m-hero-title">Compare suas escolhas</h2>

        <div class="m-compare-2col">
          <article
            v-for="(prod, idx) in comparacao.slice(0, 2)"
            :key="prod.id"
            class="m-compare-card"
            :class="{ highlight: idx === 0 }"
          >
            <span v-if="idx === 0" class="m-best-flag">Melhor preço</span>
            <img :src="prod.imagem_url" alt="" class="m-compare-img" />
            <p class="m-compare-store">{{ prod.loja?.nome }}</p>
            <h3 class="m-compare-name">{{ prod.nome }}</h3>
            <strong class="m-compare-price num">{{ formatCurrency(prod.preco_final) }}</strong>
            <span class="m-compare-meta">
              <AppIcon name="layers" :size="12" />
              {{ prod.loja?.pavimento }}
            </span>
            <span class="m-compare-meta">
              <AppIcon name="percent" :size="12" />
              {{ prod.percentual_desconto ? `${prod.percentual_desconto}% OFF` : 'Preço normal' }}
            </span>
            <button type="button" class="btn-gold full-width btn-sm" @click="abrirRotaMobile(prod)">
              <AppIcon name="navigation" :size="14" />
              Como chegar
            </button>
          </article>
        </div>

        <button
          v-for="prod in comparacao.slice(2, 4)"
          :key="prod.id"
          type="button"
          class="m-compare-extra"
          @click="abrirDetalheMobile(prod)"
        >
          <img :src="prod.imagem_url" alt="" />
          <span class="m-compare-extra-text">
            <strong>{{ prod.nome }}</strong>
            <span class="num">{{ formatCurrency(prod.preco_final) }} · {{ prod.loja?.nome }}</span>
          </span>
          <AppIcon name="chevron-right" :size="16" />
        </button>
      </section>

      <!-- SUB: DETALHES DO PRODUTO -->
      <section v-else-if="activeTab === 'detalhe' && selectedProduct" class="m-section">
        <button type="button" class="btn-ghost btn-sm m-back" @click="activeTab = voltarDoDetalhe">
          <AppIcon name="arrow-left" :size="16" />
          Voltar
        </button>

        <div class="m-detail-img-wrap">
          <img :src="selectedProduct.imagem_url" alt="" />
          <span v-if="selectedProduct.percentual_desconto > 0" class="m-detail-discount num">
            -{{ selectedProduct.percentual_desconto }}%
          </span>
        </div>

        <div class="m-detail-head">
          <span class="badge badge-neutral">{{ selectedProduct.categoria }}</span>
          <h2 class="m-detail-title">{{ selectedProduct.nome }}</h2>
          <p class="m-detail-desc">{{ selectedProduct.descricao }}</p>
        </div>

        <div class="m-detail-price-box">
          <div class="m-price-line">
            <strong class="m-big-price num">{{ formatCurrency(selectedProduct.preco_final) }}</strong>
            <span v-if="selectedProduct.preco_promocional" class="m-old-price num">
              {{ formatCurrency(selectedProduct.preco_original) }}
            </span>
          </div>
          <span class="m-updated">
            <AppIcon name="check-circle" :size="13" />
            {{ selectedProduct.atualizado_formatado }}
          </span>
        </div>

        <button type="button" class="m-store-card" @click="abrirPerfilLoja(selectedProduct.loja_id)">
          <span class="m-store-avatar" aria-hidden="true">
            <AppIcon :name="iconeCategoria(selectedProduct.loja?.categoria)" :size="18" />
          </span>
          <span class="m-store-card-text">
            <strong>{{ selectedProduct.loja?.nome }}</strong>
            <span>{{ selectedProduct.loja?.pavimento }} · {{ selectedProduct.loja?.localizacao }}</span>
          </span>
          <span class="m-store-card-cta">
            Ver loja
            <AppIcon name="chevron-right" :size="14" />
          </span>
        </button>

        <button type="button" class="btn-gold btn-lg full-width" @click="abrirRotaMobile(selectedProduct)">
          <AppIcon name="navigation" :size="18" />
          Como chegar
        </button>
      </section>

      <!-- ABA: LOJAS -->
      <section v-else-if="activeTab === 'lojas'" class="m-section">
        <h2 class="m-hero-title">Lojas</h2>

        <div class="search-field">
          <AppIcon name="search" :size="18" />
          <input v-model="buscaLoja" type="search" aria-label="Buscar loja" placeholder="Buscar loja ou segmento" />
        </div>

        <div class="m-chips-scroll" role="group" aria-label="Filtrar lojas">
          <button type="button" class="chip" :class="{ active: !segmentoLoja && !soPromocao }" @click="segmentoLoja = ''; soPromocao = false">
            Todas
          </button>
          <button type="button" class="chip" :class="{ active: soPromocao }" @click="soPromocao = !soPromocao">
            <AppIcon name="percent" :size="14" />
            Com promoção
          </button>
          <button
            v-for="seg in segmentosLoja"
            :key="seg"
            type="button"
            class="chip"
            :class="{ active: segmentoLoja === seg }"
            @click="segmentoLoja = segmentoLoja === seg ? '' : seg"
          >
            {{ seg }}
          </button>
        </div>

        <p class="m-count num">{{ lojasFiltradas.length }} lojas</p>

        <div class="m-list-vertical">
          <StoreCard
            v-for="loja in lojasFiltradas"
            :key="loja.id"
            :loja="loja"
            compact
            @open="abrirPerfilLoja(loja.id)"
          />
        </div>
      </section>

      <!-- SUB: PERFIL DA LOJA -->
      <section v-else-if="activeTab === 'loja' && lojaPerfilId" class="m-section">
        <StoreProfile
          :loja-id="lojaPerfilId"
          :totem-id="totemOrigemId"
          :origem-nome="`Totem Piso ${totemOrigemId}`"
          :map-height="600"
          compact
          :back-label="voltarDoPerfil === 'lojas' ? 'Todas as lojas' : 'Voltar'"
          @back="activeTab = voltarDoPerfil"
          @select="abrirDetalheMobile"
          @route="abrirRotaMobile"
        />
      </section>

      <!-- ABA: MAPA -->
      <section v-else-if="activeTab === 'mapa'" class="m-section">
        <h2 class="m-hero-title">Mapa e rota</h2>

        <label class="form-field">
          <span>Loja de destino</span>
          <span class="m-select-wrap">
            <AppIcon name="map-pin" :size="16" class="m-select-icon" />
            <select class="m-store-select" :value="selectedStore?.id" @change="onSelectStoreChange($event)">
              <option v-for="l in lojas" :key="l.id" :value="l.id">
                {{ l.nome }} — {{ l.pavimento }}
              </option>
            </select>
            <AppIcon name="chevron-down" :size="16" class="m-select-chevron" />
          </span>
        </label>

        <MappedinViewer
          :height="600"
          allow-fullscreen
          :totem-label="`Totem Piso ${totemOrigemId}`"
          :loja-destino="selectedStore"
          :rota="currentRoute"
          :produto-nome="selectedProduct?.loja_id === selectedStore?.id ? selectedProduct?.nome : ''"
        >
          <template #actions>
            <button
              v-if="selectedStore"
              type="button"
              class="btn-cream full-width"
              @click="abrirPerfilLoja(selectedStore.id)"
            >
              <AppIcon name="store" :size="16" />
              Ver perfil da loja
            </button>
          </template>
        </MappedinViewer>
      </section>
    </div>

    <CouponModal
      v-if="mostrarCupom"
      modo="mobile"
      :salvo="sexta13.temCupom.value"
      @salvar="sexta13.salvarCupom()"
      @fechar="mostrarCupom = false"
    />

    <!-- Barra de navegação inferior -->
    <nav class="mobile-bottom-nav" aria-label="Navegação principal">
      <button
        v-for="item in navItems"
        :key="item.id"
        type="button"
        class="m-nav-item"
        :class="{ active: item.tabs.includes(activeTab) }"
        :aria-current="item.tabs.includes(activeTab) ? 'page' : undefined"
        @click="item.action ? item.action() : (activeTab = item.id)"
      >
        <span class="m-nav-icon">
          <AppIcon :name="item.icon" :size="22" :stroke-width="item.tabs.includes(activeTab) ? 2.2 : 1.8" />
        </span>
        <span>{{ item.label }}</span>
      </button>
    </nav>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { api, formatCurrency, mensagemErroApi } from '@/services/api'
import { useProductSearch } from '@/composables/useProductSearch'
import { iconeCategoria } from '@/utils/categorias'
import { normalizar } from '@/utils/texto'
import MappedinViewer from '@/components/common/MappedinViewer.vue'
import ProductCard from '@/components/common/ProductCard.vue'
import SearchFilters from '@/components/common/SearchFilters.vue'
import StoreCard from '@/components/common/StoreCard.vue'
import StoreProfile from '@/components/common/StoreProfile.vue'
import BlackCat from '@/components/sexta13/BlackCat.vue'
import CouponModal from '@/components/sexta13/CouponModal.vue'
import SextaAviso from '@/components/sexta13/SextaAviso.vue'
import { CUPOM_SEXTA13, useSexta13 } from '@/composables/useSexta13'

const route = useRoute()

// 'inicio' | 'ofertas' | 'comparar' | 'detalhe' | 'lojas' | 'loja' | 'mapa'
const activeTab = ref('inicio')
const inheritedFromTotem = ref(false)
const totemOrigemId = ref(1)
const termoInicio = ref('')
const mostrarFiltros = ref(false)
const scrollBody = ref(null)
const erroApi = ref('')

// Easter egg sexta-feira 13
const sexta13 = useSexta13()
const mostrarCupom = ref(false)

const search = useProductSearch({ totemId: totemOrigemId })

const lojas = ref([])
const categorias = ref([])
const destaques = ref([])
const totalPromocoes = ref(0)
const selectedProduct = ref(null)
const selectedStore = ref(null)
const currentRoute = ref(null)

const lojaPerfilId = ref(null)
const voltarDoPerfil = ref('lojas')
const voltarDoDetalhe = ref('ofertas')

const buscaLoja = ref('')
const segmentoLoja = ref('')
const soPromocao = ref(false)

const navItems = [
  { id: 'inicio', label: 'Início', icon: 'home', tabs: ['inicio'] },
  { id: 'ofertas', label: 'Buscar', icon: 'search', tabs: ['ofertas', 'comparar', 'detalhe'] },
  { id: 'lojas', label: 'Lojas', icon: 'store', tabs: ['lojas', 'loja'] },
  { id: 'mapa', label: 'Mapa', icon: 'map', tabs: ['mapa'] }
]

const lojasDestaque = computed(() =>
  [...lojas.value].filter((l) => l.total_promocoes > 0).sort((a, b) => b.maior_desconto - a.maior_desconto).slice(0, 8)
)

const segmentosLoja = computed(() => [...new Set(lojas.value.map((l) => l.categoria))])

const lojasFiltradas = computed(() => {
  const termo = normalizar(buscaLoja.value.trim())
  return lojas.value.filter((l) => {
    if (segmentoLoja.value && l.categoria !== segmentoLoja.value) return false
    if (soPromocao.value && !l.total_promocoes) return false
    if (!termo) return true
    return normalizar(`${l.nome} ${l.categoria} ${l.descricao} ${l.categorias_produtos.join(' ')}`).includes(termo)
  })
})

const comparacao = computed(() =>
  [...search.resultados.value].sort((a, b) => a.preco_final - b.preco_final).slice(0, 4)
)

async function inicializarMobile(tentativa = 1) {
  try {
    if (route.query.fromTotem) totemOrigemId.value = Number(route.query.fromTotem) || 1

    // Cada bloco carrega de forma independente: uma falha não esvazia a tela inteira
    const [lRes, cRes, dRes] = await Promise.allSettled([
      api.listarLojas({ totem_id: totemOrigemId.value }),
      api.listarCategorias(),
      api.listarProdutos({ ordenar_por: 'maior_desconto', totem_id: totemOrigemId.value })
    ])
    const falhas = [lRes, cRes, dRes].filter((r) => r.status === 'rejected')
    erroApi.value = falhas.length ? mensagemErroApi(falhas[0].reason) : ''
    if (falhas.length && tentativa < 3) setTimeout(() => inicializarMobile(tentativa + 1), 1500)

    const lData = lRes.status === 'fulfilled' ? lRes.value : lojas.value
    const cData = cRes.status === 'fulfilled' ? cRes.value : categorias.value
    const dData = dRes.status === 'fulfilled' ? dRes.value : []
    lojas.value = lData
    categorias.value = cData
    destaques.value = dData.slice(0, 6)
    totalPromocoes.value = dData.filter((p) => p.percentual_desconto > 0).length
    selectedProduct.value = dData[0] || null
    selectedStore.value = selectedProduct.value?.loja || lData[0] || null

    // Cupom de sexta-feira 13 levado do totem pelo QR Code
    if (route.query.cupom === CUPOM_SEXTA13.codigo) {
      sexta13.salvarCupom()
      mostrarCupom.value = true
    }

    // Continuidade vinda do QR Code do Totem (RN10)
    if (route.query.fromTotem && !route.query.cupom) {
      inheritedFromTotem.value = true
      let produtoDoTotem = null
      if (route.query.produtoId) {
        produtoDoTotem = dData.find((p) => p.id === Number(route.query.produtoId)) || null
        if (produtoDoTotem) {
          selectedProduct.value = produtoDoTotem
          selectedStore.value = produtoDoTotem.loja
        }
      }
      if (route.query.lojaId) {
        const foundLoja = lData.find((l) => l.id === Number(route.query.lojaId))
        if (foundLoja) selectedStore.value = foundLoja
      }
      search.aplicar({ q: String(route.query.q || '') })
      if (produtoDoTotem) {
        // A pessoa escolheu um produto no totem: abre direto nele (o "Voltar" leva à busca)
        voltarDoDetalhe.value = 'ofertas'
        activeTab.value = 'detalhe'
      } else {
        activeTab.value = 'ofertas'
      }
    } else {
      search.aplicar({})
    }

    if (selectedStore.value) {
      currentRoute.value = await api.obterRota(totemOrigemId.value, selectedStore.value.id)
    }
  } catch (err) {
    console.error('Erro ao inicializar Mobile:', err)
  }
}

function buscarTexto(texto) {
  search.aplicar({ q: texto || '' })
  activeTab.value = 'ofertas'
}

function aplicarOrcamento() {
  search.aplicar({ q: 'tênis', categoria: 'Calçados', preco_max: 350, ordenar_por: 'menor_preco' })
  activeTab.value = 'ofertas'
}

function abrirOfertas() {
  search.aplicar({ promocao: 'com', ordenar_por: 'maior_desconto' })
  activeTab.value = 'ofertas'
}

function abrirDetalheMobile(prod) {
  if (activeTab.value !== 'detalhe') voltarDoDetalhe.value = activeTab.value === 'loja' ? 'loja' : activeTab.value === 'inicio' ? 'inicio' : 'ofertas'
  selectedProduct.value = prod
  selectedStore.value = prod.loja
  activeTab.value = 'detalhe'
}

function abrirPerfilLoja(lojaId) {
  if (activeTab.value !== 'loja') voltarDoPerfil.value = activeTab.value
  lojaPerfilId.value = lojaId
  activeTab.value = 'loja'
}

async function abrirRotaMobile(prod) {
  selectedProduct.value = prod
  selectedStore.value = lojas.value.find((l) => l.id === prod.loja_id) || prod.loja
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

// Ao trocar de aba, volta ao topo do conteúdo
watch(activeTab, () => {
  scrollBody.value?.scrollTo({ top: 0 })
})

onMounted(() => {
  inicializarMobile()
})
</script>

<style scoped>
.mobile-view-wrap {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-height: 0;
}

.mobile-scroll-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 18px 18px 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scrollbar-width: none;
}

.mobile-scroll-body::-webkit-scrollbar {
  display: none;
}

/* Banner herdado do totem */
.totem-inherited-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--color-success-bg);
  border: 1px solid var(--color-success-border);
  border-radius: 12px;
  padding: 10px 6px 10px 12px;
  color: var(--color-success-text);
}

.inherited-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-success-text);
  color: var(--color-white);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.inherited-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  font-size: 12px;
}

.inherited-text strong {
  font-size: 13px;
  font-weight: 600;
}

.totem-inherited-banner .icon-btn {
  color: var(--color-success-text);
}

.api-error-banner {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px 10px;
  padding: 12px;
  border-radius: var(--radius-sm);
  background: var(--color-danger-bg);
  color: var(--color-danger-text);
  font-size: 13px;
  font-weight: 500;
  line-height: 1.4;
}

.api-error-banner span {
  flex: 1;
  min-width: 180px;
}

.cat-stage {
  position: relative;
}

.m-coupon-card {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 12px 14px;
  border: 1px dashed rgba(201, 163, 74, 0.7);
  border-radius: var(--radius-md);
  background: linear-gradient(120deg, #1A1A1A 0%, #2E2A25 100%);
  color: #E8E2D3;
  text-align: left;
  cursor: pointer;
}

.m-coupon-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: rgba(201, 163, 74, 0.16);
  color: var(--color-gold);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.m-coupon-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  font-size: 12px;
  color: #CFC8B8;
}

.m-coupon-text strong {
  font-size: 15px;
  color: var(--color-gold);
  letter-spacing: 0.02em;
}

/* Seções */
.m-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.m-hero {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.m-hero-eyebrow {
  color: var(--color-gold-deep);
}

.m-hero-title {
  font-size: 26px;
  font-weight: 700;
  line-height: 1.15;
  letter-spacing: -0.03em;
}

.m-back {
  align-self: flex-start;
  margin: -4px 0 -8px -10px;
}

.m-chips-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.m-chips-scroll,
.m-cat-scroll,
.m-store-scroll,
.m-found-row {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  margin: 0 -18px;
  padding: 0 18px 2px;
  scrollbar-width: none;
}

.m-chips-scroll::-webkit-scrollbar,
.m-cat-scroll::-webkit-scrollbar,
.m-store-scroll::-webkit-scrollbar,
.m-found-row::-webkit-scrollbar {
  display: none;
}

/* Promo */
.m-promo-banner {
  width: 100%;
  text-align: left;
  background: linear-gradient(120deg, var(--color-graphite) 0%, #3A3631 100%);
  border: none;
  border-radius: var(--radius-md);
  padding: 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  cursor: pointer;
  color: var(--color-white);
  box-shadow: var(--shadow-md);
}

.m-promo-text {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.m-promo-eyebrow {
  color: var(--color-gold);
}

.m-promo-title {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
}

.m-promo-cta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  font-weight: 500;
  color: #D9D3C4;
}

.m-promo-img {
  width: 96px;
  height: 84px;
  object-fit: cover;
  border-radius: 12px;
  background: var(--color-white);
  flex-shrink: 0;
}

.m-section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 4px;
  margin-bottom: -6px;
}

.m-section-subtitle {
  font-size: 18px;
  font-weight: 700;
  letter-spacing: -0.015em;
}

/* Categorias */
.m-cat-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 76px;
  padding: 10px 6px;
  border: 1px solid var(--color-border);
  border-radius: 14px;
  background: var(--color-white);
  font-size: 12px;
  font-weight: 600;
  color: var(--color-graphite);
  cursor: pointer;
}

.m-cat-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--color-cream);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* Lojas em destaque */
.m-store-pill {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  min-width: 128px;
  padding: 12px;
  border: 1px solid var(--color-border);
  border-radius: 14px;
  background: var(--color-white);
  text-align: left;
  cursor: pointer;
}

.m-store-pill-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: var(--color-graphite);
  color: var(--color-gold);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 6px;
}

.m-store-pill-name {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-graphite);
}

.m-store-pill-meta {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-gold-deep);
}

.m-list-vertical {
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: opacity 0.15s var(--ease);
}

.m-list-vertical.loading {
  opacity: 0.55;
}

/* Filtros */
.m-filter-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  min-height: 44px;
  padding: 0 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-graphite);
  cursor: pointer;
  margin-bottom: -4px;
}

.m-filter-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-gold);
}

.m-filter-chev {
  margin-left: auto;
  color: var(--color-graphite-muted);
}

.m-results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.m-results-header h2 {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.m-found {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: -6px;
}

.m-found-label,
.m-count {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-graphite-muted);
}

.m-count {
  margin: -6px 0 -6px;
}

.chip-meta {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.m-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 6px;
  padding: 28px 16px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  color: var(--color-graphite-muted);
  font-size: 13px;
}

.m-empty strong {
  font-size: 15px;
  color: var(--color-graphite);
}

.m-sticky-cta {
  position: sticky;
  bottom: 0;
  box-shadow: 0 8px 24px -6px rgba(41, 41, 41, 0.25);
}

/* Comparar */
.m-compare-2col {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  padding-top: 8px;
}

.m-compare-card {
  position: relative;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.m-compare-card.highlight {
  border-color: var(--color-gold);
  box-shadow: 0 0 0 1px var(--color-gold);
}

.m-best-flag {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-gold);
  font-size: 11px;
  font-weight: 700;
  padding: 2px 10px;
  border-radius: var(--radius-pill);
  white-space: nowrap;
}

.m-compare-img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 10px;
  background: var(--color-cream);
  margin-bottom: 6px;
}

.m-compare-store {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-graphite-muted);
}

.m-compare-name {
  font-size: 14px;
  font-weight: 600;
  line-height: 1.3;
}

.m-compare-price {
  font-size: 19px;
  font-weight: 700;
  letter-spacing: -0.02em;
  margin: 2px 0;
}

.m-compare-meta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.m-compare-card .btn-gold {
  margin-top: 8px;
}

.m-compare-extra {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  text-align: left;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 10px;
  cursor: pointer;
  color: var(--color-graphite-muted);
}

.m-compare-extra img {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  object-fit: cover;
}

.m-compare-extra-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  font-size: 12px;
}

.m-compare-extra-text strong {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-graphite);
}

/* Detalhe */
.m-detail-img-wrap {
  position: relative;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
}

.m-detail-img-wrap img {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

.m-detail-discount {
  position: absolute;
  top: 12px;
  left: 12px;
  background: var(--color-graphite);
  color: var(--color-white);
  font-size: 13px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: var(--radius-xs);
}

.m-detail-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
}

.m-detail-title {
  font-size: 24px;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.15;
}

.m-detail-desc {
  font-size: 14px;
  color: var(--color-graphite-muted);
  line-height: 1.55;
}

.m-detail-price-box {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.m-price-line {
  display: flex;
  align-items: baseline;
  gap: 10px;
}

.m-big-price {
  font-size: 30px;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.m-old-price {
  font-size: 15px;
  color: var(--color-graphite-muted);
  text-decoration: line-through;
}

.m-updated {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: var(--color-success-text);
}

.m-store-card {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  text-align: left;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  cursor: pointer;
}

.m-store-avatar {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: var(--color-graphite);
  color: var(--color-gold);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.m-store-card-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.m-store-card-text strong {
  font-size: 15px;
  font-weight: 600;
  color: var(--color-graphite);
}

.m-store-card-cta {
  display: inline-flex;
  align-items: center;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-gold-deep);
}

/* Mapa */
.m-select-wrap {
  position: relative;
  display: block;
}

.m-select-icon,
.m-select-chevron {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-graphite-muted);
  pointer-events: none;
}

.m-select-icon {
  left: 14px;
}

.m-select-chevron {
  right: 14px;
}

.form-field .m-store-select {
  width: 100%;
  appearance: none;
  padding-left: 38px;
  padding-right: 38px;
  font-weight: 600;
  cursor: pointer;
}

/* Barra de Navegação Inferior */
.mobile-bottom-nav {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid var(--color-border);
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(8px);
  padding: 6px 4px max(14px, env(safe-area-inset-bottom));
  flex-shrink: 0;
}

.m-nav-item {
  background: none;
  border: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 6px 0 2px;
  font-size: 11px;
  font-weight: 500;
  color: var(--color-graphite-muted);
  cursor: pointer;
}

.m-nav-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 56px;
  height: 30px;
  border-radius: var(--radius-pill);
  transition: background-color 0.2s var(--ease);
}

.m-nav-item.active {
  color: var(--color-graphite);
  font-weight: 700;
}

.m-nav-item.active .m-nav-icon {
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
}
</style>
