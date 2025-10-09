import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import '@vueuse/core'
import './assets/styles.css'
import '@fortawesome/fontawesome-free/css/all.css'
import './assets/main.css'
import router from './router'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.mount('#app')