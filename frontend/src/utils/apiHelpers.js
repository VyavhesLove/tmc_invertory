// src/utils.js
import api from '@/api/axios' // импорт API для запросов
import { ref } from 'vue'

// общие реактивные переменные
export const locations = ref([])
export const responsible_names = ref([])
export const statuses = ref([])
export const message = ref('')

export async function loadItem(id) {
  try {
    const { data } = await api.get(`/items/${id}`)
    return data // ⚠️ Обязательно возвращаем результат
  } catch (e) {
    message.value = 'Ошибка загрузки ТМЦ: ' + (e.response?.data?.detail || e.message)
    return null
  }
}

// Загрузка одного ТМЦ по ID уже устарела
export async function loadItemOld(id, form) {
  try {
    const { data } = await api.get(`/items/${id}`)
    // Заполним переданную форму
    form.name = data.name || ''
    form.serial_number = data.serial_number || ''
    form.brand = data.brand || ''
    form.status = data.status_id || null
    form.responsible_id = data.responsible_id || null
    form.location_id = data.location_id || null
    message.value = `Загружен ТМЦ: ${data.name}`
  } catch (e) {
    message.value = 'Ошибка загрузки ТМЦ: ' + (e.response?.data?.detail || e.message)
  }
}

// функции загрузки локаций иResponsibles
export async function loadLocations() {
  try {
    const res = await api.get('/locations')
    locations.value = res.data
  } catch (e) {
    message.value = 'Ошибка загрузки локаций: ' + (e.response?.data?.detail || e.message)
  }
}

export async function loadResponsibleNames() {
  try {
    const res = await api.get('/users')
    responsible_names.value = res.data
  } catch (e) {
    message.value = 'Ошибка загрузки пользователей: ' + (e.response?.data?.detail || e.message)
  }
}

export async function loadStatuses() {
  try {
    const res = await api.get('/statuses')
    statuses.value = res.data
  } catch (e) {
    message.value = 'Ошибка загрузки статусов: ' + (e.response?.data?.detail || e.message)
  }
}

// функция отправки формы
export async function submitForm(form) {
  try {
    const response = await api.post('/items/', form)
    message.value = 'ТМЦ успешно создан: ID ' + response.data.id
    // очистка формы (если нужно)
    Object.keys(form).forEach(key => {
      if (typeof form[key] === 'string') {
        form[key] = ''
      } else {
        form[key] = null
      }
    })
  } catch (e) {
    message.value = 'Ошибка при создании: ' + (e.response?.data?.detail || e.message)
  }
}

// функция возврата на главную
export function back() {
  window.location.href = 'http://localhost/'
}