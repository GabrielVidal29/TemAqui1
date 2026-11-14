<template>
  <div class="lojista-workspace">
    <!-- TELA DE LOGIN DO LOJISTA (Caso não autenticado) -->
    <main v-if="!token" class="login-container">
      <div class="login-card">
        <div class="brand-logo login-brand">
          <span class="brand-pin"></span>
          <span>TemAqui</span>
        </div>
        <div class="login-heading">
          <span class="eyebrow">Portal do Lojista · Capim Dourado Shopping</span>
          <h1>Acesse sua loja</h1>
          <p class="login-sub">
            Gerencie preços, promoções e a visibilidade dos seus produtos no totem e no site.
          </p>
        </div>

        <form class="login-form" @submit.prevent="realizarLogin">
          <label class="form-field">
            <span>E-mail corporativo da loja</span>
            <input
              v-model="loginEmail"
              type="email"
              required
              autocomplete="username"
              placeholder="admin@centauro.com.br"
            />
          </label>
          <label class="form-field">
            <span>Senha</span>
            <input
              v-model="loginSenha"
              type="password"
              required
              autocomplete="current-password"
              placeholder="••••••"
            />
          </label>
          <p v-if="errorMsg" class="error-banner" role="alert">
            <AppIcon name="info" :size="16" />
            {{ errorMsg }}
          </p>
          <button type="submit" class="btn-gold btn-lg full-width">
            Entrar no painel
            <AppIcon name="arrow-right" :size="18" />
          </button>
        </form>

        <div class="demo-accounts-box">
          <span class="demo-divider"><span>Contas de demonstração</span></span>
          <div class="demo-btns">
            <button
              v-for="conta in contasDemo"
              :key="conta.email"
              type="button"
              class="demo-account-btn"
              @click="loginRapido(conta.email)"
            >
              <span class="demo-avatar" aria-hidden="true">{{ conta.nome.charAt(0) }}</span>
              <span class="demo-info">
                <strong>{{ conta.nome }}</strong>
                <span>{{ conta.piso }}</span>
              </span>
              <AppIcon name="chevron-right" :size="16" />
            </button>
          </div>
        </div>
      </div>
    </main>

    <!-- PAINEL ADMINISTRATIVO DO LOJISTA -->
    <template v-else>
      <!-- Sidebar Esquerda -->
      <aside class="lojista-sidebar">
        <div class="sidebar-top">
          <div class="sidebar-brand">
            <div class="brand-logo sidebar-logo">
              <span class="brand-pin"></span>
              <span>TemAqui</span>
            </div>
            <span class="eyebrow">Portal do Lojista</span>
          </div>

          <!-- Card da Loja Vinculada (RN08) -->
          <div class="store-identity-box">
            <span class="store-identity-avatar" aria-hidden="true">
              {{ (dashboard.loja?.nome || 'Centauro').charAt(0) }}
            </span>
            <div>
              <strong>{{ dashboard.loja?.nome || 'Centauro' }}</strong>
              <span>{{ dashboard.loja?.localizacao || '1º Pavimento · Loja 104' }}</span>
            </div>
          </div>

          <nav class="sidebar-nav" aria-label="Menu do lojista">
            <button
              type="button"
              class="side-nav-btn"
              :class="{ active: !filterOnlyPromos }"
              :aria-current="!filterOnlyPromos ? 'page' : undefined"
              @click="mostrarTodos()"
            >
              <AppIcon name="package" :size="18" />
              Meus produtos
            </button>
            <button
              type="button"
              class="side-nav-btn"
              :class="{ active: filterOnlyPromos }"
              :aria-current="filterOnlyPromos ? 'page' : undefined"
              @click="toggleFiltroPromos()"
            >
              <AppIcon name="percent" :size="18" />
              Promoções ativas
            </button>
            <button type="button" class="side-nav-btn" @click="mode = 'list'">
              <AppIcon name="bar-chart" :size="18" />
              Desempenho no totem
            </button>
          </nav>
        </div>

        <div class="sidebar-footer">
          <span class="sync-status">
            <span class="sync-dot" aria-hidden="true"></span>
            Sincronizado com o TemAqui
          </span>
          <p class="mall-foot">Capim Dourado Shopping · Palmas, TO</p>
          <button type="button" class="btn-cream btn-sm full-width" @click="sair()">
            <AppIcon name="log-out" :size="16" />
            Trocar de loja / Sair
          </button>
        </div>
      </aside>

      <!-- Área Principal de Conteúdo -->
      <main class="lojista-main">
        <!-- Topbar -->
        <header class="lojista-topbar">
          <nav class="breadcrumb" aria-label="Você está em">
            <span>Área da loja</span>
            <AppIcon name="chevron-right" :size="14" />
            <strong>
              {{
                mode === 'edit'
                  ? 'Editar preço'
                  : mode === 'create'
                    ? 'Cadastrar novo produto'
                    : 'Meus produtos'
              }}
            </strong>
          </nav>
          <div class="lojista-user-tag">
            <span class="user-avatar" aria-hidden="true"><AppIcon name="user" :size="16" /></span>
            <strong>{{ dashboard.lojista?.nome || 'Centauro · Administrador' }}</strong>
          </div>
        </header>

        <!-- Aviso de erro das ações (substitui alert()) -->
        <div v-if="actionError" class="action-error-banner" role="alert">
          <AppIcon name="info" :size="18" />
          <span>{{ actionError }}</span>
          <button type="button" class="icon-btn" aria-label="Fechar aviso" @click="actionError = ''">
            <AppIcon name="x" :size="16" />
          </button>
        </div>

        <!-- MODO 1: VISÃO GERAL • MEUS PRODUTOS -->
        <section v-if="mode === 'list'" class="lojista-body">
          <!-- Banner de confirmação após salvar -->
          <div v-if="publishedBanner" class="published-alert-banner" role="status">
            <span class="published-icon"><AppIcon name="check" :size="16" :stroke-width="2.6" /></span>
            <div>
              <strong>Alterações publicadas no totem e no site</strong>
              <p>Seus produtos já podem ser encontrados pelos consumidores. Simulação do protótipo.</p>
            </div>
            <button
              type="button"
              class="icon-btn"
              aria-label="Fechar aviso"
              @click="publishedBanner = false"
            >
              <AppIcon name="x" :size="16" />
            </button>
          </div>

          <div class="page-title-row">
            <div class="page-title-block">
              <h1>{{ filterOnlyPromos ? 'Promoções ativas' : 'Meus produtos' }}</h1>
              <p>Gerencie os achados que levam mais pessoas até sua loja.</p>
            </div>
            <button type="button" class="btn-gold" @click="abrirModalCadastro()">
              <AppIcon name="plus" :size="18" />
              Cadastrar produto
            </button>
          </div>

          <!-- KPIs do Topo -->
          <div class="kpi-grid">
            <div class="kpi-card">
              <div class="kpi-head">
                <span class="kpi-label">Produtos ativos no totem</span>
                <span class="kpi-icon"><AppIcon name="package" :size="18" /></span>
              </div>
              <strong class="kpi-value num">{{ dashboard.kpis?.produtos_ativos_display ?? 24 }}</strong>
              <span class="kpi-sub positive">
                <AppIcon name="trending-up" :size="14" />
                +3 novidades nesta semana
              </span>
            </div>
            <div class="kpi-card">
              <div class="kpi-head">
                <span class="kpi-label">Promoções em destaque</span>
                <span class="kpi-icon"><AppIcon name="percent" :size="18" /></span>
              </div>
              <strong class="kpi-value num">{{ dashboard.kpis?.promocoes_destaque_display ?? 8 }}</strong>
              <span class="kpi-sub">
                <AppIcon name="check-circle" :size="14" />
                Todas com preço atualizado
              </span>
            </div>
            <div class="kpi-card">
              <div class="kpi-head">
                <span class="kpi-label">Visualizações / rotas geradas</span>
                <span class="kpi-icon"><AppIcon name="eye" :size="18" /></span>
              </div>
              <strong class="kpi-value num">
                {{ (dashboard.kpis?.visualizacoes_7d || 1284).toLocaleString('pt-BR') }}
                <span class="kpi-divider">/</span>
                {{ dashboard.kpis?.rotas_geradas_7d || 186 }}
              </strong>
              <span class="kpi-sub">Últimos 7 dias · dados demonstrativos</span>
            </div>
          </div>

          <!-- Tabela de Produtos da Loja -->
          <div class="products-table-card">
            <div class="table-header-bar">
              <h2>Produtos cadastrados</h2>
              <span class="badge badge-neutral num">{{ produtosExibidos.length }} itens</span>
            </div>

            <table class="lojista-table">
              <thead>
                <tr>
                  <th scope="col">Produto</th>
                  <th scope="col">Preço</th>
                  <th scope="col">Status</th>
                  <th scope="col">Atualização</th>
                  <th scope="col" class="th-actions">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="prod in produtosExibidos" :key="prod.id">
                  <td>
                    <div class="prod-cell">
                      <img :src="prod.imagem_url" alt="" class="prod-cell-img" />
                      <div>
                        <strong class="prod-cell-name">{{ prod.nome }}</strong>
                        <p class="prod-cell-cat">{{ prod.categoria }} · {{ resumo(prod.descricao) }}</p>
                      </div>
                    </div>
                  </td>
                  <td>
                    <div class="price-cell num">
                      <template v-if="prod.preco_promocional">
                        <strong class="curr-p">{{ formatCurrency(prod.preco_final) }}</strong>
                        <span class="old-p">{{ formatCurrency(prod.preco_original) }}</span>
                      </template>
                      <template v-else>
                        <strong class="curr-p">{{ formatCurrency(prod.preco_original) }}</strong>
                        <span class="no-promo">Sem promoção</span>
                      </template>
                    </div>
                  </td>
                  <td>
                    <span class="badge" :class="prod.ativo ? 'badge-success' : 'badge-neutral'">
                      <span class="status-dot" aria-hidden="true"></span>
                      {{ prod.ativo ? 'Ativo no totem' : 'Pausado' }}
                    </span>
                  </td>
                  <td class="date-cell num">
                    {{ dataBR(prod.atualizado_em) }}
                    <span>{{ horaBR(prod.atualizado_em) }}</span>
                  </td>
                  <td>
                    <div class="actions-cell">
                      <button type="button" class="btn-cream btn-sm" @click="abrirEdicao(prod)">
                        <AppIcon name="pencil" :size="14" />
                        Editar preço
                      </button>
                      <button
                        type="button"
                        class="btn-ghost btn-sm"
                        @click="alternarStatus(prod)"
                      >
                        <AppIcon :name="prod.ativo ? 'pause' : 'play'" :size="14" />
                        {{ prod.ativo ? 'Pausar' : 'Ativar' }}
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>

            <div class="table-footer">
              <span class="num">
                Exibindo {{ produtosExibidos.length }} de
                {{ (dashboard.produtos || []).length }} produtos cadastrados
              </span>
              <span class="num">
                {{ (dashboard.produtos || []).filter((p) => !p.ativo).length }} pausados
              </span>
            </div>
          </div>
        </section>

        <!-- MODO 2: EDITAR PREÇO -->
        <section v-else-if="mode === 'edit' && editingProduct" class="lojista-body">
          <button type="button" class="btn-ghost btn-sm back-btn" @click="mode = 'list'">
            <AppIcon name="arrow-left" :size="16" />
            Voltar aos produtos
          </button>

          <div class="page-title-block">
            <h1>Editar preço</h1>
            <p>Atualize o preço com transparência para quem está procurando.</p>
          </div>

          <div class="editor-card">
            <div class="editor-product-summary">
              <img :src="editingProduct.imagem_url" alt="" class="editor-thumb" />
              <div>
                <h2>{{ editingProduct.nome }}</h2>
                <p class="editor-meta">
                  {{ editingProduct.categoria }} · SKU TDV-{{ 100 + editingProduct.id }}
                </p>
                <div class="editor-badges">
                  <span class="badge" :class="editingProduct.ativo ? 'badge-success' : 'badge-neutral'">
                    {{ editingProduct.ativo ? 'Ativo no totem' : 'Pausado' }}
                  </span>
                  <span class="editor-meta">
                    <AppIcon name="clock" :size="13" />
                    Última atualização: {{ dataBR(editingProduct.atualizado_em) }} às {{ horaBR(editingProduct.atualizado_em) }}
                  </span>
                </div>
              </div>
            </div>

            <div class="editor-fields-grid">
              <label class="form-field">
                <span>Preço original (R$)</span>
                <input v-model.number="formPrecoOriginal" type="number" step="0.10" min="1" />
              </label>
              <label class="form-field">
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

            <div v-if="descontoCalculado > 0" class="discount-preview-line">
              <span class="discount-preview-icon"><AppIcon name="percent" :size="16" /></span>
              <div>
                <strong class="num">{{ descontoCalculado }}% de desconto</strong>
                <span>Promoção ativa até 20/11/2026</span>
              </div>
            </div>

            <p class="editor-disclaimer">
              <AppIcon name="info" :size="14" />
              O novo preço será publicado no totem e no site. Valores preenchidos apenas para
              demonstração do protótipo.
            </p>

            <div class="editor-actions">
              <button type="button" class="btn-cream" @click="mode = 'list'">
                Cancelar
              </button>
              <button type="button" class="btn-gold" @click="salvarEdicaoPreco()">
                <AppIcon name="check" :size="16" />
                Salvar alterações
              </button>
            </div>
          </div>
        </section>

        <!-- MODO 3: CADASTRAR NOVO PRODUTO -->
        <section v-else-if="mode === 'create'" class="lojista-body">
          <button type="button" class="btn-ghost btn-sm back-btn" @click="mode = 'list'">
            <AppIcon name="arrow-left" :size="16" />
            Voltar aos produtos
          </button>

          <div class="page-title-block">
            <h1>Cadastrar novo produto</h1>
            <p>Preencha os dados da oferta para publicação imediata no totem e no site.</p>
          </div>

          <form class="editor-card" @submit.prevent="salvarNovoProduto">
            <div class="editor-fields-grid">
              <label class="form-field">
                <span>Nome do produto</span>
                <input
                  v-model="novoForm.nome"
                  type="text"
                  required
                  placeholder="Ex: Tênis Run Pro Max"
                />
              </label>
              <label class="form-field">
                <span>Categoria</span>
                <select v-model="novoForm.categoria">
                  <option v-for="c in CATEGORIAS_PRODUTO" :key="c" :value="c">{{ c }}</option>
                </select>
              </label>
              <label class="form-field">
                <span>Preço original (R$)</span>
                <input
                  v-model.number="novoForm.preco"
                  type="number"
                  step="0.10"
                  min="1"
                  required
                />
              </label>
              <label class="form-field">
                <span>Preço promocional (R$) <span class="form-hint">— opcional</span></span>
                <input
                  v-model.number="novoForm.preco_promocional"
                  type="number"
                  step="0.10"
                  min="0"
                />
              </label>
            </div>

            <label class="form-field">
              <span>Descrição curta</span>
              <input
                v-model="novoForm.descricao"
                type="text"
                placeholder="Leveza, conforto e amortecimento. Consulte tamanhos na loja."
              />
              <span class="form-hint">Tamanhos, cores e condições na loja física.</span>
            </label>

            <div class="editor-actions">
              <button type="button" class="btn-cream" @click="mode = 'list'">
                Cancelar
              </button>
              <button type="submit" class="btn-gold">
                <AppIcon name="check" :size="16" />
                Publicar no totem e site
              </button>
            </div>
          </form>
        </section>
      </main>
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
const actionError = ref('')

