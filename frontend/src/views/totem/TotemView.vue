<template>
  <div class="totem-container">
    <!-- Top Header do Totem -->
    <header class="totem-topbar">
      <button
        type="button"
        class="brand-logo totem-brand"
        aria-label="TemAqui, voltar à tela inicial"
        @click="onLogoClick"
      >
        <span class="brand-pin"></span>
        <span>TemAqui</span>
      </button>
      <div class="totem-location-meta">
        <strong>Capim Dourado Shopping</strong>
        <span>
          <AppIcon name="map-pin" :size="12" />
          {{ totemInfo.identificacao }} · {{ totemInfo.posicao_referencia }}
        </span>
      </div>
    </header>

    <!-- 1. TELA DE DESCANSO / BOAS-VINDAS -->
    <main v-if="screen === 'welcome'" class="welcome-screen">
      <div class="hero-image-card">
        <img
          src="/assets/capim-dourado-hero.webp"
          alt="Fachada do Capim Dourado Shopping, em Palmas (TO)"
          class="hero-photo"
        />
        <div class="hero-overlay" aria-hidden="true"></div>
        <span class="hero-badge">
          <AppIcon name="sparkles" :size="14" />
          Experimente novas descobertas
        </span>
      </div>

      <div class="welcome-copy">
        <span class="eyebrow welcome-eyebrow">Capim Dourado Shopping · Palmas, TO</span>
        <h1 class="welcome-title">Bem-vindo ao TemAqui!</h1>
        <p class="welcome-lead">O que você procura, tem aqui.</p>
        <p class="welcome-desc">
          Ofertas, lojas e o melhor caminho até elas — tudo a um toque de você.
        </p>
      </div>

      <ul class="welcome-features">
        <li>
          <span class="feature-icon"><AppIcon name="tag" :size="20" /></span>
          <span><strong class="num">{{ totalProdutos || '+60' }} ofertas</strong>atualizadas pelas lojas</span>
        </li>
        <li>
          <span class="feature-icon"><AppIcon name="store" :size="20" /></span>
          <span><strong class="num">{{ lojas.length || 11 }} lojas</strong>com perfil e localização</span>
        </li>
        <li>
          <span class="feature-icon"><AppIcon name="navigation" :size="20" /></span>
          <span><strong>Rota</strong>até a porta da loja</span>
        </li>
      </ul>

      <div class="welcome-cta-area">
        <button type="button" class="btn-gold btn-totem-hero" @click="irParaVitrine()">
          <AppIcon name="touch" :size="22" />
          Toque para explorar
        </button>
        <p class="welcome-footnote">
          <AppIcon name="shield-check" :size="14" />
          Sem baixar aplicativo. Sem cadastro para explorar.
        </p>
      </div>
    </main>

    <!-- DEMAIS TELAS DO TOTEM -->
    <template v-else>
      <nav class="totem-tabs" aria-label="Seções do totem">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          type="button"
          class="totem-tab"
          :class="{ active: tab.isActive() }"
          :aria-current="tab.isActive() ? 'page' : undefined"
          @click="tab.action()"
        >
          <AppIcon :name="tab.icon" :size="18" />
          {{ tab.label }}
        </button>
      </nav>

      <div v-if="erroApi" class="api-error-banner" role="alert">
        <AppIcon name="info" :size="18" />
        <span>{{ erroApi }}</span>
        <button type="button" class="btn-cream btn-sm" @click="carregarDadosTotem()">Tentar de novo</button>
      </div>

      <!-- 2. INÍCIO / VITRINE -->
      <main v-if="screen === 'vitrine'" class="totem-content">
        <SextaAviso />
        <form class="search-field totem-search" role="search" @submit.prevent="buscarTexto(termoInicio)">
          <AppIcon name="search" :size="20" />
          <input
            v-model="termoInicio"
            type="search"
            aria-label="Buscar produtos, lojas ou ocasiões"
            placeholder="Busque produtos, lojas ou “presente para minha mãe”"
          />
          <button type="submit" class="btn-gold btn-sm">Buscar</button>
        </form>

        <div class="quick-suggestions-row">
          <span class="sug-label">Experimente:</span>
          <button type="button" class="chip" @click="aplicarBuscaOrcamento()">
            <AppIcon name="footprints" :size="14" />
            Tênis até R$ 350
          </button>
          <button type="button" class="chip" @click="aplicarBuscaOcasiao()">
            <AppIcon name="gift" :size="14" />
            Presente para minha mãe
          </button>
          <button type="button" class="chip" @click="buscarTexto('cinema')">
            <AppIcon name="film" :size="14" />
            Cinema
          </button>
        </div>

        <CampaignBanner @action="onCampaignAction" />

        <section aria-labelledby="cat-title" class="block">
          <div class="section-header-row">
            <h2 id="cat-title">Navegue por categoria</h2>
          </div>
          <div class="category-icons-grid">
            <button
              v-for="cat in categorias"
              :key="cat.categoria"
              type="button"
              class="cat-icon-btn"
              @click="search.aplicar({ categoria: cat.categoria }); screen = 'busca'"
            >
              <span class="cat-icon"><AppIcon :name="iconeCategoria(cat.categoria)" :size="22" /></span>
              <span class="cat-name">{{ cat.categoria }}</span>
              <span class="cat-count num">{{ cat.total }} itens</span>
            </button>
          </div>
        </section>

        <section class="block">
          <div class="section-header-row">
            <h2>Maiores descontos agora</h2>
            <button type="button" class="link-action" @click="abrirOfertas()">
              Ver todas as ofertas
              <AppIcon name="arrow-right" :size="16" />
            </button>
          </div>
          <div class="products-grid-3 cat-stage">
            <!-- Easter egg sexta-feira 13: o gato anda entre as duas linhas de cards -->
            <BlackCat v-if="sexta13.ativo.value" top="50%" @pegar="mostrarCupom = true" />
            <ProductCard
              v-for="prod in destaques"
              :key="prod.id"
              :produto="prod"
              @select="abrirDetalhe"
              @route="abrirRotaProduto"
            />
          </div>
        </section>

        <section class="block">
          <div class="section-header-row">
            <h2>Lojas com promoções</h2>
            <button type="button" class="link-action" @click="screen = 'lojas'">
              Todas as lojas
              <AppIcon name="arrow-right" :size="16" />
            </button>
          </div>
          <div class="stores-grid-2">
            <StoreCard
              v-for="loja in lojasComPromocao.slice(0, 4)"
              :key="loja.id"
              :loja="loja"
              compact
              @open="abrirPerfilLoja(loja.id)"
            />
          </div>
        </section>
      </main>

      <!-- 3. RESULTADOS DA BUSCA (filtragem real) -->
      <main v-else-if="screen === 'busca'" class="totem-content">
        <SextaAviso />
        <div class="search-field totem-search">
          <AppIcon name="search" :size="20" />
          <input
            v-model="search.filtros.q"
            type="search"
            aria-label="Buscar produtos, lojas ou ocasiões"
            placeholder="O que você está procurando?"
          />
          <button
            v-if="search.filtros.q"
            type="button"
            class="icon-btn"
            aria-label="Limpar texto da busca"
            @click="search.filtros.q = ''"
          >
            <AppIcon name="x" :size="18" />
          </button>
        </div>

        <div class="mode-header">
          <h2>{{ tituloBusca.titulo }}</h2>
          <p>{{ tituloBusca.subtitulo }}</p>
        </div>

        <SearchFilters
          :filtros="search.filtros"
          :contagem="search.contagem.value"
          :categorias="categorias"
          @change="(patch) => Object.assign(search.filtros, patch)"
        />

        <div class="results-toolbar">
          <strong class="num" aria-live="polite">
            {{ search.carregando.value ? 'Buscando…' : `${search.resultados.value.length} produtos encontrados` }}
          </strong>
          <button v-if="search.temFiltroAtivo.value" type="button" class="link-action" @click="search.limpar()">
            <AppIcon name="x" :size="14" />
            Limpar filtros
          </button>
        </div>

        <!-- Lojas onde os resultados estão -->
        <div v-if="search.lojasEncontradas.value.length" class="found-stores">
          <span class="found-label">
            <AppIcon name="store" :size="14" />
            Encontrado em {{ search.lojasEncontradas.value.length }}
            {{ search.lojasEncontradas.value.length === 1 ? 'loja' : 'lojas' }}:
          </span>
          <div class="found-row">
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

        <p v-if="search.erro.value" class="error-line" role="alert">{{ search.erro.value }}</p>

        <div v-if="search.resultados.value.length" class="products-grid-3 cat-stage" :class="{ loading: search.carregando.value }">
          <BlackCat
            v-if="sexta13.ativo.value && search.resultados.value.length > 3"
            top="calc(50% - 10px)"
            :duracao="30"
            @pegar="mostrarCupom = true"
          />
          <ProductCard
            v-for="prod in search.resultados.value"
            :key="prod.id"
            :produto="prod"
            @select="abrirDetalhe"
            @route="abrirRotaProduto"
          />
        </div>
        <div v-else-if="!search.carregando.value" class="empty-state">
          <AppIcon name="search-x" :size="32" />
          <strong>Nenhum produto encontrado</strong>
          <p>Tente outro termo, remova filtros ou navegue pelas lojas.</p>
          <div class="empty-actions">
            <button type="button" class="btn-cream btn-sm" @click="search.limpar()">Limpar filtros</button>
            <button type="button" class="btn-gold btn-sm" @click="screen = 'lojas'">Ver lojas</button>
          </div>
        </div>

        <button
          v-if="search.resultados.value.length > 1"
          type="button"
          class="btn-gold btn-lg full-width"
          @click="screen = 'compare'"
        >
          <AppIcon name="bar-chart" :size="18" />
          Comparar os {{ Math.min(search.resultados.value.length, 3) }} melhores preços
        </button>

        <div class="info-disclaimer-box">
          <AppIcon name="info" :size="18" />
          <div>
            <strong>Preços informados pelas próprias lojas</strong>
            <p>Confirme disponibilidade, tamanhos e condições na loja física.</p>
          </div>
        </div>
      </main>

      <!-- 4. COMPARAR OFERTAS -->
      <main v-else-if="screen === 'compare'" class="totem-content">
        <button type="button" class="btn-ghost btn-sm back-btn" @click="screen = 'busca'">
          <AppIcon name="arrow-left" :size="16" />
          Voltar aos resultados
        </button>

        <div class="mode-header">
          <h2>Compare e escolha seu caminho</h2>
          <p>Os menores preços da sua busca, lado a lado.</p>
        </div>

        <div class="compare-grid">
          <article
            v-for="(prod, idx) in produtosComparacao"
            :key="prod.id"
            class="compare-col-card"
            :class="{ highlight: idx === 0 }"
          >
            <span v-if="idx === 0" class="best-flag">
              <AppIcon name="check" :size="12" :stroke-width="3" />
              Melhor preço
            </span>
            <img :src="prod.imagem_url" alt="" class="compare-img" />
            <div class="compare-head">
              <p class="compare-store">{{ prod.loja?.nome }}</p>
              <h3 class="compare-prod-name">{{ prod.nome }}</h3>
            </div>

            <div class="compare-price-box">
              <strong class="compare-price num">{{ formatCurrency(prod.preco_final) }}</strong>
              <span v-if="prod.percentual_desconto > 0" class="badge badge-gold num">
                {{ prod.percentual_desconto }}% OFF
              </span>
              <span v-else class="badge badge-neutral">Preço normal</span>
            </div>

            <dl class="compare-meta-list">
              <div>
                <dt><AppIcon name="layers" :size="14" /> Piso</dt>
                <dd>{{ prod.loja?.pavimento }}</dd>
              </div>
              <div>
                <dt><AppIcon name="clock" :size="14" /> Distância</dt>
                <dd>{{ prod.tempo_estimado_min || 2 }} min a pé</dd>
              </div>
              <div>
                <dt><AppIcon name="refresh" :size="14" /> Preço</dt>
                <dd>{{ (prod.atualizado_formatado || '').replace('Atualizado ', '') }}</dd>
              </div>
            </dl>

            <div class="compare-actions">
              <button type="button" class="btn-gold full-width" @click="abrirRotaProduto(prod)">
                <AppIcon name="navigation" :size="16" />
                Como chegar
              </button>
              <button type="button" class="btn-cream full-width" @click="abrirDetalhe(prod)">
                Ver detalhes
              </button>
            </div>
          </article>
        </div>

        <button type="button" class="btn-cream btn-lg full-width" @click="screen = 'qr'">
          <AppIcon name="qr-code" :size="18" />
          Continuar no celular
        </button>
      </main>

      <!-- 5. DETALHES DO PRODUTO -->
      <main v-else-if="screen === 'detail' && selectedProduct" class="totem-content">
        <button type="button" class="btn-ghost btn-sm back-btn" @click="screen = voltarDoDetalhe">
          <AppIcon name="arrow-left" :size="16" />
          Voltar
        </button>

        <div class="detail-hero-card">
          <img :src="selectedProduct.imagem_url" alt="" class="detail-hero-img" />
          <span v-if="selectedProduct.percentual_desconto > 0" class="detail-discount-pill num">
            -{{ selectedProduct.percentual_desconto }}%
          </span>
        </div>

        <div class="detail-info-block">
          <div class="detail-tags">
            <span class="badge badge-neutral">{{ selectedProduct.categoria }}</span>
            <span class="badge badge-success">
              <AppIcon name="shield-check" :size="13" />
              Oferta verificada
            </span>
          </div>
          <h2 class="detail-prod-title">{{ selectedProduct.nome }}</h2>
          <p class="detail-prod-desc">{{ selectedProduct.descricao }}</p>

          <div class="detail-price-row">
            <strong class="detail-final-price num">
              {{ formatCurrency(selectedProduct.preco_final) }}
            </strong>
            <span v-if="selectedProduct.preco_promocional" class="detail-old-price num">
              {{ formatCurrency(selectedProduct.preco_original) }}
            </span>
          </div>

          <p class="detail-updated-stamp">
            <AppIcon name="check-circle" :size="14" />
            Preço informado pela loja · {{ selectedProduct.atualizado_formatado }}
            <span v-if="selectedProduct.validade_promocao"> · promoção até {{ selectedProduct.validade_promocao }}</span>
          </p>

          <button type="button" class="detail-store-box" @click="abrirPerfilLoja(selectedProduct.loja_id)">
            <span class="store-avatar" aria-hidden="true">
              <AppIcon :name="iconeCategoria(selectedProduct.loja?.categoria)" :size="20" />
            </span>
            <span class="detail-store-text">
              <strong>{{ selectedProduct.loja?.nome }}</strong>
              <span>
                {{ selectedProduct.loja?.pavimento }} · {{ selectedProduct.loja?.localizacao }}
              </span>
            </span>
            <span class="detail-store-cta">
              Ver loja
              <AppIcon name="chevron-right" :size="16" />
            </span>
          </button>
        </div>

        <div class="detail-actions">
          <button
            type="button"
            class="btn-gold btn-lg full-width"
            @click="abrirRotaProduto(selectedProduct)"
          >
            <AppIcon name="navigation" :size="18" />
            Como chegar
          </button>
          <button type="button" class="btn-cream btn-lg full-width" @click="screen = 'qr'">
            <AppIcon name="qr-code" :size="18" />
            Continuar no celular
          </button>
        </div>
      </main>

      <!-- 6. MAPA + ROTA -->
      <main v-else-if="screen === 'map'" class="totem-content">
        <div class="mode-header">
          <h2>Seu caminho, sem complicação.</h2>
          <p>Escolha a loja de destino e siga a rota a partir deste totem.</p>
        </div>

        <div class="map-store-selector" role="group" aria-label="Loja de destino">
          <button
            v-for="loja in lojas"
            :key="loja.id"
            type="button"
            class="chip"
            :class="{ active: selectedStore?.id === loja.id }"
            :aria-pressed="selectedStore?.id === loja.id"
            @click="abrirRotaLoja(loja)"
          >
            {{ loja.nome }}
            <span class="chip-meta">{{ loja.pavimento }}</span>
          </button>
        </div>

        <MappedinViewer
          :height="540"
          :totem-label="totemInfo.identificacao"
          :loja-destino="selectedStore"
          :rota="currentRoute"
          :produto-nome="selectedProduct?.loja_id === selectedStore?.id ? selectedProduct?.nome : ''"
        >
          <template #actions>
            <div class="map-actions">
              <button type="button" class="btn-gold btn-lg" @click="screen = 'qr'">
                <AppIcon name="qr-code" :size="18" />
                Levar rota no celular
              </button>
              <button
                v-if="selectedStore"
                type="button"
                class="btn-cream btn-lg"
                @click="abrirPerfilLoja(selectedStore.id)"
              >
                <AppIcon name="store" :size="18" />
                Ver perfil da loja
              </button>
            </div>
          </template>
        </MappedinViewer>
      </main>

      <!-- 7. QR CODE -->
      <main v-else-if="screen === 'qr'" class="totem-content">
        <QrCodeModal
          :totem-id="totemId"
          :search-query="search.filtros.q || ''"
          :produto="selectedProduct"
          :loja="selectedStore || selectedProduct?.loja"
          @close="screen = 'map'"
        />
      </main>

      <!-- 8. LOJAS (perfis) -->
      <main v-else-if="screen === 'lojas'" class="totem-content">
        <div class="mode-header">
          <h2>Lojas do Capim Dourado</h2>
          <p>Veja o perfil de cada loja: produtos atualizados, promoções e localização.</p>
        </div>

        <div class="search-field">
          <AppIcon name="search" :size="18" />
          <input v-model="buscaLoja" type="search" aria-label="Buscar loja" placeholder="Buscar loja pelo nome ou segmento" />
        </div>

        <div class="store-filters">
          <div class="cat-row" role="group" aria-label="Segmento da loja">
            <button type="button" class="chip" :class="{ active: !segmentoLoja }" @click="segmentoLoja = ''">
              Todos os segmentos
            </button>
            <button
              v-for="seg in segmentosLoja"
              :key="seg"
              type="button"
              class="chip"
              :class="{ active: segmentoLoja === seg }"
              @click="segmentoLoja = segmentoLoja === seg ? '' : seg"
            >
              <AppIcon :name="iconeCategoria(seg)" :size="14" />
              {{ seg }}
            </button>
          </div>
          <div class="cat-row" role="group" aria-label="Filtros de loja">
            <button
              v-for="p in ['', '1º Piso', '2º Piso']"
              :key="p"
              type="button"
              class="chip"
              :class="{ active: pisoLoja === p }"
              @click="pisoLoja = p"
            >
              <AppIcon name="layers" :size="14" />
              {{ p || 'Todos os pisos' }}
            </button>
            <button type="button" class="chip" :class="{ active: soPromocao }" @click="soPromocao = !soPromocao">
              <AppIcon name="percent" :size="14" />
              Com promoção
            </button>
          </div>
        </div>

        <p class="results-count num" aria-live="polite">{{ lojasFiltradas.length }} lojas</p>

        <div v-if="lojasFiltradas.length" class="stores-grid-2">
          <StoreCard v-for="loja in lojasFiltradas" :key="loja.id" :loja="loja" @open="abrirPerfilLoja(loja.id)" />
        </div>
        <div v-else class="empty-state">
          <AppIcon name="search-x" :size="32" />
          <strong>Nenhuma loja encontrada</strong>
        </div>
      </main>

      <!-- 9. PERFIL DA LOJA -->
      <main v-else-if="screen === 'loja' && lojaPerfilId" class="totem-content">
        <StoreProfile
          :loja-id="lojaPerfilId"
          :totem-id="totemId"
          :origem-nome="totemInfo.identificacao"
          :back-label="voltarDoPerfil === 'lojas' ? 'Todas as lojas' : 'Voltar'"
          @back="screen = voltarDoPerfil"
          @select="abrirDetalhe"
          @route="abrirRotaProduto"
        >
          <template #map-actions>
            <button type="button" class="btn-gold btn-lg full-width" @click="levarLojaNoCelular">
              <AppIcon name="qr-code" :size="18" />
              Levar rota no celular
            </button>
          </template>
        </StoreProfile>
      </main>

      <!-- 10. AJUDA -->
      <main v-else-if="screen === 'ajuda'" class="totem-content">
        <div class="mode-header">
          <h2>Como funciona o TemAqui?</h2>
          <p>Encontre produtos, compare preços e chegue rápido à loja física.</p>
        </div>
        <ol class="help-steps">
          <li class="help-step-card">
            <span class="step-icon"><AppIcon name="search" :size="22" /></span>
            <div>
              <span class="step-number">Passo 1</span>
              <strong>Encontre</strong>
              <p>Busque por produto, loja, orçamento (“tênis até R$ 350”) ou ocasião (“presente para mãe”).</p>
            </div>
          </li>
          <li class="help-step-card">
            <span class="step-icon"><AppIcon name="filter" :size="22" /></span>
            <div>
              <span class="step-number">Passo 2</span>
              <strong>Filtre e compare</strong>
              <p>Separe o que está em promoção do que está com preço normal, por categoria, piso e faixa de preço.</p>
            </div>
          </li>
          <li class="help-step-card">
            <span class="step-icon"><AppIcon name="store" :size="22" /></span>
            <div>
              <span class="step-number">Passo 3</span>
              <strong>Conheça a loja</strong>
              <p>Cada loja tem um perfil com todos os produtos atualizados, promoções e localização.</p>
            </div>
          </li>
          <li class="help-step-card">
            <span class="step-icon"><AppIcon name="navigation" :size="22" /></span>
            <div>
              <span class="step-number">Passo 4</span>
              <strong>Vá até a loja</strong>
              <p>Siga o mapa a partir deste totem ou leve a rota no celular pelo QR Code.</p>
            </div>
          </li>
        </ol>
      </main>

      <CouponModal
        v-if="mostrarCupom"
        modo="totem"
        :totem-id="totemId"
        @fechar="mostrarCupom = false"
      />

      <footer class="totem-footer">
        <span>Palmas, TO · Mapa e ofertas demonstrativas</span>
        <button type="button" class="chip" @click="screen = 'ajuda'">
          <AppIcon name="help-circle" :size="15" />
          Precisa de ajuda?
        </button>
      </footer>
    </template>
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
import CampaignBanner from '@/components/common/CampaignBanner.vue'
import QrCodeModal from '@/components/common/QrCodeModal.vue'
import SearchFilters from '@/components/common/SearchFilters.vue'
import StoreCard from '@/components/common/StoreCard.vue'
import StoreProfile from '@/components/common/StoreProfile.vue'
import BlackCat from '@/components/sexta13/BlackCat.vue'
import CouponModal from '@/components/sexta13/CouponModal.vue'
import SextaAviso from '@/components/sexta13/SextaAviso.vue'
import { useSexta13 } from '@/composables/useSexta13'

