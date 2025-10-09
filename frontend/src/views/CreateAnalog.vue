<template>
  <div class="main-content">
    <h2>Создать по аналогии</h2>
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
          <!-- Добавь остальные статусы -->
        </select>
      </div>
      <div>
        <label>Ответственный:</label>
        <select v-model="form.responsible_id" required>
          <option disabled value="">Выберите пользователя</option>
          <option v-for="res in responsible_names" :key="res.id" :value="res.id">
            {{ res.username }}
          </option>
        </select>
      </div>
      <div>
        <label>Локация:</label>
        <select v-model="form.location_id" required>
          <option disabled value="">Выберите локацию</option>
          <option v-for="loc in locations" :key="loc.id" :value="loc.id">
            {{ loc.location }}
          </option>
        </select>
      </div>
      <button type="submit">Создать</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <!-- Кнопка для выхода -->
    <button @click="back" class="logout-button mt-2">к списку ТМЦ</button>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
//import axios from 'axios'
import api from '@/api/axios' // или '../api/axios' я хз

const form = reactive({
  name: '',
  serial_number: '',
  brand: '',
  status: '',
  responsible_id: null,
  location_id: null
})

const responsible_names = ref([])
const locations = ref([])
const message = ref('')
const itemId = ref(null)
const statusMap = {
  "В работе": "at_work",
  "В ремонте": "in_repair",
  "Выдано": "issued",
  "Доступно": "available",
  "Подтвердить ТМЦ": "confirm",
  "Подтвердить ремонт": "confirm_repair"
}

async function loadLocations() {
  try {
    const res = await api.get('/locations')
    locations.value = res.data
  } catch (e) {
    message.value = 'Ошибка загрузки локаций: ' + (e.response?.data?.detail || e.message)
  }
}

async function loadResponsibleNames() {
  try {
    const res = await api.get('/users')
    responsible_names.value = res.data
  } catch (e) {
    message.value = 'Ошибка загрузки пользователей: ' + (e.response?.data?.detail || e.message)
  }
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
    const response = await api.post('/items/', form)
    message.value = 'ТМЦ успешно создан: ID ' + response.data.id
    // Можно очистить форму, если нужно
    // Object.keys(form).forEach(key => form[key] = '')
  } catch (e) {
    message.value = 'Ошибка при создании: ' + (e.response?.data?.detail || e.message)
  }
}

onMounted(() => {
  const savedId = localStorage.getItem('selectedItemId')
  if (savedId) {
    itemId.value = savedId
    loadItem(savedId)
  }
  loadLocations()
  loadResponsibleNames()
})

// Функция возврата, редирект на http://localhost/
function back() {
  window.location.href = 'http://localhost/'
}

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
