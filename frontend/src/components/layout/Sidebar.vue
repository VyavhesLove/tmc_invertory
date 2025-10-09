<template>
  <nav :class="['sidebar', { collapsed }]">
    <div class="sidebar-header">
      <h3 v-if="!collapsed">Учёт ТМЦ</h3>
      <button class="toggle-btn" @click="toggleCollapse" :aria-expanded="!collapsed" :title="collapsed ? 'Развернуть' : 'Свернуть'">
        <span v-if="collapsed">»</span>
        <span v-else>«</span>
      </button>
    </div>

    <ul class="menu">
      <li v-for="item in menuItems" :key="item.label" class="menu-item" @click="onMenuClick(item)">
        <i :class="item.icon" aria-hidden="true"></i>
        <span v-if="!collapsed" class="label">{{ item.label }}</span>
      </li>
    </ul>

    <div class="bottom-section">
      <!-- ThemeSwitcher. Если у тебя внешняя реализация, импортируй её -->
      <ThemeSwitcher v-if="!collapsed" />
      <button v-else class="theme-btn" @click="toggleTheme" title="Тема">🌓</button>
      <!-- <ThemeSwitcher :compact="collapsed" /> -->

      <button class="logout-btn" @click="logout">
        <i class="fas fa-sign-out-alt"></i>
        <span v-if="!collapsed">Выйти</span>
      </button>
    </div>
  </nav>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import ThemeSwitcher from '../ThemeSwitcher.vue'
import { useDark, useToggle } from '@vueuse/core'
import { useRouter } from 'vue-router'

const isDark = useDark()
const toggleTheme = useToggle(isDark)

const collapsed = ref(false)

function toggleCollapse() {
  collapsed.value = !collapsed.value
}

// пробрасываем ширину сайдбара в CSS-переменную корня, чтобы основной контент подстраивался
watch(collapsed, val => {
  const w = val ? '70px' : '230px'
  document.documentElement.style.setProperty('--sidebar-width', w)
})

onMounted(() => {
  // инициализация
  document.documentElement.style.setProperty('--sidebar-width', collapsed.value ? '70px' : '230px')
})

function logout() {
  // Попытка аккуратно выйти: сначала вызвать глобальную функцию, если есть,
  // иначе удалить типичные ключи из localStorage и перезагрузить страницу.
  try {
    if (window.auth && typeof window.auth.logout === 'function') {
      window.auth.logout()
    } else {
      // попробуем несколько распространённых ключей
      ['access_token','token','auth_token','user'].forEach(k => localStorage.removeItem(k))
    }
  } catch (e) {
    // ignore
  }
  window.location.reload()
}

// Простой обработчик клика по пунктам меню.
// Сейчас просто логируем; можно заменить на router push или на emit событий.
// function onMenuClick(item) {
//  if (item.action && typeof item.action === 'function') {
//    item.action()
//    return
  //  }
  // Если нужно — реализуй здесь навигацию по v-if экранам:
  // emit('navigate', item.key) или router.push(item.to)
//  console.log('menu click', item.label)
//}

const router = useRouter()

function onMenuClick(item) {
  if (item.to) {
    router.push(item.to)
  } else {
    console.log('menu click', item.label)
  }
}

const menuItems = [
  { label: 'Создать ТМЦ', icon: 'fas fa-plus', to: '/create-item' },
  { label: 'Создать по аналогии', icon: 'fas fa-copy', to: '/create-analog' },
  { label: 'Редактировать ТМЦ', icon: 'fas fa-pen', to: '/edit-item' },
  { label: 'Передать ТМЦ', icon: 'fas fa-share' },
  { label: 'В работу', icon: 'fas fa-hammer' },
  { label: 'Отправить в сервис', icon: 'fas fa-tools' },
  { label: 'Вернуть из сервиса', icon: 'fas fa-undo' },
  { label: 'Аналитика', icon: 'fas fa-chart-line' },
  { label: 'Списание/затраты', icon: 'fas fa-trash' },
  { label: 'Профиль пользователя', icon: 'fas fa-user' }
]
</script>

<style scoped>
.sidebar {
  position: fixed;
  left: 0;
  top: 0;
  height: 100vh;
  width: 230px;
  background: var(--sidebar-bg, #111);
  color: var(--sidebar-text, #fff);
  display: flex;
  flex-direction: column;
  padding: 10px;
  transition: width .25s ease;
  box-sizing: border-box;
  border-right: 1px solid rgba(255,255,255,0.04);
  z-index: 1000;
}

.sidebar.collapsed {
  width: 70px;
}

.sidebar-header { display:flex; justify-content:space-between; align-items:center; padding: 6px 4px; }
.toggle-btn {
  border: none;
  background: none;
  color: inherit;
  cursor: pointer;
  font-size: 14px;
}

/* меню */
.menu { list-style:none; padding:0; margin-top:12px; flex:1; overflow:auto; }
.menu-item {
  display:flex;
  align-items:center;
  gap:10px;
  padding:8px 6px;
  cursor:pointer;
  border-radius:6px;
}
.menu-item i { width:20px; text-align:center; }
.menu-item:hover { background: rgba(255,255,255,0.03); }

/* низ */
/*.bottom-section { padding-top:8px; border-top:1px solid rgba(255,255,255,0.03); display:flex; flex-direction:column; gap:8px; }
.theme-btn { border:none; background:transparent; color:inherit; cursor:pointer; font-size:18px; }
.logout-btn {
  border: none;
  background: transparent;
  color: #ffdddd;
  display:flex;
  gap:8px;
  align-items:center;
  padding:6px;
  cursor:pointer;
}
.logout-btn i { width:20px; text-align:center; }*/
</style>