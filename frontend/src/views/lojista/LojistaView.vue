<template>
  <div class="lojista-workspace">
    <!-- TELA DE LOGIN DO LOJISTA (Caso não autenticado) -->
    <div v-if="!token" class="login-container">
      <div class="login-card">
        <div class="brand-logo" style="font-size: 24px">
          <span class="brand-pin"></span>
          <span>TemAqui</span>
        </div>
        <span class="portal-tag">PORTAL DO LOJISTA • CAPIM DOURADO SHOPPING</span>
        <h1>Acesso da Loja</h1>
        <p class="login-sub">
          Gerencie preços, promoções e visibilidade dos produtos da sua loja no Totem e no Site Mobile (RN06 / RN08).
        </p>

        <form class="login-form" @submit.prevent="realizarLogin">
          <label>
            <span>E-mail corporativo da loja</span>
            <input v-model="loginEmail" type="email" required placeholder="admin@centauro.com.br" />
          </label>
          <label>
            <span>Senha</span>
            <input v-model="loginSenha" type="password" required placeholder="••••••" />
          </label>
          <p v-if="errorMsg" class="error-banner">{{ errorMsg }}</p>
          <button type="submit" class="btn-gold full-width">Entrar no Painel →</button>
        </form>

        <div class="demo-accounts-box">
          <strong>Acesso rápido de demonstração (RN08 — Isolamento por Loja):</strong>
          <div class="demo-btns">
            <button
              type="button"
              class="btn-cream btn-sm"
              @click="loginRapido('admin@centauro.com.br')"
            >
              Entrar como Centauro (1º Piso)
            </button>
            <button
              type="button"
              class="btn-cream btn-sm"
              @click="loginRapido('admin@riachuelo.com.br')"
            >
              Entrar como Riachuelo (1º Piso)
            </button>
            <button
              type="button"
              class="btn-cream btn-sm"
              @click="loginRapido('admin@lojaesporte.com.br')"
            >
              Entrar como Loja Esporte (2º Piso)
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- PAINEL ADMINISTRATIVO DO LOJISTA (1440 x 900 — Fiel ao Print 04) -->
    <template v-else>
      <!-- Sidebar Esquerda -->
      <aside class="lojista-sidebar">
        <div class="sidebar-top">
          <div class="brand-logo" style="font-size: 20px">
            <span class="brand-pin"></span>
            <span>TemAqui</span>
          </div>
          <span class="sidebar-eyebrow">PORTAL DO LOJISTA</span>

          <!-- Card da Loja Vinculada (RN08) -->
          <div class="store-identity-box">
            <strong>{{ dashboard.loja?.nome || 'Centauro' }}</strong>
            <span>{{ dashboard.loja?.localizacao || '1º Pavimento • Loja 104' }}</span>
          </div>

          <nav class="sidebar-nav">
            <button
              type="button"
              class="side-nav-btn"
              :class="{ active: mode === 'list' || mode === 'edit' || mode === 'create' }"
              @click="mode = 'list'"
            >
              Meus Produtos
            </button>
            <button
              type="button"
              class="side-nav-btn"
              :class="{ active: filterOnlyPromos }"
              @click="toggleFiltroPromos()"
            >
              Promoções Ativas
            </button>
            <button
              type="button"
              class="side-nav-btn"
              @click="mode = 'list'"
            >
              Desempenho no Totem
            </button>
          </nav>
        </div>

        <div class="sidebar-footer">
          <span class="sync-status">● Sincronizado com o TemAqui</span>
          <p class="mall-foot">Capim Dourado Shopping<br />Palmas, Tocantins</p>
          <button type="button" class="logout-btn" @click="sair()">Trocar de loja / Sair</button>
        </div>
      </aside>

      <!-- Área Principal de Conteúdo -->
      <div class="lojista-main">
        <!-- Topbar -->
        <header class="lojista-topbar">
          <span class="breadcrumb">
            Área da loja /
            <strong>
              {{
                mode === 'edit'
                  ? 'Editar preço'
                  : mode === 'create'
                    ? 'Cadastrar novo produto'
                    : 'Meus produtos'
              }}
            </strong>
          </span>
          <div class="lojista-user-tag">
            <strong>{{ dashboard.lojista?.nome || 'Centauro • Administrador' }}</strong>
          </div>
        </header>

        <!-- MODO 1: VISÃO GERAL • MEUS PRODUTOS (Frames 1 e 4 do Print 04) -->
        <section v-if="mode === 'list'" class="lojista-body">
          <!-- Banner de confirmação após salvar (Frame 4 do Print 04) -->
          <div v-if="publishedBanner" class="published-alert-banner">
            <div>
              <strong>✓ Alterações publicadas no Totem e Site</strong>
              <p>Seus produtos já podem ser encontrados pelos consumidores. Simulação do protótipo.</p>
            </div>
            <button type="button" class="close-alert" @click="publishedBanner = false">✕</button>
          </div>

          <div class="page-title-block">
            <h1>Meus produtos</h1>
            <p>Gerencie os achados que levam mais pessoas até sua loja.</p>
          </div>

          <!-- 3 KPIs do Topo (24 | 8 | 1.284 / 186 conforme Print 04) -->
          <div class="kpi-grid">
            <div class="kpi-card">
              <span class="kpi-label">Produtos ativos no totem</span>
              <strong class="kpi-value">{{ dashboard.kpis?.produtos_ativos_display ?? 24 }}</strong>
              <span class="kpi-sub">+3 novidades nesta semana</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Promoções em destaque</span>
              <strong class="kpi-value">{{ dashboard.kpis?.promocoes_destaque_display ?? 8 }}</strong>
              <span class="kpi-sub">Todas com preço atualizado</span>
            </div>
            <div class="kpi-card">
              <span class="kpi-label">Visualizações / rotas geradas</span>
              <strong class="kpi-value">
                {{
                  (dashboard.kpis?.visualizacoes_7d || 1284).toLocaleString('pt-BR')
                }}
                / {{ dashboard.kpis?.rotas_geradas_7d || 186 }}
              </strong>
              <span class="kpi-sub">Últimos 7 dias • dados demonstrativos</span>
            </div>
          </div>

          <!-- Barra de Ação da Tabela -->
          <div class="table-header-bar">
            <h2>Produtos cadastrados</h2>
            <button type="button" class="btn-gold" @click="abrirModalCadastro()">
              + Cadastrar novo produto
            </button>
          </div>

          <!-- Tabela de Produtos da Loja -->
          <div class="products-table-card">
            <table class="lojista-table">
              <thead>
                <tr>
                  <th>PRODUTO</th>
                  <th>PREÇO / PROMO</th>
                  <th>STATUS</th>
                  <th>ATUALIZAÇÃO</th>
                  <th>AÇÕES</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="prod in produtosExibidos" :key="prod.id">
                  <td>
                    <div class="prod-cell">
                      <img :src="prod.imagem_url" :alt="prod.nome" class="prod-cell-img" />
                      <div>
                        <strong class="prod-cell-name">{{ prod.nome }}</strong>
                        <p class="prod-cell-cat">{{ prod.categoria }} • Corrida, passeio, esporte</p>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div v-if="prod.preco_promocional" class="price-cell">
                      <span class="old-p">{{ formatCurrency(prod.preco_original) }}</span>
                      <strong class="curr-p">{{ formatCurrency(prod.preco_final) }}</strong>
                    </div>
                    <div v-else class="price-cell">
                      <span class="old-p">{{ formatCurrency(prod.preco_original) }}</span>
                      <strong class="curr-p">Sem promoção</strong>
                    </div>
                  </td>
                  <td>
                    <span
                      class="status-pill"
                      :class="prod.ativo ? 'status-active' : 'status-paused'"
                    >
                      {{ prod.ativo ? 'Ativo no Totem' : 'Pausado' }}
                    </span>
                  </td>
                  <td class="date-cell">
                    13/11/2026<br />
                    {{ prod.atualizado_formatado.replace('Atualizado hoje, ', '') }}
                  </td>
                  <td>
                    <div class="actions-cell">
                      <button type="button" class="table-action-link" @click="abrirEdicao(prod)">
                        Editar Preço
                      </button>
                      <button
                        type="button"
                        class="table-action-link"
                        @click="alternarStatus(prod)"
                      >
                        {{ prod.ativo ? 'Pausar exibição' : 'Ativar Promoção' }}
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <div class="table-footer">
              <span>
                Exibindo {{ produtosExibidos.length }} de
                {{ dashboard.kpis?.produtos_ativos_display || produtosExibidos.length }} produtos
              </span>
              <span class="pagination">‹ 1 2 3 ›</span>
            </div>
          </div>
        </section>

        <!-- MODO 2: EDITAR PREÇO (Frame 2 do Print 04) -->
        <section v-else-if="mode === 'edit' && editingProduct" class="lojista-body">
          <div class="page-title-block">
            <h1>Editar preço</h1>
            <p>Atualize o preço com transparência para quem está procurando.</p>
          </div>

          <div class="editor-card">
            <div class="editor-product-summary">
              <img
                :src="editingProduct.imagem_url"
                :alt="editingProduct.nome"
                class="editor-thumb"
              />
              <div>
                <h2>{{ editingProduct.nome }}</h2>
                <p class="editor-meta">
                  {{ editingProduct.categoria }} • SKU TDV-{{ 100 + editingProduct.id }} •
                  {{ editingProduct.ativo ? 'Ativo no Totem' : 'Pausado' }}
                </p>
                <p class="editor-meta">
                  Última atualização: 13/11/2026 às 10:42
                </p>
              </div>
            </div>

            <div class="editor-fields-grid">
              <label class="editor-field">
                <span>Preço original (R$)</span>
                <input v-model.number="formPrecoOriginal" type="number" step="0.10" min="1" />
              </label>
              <label class="editor-field">
                <span>Preço promocional (R$)</span>
                <input
                  v-model.number="formPrecoPromocional"
                  type="number"
                  step="0.10"
                  min="0"
                  placeholder="Deixe vazio para sem promoção"
                />
              </label>
            </div>

            <p v-if="descontoCalculado > 0" class="discount-preview-line">
              {{ descontoCalculado }}% de desconto • Promoção ativa até 20/11/2026
            </p>
            <p class="editor-disclaimer">
              O novo preço será publicado no totem e no site.<br />
              Valores preenchidos apenas para demonstração do protótipo (RN06 / RN07).
            </p>

            <div class="editor-actions">
              <button type="button" class="btn-cream" @click="mode = 'list'">
                Cancelar
              </button>
              <button type="button" class="btn-gold" @click="salvarEdicaoPreco()">
                Salvar alterações
              </button>
            </div>
          </div>
        </section>

        <!-- MODO 3: CADASTRAR NOVO PRODUTO (Frame 3 do Print 04) -->
        <section v-else-if="mode === 'create'" class="lojista-body">
          <div class="page-title-block">
            <h1>Cadastrar novo produto</h1>
            <p>Preencha os dados da oferta para publicação imediata no Totem e Site Mobile.</p>
          </div>

          <form class="editor-card" @submit.prevent="salvarNovoProduto">
            <div class="editor-fields-grid">
              <label class="editor-field">
                <span>Nome do produto</span>
                <input
                  v-model="novoForm.nome"
                  type="text"
                  required
                  placeholder="Ex: Tênis Run Pro Max"
                />
              </label>
              <label class="editor-field">
                <span>Categoria</span>
                <select v-model="novoForm.categoria">
                  <option value="Calçados">Calçados</option>
                  <option value="Moda">Moda</option>
                  <option value="Perfumaria">Perfumaria</option>
                  <option value="Acessórios">Acessórios</option>
                </select>
              </label>
              <label class="editor-field">
                <span>Preço original (R$)</span>
                <input
                  v-model.number="novoForm.preco"
                  type="number"
                  step="0.10"
                  min="1"
                  required
                />
              </label>
              <label class="editor-field">
                <span>Preço promocional (R$) — Opcional</span>
                <input
                  v-model.number="novoForm.preco_promocional"
                  type="number"
                  step="0.10"
                  min="0"
                />
              </label>
            </div>

            <label class="editor-field">
              <span>Descrição curta (tamanhos, cores e condições na loja física)</span>
              <input
                v-model="novoForm.descricao"
                type="text"
                placeholder="Leveza, conforto e amortecimento. Consulte tamanhos na loja."
              />
            </label>

            <div class="editor-actions">
              <button type="button" class="btn-cream" @click="mode = 'list'">
                Cancelar
              </button>
              <button type="submit" class="btn-gold">
                Publicar no Totem e Site
              </button>
            </div>
          </form>
        </section>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { api, formatCurrency } from '@/services/api'

