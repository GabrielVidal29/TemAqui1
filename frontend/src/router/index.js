import { createRouter, createWebHistory } from 'vue-router'
import MobileLayout from '@/layouts/MobileLayout.vue'
import TotemLayout from '@/layouts/TotemLayout.vue'
import LojistaLayout from '@/layouts/LojistaLayout.vue'
import MobileView from '@/views/mobile/MobileView.vue'
import TotemView from '@/views/totem/TotemView.vue'
import LojistaView from '@/views/lojista/LojistaView.vue'

const routes = [
  {
    path: '/',
    component: MobileLayout,
    children: [
      {
        path: '',
        name: 'mobile-home',
        component: MobileView
      }
    ]
  },
  {
    // Aberto pelo QR Code do totem: SOMENTE o layout mobile, em tela cheia,
    // sem a barra de demonstração e sem acesso ao totem/painel do lojista.
    path: '/celular',
    component: MobileLayout,
    meta: { standalone: true },
    children: [
      {
        path: '',
        name: 'mobile-celular',
        component: MobileView
      }
    ]
  },
  {
    path: '/totem',
    redirect: '/totem/1'
  },
  {
    path: '/totem/:totemId',
    component: TotemLayout,
    children: [
      {
        path: '',
        name: 'totem-home',
        component: TotemView
      }
    ]
  },
  {
    path: '/lojista',
    component: LojistaLayout,
    children: [
      {
        path: '',
        name: 'lojista-home',
        component: LojistaView
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