const mode = ref('list') // 'list' | 'edit' | 'create'
const filterOnlyPromos = ref(false)
const publishedBanner = ref(false)

// Contas demo carregadas da API (uma por loja); estas três aparecem enquanto a API responde
const contasDemo = ref([
  { email: 'admin@centauro.com.br', nome: 'Centauro', piso: '1º Piso' },
  { email: 'admin@riachuelo.com.br', nome: 'Riachuelo', piso: '1º Piso' },
  { email: 'admin@lojaesporte.com.br', nome: 'Loja Esporte', piso: '2º Piso' }
])

const CATEGORIAS_PRODUTO = [
  'Calçados',
  'Moda',
  'Esportes',
  'Perfumaria',
  'Acessórios',
  'Alimentação',
  'Lazer',
  'Livros',
  'Brinquedos'
]

// Ilustração padrão por categoria para novos produtos
const IMAGEM_POR_CATEGORIA = {
  'Calçados': 'tenis-sprint',
  Moda: 'camiseta-branca',
  Esportes: 'camiseta-grafite',
  Perfumaria: 'perfume-essencial',
  'Acessórios': 'bolsa-caramelo',
  'Alimentação': 'prato-executivo',
  Lazer: 'ingresso',
  Livros: 'livro',
  Brinquedos: 'blocos'
}

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

