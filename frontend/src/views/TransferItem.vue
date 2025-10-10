<template>
  <div class="main-content">
    <h2>Передача ТМЦ</h2>
    <form @submit.prevent="submitTransfer">
      <div>
        <label>Объект назначения</label>
        <select v-model="form.location_id" required>
          <option disabled value="">Выберите объект</option>
          <option v-for="loc in locations" :key="loc.id" :value="loc.id">
            {{ loc.location }}
          </option>
        </select>
      </div>
      <div>
        <label>Ответственный</label>
        <select v-model="form.responsible_id" required>
          <option disabled value="">Выберите ответственного</option>
          <option v-for="user in responsible_names" :key="user.id" :value="user.id">
            {{ user.username }}
          </option>
        </select>
      </div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Наименование</th>
            <th>Серийный номер</th>
            <th>Текущее местоположение</th>
            <th>Текущий ответственный</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="form">
            <td>{{ form.id }}</td>
            <td>{{ form.name }}</td>
            <td>{{ form.serial_number }}</td>
            <td>{{ form.location_name  }}</td>
            <td>{{ form.responsible_name  }}</td>
          </tr>
        </tbody>
      </table>
      <button type="submit">Подтвердить передачу</button>
    </form>
    <p v-if="message">{{ message }}</p>
    <button @click="back" class="logout-button mt-2">к списку ТМЦ</button>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import api from '@/api/axios'

const form = reactive({
  location_id: null,
  responsible_id: null
})

const item = ref(null)               // текущий объект ТМЦ
const itemId = ref(null)             // id выбранного объекта
const responsible_names = ref([])    // список ответственных
const locations = ref([])            // список локаций
const message = ref('')

const back = () => {
  window.location.href = 'http://localhost/' // можно заменить на router.push('/')
}

// Основная функция загрузки объекта по аналогии
async function loadItem(id) {
  try {
    const { data } = await api.get(`/items/${id}`)
    form.id = data.id
    form.name = data.name
    form.serial_number = data.serial_number
    form.responsible_id = data.responsible_id
    form.location_id = data.location_id

    // Получить имена по id асинхронно
    form.location_name = await loadLocationNameById(data.location_id)
    form.responsible_name = await loadResponsibleNameById(data.responsible_id)
    
  } catch (e) {
    message.value = 'Ошибка загрузки: ' + (e.response?.data?.detail || e.message)
  }
}

async function loadLocations() {
  try {
    const res = await api.get('/locations')
    locations.value = res.data
    console.log('loc', res.data)
  } catch (e) {
    message.value = 'Ошибка загрузки локаций: ' + (e.response?.data?.detail || e.message)
  }
}

// Получить имя локации по id
async function loadLocationNameById(id) {
  try {
    const res = await api.get('/locations')
    const loc = res.data.find(location => location.id === id)
    if (loc) {
      return loc.location
    }
    return ''
  } catch (e) {
    message.value = 'Ошибка загрузки локаций: ' + (e.response?.data?.detail || e.message)
    return ''
  }
}

async function loadResponsibleNames() {
  try {
    const res = await api.get('/users')
    responsible_names.value = res.data
    console.log('res', res.data)
  } catch (e) {
    message.value = 'Ошибка загрузки ответственных: ' + (e.response?.data?.detail || e.message)
  }
}

// Получить имя ответственного по id
async function loadResponsibleNameById(id) {
  try {
    const res = await api.get('/users')
    const user = res.data.find(user => user.id === id)
    if (user) {
      return user.username
    }
    return ''
  } catch (e) {
    message.value = 'Ошибка загрузки ответственных: ' + (e.response?.data?.detail || e.message)
    return ''
  }
}

async function submitTransfer() {
  if (!form.location_id || !form.responsible_id) {
    message.value = 'Выберите и локацию и ответственного'
    return
  }

  try {
    // Вытаскиваем id редактируемого объекта (ТМЦ)
    const id = form.id
    if (!id) {
      message.value = 'ID ТМЦ не определён'
      return
    }
    // Передаем только нужные поля
    const payload = {
      name: form.name, // обязательно для API
      location_id: form.location_id,
      responsible_id: form.responsible_id
    }
    const res = await api.put(`/items/${id}`, payload)
    message.value = 'Передача успешно подтверждена'
  } catch (e) {
    message.value = 'Ошибка при передаче: ' + (e.response?.data?.detail || e.message)
  }
}

// загрузка текущего объекта, локаций и ответственных при монтировании
onMounted(() => {
  const savedId = localStorage.getItem('selectedItemId')
  if (savedId) {
    itemId.value = savedId
    loadItem(savedId)
  }
  loadLocations()
  loadResponsibleNames()
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