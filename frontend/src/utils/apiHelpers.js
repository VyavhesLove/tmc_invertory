import { ref } from 'vue'
import {
  fetchItem, createItem, fetchLocations, fetchUsers, fetchStatuses
} from '@/api/items'

export const locations = ref([])
export const responsible_names = ref([])
export const statuses = ref([])
export const message = ref('')

// --- Загрузка справочников ---
export async function loadLocations() {
  try {
    locations.value = await fetchLocations()
  } catch (e) {
    message.value = 'Ошибка загрузки локаций: ' + e.message
  }
}
// --- Загрузка ответственных ---
export async function loadResponsibleNames() {
  try {
    responsible_names.value = await fetchUsers()
  } catch (e) {
    message.value = 'Ошибка загрузки пользователей: ' + e.message
  }
}

export async function loadStatuses() {
  try {
    statuses.value = await fetchStatuses()
  } catch (e) {
    message.value = 'Ошибка загрузки статусов: ' + e.message
  }
}

// --- Загрузка одного ТМЦ ---
export async function loadItem(id) {
  try {
    return await fetchItem(id)
  } catch (e) {
    message.value = 'Ошибка загрузки ТМЦ: ' + e.message
    return null
  }
}

// --- Создание ---
//export async function submitForm(form) {
//  try {
//    const data = await createItem(form)
//    message.value = `✅ ТМЦ создан: ID ${data.id}`
//    Object.keys(form).forEach(k => (form[k] = typeof form[k] === 'string' ? '' : null))
//  } catch (e) {
//    message.value = 'Ошибка при создании: ' + e.message
//  }
//}

export async function submitForm(form) {
  try {
    const data = await createItem(form)
    message.value = `✅ ТМЦ создан: ID ${data.id}`
    // очистка формы
    Object.keys(form).forEach(k => (form[k] = typeof form[k] === 'string' ? '' : null))
  } catch (e) {
    // аккуратно выводим ошибку
    const errMsg = e?.response?.data?.detail || e?.message || String(e)
    message.value = 'Ошибка при создании: ' + errMsg
    throw e // (опционально) пробросить дальше, если вызывающий хочет обработать
  }
}

// --- Навигация ---
export function back() {
  window.location.href = 'http://localhost/'
}