function dataBR(iso) {
  return iso ? new Date(iso).toLocaleDateString('pt-BR') : '—'
}

function horaBR(iso) {
  return iso ? new Date(iso).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) : ''
}

function resumo(texto, max = 48) {
  if (!texto) return ''
  return texto.length > max ? `${texto.slice(0, max).trimEnd()}…` : texto
}

function mostrarTodos() {
  mode.value = 'list'
  filterOnlyPromos.value = false
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
  actionError.value = ''
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
    actionError.value = err.message || 'Não foi possível salvar as alterações.'
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
  actionError.value = ''
  try {
    const imagem = IMAGEM_POR_CATEGORIA[novoForm.value.categoria] || 'tenis-sprint'
    await api.cadastrarProduto(token.value, {
      ...novoForm.value,
      imagem_url: `/assets/products/${imagem}.svg`,
      ativo: true
    })
    await carregarDashboard()
    mode.value = 'list'
    publishedBanner.value = true
  } catch (err) {
    actionError.value = err.message || 'Não foi possível cadastrar o produto.'
  }
}

async function alternarStatus(prod) {
  actionError.value = ''
  try {
    await api.alternarStatusProduto(token.value, prod.id, !prod.ativo)
    await carregarDashboard()
    publishedBanner.value = true
  } catch (err) {
    actionError.value = err.message || 'Não foi possível alterar o status do produto.'
  }
}

