import qrcode from 'qrcode-generator'

/**
 * Endereço público do site, usado no QR Code lido pelo celular.
 * - Em produção (Render) é o próprio domínio do site.
 * - Em rede local, defina PUBLIC_SITE_URL no container (ex.: http://192.168.0.10:5173),
 *   porque o celular não enxerga o "localhost" do totem.
 */
export function urlPublicaDoSite() {
  const configurado = window.__TEMAQUI_CONFIG__?.PUBLIC_SITE_URL
  return (configurado || window.location.origin).replace(/\/$/, '')
}

/**
 * URL que o QR Code abre no celular: rota /celular (somente o layout mobile, sem
 * a barra de demonstração) + contexto do totem (busca, produto, loja, cupom).
 */
export function urlCelular(contexto = {}) {
  const params = new URLSearchParams()
  Object.entries(contexto).forEach(([chave, valor]) => {
    if (valor !== undefined && valor !== null && valor !== '') params.set(chave, String(valor))
  })
  const qs = params.toString()
  return `${urlPublicaDoSite()}/celular${qs ? `?${qs}` : ''}`
}

/**
 * Gera a matriz do QR Code (true = módulo escuro).
 * Correção de erro "Q" (25%): aguenta o selo do TemAqui desenhado no centro.
 */
export function matrizQr(texto, correcao = 'Q') {
  const qr = qrcode(0, correcao)
  qr.addData(texto)
  qr.make()
  const n = qr.getModuleCount()
  const linhas = []
  for (let r = 0; r < n; r++) {
    const linha = []
    for (let c = 0; c < n; c++) linha.push(qr.isDark(r, c))
    linhas.push(linha)
  }
  return linhas
}