const route = useRoute()
const totemId = computed(() => Number(route.params.totemId || 1))

// 'welcome' | 'vitrine' | 'busca' | 'compare' | 'detail' | 'map' | 'qr' | 'lojas' | 'loja' | 'ajuda'
const screen = ref('welcome')
const termoInicio = ref('')
const erroApi = ref('')

const totemInfo = ref({
  id: 1,
  identificacao: 'Totem Piso 1',
  pavimento: '1º Piso',
  posicao_referencia: 'Entrada Principal'
})

const search = useProductSearch({ totemId })

// Easter egg sexta-feira 13
const sexta13 = useSexta13()
const mostrarCupom = ref(false)

function onLogoClick() {
  // O 1º toque volta ao início; 13 toques seguidos ligam/desligam o modo sexta-feira 13
  if (sexta13.registrarToqueLogo() === 1) screen.value = 'welcome'
}

const lojas = ref([])
const categorias = ref([])
const destaques = ref([])
const totalProdutos = ref(0)
const selectedProduct = ref(null)
const selectedStore = ref(null)
const currentRoute = ref(null)

const lojaPerfilId = ref(null)
const voltarDoPerfil = ref('lojas')
const voltarDoDetalhe = ref('busca')

// Filtros da aba Lojas
const buscaLoja = ref('')
const segmentoLoja = ref('')
const pisoLoja = ref('')
const soPromocao = ref(false)

