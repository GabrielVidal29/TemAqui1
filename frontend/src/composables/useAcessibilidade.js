import { computed, onBeforeUnmount, reactive, watch } from 'vue'

/*
 * Preferências de acessibilidade do TemAqui.
 *
 * - Totem: ficam só na memória (o próximo visitante começa do padrão ou usa "Restaurar padrão").
 * - Celular: ficam salvas no aparelho (localStorage).
 * - Do totem para o celular, vão na URL do QR Code / NFC: ?a11y=contraste,fonte2,voz,rota,cadeirante
 *
 * Os modos visuais são aplicados como atributos no <html> enquanto a tela está aberta
 * (data-contraste, data-fonte, data-cadeirante, data-a11y-visual); as variáveis
 * ficam em assets/styles/tokens.css.
 */

const PADRAO = {
  cadeirante: false, // Modo cadeirante: controles na metade de baixo da tela
  rotaAcessivel: false, // Rota 100% acessível: só elevador, WC PCD em destaque
  altoContraste: false, // Preto, branco e amarelo
  fonte: 0, // 0 = normal, 1 = A+, 2 = A++
  leituraVoz: false // Lê em voz alta resultados, ofertas e rotas
}

const CHAVE_CELULAR = 'temaqui_a11y'
const estados = {}

function criarEstado(contexto) {
  const estado = reactive({ ...PADRAO })
  if (contexto === 'mobile') {
    try {
      Object.assign(estado, JSON.parse(localStorage.getItem(CHAVE_CELULAR) || '{}'))
    } catch {
      // preferências corrompidas: segue com o padrão
    }
    watch(estado, () => localStorage.setItem(CHAVE_CELULAR, JSON.stringify(estado)), { deep: true })
  }
  return estado
}

/** Converte o estado para o parâmetro ?a11y= (só o que está ativo). */
export function serializarA11y(estado) {
  const partes = []
  if (estado.altoContraste) partes.push('contraste')
  if (estado.fonte) partes.push(`fonte${estado.fonte}`)
  if (estado.leituraVoz) partes.push('voz')
  if (estado.rotaAcessivel) partes.push('rota')
  if (estado.cadeirante) partes.push('cadeirante')
  return partes.join(',')
}

/** Lê o parâmetro ?a11y= e devolve as preferências correspondentes. */
export function lerParametroA11y(valor) {
  const itens = String(valor || '')
    .toLowerCase()
    .split(/[,\s.]+/)
    .filter(Boolean)
  if (!itens.length) return null
  const fonte = itens.includes('fonte2') ? 2 : itens.includes('fonte1') ? 1 : 0
  return {
    altoContraste: itens.includes('contraste'),
    fonte,
    leituraVoz: itens.includes('voz'),
    rotaAcessivel: itens.includes('rota') || itens.includes('cadeirante'),
    cadeirante: itens.includes('cadeirante')
  }
}

export function useAcessibilidade(contexto = 'totem') {
  if (!estados[contexto]) estados[contexto] = criarEstado(contexto)
  const estado = estados[contexto]

  const modoVisualAtivo = computed(() => estado.altoContraste || estado.fonte > 0)
  const temAlgumAtivo = computed(() => Object.keys(PADRAO).some((k) => estado[k] !== PADRAO[k]))
  const parametro = computed(() => serializarA11y(estado))

  function restaurar() {
    Object.assign(estado, PADRAO)
  }

  function aplicarParametro(valor) {
    const prefs = lerParametroA11y(valor)
    if (!prefs) return false
    // No celular não existe modo cadeirante (o aparelho já está na mão); fica só a rota acessível
    if (contexto === 'mobile') prefs.cadeirante = false
    Object.assign(estado, prefs)
    return true
  }

  /** Aplica os atributos no <html> enquanto o componente que chamou estiver montado. */
  function aplicarNoDocumento() {
    const raiz = document.documentElement
    const parar = watch(
      () => ({ ...estado }),
      (e) => {
        const set = (nome, valor) => (valor ? raiz.setAttribute(nome, valor) : raiz.removeAttribute(nome))
        set('data-contraste', e.altoContraste ? 'alto' : '')
        set('data-fonte', e.fonte ? String(e.fonte) : '')
        set('data-cadeirante', e.cadeirante ? 'sim' : '')
        set('data-a11y-visual', e.altoContraste || e.fonte ? 'sim' : '')
      },
      { immediate: true }
    )
    onBeforeUnmount(() => {
      parar()
      ;['data-contraste', 'data-fonte', 'data-cadeirante', 'data-a11y-visual'].forEach((a) =>
        raiz.removeAttribute(a)
      )
    })
  }

  return { estado, modoVisualAtivo, temAlgumAtivo, parametro, restaurar, aplicarParametro, aplicarNoDocumento }
}
