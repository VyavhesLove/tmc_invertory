<template>
  <div class="main-content">
    <h2>{{ title }}</h2>

    <form @submit.prevent="handleSubmit">
      <!-- Основные поля -->
      <div>
        <label>Наименование:</label>
        <input v-model="form.name" required />
      </div>

        <div>
        <label>Серийный номер:</label>
        <input v-model="form.serial_number" :disabled="form.serial_missing" />
        <div class="serial-missing-row reverse">
            <input type="checkbox" v-model="form.serial_missing" id="serial_missing" />
            <label for="serial_missing">Серийный номер отсутствует</label>
        </div>
        </div>

      <div>
        <label>Бренд:</label>
        <input v-model="form.brand" />
      </div>

      <!-- Остальные поля только для просмотра -->
      <div>
        <label>Статус:</label>
        <input :value="currentStatus" disabled />
      </div>

      <div>
        <label>Ответственный:</label>
        <input :value="currentResponsible" disabled />
      </div>

      <div>
        <label>Локация:</label>
        <input :value="currentLocation" disabled />
      </div>

      <button type="submit">💾 Создать</button>
    </form>

    <p v-if="message">{{ message }}</p>

    <button @click="back" class="logout-button mt-2">⬅ Вернуться к списку ТМЦ</button>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import {
  loadLocations, loadResponsibleNames, loadStatuses,
  loadItem, submitForm, back, message
} from '@/utils/apiHelpers.js'

// пропс для режима
const props = defineProps({
  mode: { type: String, default: 'new' } // 'new' | 'analog'
})

const form = reactive({
  name: '',
  serial_number: '',
  brand: '',
  status: '',
  responsible_id: null,
  location_id: null,
  serial_missing: false
})

// дополнительные поля (для просмотра)
const currentStatus = ref('')
const currentResponsible = ref('')
const currentLocation = ref('')

const title = computed(() =>
  props.mode === 'analog' ? 'Создать по аналогии' : 'Создать новый ТМЦ'
)

onMounted(async () => {
  await Promise.all([
    loadLocations(),
    loadResponsibleNames(),
    loadStatuses()
  ])

  if (props.mode === 'analog') {
    const savedId = localStorage.getItem('selectedItemId')
    if (savedId) {
      const item = await loadItem(savedId)
      if (!item) return
        form.name = item.name
        form.serial_number = item.serial_number
        form.brand = item.brand
        form.status = item.status_id
        form.responsible_id = item.responsible_id
        form.location_id = item.location_id

        currentStatus.value = item.status
        currentResponsible.value = item.responsible_name
        currentLocation.value = item.location
    }
  }
})

async function handleSubmit() {
  await submitForm(form)
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

.serial-missing-row.reverse {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
  width: max-content;
}

.serial-missing-row.reverse label {
  margin: 0;
  white-space: nowrap;
}

.serial-missing-row.reverse input[type="checkbox"] {
  order: 2;
}

</style>