const token = ref(localStorage.getItem('temaqui_lojista_token') || '')
const loginEmail = ref('admin@centauro.com.br')
const loginSenha = ref('123456')
const errorMsg = ref('')

const mode = ref('list') // 'list' | 'edit' | 'create'
const filterOnlyPromos = ref(false)
const publishedBanner = ref(false)

const dashboard = ref({
  loja: null,
  lojista: null,
  kpis: {},
  produtos: []
})

const editingProduct = ref(null)
const formPrecoOriginal = ref(399.9)
const formPrecoPromocional = ref(299.9)

const novoForm = ref({
  nome: '',
  categoria: 'Calçados',
  preco: 349.9,
  preco_promocional: 279.9,
  descricao: 'Leveza, conforto e amortecimento para acompanhar sua rotina.',
  imagem_url: '/assets/products/tenis-sprint.svg'
})

const produtosExibidos = computed(() => {
  const lista = dashboard.value.produtos || []
  if (filterOnlyPromos.value) {
    return lista.filter((p) => p.percentual_desconto > 0)
  }
  return lista
})

const descontoCalculado = computed(() => {
  if (
    !formPrecoOriginal.value ||
    !formPrecoPromocional.value ||
    formPrecoPromocional.value >= formPrecoOriginal.value
  ) {
    return 0
  }
  return Math.round(
    ((formPrecoOriginal.value - formPrecoPromocional.value) / formPrecoOriginal.value) * 100
  )
})