const TELAS_BUSCA = ['busca', 'compare', 'detail']

const tabs = [
  {
    id: 'inicio',
    label: 'Início',
    icon: 'home',
    isActive: () => screen.value === 'vitrine',
    action: () => irParaVitrine()
  },
  {
    id: 'ofertas',
    label: 'Ofertas',
    icon: 'tag',
    isActive: () => TELAS_BUSCA.includes(screen.value),
    action: () => abrirOfertas()
  },
  {
    id: 'lojas',
    label: 'Lojas',
    icon: 'store',
    isActive: () => screen.value === 'lojas' || screen.value === 'loja',
    action: () => {
      screen.value = 'lojas'
    }
  },
  {
    id: 'mapa',
    label: 'Mapa',
    icon: 'map',
    isActive: () => screen.value === 'map' || screen.value === 'qr',
    action: () => abrirMapaGeral()
  },
  {
    id: 'ajuda',
    label: 'Ajuda',
    icon: 'help-circle',
    isActive: () => screen.value === 'ajuda',
    action: () => {
      screen.value = 'ajuda'
    }
  }
]

const lojasComPromocao = computed(() =>
  [...lojas.value].filter((l) => l.total_promocoes > 0).sort((a, b) => b.maior_desconto - a.maior_desconto)
)

