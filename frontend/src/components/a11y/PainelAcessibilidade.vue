<template>
  <div class="a11y-overlay" @click.self="fechar" @keydown.esc="fechar">
    <section
      ref="painel"
      class="a11y-sheet"
      :class="{ compacto }"
      role="dialog"
      aria-modal="true"
      aria-labelledby="a11y-titulo"
      aria-describedby="a11y-descricao"
      tabindex="-1"
    >
      <header class="a11y-head">
        <span class="a11y-head-icon"><AppIcon name="accessibility" :size="24" /></span>
        <div>
          <h2 id="a11y-titulo">Acessibilidade</h2>
          <p id="a11y-descricao">
            {{ compacto ? 'Ajuste o site do seu jeito. Fica salvo neste celular.' : 'Ajuste o totem do seu jeito. Vale até você voltar ao início.' }}
          </p>
        </div>
        <button type="button" class="icon-btn a11y-close" aria-label="Fechar painel de acessibilidade" @click="fechar">
          <AppIcon name="x" :size="20" />
        </button>
      </header>

      <ul class="a11y-opcoes">
        <li v-if="!compacto">
          <button type="button" role="switch" class="a11y-switch" :aria-checked="estado.cadeirante" @click="alternar('cadeirante')">
            <span class="a11y-opt-icon"><AppIcon name="accessibility" :size="20" /></span>
            <span class="a11y-opt-text">
              <strong>Modo cadeirante</strong>
              <span>Busca, abas e filtros descem para a parte de baixo da tela, ao alcance da mão.</span>
            </span>
            <span class="a11y-track" aria-hidden="true"><span class="a11y-thumb"></span></span>
          </button>
        </li>
        <li>
          <button type="button" role="switch" class="a11y-switch" :aria-checked="estado.rotaAcessivel" @click="alternar('rotaAcessivel')">
            <span class="a11y-opt-icon"><AppIcon name="elevator" :size="20" /></span>
            <span class="a11y-opt-text">
              <strong>Rota 100% acessível</strong>
              <span>Só elevadores, sem escadas. Mostra o banheiro acessível (WC PCD).</span>
            </span>
            <span class="a11y-track" aria-hidden="true"><span class="a11y-thumb"></span></span>
          </button>
        </li>
        <li>
          <button type="button" role="switch" class="a11y-switch" :aria-checked="estado.altoContraste" @click="alternar('altoContraste')">
            <span class="a11y-opt-icon"><AppIcon name="contrast" :size="20" /></span>
            <span class="a11y-opt-text">
              <strong>Alto contraste</strong>
              <span>Preto, branco e amarelo para enxergar melhor.</span>
            </span>
            <span class="a11y-track" aria-hidden="true"><span class="a11y-thumb"></span></span>
          </button>
        </li>
        <li class="a11y-fonte">
          <span class="a11y-opt-icon"><AppIcon name="type" :size="20" /></span>
          <span class="a11y-opt-text">
            <strong id="a11y-fonte-rotulo">Tamanho da fonte</strong>
            <span>Aumenta textos, preços e instruções.</span>
          </span>
          <div class="a11y-seg" role="radiogroup" aria-labelledby="a11y-fonte-rotulo">
            <button
              v-for="op in FONTES"
              :key="op.valor"
              type="button"
              role="radio"
              :aria-checked="estado.fonte === op.valor"
              :aria-label="op.descricao"
              :class="['a11y-seg-btn', `tam-${op.valor}`]"
              @click="definirFonte(op.valor)"
            >
              {{ op.rotulo }}
            </button>
          </div>
        </li>
        <li>
          <button type="button" role="switch" class="a11y-switch" :aria-checked="estado.leituraVoz" @click="alternar('leituraVoz')">
            <span class="a11y-opt-icon"><AppIcon :name="estado.leituraVoz ? 'volume-2' : 'volume-x'" :size="20" /></span>
            <span class="a11y-opt-text">
              <strong>Leitura por voz</strong>
              <span>
                {{ suportaFala ? 'Lê em voz alta ofertas, resultados e o caminho até a loja.' : 'Este navegador não tem voz disponível.' }}
              </span>
            </span>
            <span class="a11y-track" aria-hidden="true"><span class="a11y-thumb"></span></span>
          </button>
        </li>
      </ul>

      <footer class="a11y-foot">
        <button type="button" class="btn-cream" :disabled="!temAlgumAtivo" @click="restaurarPadrao">
          Restaurar padrão
        </button>
        <button type="button" class="btn-gold" @click="fechar">
          <AppIcon name="check" :size="16" />
          Concluir
        </button>
      </footer>
    </section>
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useAcessibilidade } from '@/composables/useAcessibilidade'
import { anunciar, falar, pararFala, suportaFala } from '@/composables/useVoz'

const props = defineProps({
  contexto: { type: String, default: 'totem' }, // 'totem' | 'mobile'
  compacto: { type: Boolean, default: false }
})
const emit = defineEmits(['fechar'])

const { estado, temAlgumAtivo, restaurar } = useAcessibilidade(props.contexto)

const FONTES = [
  { valor: 0, rotulo: 'A', descricao: 'Fonte normal' },
  { valor: 1, rotulo: 'A+', descricao: 'Fonte grande' },
  { valor: 2, rotulo: 'A++', descricao: 'Fonte muito grande' }
]

