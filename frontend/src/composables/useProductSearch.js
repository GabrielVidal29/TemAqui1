import { computed, reactive, ref, watch } from 'vue'
import { api } from '@/services/api'

/**
 * Busca de produtos compartilhada entre Totem e Mobile.
 *
 * - O texto, categoria, piso, faixa de preço e ordenação são enviados à API (filtragem real no backend).
 * - O filtro "Em promoção / Preço normal" é aplicado sobre o resultado para exibir as contagens de cada grupo.
 */
export const FILTROS_PADRAO = Object.freeze({
  q: '',
  categoria: '',
  pavimento: '',
  preco_max: null,
  promocao: 'todas', // 'todas' | 'com' | 'sem'
  ordenar_por: 'relevancia'
})

export function useProductSearch({ totemId = 1, debounceMs = 250 } = {}) {
  const filtros = reactive({ ...FILTROS_PADRAO })
  const brutos = ref([])
  const carregando = ref(false)
  const erro = ref('')
  let timer = null
  let ultimaReq = 0

  async function buscar() {
    const reqId = ++ultimaReq
    carregando.value = true
    erro.value = ''
    try {
      const ordenar = filtros.ordenar_por === 'relevancia' && !filtros.q.trim() ? 'maior_desconto' : filtros.ordenar_por
      const dados = await api.listarProdutos({
        q: filtros.q.trim(),
        categoria: filtros.categoria,
        pavimento: filtros.pavimento,
        preco_max: filtros.preco_max,
        ordenar_por: ordenar,
        totem_id: typeof totemId === 'object' ? totemId.value : totemId
      })
      if (reqId === ultimaReq) brutos.value = dados
    } catch (e) {
      if (reqId === ultimaReq) {
        erro.value = 'Não foi possível carregar os produtos. Tente novamente.'
        brutos.value = []
      }
    } finally {
      if (reqId === ultimaReq) carregando.value = false
    }
  }

  watch(
    () => [filtros.q, filtros.categoria, filtros.pavimento, filtros.preco_max, filtros.ordenar_por],
    () => {
      clearTimeout(timer)
      timer = setTimeout(buscar, debounceMs)
    }
  )

  const contagem = computed(() => {
    const com = brutos.value.filter((p) => p.percentual_desconto > 0).length
    return { todas: brutos.value.length, com, sem: brutos.value.length - com }
  })

  const resultados = computed(() => {
    if (filtros.promocao === 'com') return brutos.value.filter((p) => p.percentual_desconto > 0)
    if (filtros.promocao === 'sem') return brutos.value.filter((p) => p.percentual_desconto === 0)
    return brutos.value
  })

  // Lojas que têm produtos no resultado atual (atalho para o perfil da loja)
  const lojasEncontradas = computed(() => {
    const mapa = new Map()
    resultados.value.forEach((p) => {
      const atual = mapa.get(p.loja_id) || { loja: p.loja, total: 0, promocoes: 0 }
      atual.total += 1
      if (p.percentual_desconto > 0) atual.promocoes += 1
      mapa.set(p.loja_id, atual)
    })
    return [...mapa.values()].sort((a, b) => b.total - a.total)
  })

  const temFiltroAtivo = computed(
    () =>
      !!filtros.q.trim() ||
      !!filtros.categoria ||
      !!filtros.pavimento ||
      filtros.preco_max !== null ||
      filtros.promocao !== 'todas'
  )

  function aplicar(novos = {}) {
    Object.assign(filtros, { ...FILTROS_PADRAO }, novos)
    clearTimeout(timer)
    buscar()
  }

  function limpar() {
    aplicar({})
  }

  return {
    filtros,
    resultados,
    contagem,
    lojasEncontradas,
    carregando,
    erro,
    temFiltroAtivo,
    buscar,
    aplicar,
    limpar
  }
}
