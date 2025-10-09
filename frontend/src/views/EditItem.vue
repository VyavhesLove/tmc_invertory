<template>
  <div class="main-content">
    <h2>Создать ТМЦ по аналогии</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label>Название:</label>
        <input v-model="form.name" required />
      </div>
      <div>
        <label>Серийный номер:</label>
        <input v-model="form.serial_number" />
      </div>
      <div>
        <label>Бренд:</label>
        <input v-model="form.brand" />
      </div>
      <div>
        <label>Статус:</label>
        <select v-model="form.status">
          <option value="at_work">В работе</option>
          <option value="in_repair">В ремонте</option>
          <option value="issued">Выдано</option>
          <option value="available">Доступно</option>
          <option value="confirm">Подтвердить ТМЦ</option>
          <option value="confirm_repair">Подтвердить ремонт</option>
        </select>
      </div>
      <div>
        <label>Ответственный:</label>
        <input v-model="form.responsible" />
      </div>
      <div>
        <label>Локация:</label>
        <input v-model="form.location" />
      </div>
      <button type="submit">Записать</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <!-- Кнопка для выхода -->
    <button @click="back" class="logout-button mt-2">к списку ТМЦ</button>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import api from '@/api/axios'

const form = reactive({
  name: '',
  serial_number: '',
  brand: '',
  status: '',
  responsible: '',
  location: ''
})

const message = ref('')
const itemId = ref(null)

const back = () => {
  window.location.href = 'http://localhost/' // можно заменить на router.push('/')
}

const statusMap = {
  "В работе": "at_work",
  "В ремонте": "in_repair",
  "Выдано": "issued",
  "Доступно": "available",
  "Подтвердить ТМЦ": "confirm",
  "Подтвердить ремонт": "confirm_repair"
}

async function loadItem(id) {
  try {
    const { data } = await api.get(`/items/${id}`)
    Object.assign(form, data)
    form.status = statusMap[data.status] || 'confirm'
  } catch (e) {
    message.value = 'Ошибка загрузки: ' + (e.response?.data?.detail || e.message)
  }
}

async function submitForm() {
  try {
    if (!itemId.value) {
      message.value = 'ID ТМЦ не найден.'
      return
    }
    const { data } = await api.put(`/items/${itemId.value}`, form)
    message.value = `ТМЦ обновлён: ID ${data.id}`
  } catch (e) {
    message.value = 'Ошибка при обновлении: ' + (e.response?.data?.detail || e.message)
  }
}

onMounted(() => {
  const savedId = localStorage.getItem('selectedItemId')
  if (savedId) {
    itemId.value = savedId
    loadItem(savedId)
  }
})
</script>

<style scoped>
form div {
  margin-bottom: 10px;
}
label {
  display: inline-block;
  width: 120px;
}
input, select {
  padding: 5px;
  width: 200px;
}
button {
  padding: 6px 15px;
}
.mt-2 {
  margin-top: 10px;
}
</style>