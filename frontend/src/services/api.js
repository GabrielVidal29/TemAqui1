// Ordem: config do container (public/config.js) → variável do Vite → padrão local
const API_BASE = (
  window.__TEMAQUI_CONFIG__?.API_BASE_URL ||
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:8000/api'
).replace(/\/$/, '')

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  }
  const response = await fetch(url, { ...options, headers })
  if (!response.ok) {
    let errorDetail = `Erro HTTP ${response.status}`
    try {
      const errData = await response.json()
      if (typeof errData.detail === 'string') errorDetail = errData.detail
    } catch {
      // ignore json parse error
    }
    const erro = new Error(errorDetail)
    erro.status = response.status
    throw erro
  }
  return response.json()
}

export const api = {
  // Vitrine & Comparação (Público - RN02)
  listarProdutos(params = {}) {
    const qs = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') qs.append(k, v)
    })
    const queryStr = qs.toString() ? `?${qs.toString()}` : ''
    return request(`/produtos${queryStr}`)
  },

  compararProdutos(params = {}) {
    const qs = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') qs.append(k, v)
    })
    return request(`/produtos/comparar?${qs.toString()}`)
  },

  obterProduto(id, totemId = 1) {
    return request(`/produtos/${id}?totem_id=${totemId}`)
  },

  listarCategorias() {
    return request('/produtos/categorias')
  },

  // Shopping, Totens, POIs & Rotas (RN03-RN05)
  listarLojas(params = {}) {
    const qs = new URLSearchParams()
    Object.entries(params).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') qs.append(k, v)
    })
    const queryStr = qs.toString() ? `?${qs.toString()}` : ''
    return request(`/lojas${queryStr}`)
  },

  obterPerfilLoja(lojaId, totemId = 1) {
    return request(`/lojas/${lojaId}/perfil?totem_id=${totemId}`)
  },

  obterTotem(totemId = 1) {
    return request(`/totens/${totemId}`)
  },

  obterRota(totemId = 1, lojaId = 1) {
    return request(`/rotas?totem_id=${totemId}&loja_id=${lojaId}`)
  },

  listarPontosInteresse(pavimento = '') {
    const qs = pavimento ? `?pavimento=${encodeURIComponent(pavimento)}` : ''
    return request(`/pontos-interesse${qs}`)
  },

  // Painel Administrativo do Lojista (RN06-RN09)
  listarContasDemo() {
    return request('/lojista/contas-demo')
  },

  loginLojista(email, senha) {
    return request('/lojista/login', {
      method: 'POST',
      body: JSON.stringify({ email, senha })
    })
  },

  obterDashboardLojista(token) {
    return request('/lojista/dashboard', {
      headers: { Authorization: `Bearer ${token}` }
    })
  },

  cadastrarProduto(token, payload) {
    return request('/lojista/produtos', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload)
    })
  },

  atualizarProduto(token, produtoId, payload) {
    return request(`/lojista/produtos/${produtoId}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify(payload)
    })
  },

  alternarStatusProduto(token, produtoId, ativo) {
    return request(`/lojista/produtos/${produtoId}/status`, {
      method: 'PATCH',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ ativo })
    })
  }
}

export const API_URL = API_BASE

// Mensagem clara para quando o frontend não consegue falar com o backend
export function mensagemErroApi(err) {
  const msg = String(err?.message || '')
  // 404/422 em rotas públicas = backend de uma versão anterior, sem os endpoints novos
  if (err?.status === 404 || err?.status === 422) {
    return `A API em ${API_BASE} está desatualizada (endpoint não encontrado). Atualize o backend e reinicie-o.`
  }
  if (err instanceof TypeError || msg.includes('fetch')) {
    return `Não foi possível conectar à API em ${API_BASE}. Verifique se o backend está rodando.`
  }
  return `Erro ao carregar dados da API (${msg || 'desconhecido'}).`
}

export function formatCurrency(value) {
  if (value === null || value === undefined) return '—'
  return Number(value).toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  })
}
