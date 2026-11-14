// Ícone de cada categoria de produto ou loja (nomes do componente AppIcon)
const ICONES = {
  Moda: 'shirt',
  'Calçados': 'footprints',
  Esportes: 'dumbbell',
  Perfumaria: 'sparkles',
  'Acessórios': 'shopping-bag',
  'Alimentação': 'utensils',
  Restaurantes: 'utensils',
  Lazer: 'film',
  Livros: 'book-open',
  Livraria: 'book-open',
  Brinquedos: 'gift'
}

export function iconeCategoria(categoria) {
  return ICONES[categoria] || 'tag'
}

export const FAIXAS_PRECO = [
  { valor: null, label: 'Qualquer preço' },
  { valor: 50, label: 'Até R$ 50' },
  { valor: 100, label: 'Até R$ 100' },
  { valor: 200, label: 'Até R$ 200' },
  { valor: 350, label: 'Até R$ 350' },
  { valor: 500, label: 'Até R$ 500' }
]

export const ORDENACOES = [
  { valor: 'relevancia', label: 'Mais relevantes' },
  { valor: 'menor_preco', label: 'Menor preço' },
  { valor: 'maior_preco', label: 'Maior preço' },
  { valor: 'maior_desconto', label: 'Maior desconto' },
  { valor: 'recente', label: 'Atualizados agora' }
]

export const PISOS = [
  { valor: '', label: 'Todos os pisos' },
  { valor: '1º Piso', label: '1º Piso' },
  { valor: '2º Piso', label: '2º Piso' }
]
