<template>
  <div>
    <!-- <h1>Учёт ТМЦ</h1> -->    
    <div v-if="!isAuthed">
      <LoginForm />
    </div>
    <div v-else>
      <!-- <Sidebar /> -->
      <router-view />
      <button @click="logout">Выйти</button>
      <ItemsList />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from './stores/auth'
import LoginForm from './components/LoginForm.vue'
import ItemsList from './components/ItemsList.vue'
// import Sidebar from './components/layout/Sidebar.vue'
// import CreateItem from './views/CreateItem.vue'

const auth = useAuthStore()
const isAuthed = computed(() => !!auth.token)

function logout() {
  auth.logout()
  window.location.reload()
}
</script>