const NOMES = {
  cadeirante: 'Modo cadeirante',
  rotaAcessivel: 'Rota acessível',
  altoContraste: 'Alto contraste',
  leituraVoz: 'Leitura por voz'
}

const painel = ref(null)
let focoAnterior = null

function avisar(texto) {
  // Com a leitura ligada, fala; sem ela, só avisa o leitor de tela
  if (estado.leituraVoz) falar(texto)
  else anunciar(texto)
}

function alternar(chave) {
  estado[chave] = !estado[chave]
  if (chave === 'leituraVoz' && !estado.leituraVoz) {
    pararFala()
    anunciar('Leitura por voz desligada.')
    return
  }
  avisar(`${NOMES[chave]} ${estado[chave] ? 'ativado' : 'desativado'}.`)
}

function definirFonte(valor) {
  estado.fonte = valor
  avisar(FONTES[valor].descricao + '.')
}

function restaurarPadrao() {
  pararFala()
  restaurar()
  anunciar('Configurações de acessibilidade restauradas.')
}

function fechar() {
  emit('fechar')
}

onMounted(async () => {
  focoAnterior = document.activeElement
  await nextTick()
  painel.value?.focus()
})

onBeforeUnmount(() => {
  if (focoAnterior && typeof focoAnterior.focus === 'function') focoAnterior.focus()
})
</script>

<style scoped>
.a11y-overlay {
  position: fixed;
  inset: 0;
  z-index: 60;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  padding: 16px;
  background: rgba(20, 20, 20, 0.5);
}

/* Painel na parte de baixo da tela: alcançável por quem está sentado */
.a11y-sheet {
  width: 100%;
  max-width: 640px;
  max-height: calc(100dvh - 32px);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px;
  border-radius: var(--radius-lg);
  background: var(--color-white);
  color: var(--color-graphite);
  box-shadow: var(--shadow-lg);
  outline: none;
}

.a11y-head {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.a11y-head-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: var(--color-gold-soft);
  color: var(--color-gold-deep);
}

.a11y-head h2 {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.a11y-head p {
  font-size: 14px;
  color: var(--color-graphite-muted);
  margin-top: 2px;
}

.a11y-close {
  margin-left: auto;
  width: 44px;
  height: 44px;
}

.a11y-opcoes {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.a11y-switch,
.a11y-fonte {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 14px;
  min-height: 64px;
  padding: 12px 14px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  text-align: left;
}

.a11y-switch {
  cursor: pointer;
}

.a11y-switch[aria-checked='true'] {
  border-color: var(--color-gold);
  background: var(--color-gold-soft);
}

.a11y-opt-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
  color: var(--color-graphite);
}

.a11y-opt-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  min-width: 0;
}

.a11y-opt-text strong {
  font-size: 16px;
  font-weight: 700;
}

.a11y-opt-text span {
  font-size: 13px;
  line-height: 1.4;
  color: var(--color-graphite-muted);
}

.a11y-track {
  width: 52px;
  height: 30px;
  flex-shrink: 0;
  border-radius: var(--radius-pill);
  background: var(--color-border-strong);
  position: relative;
  transition: background 0.15s var(--ease);
}

.a11y-thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--color-white);
  box-shadow: var(--shadow-sm);
  transition: transform 0.15s var(--ease);
}

.a11y-switch[aria-checked='true'] .a11y-track {
  background: var(--color-graphite);
}

.a11y-switch[aria-checked='true'] .a11y-thumb {
  transform: translateX(22px);
}

.a11y-seg {
  display: inline-flex;
  flex-shrink: 0;
  padding: 4px;
  gap: 4px;
  border-radius: 12px;
  background: var(--color-white);
  border: 1px solid var(--color-border);
}

.a11y-seg-btn {
  min-width: 52px;
  min-height: 44px;
  padding: 6px 10px;
  border: none;
  border-radius: 9px;
  background: transparent;
  font-weight: 700;
  color: var(--color-graphite);
  cursor: pointer;
}

.a11y-seg-btn.tam-0 { font-size: 14px; }
.a11y-seg-btn.tam-1 { font-size: 17px; }
.a11y-seg-btn.tam-2 { font-size: 20px; }

.a11y-seg-btn[aria-checked='true'] {
  background: var(--color-graphite);
  color: var(--color-white);
}

.a11y-foot {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.a11y-foot .btn-cream:disabled {
  opacity: 0.5;
  cursor: default;
}

/* Versão compacta (celular) */
.a11y-sheet.compacto {
  padding: 18px 16px;
  gap: 12px;
  border-radius: 20px 20px 16px 16px;
}

.compacto .a11y-head h2 {
  font-size: 19px;
}

.compacto .a11y-switch,
.compacto .a11y-fonte {
  min-height: 56px;
  padding: 10px 12px;
  gap: 10px;
}

.compacto .a11y-fonte {
  flex-wrap: wrap;
}

/* No celular, o seletor de fonte vai para a linha de baixo */
.compacto .a11y-fonte .a11y-opt-text {
  flex: 1 1 calc(100% - 60px);
}

.compacto .a11y-opt-icon {
  width: 34px;
  height: 34px;
}

.compacto .a11y-opt-text strong {
  font-size: 15px;
}

.compacto .a11y-opt-text span {
  font-size: 12px;
}

.compacto .a11y-seg {
  margin-left: 44px;
}

.compacto .a11y-foot .btn-gold,
.compacto .a11y-foot .btn-cream {
  flex: 1;
}
</style>
