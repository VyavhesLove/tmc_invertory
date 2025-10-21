import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import '@vueuse/core'
import './assets/styles.css'
import '@fortawesome/fontawesome-free/css/all.css'
import './assets/main.css'
import router from './router'
import { Toast } from 'vue-toast-notification'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(Toast, {
  position: 'bottom-left'
});
app.mount('#app')