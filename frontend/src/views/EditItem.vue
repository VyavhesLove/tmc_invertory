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

      <!-- Остальные поля — только для просмотра -->
      <div>
        <label>Статус:</label>
        <input
          :value="item.status_name"
          disabled
        />
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

    <button @click="back" class="logout-button mt-2">⬅ Вернуться к списку ТМЦ</button>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import api from '@/api/axios'

const form = reactive({
  name: '',
  serial_number: '',
  brand: '',
  status_id: null
})

const item = reactive({
  responsible_name: '',
  location_name: '',
  status_name: ''
})

const statuses = ref([])     // ✅ список статусов
const message = ref('')
const itemId = ref(null)

// -----------------------------
// Загрузка всех статусов
// -----------------------------
async function loadStatuses() {
  try {
    const res = await api.get('/statuses')
    statuses.value = res.data
    console.log('📦 Загружены статусы:', statuses.value)
  } catch (e) {
    message.value = 'Ошибка загрузки статусов: ' + (e.response?.data?.detail || e.message)
  }
}

// -----------------------------
// Загрузка карточки ТМЦ
// -----------------------------
async function loadItem(id) {
  try {
    const { data } = await api.get(`/items/${id}`)
    console.log('📦 Загружен ТМЦ:', data)

    form.name = data.name
    form.serial_number = data.serial_number
    form.brand = data.brand
    item.status_name = data.status_name || data.status || '—'
    item.responsible_name = data.responsible_name
    item.location_name = data.location_name
  } catch (e) {
    message.value = 'Ошибка загрузки: ' + (e.response?.data?.detail || e.message)
  }
}

// -----------------------------
// Сохранение изменений
// -----------------------------
async function submitForm() {
  try {
    if (!itemId.value) {
      message.value = 'ID ТМЦ не найден.'
      return
    }

    const payload = {
      name: form.name,
      serial_number: form.serial_number,
      brand: form.brand,
      status_id: form.status_id // ✅ теперь отправляем ID статуса
    }

    const { data } = await api.put(`/items/${itemId.value}`, payload)
    message.value = `✅ ТМЦ обновлён: ID ${data.id}`
  } catch (e) {
    message.value = 'Ошибка при обновлении: ' + (e.response?.data?.detail || e.message)
  }
}

// -----------------------------
// Кнопка "Назад"
// -----------------------------
const back = () => {
  window.location.href = 'http://localhost/'
}

// -----------------------------
// Инициализация
// -----------------------------
onMounted(async () => {
  await loadStatuses() // ✅ сначала статусы
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