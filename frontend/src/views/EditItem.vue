<template>
  <div class="main-content">
    <h2>Редактировать ТМЦ</h2>

    <form @submit.prevent="handleSubmit">
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

      <!-- Только просмотр -->
      <div>
        <label>Статус:</label>
        <input :value="item.status_name" disabled />
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

    <button @click="backToList" class="logout-button mt-2">⬅ Вернуться к списку ТМЦ</button>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import { loadItem, submitForm, backToList, message, showError } from '@/utils/apiHelpers'

const form = reactive({
  name: '',
  serial_number: '',
  brand: ''
})

const item = reactive({
  responsible_name: '',
  location_name: '',
  status_name: ''
})

const itemId = ref(null)

async function initForm(id) {
  const data = await loadItem(id)
  if (!data) return
  form.name = data.name
  form.serial_number = data.serial_number
  form.brand = data.brand

  item.status_name = data.status_name || data.status || '—'
  item.responsible_name = data.responsible_name
  item.location_name = data.location_name
}

async function handleSubmit() {
  await submitForm(form, 'edit', itemId.value)
}

onMounted(async () => {
  const savedId = localStorage.getItem('selectedItemId')
  if (savedId) {
    itemId.value = savedId
    await initForm(savedId)
  } else {
    message.value = 'ID ТМЦ не найден в localStorage'
    showError('ID ТМЦ не найден в localStorage')
    backToList()
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