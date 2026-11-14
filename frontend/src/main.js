import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import AppIcon from './components/common/AppIcon.vue'
import './assets/styles/main.css'

const app = createApp(App)
app.component('AppIcon', AppIcon)
app.use(router)
app.mount('#app')
