<template>
  <!-- Trilha do gato: cobre a área dos cards sem bloquear cliques neles -->
  <div class="cat-track" :style="{ top }" aria-hidden="false">
    <button
      type="button"
      class="cat-walker"
      :style="{ '--duracao': `${duracao}s` }"
      aria-label="Gato preto misterioso. Toque para ganhar um cupom de sexta-feira 13"
      @click="emit('pegar')"
    >
      <span class="cat-bubble" aria-hidden="true">miau?</span>
      <svg class="cat-svg" viewBox="0 0 120 84" width="96" height="67" aria-hidden="true">
        <!-- Rabo -->
        <g class="cat-tail">
          <path d="M26 46 C10 42 6 26 16 12" stroke="#151515" stroke-width="7" fill="none" stroke-linecap="round" />
        </g>
        <!-- Patas (dois pares alternados) -->
        <g class="cat-legs cat-legs-b" fill="#0E0E0E">
          <rect x="31" y="50" width="7" height="24" rx="3.5" />
          <rect x="75" y="50" width="7" height="24" rx="3.5" />
        </g>
        <g class="cat-legs cat-legs-a" fill="#1A1A1A">
          <rect x="41" y="50" width="7" height="24" rx="3.5" />
          <rect x="85" y="50" width="7" height="24" rx="3.5" />
        </g>
        <!-- Corpo -->
        <ellipse cx="56" cy="47" rx="34" ry="15" fill="#1A1A1A" />
        <!-- Cabeça -->
        <g class="cat-head">
          <path d="M80 27 L83 9 L93 21 Z" fill="#1A1A1A" />
          <path d="M95 21 L104 8 L107 27 Z" fill="#1A1A1A" />
          <path d="M83 24 L84.5 14 L90 21 Z" fill="#3A2F2F" />
          <path d="M98 21 L103 13 L104.5 24 Z" fill="#3A2F2F" />
          <circle cx="94" cy="34" r="16" fill="#1A1A1A" />
          <g class="cat-eyes">
            <ellipse cx="88" cy="32" rx="3.8" ry="4.2" fill="#C9A34A" />
            <ellipse cx="100" cy="32" rx="3.8" ry="4.2" fill="#C9A34A" />
            <ellipse cx="88.6" cy="32" rx="1.1" ry="3.4" fill="#111" />
            <ellipse cx="100.6" cy="32" rx="1.1" ry="3.4" fill="#111" />
          </g>
          <path d="M92.5 39 L95.5 39 L94 41 Z" fill="#B5654F" />
          <g stroke="#6B6B6B" stroke-width="1.1" stroke-linecap="round">
            <path d="M84 40 L72 38" />
            <path d="M84 42 L73 44" />
            <path d="M104 40 L116 38" />
            <path d="M104 42 L115 44" />
          </g>
        </g>
        <!-- Coleira dourada com a plaquinha 13 -->
        <path d="M80 45 Q88 50 98 46" stroke="#C9A34A" stroke-width="3" fill="none" stroke-linecap="round" />
        <circle cx="89" cy="52" r="5.5" fill="#C9A34A" />
        <text x="89" y="54.4" text-anchor="middle" font-family="Inter, sans-serif" font-size="6.5" font-weight="800" fill="#1A1A1A">13</text>
      </svg>
    </button>
  </div>
</template>

<script setup>
defineProps({
  // Altura da trilha dentro do contêiner (ex.: entre duas linhas de cards)
  top: { type: String, default: '50%' },
  // Tempo de ida e volta, em segundos
  duracao: { type: Number, default: 26 }
})

const emit = defineEmits(['pegar'])
</script>

<style scoped>
.cat-track {
  position: absolute;
  left: 0;
  right: 0;
  height: 0;
  z-index: 4;
  pointer-events: none;
}

.cat-walker {
  position: absolute;
  top: -48px;
  left: 0;
  padding: 0;
  border: none;
  background: none;
  cursor: pointer;
  pointer-events: auto;
  filter: drop-shadow(0 6px 6px rgba(0, 0, 0, 0.18));
  animation: passeio var(--duracao) linear infinite;
}

/* Vai até a direita, para um instante, vira e volta */
@keyframes passeio {
  0% { left: 0; }
  44%, 50% { left: calc(100% - 96px); }
  94%, 100% { left: 0; }
}

/* Só o desenho vira de lado (o balão de texto não espelha) */
@keyframes direcao {
  0%, 46.9% { transform: scaleX(1); }
  47%, 96.9% { transform: scaleX(-1); }
  97%, 100% { transform: scaleX(1); }
}

/* Fica parado enquanto o mouse/foco está nele, para facilitar o toque */
.cat-walker:hover,
.cat-walker:focus-visible {
  animation-play-state: paused;
}

.cat-walker:hover .cat-legs,
.cat-walker:focus-visible .cat-legs,
.cat-walker:hover .cat-svg,
.cat-walker:focus-visible .cat-svg {
  animation-play-state: paused;
}

.cat-walker:focus-visible {
  outline: 3px solid var(--color-gold);
  outline-offset: 4px;
  border-radius: 12px;
}

.cat-svg {
  display: block;
  overflow: visible;
  animation: direcao var(--duracao) linear infinite;
}

.cat-legs {
  transform-box: fill-box;
  transform-origin: top center;
  animation: passo 0.5s ease-in-out infinite alternate;
}

.cat-legs-b {
  animation-direction: alternate-reverse;
}

@keyframes passo {
  from { transform: rotate(14deg); }
  to { transform: rotate(-14deg); }
}

.cat-tail {
  transform-box: fill-box;
  transform-origin: bottom right;
  animation: rabo 1.6s ease-in-out infinite alternate;
}

@keyframes rabo {
  from { transform: rotate(-10deg); }
  to { transform: rotate(12deg); }
}

.cat-eyes {
  transform-box: fill-box;
  transform-origin: center;
  animation: piscar 4.5s infinite;
}

@keyframes piscar {
  0%, 92%, 100% { transform: scaleY(1); }
  95% { transform: scaleY(0.1); }
}

/* Balão "miau?" aparece ao passar o mouse/foco */
.cat-bubble {
  position: absolute;
  top: -26px;
  left: 50%;
  translate: -50% 0;
  padding: 3px 9px;
  border-radius: var(--radius-pill);
  background: var(--color-graphite);
  color: var(--color-gold);
  font-size: 12px;
  font-weight: 700;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.15s var(--ease);
}

.cat-walker:hover .cat-bubble,
.cat-walker:focus-visible .cat-bubble {
  opacity: 1;
}

/* Menos movimento: o gato fica sentado no canto, ainda clicável */
@media (prefers-reduced-motion: reduce) {
  .cat-walker,
  .cat-svg,
  .cat-legs,
  .cat-tail,
  .cat-eyes {
    animation: none !important;
  }
  .cat-walker {
    left: calc(100% - 96px);
  }
}
</style>