const segmentosLoja = computed(() => [...new Set(lojas.value.map((l) => l.categoria))])

const lojasFiltradas = computed(() => {
  const termo = normalizar(buscaLoja.value.trim())
  return lojas.value.filter((l) => {
    if (segmentoLoja.value && l.categoria !== segmentoLoja.value) return false
    if (pisoLoja.value && l.pavimento !== pisoLoja.value) return false
    if (soPromocao.value && !l.total_promocoes) return false
    if (!termo) return true
    return normalizar(`${l.nome} ${l.categoria} ${l.descricao} ${l.categorias_produtos.join(' ')}`).includes(termo)
  })
})

const produtosComparacao = computed(() => {
  const base = search.resultados.value.length ? search.resultados.value : destaques.value
  return [...base].sort((a, b) => a.preco_final - b.preco_final).slice(0, 3)
})

const tituloBusca = computed(() => {
  const f = search.filtros
  const q = normalizar(f.q)
  if ((q.includes('tenis') || f.categoria === 'Calçados') && f.preco_max) {
    return { titulo: 'Seu tênis. Dentro do orçamento.', subtitulo: 'Compare ofertas das lojas participantes.' }
  }
  if (q.includes('presente')) {
    return {
      titulo: q.includes('mae') ? 'Um presente com a cara dela.' : 'Ideias de presente',
      subtitulo: 'Selecionamos sugestões de diferentes lojas para você.'
    }
  }
  if (f.q.trim()) return { titulo: `Resultados para “${f.q.trim()}”`, subtitulo: 'Produtos ativos cadastrados pelas lojas.' }
  if (f.categoria) return { titulo: f.categoria, subtitulo: 'Todos os produtos da categoria nas lojas do shopping.' }
  if (f.promocao === 'com') return { titulo: 'Ofertas em promoção', subtitulo: 'Descontos atualizados pelas próprias lojas.' }
  return { titulo: 'Todos os produtos', subtitulo: 'Filtre por promoção, categoria, piso e preço.' }
})