function sair() {
  token.value = ''
  localStorage.removeItem('temaqui_lojista_token')
}

async function carregarContasDemo() {
  try {
    const contas = await api.listarContasDemo()
    contasDemo.value = contas.map((c) => ({
      email: c.email,
      nome: c.loja.nome,
      piso: `${c.loja.categoria} · ${c.loja.pavimento}`
    }))
  } catch {
    // mantém a lista padrão
  }
}

onMounted(async () => {
  carregarContasDemo()
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
  padding: 40px;
  background:
    radial-gradient(circle at 20% 15%, rgba(201, 163, 74, 0.16), transparent 45%),
    var(--color-cream);
}

.login-card {
  width: 100%;
  max-width: 520px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 36px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  box-shadow: var(--shadow-lg);
}

.login-brand {
  font-size: 24px;
  cursor: default;
}

.login-heading {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.login-heading h1 {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.login-sub {
  font-size: 14px;
  color: var(--color-graphite-muted);
  line-height: 1.5;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.error-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: var(--color-danger-bg);
  color: var(--color-danger-text);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  font-size: 13px;
  font-weight: 500;
}

.demo-accounts-box {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.demo-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  font-weight: 500;
  color: var(--color-graphite-muted);
}

.demo-divider::before,
.demo-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--color-border);
}

.demo-btns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  max-height: 300px;
  overflow-y: auto;
  padding-right: 2px;
}