async function realizarLogin() {
  errorMsg.value = ''
  try {
    const resp = await api.loginLojista(loginEmail.value, loginSenha.value)
    token.value = resp.access_token
    localStorage.setItem('temaqui_lojista_token', resp.access_token)
    await carregarDashboard()
  } catch (err) {
    errorMsg.value = err.message || 'Falha no login'
  }
}

async function loginRapido(email) {
  loginEmail.value = email
  loginSenha.value = '123456'
  await realizarLogin()
}

async function carregarDashboard() {
  if (!token.value) return
  try {
    dashboard.value = await api.obterDashboardLojista(token.value)
  } catch {
    token.value = ''
    localStorage.removeItem('temaqui_lojista_token')
  }
}

function toggleFiltroPromos() {
  mode.value = 'list'
  filterOnlyPromos.value = !filterOnlyPromos.value
}

function abrirEdicao(prod) {
  editingProduct.value = prod
  formPrecoOriginal.value = prod.preco_original
  formPrecoPromocional.value = prod.preco_promocional || prod.preco_final
  mode.value = 'edit'
}

async function salvarEdicaoPreco() {
  if (!editingProduct.value) return
  try {
    await api.atualizarProduto(token.value, editingProduct.value.id, {
      preco: Number(formPrecoOriginal.value),
      preco_promocional: formPrecoPromocional.value ? Number(formPrecoPromocional.value) : null,
      remover_promocao: !formPrecoPromocional.value
    })
    await carregarDashboard()
    mode.value = 'list'
    publishedBanner.value = true
  } catch (err) {
    alert(err.message)
  }
}