// Cada bloco carrega de forma independente: uma falha não esvazia a tela inteira
async function carregarDadosTotem(tentativa = 1) {
  const [tRes, lRes, cRes, dRes] = await Promise.allSettled([
    api.obterTotem(totemId.value),
    api.listarLojas({ totem_id: totemId.value }),
    api.listarCategorias(),
    api.listarProdutos({ ordenar_por: 'maior_desconto', totem_id: totemId.value })
  ])
  if (tRes.status === 'fulfilled') totemInfo.value = tRes.value
  if (lRes.status === 'fulfilled') lojas.value = lRes.value
  if (cRes.status === 'fulfilled') categorias.value = cRes.value
  if (dRes.status === 'fulfilled') {
    totalProdutos.value = dRes.value.length
    destaques.value = dRes.value.slice(0, 6)
    selectedProduct.value = dRes.value[0] || null
  }
  selectedStore.value = selectedProduct.value?.loja || lojas.value[0] || null

  const falha = [tRes, lRes, cRes, dRes].find((r) => r.status === 'rejected')
  erroApi.value = falha ? mensagemErroApi(falha.reason) : ''
  const falhou = !!falha
  if (falhou && tentativa < 3) setTimeout(() => carregarDadosTotem(tentativa + 1), 1500)
}