.demo-account-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  background: var(--color-white);
  text-align: left;
  cursor: pointer;
  color: var(--color-graphite-muted);
  transition: border-color 0.15s var(--ease), background-color 0.15s var(--ease);
}

.demo-account-btn:hover {
  border-color: var(--color-gold);
  background: var(--color-surface);
}

.demo-avatar {
  width: 34px;
  height: 34px;
  border-radius: 9px;
  background: var(--color-graphite);
  color: var(--color-white);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
}

.demo-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  font-size: 12px;
}

.demo-info strong {
  font-size: 14px;
  font-weight: 600;
  color: var(--color-graphite);
}

/* SIDEBAR DO LOJISTA */
.lojista-sidebar {
  width: 264px;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  padding: 24px 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex-shrink: 0;
}

.sidebar-top {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.sidebar-brand {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 0 8px;
}

.sidebar-logo {
  font-size: 20px;
  cursor: default;
}

.store-identity-box {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 12px;
  box-shadow: var(--shadow-xs);
}

.store-identity-avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: var(--color-gold);
  color: var(--color-graphite);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 16px;
  flex-shrink: 0;
}

.store-identity-box strong {
  display: block;
  font-size: 15px;
  font-weight: 600;
}

.store-identity-box span {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.sidebar-nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.side-nav-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  text-align: left;
  padding: 10px 12px;
  border-radius: 10px;
  border: none;
  background: transparent;
  font-size: 14px;
  font-weight: 500;
  color: var(--color-graphite-muted);
  cursor: pointer;
  transition: background-color 0.15s var(--ease), color 0.15s var(--ease);
}

