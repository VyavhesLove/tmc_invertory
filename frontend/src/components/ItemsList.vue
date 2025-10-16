<template>
  <div class="app-container">
    <Sidebar />
    <div class="main-content">
      <h2>Список ТМЦ</h2>
      <button @click="fetchItems">Обновить</button>
      <p v-if="error" style="color:red">{{ error }}</p>
      <table border="1" cellpadding="4">
        <thead>
          <tr>
            <th>
              №
              <span @click="toggleFilter('id')" style="cursor:pointer">🔍</span>
              <input v-if="showFilters.id" v-model="filters.id" placeholder="Фильтр..." style="width:70px" @input="resetPage" />
            </th>
            <th>
              Наименование
              <span @click="toggleFilter('name')" style="cursor:pointer">🔍</span>
              <input v-if="showFilters.name" v-model="filters.name" placeholder="Фильтр..." style="width:100px" @input="resetPage" />
            </th>
            <th>
              Серийный номер
              <span @click="toggleFilter('serial_number')" style="cursor:pointer">🔍</span>
              <input v-if="showFilters.serial_number" v-model="filters.serial_number" placeholder="Фильтр..." style="width:100px" @input="resetPage" />
            </th>
            <th>
              Бренд
              <span @click="toggleFilter('brand')" style="cursor:pointer">🔍</span>
              <input v-if="showFilters.brand" v-model="filters.brand" placeholder="Фильтр..." style="width:100px" @input="resetPage" />
            </th>
            <th>
              Статус
              <span @click="toggleFilter('status_name')" style="cursor:pointer">🔍</span>
              <select v-if="showFilters.status_name" v-model="filters.status_name" @change="resetPage">
                <option value="">-- Все --</option>
                <option v-for="opt in statuses" :key="opt.id" :value="opt.status">{{ opt.status }}</option>
              </select>
            </th>
            <th>
              Ответственный
              <span @click="toggleFilter('responsible_name')" style="cursor:pointer">🔍</span>
              <input
                v-if="showFilters.responsible_name"
                v-model="filters.responsible_name"
                placeholder="Фильтр..."
                style="width:100px"
                @input="resetPage"
              />
            </th>
            <th>
              Локация
              <span @click="toggleFilter('location')" style="cursor:pointer">🔍</span>
              <input v-if="showFilters.location" v-model="filters.location" placeholder="Фильтр..." style="width:100px" @input="resetPage" />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="item in pagedItems" 
            :key="item.id"
            @click="selectItem(item.id)"
            :class="{ selected: selectedItemId === item.id }"
            style="cursor: pointer;"
          >
            <td>{{ item.id }}</td>
            <td>{{ item.name }}</td>
            <td>{{ item.serial_number }}</td>
            <td>{{ item.brand }}</td>
            <td>{{ item.status_name || '—' }}</td>
            <td>{{ item.responsible_name || '—' }}</td>
            <td>{{ item.location_name || '—' }}</td>
          </tr>
          <tr v-if="pagedItems.length === 0">
            <td colspan="7" style="text-align:center;color:gray">Нет данных</td>
          </tr>
        </tbody>
      </table>
      <div style="margin-top:10px;">
        Кол-во на странице:
        <select v-model.number="perPage">
          <option v-for="n in [5,10,25,50,100]" :key="n" :value="n">{{ n }}</option>
        </select>
        <button :disabled="page === 1" @click="prevPage">Назад</button>
        Страница {{ page }} из {{ pageCount }}
        <button :disabled="page === pageCount" @click="nextPage">Вперёд</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import api from '../api/axios'
import Sidebar from './layout/Sidebar.vue'

const items = ref([])
const statuses = ref([]) // ✅ список статусов
const error = ref(null)
const page = ref(1)
const perPage = ref(10)
const selectedItemId = ref(localStorage.getItem('selectedItemId') ? Number(localStorage.getItem('selectedItemId')) : null)

// ========================
// Фильтры
// ========================
const filters = ref({
  id: '', name: '', serial_number: '', brand: '',
  status_name: '', responsible_name: '', location: ''
})
const showFilters = ref({
  id: false, name: false, serial_number: false, brand: false,
  status_name: false, responsible_name: false, location: false
})
function toggleFilter(key) {
  showFilters.value[key] = !showFilters.value[key]
}
function resetPage() {
  page.value = 1
}

// ========================
// Получение списка статусов
// ========================
async function fetchStatuses() {
  try {
    const res = await api.get('/statuses')
    statuses.value = res.data
    console.log('Statuses loaded:', statuses.value)
  } catch (e) {
    console.error('Ошибка загрузки статусов:', e)
  }
}

// ========================
// Получение списка ТМЦ
// ========================
async function fetchItems() {
  try {
    const res = await api.get('/items/')
    console.log('API /items response:', res.data)

    const data = Array.isArray(res.data) ? res.data : []
    const normalized = data.map(item => {
      // находим название статуса по status_id
      const foundStatus = statuses.value.find(s => s.id === item.status_id)
      return {
        id: item.id ?? null,
        name: item.name ?? '',
        serial_number: item.serial_number ?? '',
        brand: item.brand ?? '',
        status_id: item.status_id ?? null,
        status_name: foundStatus ? foundStatus.status : '', // ✅ отображаем название
        responsible_name: item.responsible_name ?? item.responsible ?? '',
        location_name: item.location_name ?? item.location ?? '',
        location_id: item.location_id ?? null,
        comment: item.comment ?? null
      }
    })

    items.value = normalized
    page.value = 1
    console.log('Normalized items:', items.value)
  } catch (e) {
    console.error('fetchItems error', e)
    error.value = e?.response?.data?.detail || e.message
  }
}

// ========================
// Компьютед фильтрация
// ========================
const filteredItems = computed(() => {
  return items.value.filter(it => {
    return Object.entries(filters.value).every(([key, val]) => {
      if (!val) return true
      return String(it[key] ?? '').toLowerCase().includes(String(val).toLowerCase())
    })
  })
})

// ========================
// Пагинация
// ========================
const pageCount = computed(() => Math.max(1, Math.ceil(filteredItems.value.length / perPage.value)))
const pagedItems = computed(() => {
  const start = (page.value - 1) * perPage.value
  return filteredItems.value.slice(start, start + perPage.value)
})
function prevPage() { if (page.value > 1) page.value-- }
function nextPage() { if (page.value < pageCount.value) page.value++ }
watch([perPage], resetPage)

function selectItem(id) {
  selectedItemId.value = id
  localStorage.setItem('selectedItemId', id)
}

// ========================
// Инициализация
// ========================
onMounted(async () => {
  await fetchStatuses() // сначала грузим статусы
  await fetchItems()    // потом сами ТМЦ
})
</script>

<style scoped>
.selected {
  background-color: #80c1ff;
}
</style>