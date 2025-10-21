import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import ItemsList from '../components/ItemsList.vue' // список ТМЦ
import CreateItem from '../views/CreateItem.vue' // страница создания
import CreateAnalog from '../views/CreateAnalog.vue' // страница создания аналога
import EditItem from '../views/EditItem.vue'     // страница редактирования
import TransferItem from '../views/TransferItem.vue'     // страница передачи
import LoginForm from '../components/LoginForm.vue' // страница входа

const routes = [
  { path: '/items-list', name: 'ItemsList', component: ItemsList },
  { path: '/create-item', name: 'CreateItem', component: CreateItem },
  { path: '/create-analog', name: 'CreateAnalog', component: CreateAnalog },
  { path: '/edit-item', name: 'EditItem', component: EditItem },
  { path: '/transfer-item', name: 'TransferItem', component: TransferItem },
  { path: '/login', name: 'Login', component: LoginForm },
  { path: '/:pathMatch(.*)*', redirect: '/items-list' } // fallback
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// --- Глобальный guard ---
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // Разрешаем доступ к странице логина всегда
  if (to.name === 'Login') {
    return next()
  }

  const isAuthenticated = authStore.token && authStore.isTokenValid

  if (!isAuthenticated) {
    // Сохраняем путь, чтобы вернуть пользователя после логина
    localStorage.setItem('redirectAfterLogin', to.fullPath)
    return next({ name: 'Login' })
  }

  next()
})

export default router