function irParaVitrine() {
  screen.value = 'vitrine'
  termoInicio.value = ''
}

function buscarTexto(texto) {
  search.aplicar({ q: texto || '' })
  screen.value = 'busca'
}

function abrirOfertas() {
  search.aplicar({ promocao: 'com', ordenar_por: 'maior_desconto' })
  screen.value = 'busca'
}

function aplicarBuscaOrcamento() {
  search.aplicar({ q: 'tênis', categoria: 'Calçados', preco_max: 350, ordenar_por: 'menor_preco' })
  screen.value = 'busca'
}

function aplicarBuscaOcasiao() {
  search.aplicar({ q: 'presente para minha mãe' })
  screen.value = 'busca'
}

function onCampaignAction(slide) {
  if (slide.filter?.preco_max) aplicarBuscaOrcamento()
  else if (slide.filter?.apenas_promocao) abrirOfertas()
  else aplicarBuscaOcasiao()
}

function abrirDetalhe(prod) {
  if (screen.value !== 'detail') voltarDoDetalhe.value = screen.value === 'loja' ? 'loja' : 'busca'
  selectedProduct.value = prod
  selectedStore.value = prod.loja
  screen.value = 'detail'
}

function abrirPerfilLoja(lojaId) {
  if (screen.value !== 'loja') voltarDoPerfil.value = screen.value === 'lojas' ? 'lojas' : screen.value
  lojaPerfilId.value = lojaId
  screen.value = 'loja'
}

