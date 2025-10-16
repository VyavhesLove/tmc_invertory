<template>
  <div class="main-content">
    <h2>Редактировать ТМЦ</h2>
    <form @submit.prevent="submitForm">
      <!-- Название -->
      <div>
        <label>Наименование:</label>
        <input v-model="form.name" required />
      </div>

      <!-- Серийный номер -->
      <div>
        <label>Серийный номер:</label>
        <input v-model="form.serial_number" />
      </div>

      <!-- Бренд -->
      <div>
        <label>Бренд:</label>
        <input v-model="form.brand" />
      </div>

      <!-- Нередактируемые поля -->
      <div>
        <label>Статус:</label>
        <input :value="item.status" disabled />
      </div>

      <div>
        <label>Ответственный:</label>
        <input :value="item.responsible_name" disabled />
      </div>

      <div>
        <label>Локация:</label>
        <input :value="item.location_name" disabled />
      </div>

      <button type="submit">💾 Сохранить изменения</button>
    </form>

    <p v-if="message">{{ message }}</p>

    <!-- Кнопка возврата -->
    <button @click="back" class="logout-button mt-2">⬅ Вернуться к списку ТМЦ</button>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import api from '@/api/axios'

const form = reactive({
  name: '',
  serial_number: '',
  brand: ''
})

const item = reactive({
  status: '',
  responsible_name: '',
  location_name: ''
})

const message = ref('')
const itemId = ref(null)

// Загрузка данных ТМЦ по ID
async function loadItem(id) {
  try {
    const { data } = await api.get(`/items/${id}`)
    form.name = data.name
    form.serial_number = data.serial_number
    form.brand = data.brand
    item.status = data.status
    item.responsible_name = data.responsible_name
    item.location_name = data.location_name
  } catch (e) {
    message.value = 'Ошибка загрузки: ' + (e.response?.data?.detail || e.message)
  }
}

// Отправка обновления
async function submitForm() {
  try {
    if (!itemId.value) {
      message.value = 'ID ТМЦ не найден.'
      return
    }

    const payload = {
      name: form.name,
      serial_number: form.serial_number,
      brand: form.brand
    }

    const { data } = await api.put(`/items/${itemId.value}`, payload)
    message.value = `✅ ТМЦ обновлён: ID ${data.id}`
  } catch (e) {
    message.value = 'Ошибка при обновлении: ' + (e.response?.data?.detail || e.message)
  }
}

// Возврат к списку
const back = () => {
  window.location.href = 'http://localhost/' // можно заменить на router.push('/')
}

// При монтировании — загрузить данные
onMounted(async () => {
  const savedId = localStorage.getItem('selectedItemId')
  if (savedId) {
    itemId.value = savedId
    await loadItem(savedId)
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
input {
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