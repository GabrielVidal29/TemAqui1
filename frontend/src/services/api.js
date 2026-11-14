// Ordem: config do container (public/config.js) → variável do Vite → padrão local
const API_BASE = (
  window.__TEMAQUI_CONFIG__?.API_BASE_URL ||
  import.meta.env.VITE_API_BASE_URL ||
  'http://localhost:8000/api'
).replace(/\/$/, '')

// Fotos enviadas pelo lojista são servidas pela API (/api/produtos/{id}/imagem).
// Como o site e a API podem estar em endereços diferentes, completamos o endereço aqui.
const API_ORIGEM = API_BASE.replace(/\/api$/, '')

function corrigirImagens(dados) {
  if (Array.isArray(dados)) {
    dados.forEach(corrigirImagens)
  } else if (dados && typeof dados === 'object') {
    for (const [chave, valor] of Object.entries(dados)) {
      if (chave === 'imagem_url' && typeof valor === 'string' && valor.startsWith('/api/')) {
        dados[chave] = `${API_ORIGEM}${valor}`
      } else if (valor && typeof valor === 'object') {
        corrigirImagens(valor)
      }
    }
  }
  return dados
}

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
  if (response.status === 204) return null
  return corrigirImagens(await response.json())
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

  // acessivel: rota 100% acessível (só elevador, WC PCD em destaque)
  obterPerfilLoja(lojaId, totemId = 1, acessivel = false) {
    return request(`/lojas/${lojaId}/perfil?totem_id=${totemId}${acessivel ? '&acessivel=true' : ''}`)
  },

  obterTotem(totemId = 1) {
    return request(`/totens/${totemId}`)
  },

  obterRota(totemId = 1, lojaId = 1, acessivel = false) {
    return request(`/rotas?totem_id=${totemId}&loja_id=${lojaId}${acessivel ? '&acessivel=true' : ''}`)
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

  // imagem: data URL ("data:image/jpeg;base64,...") gerado por prepararFoto()
  enviarFotoProduto(token, produtoId, imagem) {
    return request(`/lojista/produtos/${produtoId}/imagem`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token}` },
      body: JSON.stringify({ imagem })
    })
  },

  excluirProduto(token, produtoId) {
    return request(`/lojista/produtos/${produtoId}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token}` }
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