.side-nav-btn:hover {
  background: var(--color-cream);
  color: var(--color-graphite);
}

.side-nav-btn.active {
  background: var(--color-white);
  color: var(--color-graphite);
  font-weight: 600;
  box-shadow: var(--shadow-sm);
}

.side-nav-btn.active .app-icon {
  color: var(--color-gold-deep);
}

.sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 10px;
  font-size: 12px;
  color: var(--color-graphite-muted);
  padding: 0 4px;
}

.sync-status {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--color-success-text);
  font-weight: 600;
}

.sync-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #2E9E5B;
  box-shadow: 0 0 0 3px rgba(46, 158, 91, 0.2);
}

/* ÁREA PRINCIPAL */
.lojista-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  background: var(--color-white);
}

.lojista-topbar {
  padding: 16px 36px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.breadcrumb {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--color-graphite-muted);
}

.breadcrumb strong {
  color: var(--color-graphite);
  font-weight: 600;
}

.lojista-user-tag {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
}

.lojista-user-tag strong {
  font-weight: 600;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--color-graphite-muted);
}

.action-error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 20px 36px 0;
  padding: 10px 8px 10px 14px;
  border-radius: var(--radius-sm);
  background: var(--color-danger-bg);
  color: var(--color-danger-text);
  font-size: 14px;
  font-weight: 500;
}

.action-error-banner span {
  flex: 1;
}

.action-error-banner .icon-btn {
  color: var(--color-danger-text);
}

.lojista-body {
  padding: 28px 36px 40px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.back-btn {
  align-self: flex-start;
  margin: -8px 0 -12px -10px;
}

.published-alert-banner {
  display: flex;
  align-items: center;
  gap: 14px;
  background: var(--color-success-bg);
  border: 1px solid var(--color-success-border);
  color: var(--color-success-text);
  border-radius: var(--radius-md);
  padding: 14px 10px 14px 16px;
}

.published-alert-banner > div {
  flex: 1;
}

.published-icon {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--color-success-text);
  color: var(--color-white);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.published-alert-banner strong {
  font-size: 15px;
  font-weight: 600;
}

.published-alert-banner p {
  font-size: 13px;
  margin-top: 2px;
}

.published-alert-banner .icon-btn {
  color: var(--color-success-text);
}

.page-title-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
}

.page-title-block h1 {
  font-size: 28px;
  font-weight: 700;
  letter-spacing: -0.025em;
}

.page-title-block p {
  font-size: 14px;
  color: var(--color-graphite-muted);
  margin-top: 4px;
}

/* KPIs */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.kpi-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  box-shadow: var(--shadow-xs);
}

