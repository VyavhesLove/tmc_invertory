import { createRouter, createWebHistory } from 'vue-router'
import CreateItem from '../views/CreateItem.vue' // страница создания
import CreateAnalog from '../views/CreateAnalog.vue' // страница создания аналога
import EditItem from '../views/EditItem.vue'     // страница редактирования

const routes = [
  { path: '/create-item', name: 'CreateItem', component: CreateItem },
  { path: '/create-analog', name: 'CreateAnalog', component: CreateAnalog },
  { path: '/edit-item', name: 'EditItem', component: EditItem },
  // сюда позже можно добавить другие страницы
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router