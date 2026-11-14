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
