<template>
  <div>
    <h2>Вход</h2>
    <form @submit.prevent="doLogin">
      <div><input v-model="username" placeholder="username" /></div>
      <div><input v-model="password" type="password" placeholder="password" /></div>
      <button type="submit">Войти</button>
    </form>
    <p v-if="error" style="color:red">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import router from '../router'
import config from '../config'

const username = ref('')
const password = ref('')
const error = ref(null)
const auth = useAuthStore()

onMounted(() => {
  if (config.environment === 'dev') {
    username.value = 'admin'
    password.value = 'admin'
  }
})

async function doLogin() {
  error.value = null
  try {
    await auth.login(username.value, password.value)
    // после успешного логина перенаправляем на сохранённый путь или на список ТМЦ
    const redirect = localStorage.getItem('redirectAfterLogin') || '/items-list'
    localStorage.removeItem('redirectAfterLogin')
    router.push(redirect)
  } catch (e) {
    error.value = e?.response?.data?.detail || e.message || 'Ошибка входа'
  }
}
</script>