function abrirModalCadastro() {
  novoForm.value = {
    nome: '',
    categoria: 'Calçados',
    preco: 349.9,
    preco_promocional: 279.9,
    descricao: 'Leveza, conforto e amortecimento para acompanhar sua rotina.',
    imagem_url: '/assets/products/tenis-sprint.svg'
  }
  mode.value = 'create'
}

async function salvarNovoProduto() {
  try {
    await api.cadastrarProduto(token.value, {
      ...novoForm.value,
      ativo: true
    })
    await carregarDashboard()
    mode.value = 'list'
    publishedBanner.value = true
  } catch (err) {
    alert(err.message)
  }
}

async function alternarStatus(prod) {
  try {
    await api.alternarStatusProduto(token.value, prod.id, !prod.ativo)
    await carregarDashboard()
    publishedBanner.value = true
  } catch (err) {
    alert(err.message)
  }
}

function sair() {
  token.value = ''
  localStorage.removeItem('temaqui_lojista_token')
}

onMounted(async () => {
  if (!token.value) {
    // Auto-autentica na conta demo Centauro na primeira abertura para exibir imediatamente o Print 04
    await loginRapido('admin@centauro.com.br')
  } else {
    await carregarDashboard()
  }
})
</script>

<style scoped>
.lojista-workspace {
  display: flex;
  width: 100%;
  min-height: 100%;
}

/* LOGIN */
.login-container {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px;
  background: var(--color-cream);
}

.login-card {
  width: 100%;
  max-width: 480px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.portal-tag {
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: var(--color-graphite-muted);
}

.login-sub {
  font-size: 13px;
  color: var(--color-graphite-muted);
  line-height: 1.45;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 6px;
}

.login-form label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 12px;
  font-weight: 700;
}

.login-form input {
  padding: 12px 14px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: var(--color-cream);
  font-size: 14px;
}

.error-banner {
  color: #A61B1B;
  font-size: 12px;
  font-weight: 700;
}

.demo-accounts-box {
  margin-top: 8px;
  padding-top: 14px;
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 12px;
}