.kpi-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.kpi-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--color-graphite-muted);
}

.kpi-icon {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.kpi-value {
  font-size: 32px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--color-graphite);
  line-height: 1.1;
}

.kpi-divider {
  color: var(--color-border-strong);
  font-weight: 400;
}

.kpi-sub {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.kpi-sub.positive {
  color: var(--color-success-text);
  font-weight: 500;
}

/* TABELA */
.products-table-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-xs);
}

.table-header-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--color-border);
}

.table-header-bar h2 {
  font-size: 16px;
  font-weight: 600;
}

.lojista-table {
  width: 100%;
  border-collapse: collapse;
}

.lojista-table th {
  background: var(--color-surface);
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: var(--color-graphite-muted);
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 10px 20px;
  border-bottom: 1px solid var(--color-border);
}

.lojista-table td {
  padding: 14px 20px;
  border-bottom: 1px solid var(--color-border);
  vertical-align: middle;
}

.lojista-table tbody tr {
  transition: background-color 0.12s var(--ease);
}

.lojista-table tbody tr:hover {
  background: var(--color-surface);
}

.th-actions {
  text-align: right !important;
}

.prod-cell {
  display: flex;
  align-items: center;
  gap: 14px;
}

.prod-cell-img {
  width: 52px;
  height: 52px;
  border-radius: 10px;
  object-fit: cover;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
}

.prod-cell-name {
  font-size: 14px;
  font-weight: 600;
}

.prod-cell-cat {
  font-size: 12px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.price-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.curr-p {
  font-size: 15px;
  font-weight: 600;
}

.old-p {
  font-size: 12px;
  color: var(--color-graphite-muted);
  text-decoration: line-through;
}

.no-promo {
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.date-cell {
  font-size: 13px;
  color: var(--color-graphite);
}

.date-cell span {
  display: block;
  font-size: 12px;
  color: var(--color-graphite-muted);
}

.actions-cell {
  display: flex;
  justify-content: flex-end;
  gap: 6px;
}

.table-footer {
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: var(--color-graphite-muted);
}

.pagination {
  display: flex;
  gap: 4px;
}

.page-btn {
  min-width: 32px;
  height: 32px;
  padding: 0 8px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  background: var(--color-white);
  font-size: 13px;
  font-weight: 500;
  color: var(--color-graphite);
  cursor: pointer;
}

.page-btn:hover:not(:disabled) {
  background: var(--color-cream);
}

.page-btn.active {
  background: var(--color-graphite);
  border-color: var(--color-graphite);
  color: var(--color-white);
}

.page-btn:disabled {
  color: var(--color-border-strong);
  cursor: not-allowed;
}

/* EDITOR DE PREÇO / CADASTRO */
.editor-card {
  background: var(--color-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 22px;
  max-width: 820px;
  box-shadow: var(--shadow-sm);
}

.editor-product-summary {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-bottom: 22px;
  border-bottom: 1px solid var(--color-border);
}

.editor-thumb {
  width: 96px;
  height: 96px;
  border-radius: 14px;
  object-fit: cover;
  background: var(--color-cream);
  border: 1px solid var(--color-border);
}

.editor-product-summary h2 {
  font-size: 20px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.editor-meta {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--color-graphite-muted);
  margin-top: 4px;
}

.editor-badges {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 8px;
}

.editor-badges .editor-meta {
  margin-top: 0;
}

.editor-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.discount-preview-line {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--color-gold-soft);
  border: 1px solid rgba(201, 163, 74, 0.45);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
}

.discount-preview-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: var(--color-gold);
  color: var(--color-graphite);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.discount-preview-line strong {
  display: block;
  font-size: 15px;
  font-weight: 700;
}

.discount-preview-line span {
  font-size: 13px;
  color: var(--color-gold-deep);
}

.editor-disclaimer {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  font-size: 13px;
  color: var(--color-graphite-muted);
  line-height: 1.5;
}

.editor-disclaimer .app-icon {
  margin-top: 3px;
}

.editor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 20px;
  border-top: 1px solid var(--color-border);
}
</style>
