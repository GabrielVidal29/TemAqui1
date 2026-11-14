// Prepara a foto escolhida pelo lojista antes do envio:
// valida o formato, reduz para no máximo 1200 px e converte para JPEG (fica leve para o totem e o celular).

export const TIPOS_FOTO = ['image/jpeg', 'image/png', 'image/webp']
const LADO_MAXIMO = 1200
const TAMANHO_MAXIMO_ORIGINAL = 15 * 1024 * 1024 // 15 MB antes de reduzir

function carregarImagem(arquivo) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(arquivo)
    const img = new Image()
    img.onload = () => {
      URL.revokeObjectURL(url)
      resolve(img)
    }
    img.onerror = () => {
      URL.revokeObjectURL(url)
      reject(new Error('Não foi possível ler esta imagem. Tente outra foto.'))
    }
    img.src = url
  })
}

export async function prepararFoto(arquivo) {
  if (!arquivo) throw new Error('Nenhuma foto selecionada.')
  if (!TIPOS_FOTO.includes(arquivo.type)) {
    throw new Error('Formato não suportado. Envie uma foto JPG, PNG ou WebP.')
  }
  if (arquivo.size > TAMANHO_MAXIMO_ORIGINAL) {
    throw new Error('A foto é muito grande (máximo de 15 MB).')
  }

  const img = await carregarImagem(arquivo)
  const escala = Math.min(1, LADO_MAXIMO / Math.max(img.naturalWidth, img.naturalHeight))
  const largura = Math.round(img.naturalWidth * escala)
  const altura = Math.round(img.naturalHeight * escala)

  const canvas = document.createElement('canvas')
  canvas.width = largura
  canvas.height = altura
  const ctx = canvas.getContext('2d')
  // Fundo branco para PNGs com transparência
  ctx.fillStyle = '#ffffff'
  ctx.fillRect(0, 0, largura, altura)
  ctx.drawImage(img, 0, 0, largura, altura)
  return canvas.toDataURL('image/jpeg', 0.85)
}