async function abrirRotaProduto(prod) {
  selectedProduct.value = prod
  await abrirRotaLoja(prod.loja)
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

function levarLojaNoCelular() {
  selectedStore.value = lojas.value.find((l) => l.id === lojaPerfilId.value) || selectedStore.value
  screen.value = 'qr'
}

async function abrirMapaGeral() {
  if (!selectedStore.value && lojas.value.length) selectedStore.value = lojas.value[0]
  if (selectedStore.value) await abrirRotaLoja(selectedStore.value)
  else screen.value = 'map'
}

// Ao trocar de tela, volta ao topo (comportamento esperado em um totem)
watch(screen, () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
})

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

/* TOPO */
.totem-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 28px 16px;
  border-bottom: 1px solid var(--color-border);
}

.totem-brand {
  font-size: 24px;
  padding: 4px 0;
}

.totem-location-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 2px;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.totem-location-meta strong {
  color: var(--color-graphite);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.totem-location-meta span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

/* BOAS-VINDAS */
.welcome-screen {
  flex: 1;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 28px;
}

.hero-image-card {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  height: 420px;
  box-shadow: var(--shadow-lg);
}

.hero-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0) 55%, rgba(31, 31, 31, 0.45) 100%);
}

.hero-badge {
  position: absolute;
  left: 20px;
  bottom: 20px;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.95);
  color: var(--color-graphite);
  font-size: 13px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: var(--radius-pill);
  box-shadow: var(--shadow-md);
}

.hero-badge .app-icon {
  color: var(--color-gold-deep);
}

.welcome-copy {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.welcome-eyebrow {
  color: var(--color-gold-deep);
}

.welcome-title {
  font-size: 52px;
  font-weight: 800;
  line-height: 1.04;
  letter-spacing: -0.04em;
}

.welcome-lead {
  font-size: 22px;
  font-weight: 600;
  letter-spacing: -0.01em;
}

.welcome-desc {
  font-size: 17px;
  line-height: 1.5;
  color: var(--color-graphite-muted);
}

.welcome-features {
  list-style: none;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.welcome-features li {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
  border-radius: var(--radius-md);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  font-size: 13px;
  color: var(--color-graphite-muted);
  line-height: 1.4;
}

.welcome-features strong {
  display: block;
  font-size: 15px;
  color: var(--color-graphite);
}

.feature-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.welcome-cta-area {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.btn-totem-hero {
  width: 100%;
  min-height: 72px;
  font-size: 20px;
  font-weight: 700;
  border-radius: var(--radius-md);
  box-shadow: 0 10px 24px -8px rgba(201, 163, 74, 0.7);
}

.welcome-footnote {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-graphite-muted);
}

/* ABAS */
.totem-tabs {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  padding: 0 16px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-white);
  position: sticky;
  top: 0;
  z-index: 5;
}

.totem-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  font-size: 13px;
  font-weight: 500;
  color: var(--color-graphite-muted);
  padding: 12px 4px 10px;
  cursor: pointer;
  border-bottom: 3px solid transparent;
  margin-bottom: -1px;
  transition: color 0.15s var(--ease), border-color 0.15s var(--ease);
}

.totem-tab:hover {
  color: var(--color-graphite);
}

.totem-tab.active {
  color: var(--color-graphite);
  font-weight: 700;
  border-bottom-color: var(--color-gold);
}

.totem-tab.active .app-icon {
  color: var(--color-gold-deep);
}

.api-error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 16px 28px 0;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  background: var(--color-danger-bg);
  color: var(--color-danger-text);
  font-size: 14px;
  font-weight: 500;
}

.api-error-banner span {
  flex: 1;
}

/* CONTEÚDO */
.totem-content {
  flex: 1;
  padding: 24px 28px 32px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.block {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.back-btn {
  align-self: flex-start;
  margin-left: -10px;
  margin-bottom: -8px;
}

.totem-search {
  min-height: 56px;
  padding-left: 18px;
}

.totem-search input {
  font-size: 16px;
}

.quick-suggestions-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: -8px;
}

.sug-label {
  font-size: 13px;
  color: var(--color-graphite-muted);
  margin-right: 2px;
}

.category-icons-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
}

.cat-icon-btn {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 14px 4px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  transition: border-color 0.15s var(--ease), background-color 0.15s var(--ease), transform 0.15s var(--ease);
}

.cat-icon-btn:hover {
  border-color: var(--color-gold);
  background: var(--color-surface);
  transform: translateY(-1px);
}

.cat-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--color-cream);
  color: var(--color-graphite);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.cat-icon-btn:hover .cat-icon {
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
}

.cat-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-graphite);
}

