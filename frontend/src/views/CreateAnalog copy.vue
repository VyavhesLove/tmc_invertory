<template>
  <div class="main-content">
    <h2>Создать по аналогии</h2>
    <form @submit.prevent="submitForm">
      <div>
        <label>Наименование:</label>
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
import {
  loadLocations, locations,
  loadResponsibleNames, responsible_names,
  loadStatuses, statuses,
  submitForm,
  loadItem,
  back,
  message
} from '@/utils.js'

const form = reactive({
  name: '',
  serial_number: '',
  brand: '',
  status: '',
  responsible_id: null,
  location_id: null
})

const itemId = ref(null)

async function handleSubmit() {
  await submitForm(form)
}

onMounted(async () => {
  await Promise.all([
    loadLocations(),
    loadResponsibleNames(),
    loadStatuses()
  ])
  
  const savedId = localStorage.getItem('selectedItemId')
  if (savedId) {
    itemId.value = savedId
    await loadItem(savedId, form)
  }
})

function handleBack() {
  back()
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
