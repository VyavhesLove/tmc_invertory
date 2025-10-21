import { ref } from 'vue'
import { useToast } from 'vue-toast-notification'
import {
  fetchItem,
  createItem,
  updateItem,
  fetchLocations,
  fetchUsers,
  fetchStatuses
} from '@/api/items'

export const locations = ref([])
export const responsible_names = ref([])
export const statuses = ref([])
export const message = ref('')
const toast = useToast();

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

//export async function submitForm(form) {
//  try {
//    const data = await createItem(form)
//    message.value = `✅ ТМЦ создан: ID ${data.id}`
    // очистка формы
//    Object.keys(form).forEach(k => (form[k] = typeof form[k] === 'string' ? '' : null))
//  } catch (e) {
    // аккуратно выводим ошибку
//    const errMsg = e?.response?.data?.detail || e?.message || String(e)
//    message.value = 'Ошибка при создании: ' + errMsg
//    throw e // (опционально) пробросить дальше, если вызывающий хочет обработать
//  }
//}

// -----------------------------
// Универсальная отправка формы
// mode = 'create' | 'edit'
// -----------------------------
export async function submitForm(form, mode = 'create') {
  try {
    let data

    if (mode === 'edit') {
      const id = localStorage.getItem('selectedItemId')
      if (!id) throw new Error('ID ТМЦ не найден')
      data = await updateItem(id, form)
      message.value = `✅ ТМЦ обновлён: ID ${data.id}`
      toast.success(`✅ ТМЦ обновлён: ID ${data.id}`, { position: 'top-right' })
      toast.open({
        message: `✅ ТМЦ обновлён: ID ${data.id}`,
        toastClassName: "my-toast-success",
        position: "bottom-left",
        duration: 5000
      });
    } else {
      data = await createItem(form)
      message.value = `✅ ТМЦ создан: ID ${data.id}`
      toast.success(`✅ ТМЦ создан: ID ${data.id}`, { position: 'top-right' });
      // очистим форму только при создании
      Object.keys(form).forEach(k => (form[k] = typeof form[k] === 'string' ? '' : null))
    }

    return data
  } catch (e) {
    const errMsg = e?.response?.data?.detail || e?.message || String(e)
    message.value = `Ошибка при ${mode === 'edit' ? 'обновлении' : 'создании'}: ` + errMsg
    toast.error(`Ошибка при ${mode === 'edit' ? 'обновлении' : 'создании'}: ${errMsg}`, { position: 'top-right' });
    throw e
  }
}

// --- Навигация ---
export function back() {
  window.location.href = 'http://localhost/'
}