// Textos usados pela leitura por voz (e pela região aria-live dos leitores de tela).

export const AVISO_NFC =
  'Aproxime seu celular no leitor NFC localizado no centro abaixo da tela do totem, ou escaneie o QR Code.'

/** 299.9 -> "299 reais e 90 centavos" (as vozes leem melhor do que "R$ 299,90"). */
export function precoFalado(valor) {
  if (valor === null || valor === undefined) return ''
  const centavosTotais = Math.round(Number(valor) * 100)
  const reais = Math.floor(centavosTotais / 100)
  const centavos = centavosTotais % 100
  const parteReais = `${reais} ${reais === 1 ? 'real' : 'reais'}`
  return centavos ? `${parteReais} e ${centavos} centavos` : parteReais
}

export function textoProduto(prod, { curto = false } = {}) {
  if (!prod) return ''
  let texto = `${prod.nome}, ${precoFalado(prod.preco_final)}`
  if (prod.percentual_desconto > 0) {
    texto += curto
      ? `, ${prod.percentual_desconto} por cento de desconto`
      : `, com ${prod.percentual_desconto} por cento de desconto. Antes custava ${precoFalado(prod.preco_original)}`
  }
  if (prod.loja?.nome) texto += `. Na loja ${prod.loja.nome}, ${prod.loja.pavimento}`
  return `${texto}.`
}

export function textoDetalheProduto(prod) {
  if (!prod) return ''
  const local = prod.loja?.localizacao ? ` Localização: ${prod.loja.localizacao}.` : ''
  return (
    `${textoProduto(prod)}${local} ${prod.descricao || ''} ` +
    'Para ir até a loja, toque em Como chegar. Para levar no celular, toque em Continuar no celular.'
  )
}

export function textoListaProdutos(lista, { titulo = '', max = 3 } = {}) {
  const n = lista.length
  if (!n) return `${titulo ? titulo + '. ' : ''}Nenhum produto encontrado. Tente outro termo ou remova filtros.`
  const primeiros = lista
    .slice(0, max)
    .map((p, i) => `${i + 1}: ${textoProduto(p, { curto: true })}`)
    .join(' ')
  const cabecalho = `${titulo ? titulo + '. ' : ''}${n} ${n === 1 ? 'produto encontrado' : 'produtos encontrados'}.`
  return `${cabecalho} ${n > 1 ? 'Os primeiros:' : ''} ${primeiros} Toque em um produto para ouvir os detalhes.`
}

export function textoDaRota(rota) {
  if (!rota) return ''
  const passos = (rota.passos || []).map((p, i) => `Passo ${i + 1}: ${p}`).join(' ')
  const inicio =
    `Rota até ${rota.loja_nome}, cerca de ${rota.tempo_estimado_min} minutos a pé` +
    `${rota.acessivel ? ', rota acessível só com elevador' : ''}.`
  return `${inicio} ${passos || rota.instrucoes}`
}