.demo-btns {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* SIDEBAR DO LOJISTA */
.lojista-sidebar {
  width: 260px;
  background: var(--color-white);
  border-right: 1px solid var(--color-border);
  padding: 26px 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-shrink: 0;
}

.sidebar-top {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.sidebar-eyebrow {
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: var(--color-graphite-muted);
}

.store-identity-box {
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.store-identity-box strong {
  font-size: 15px;
}

.store-identity-box span {
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.side-nav-btn {
  text-align: left;
  padding: 11px 14px;
  border-radius: 10px;
  border: none;
  background: transparent;
  font-size: 13px;
  font-weight: 600;
  color: var(--color-graphite-muted);
  cursor: pointer;
}

.side-nav-btn.active {
  background: var(--color-cream);
  color: var(--color-graphite);
  font-weight: 800;
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.sync-status {
  color: var(--color-graphite);
  font-weight: 700;
}

.logout-btn {
  margin-top: 6px;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
}

/* ÁREA PRINCIPAL */
.lojista-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #FAF8F3;
}

.lojista-topbar {
  padding: 18px 34px;
  background: var(--color-white);
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.lojista-user-tag strong {
  color: var(--color-graphite);
}

.lojista-body {
  padding: 28px 34px;
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.published-alert-banner {
  background: var(--color-success-bg);
  border: 1px solid #B7DEC5;
  color: var(--color-success-text);
  border-radius: 14px;
  padding: 16px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.published-alert-banner strong {
  font-size: 16px;
}

.published-alert-banner p {
  font-size: 12px;
  margin-top: 2px;
}

.close-alert {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: var(--color-success-text);
}

.page-title-block h1 {
  font-size: 28px;
  font-weight: 800;
}

.page-title-block p {
  font-size: 13px;
  color: var(--color-graphite-muted);
  margin-top: 4px;
}

.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.kpi-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: 14px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.kpi-label {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.kpi-value {
  font-size: 28px;
  font-weight: 800;
  color: var(--color-graphite);
}

.kpi-sub {
  font-size: 11px;
  color: var(--color-graphite-muted);
}

.table-header-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-header-bar h2 {
  font-size: 18px;
  font-weight: 800;
}

.products-table-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  overflow: hidden;
}

.lojista-table {
  width: 100%;
  border-collapse: collapse;
}

.lojista-table thead tr {
  background: var(--color-cream);
  text-align: left;
  font-size: 11px;
  font-weight: 800;
  color: var(--color-graphite-muted);
  letter-spacing: 0.05em;
}

.lojista-table th,
.lojista-table td {
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
}

.prod-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.prod-cell-img {
  width: 56px;
  height: 56px;
  border-radius: 10px;
  object-fit: cover;
  background: var(--color-cream);
}

.prod-cell-name {
  font-size: 14px;
  font-weight: 800;
}

.prod-cell-cat {
  font-size: 12px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.price-cell {
  display: flex;
  flex-direction: column;
}

.old-p {
  font-size: 11px;
  color: var(--color-graphite-muted);
  text-decoration: line-through;
}

.curr-p {
  font-size: 15px;
  font-weight: 800;
}

.status-pill {
  display: inline-block;
  padding: 5px 12px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
}

.status-active {
  background: var(--color-success-bg);
  color: var(--color-success-text);
}

.status-paused {
  background: var(--color-cream);
  color: var(--color-graphite-muted);
}

.date-cell {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.actions-cell {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.table-action-link {
  background: none;
  border: none;
  font-size: 12px;
  font-weight: 700;
  color: var(--color-graphite);
  cursor: pointer;
}

.table-action-link:hover {
  text-decoration: underline;
}

.table-footer {
  padding: 14px 20px;
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

/* EDITOR DE PREÇO / CADASTRO */
.editor-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: 18px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  max-width: 820px;
}

.editor-product-summary {
  display: flex;
  align-items: center;
  gap: 20px;
}

.editor-thumb {
  width: 110px;
  height: 110px;
  border-radius: 14px;
  object-fit: cover;
  background: var(--color-cream);
}

.editor-product-summary h2 {
  font-size: 22px;
  font-weight: 800;
}

.editor-meta {
  font-size: 12px;
  color: var(--color-graphite-muted);
  margin-top: 4px;
}

.editor-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.editor-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 12px;
  font-weight: 700;
}

.editor-field input,
.editor-field select {
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid var(--color-border);
  background: var(--color-cream);
  font-size: 15px;
  font-weight: 600;
}

.discount-preview-line {
  font-size: 14px;
  font-weight: 800;
  color: var(--color-graphite);
}

.editor-disclaimer {
  font-size: 12px;
  color: var(--color-graphite-muted);
  line-height: 1.45;
}

.editor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.full-width {
  width: 100%;
}
</style>