.cat-count {
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.section-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.section-header-row h2 {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.products-grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  transition: opacity 0.15s var(--ease);
}

.cat-stage {
  position: relative;
}

.products-grid-3.loading {
  opacity: 0.55;
}

.stores-grid-2 {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.mode-header {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.mode-header h2 {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.025em;
  line-height: 1.15;
}

.mode-header p {
  font-size: 15px;
  color: var(--color-graphite-muted);
}

.results-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 15px;
  margin-bottom: -8px;
}

.results-toolbar strong {
  font-weight: 600;
}

.results-count {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-graphite-muted);
  margin-bottom: -8px;
}

.found-stores {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 12px 14px;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
}

.found-label {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-graphite-muted);
}

.found-row,
.cat-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.store-filters {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chip-meta {
  font-size: 12px;
  color: var(--color-graphite-muted);
  font-weight: 500;
}

.error-line {
  color: var(--color-danger-text);
  font-size: 14px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 6px;
  padding: 40px 20px;
  border: 1px dashed var(--color-border-strong);
  border-radius: var(--radius-md);
  color: var(--color-graphite-muted);
}

.empty-state strong {
  font-size: 17px;
  color: var(--color-graphite);
}

.empty-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.info-disclaimer-box {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 14px 16px;
  font-size: 13px;
  color: var(--color-graphite-muted);
}

.info-disclaimer-box strong {
  color: var(--color-graphite);
  font-weight: 600;
}

.info-disclaimer-box p {
  margin-top: 2px;
}

/* COMPARADOR */
.compare-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.compare-col-card {
  position: relative;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: var(--shadow-xs);
}

.compare-col-card.highlight {
  border-color: var(--color-gold);
  box-shadow: 0 0 0 1px var(--color-gold), var(--shadow-md);
}

.best-flag {
  position: absolute;
  top: -11px;
  left: 50%;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--color-gold);
  color: var(--color-graphite);
  font-size: 11px;
  font-weight: 700;
  padding: 3px 10px;
  border-radius: var(--radius-pill);
  white-space: nowrap;
}

.compare-img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 10px;
  background: var(--color-cream);
}

.compare-store {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-graphite-muted);
}

.compare-prod-name {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.3;
  margin-top: 2px;
}

.compare-price-box {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.compare-price {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.compare-meta-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 12px;
  padding: 10px 0;
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
}

.compare-meta-list div {
  display: flex;
  justify-content: space-between;
  gap: 6px;
}

.compare-meta-list dt {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  color: var(--color-graphite-muted);
}

.compare-meta-list dd {
  font-weight: 600;
  text-align: right;
}

.compare-actions {
  margin-top: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.compare-actions .btn-gold,
.compare-actions .btn-cream {
  padding-inline: 10px;
  font-size: 13px;
}

/* DETALHES */
.detail-hero-card {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
}

.detail-hero-img {
  width: 100%;
  height: 320px;
  object-fit: cover;
}

.detail-discount-pill {
  position: absolute;
  top: 16px;
  left: 16px;
  background: var(--color-graphite);
  color: var(--color-white);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 15px;
}

.detail-info-block {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.detail-tags {
  display: flex;
  gap: 6px;
}

.detail-prod-title {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.03em;
  line-height: 1.1;
}

.detail-prod-desc {
  font-size: 16px;
  color: var(--color-graphite-muted);
  line-height: 1.55;
}

.detail-price-row {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-top: 4px;
}

.detail-final-price {
  font-size: 40px;
  font-weight: 800;
  letter-spacing: -0.03em;
}

.detail-old-price {
  font-size: 18px;
  color: var(--color-graphite-muted);
  text-decoration: line-through;
}

.detail-updated-stamp {
  display: inline-flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px;
  font-size: 13px;
  color: var(--color-success-text);
}

.detail-store-box {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  text-align: left;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  padding: 14px 16px;
  border-radius: var(--radius-md);
  margin-top: 6px;
  cursor: pointer;
  transition: border-color 0.15s var(--ease);
}

.detail-store-box:hover {
  border-color: var(--color-gold);
}

.detail-store-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.detail-store-text strong {
  font-size: 16px;
  font-weight: 600;
}

.detail-store-text span {
  font-size: 13px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.detail-store-cta {
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-gold-deep);
}

.store-avatar {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: var(--color-graphite);
  color: var(--color-gold);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.detail-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

/* MAPA */
.map-store-selector {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding: 2px 2px 6px;
  scrollbar-width: thin;
}

.map-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

/* AJUDA */
.help-steps {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.help-step-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 18px;
}

.step-icon {
  width: 48px;
  height: 48px;
  border-radius: 14px;
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.step-number {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-gold-deep);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.help-step-card strong {
  display: block;
  font-size: 18px;
  font-weight: 700;
  margin-top: 2px;
}

.help-step-card p {
  font-size: 14px;
  color: var(--color-graphite-muted);
  line-height: 1.5;
  margin-top: 4px;
}

/* RODAPÉ */
.totem-footer {
  margin-top: auto;
  padding: 14px 28px;
  border-top: 1px solid var(--color-border);
  background: var(--color-surface);
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: var(--color-graphite-muted);
}
</style>
