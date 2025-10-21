import { ref } from 'vue'
import router from '@/router'
import { useToast } from 'vue-toast-notification'
import 'vue-toast-notification/dist/theme-default.css'
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
const toast = useToast()

// --- Загрузка локаций ---
export async function loadLocations() {
  try {
    locations.value = await fetchLocations()
  } catch (e) {
    showError('Ошибка загрузки локаций', e)
  }
}

// --- Загрузка ответственных ---
export async function loadResponsibleNames() {
  try {
    responsible_names.value = await fetchUsers()
  } catch (e) {
    showError('Ошибка загрузки пользователей', e)
  }
}

// --- Загрузка статусов ---
export async function loadStatuses() {
  try {
    statuses.value = await fetchStatuses()
  } catch (e) {
    showError('Ошибка загрузки статусов', e)
  }
}

// --- Загрузка всех справочников ---
export async function loadAllDictionaries() {
  try {
    await Promise.all([loadLocations(), loadResponsibleNames(), loadStatuses()])
  } catch (e) {
    throw e
  }
}

// --- Загрузка одного ТМЦ ---
export async function loadItem(id) {
  try {
    const data = await fetchItem(id)
    return data
  } catch (e) {
    showError('Ошибка загрузки ТМЦ', e)
    return null
  }
}

// --- Универсальная отправка формы ---
export async function submitForm(form, mode = 'create', id = null) {
  try {
    let data
    if (mode === 'edit') {
      const itemId = id || localStorage.getItem('selectedItemId')
      if (!itemId) throw new Error('ID ТМЦ не найден')
      data = await updateItem(itemId, form)
      showSuccess(`✅ ТМЦ обновлён: ID ${data.id}`)
    } else {
      data = await createItem(form)
      showSuccess(`✅ ТМЦ создан: ID ${data.id}`)
      Object.keys(form).forEach(k => (form[k] = typeof form[k] === 'string' ? '' : null))
    }
    return data
  } catch (e) {
    showError(`Ошибка при ${mode === 'edit' ? 'обновлении' : 'создании'}`, e)
    throw e
  }
}

// --- Навигация ---
export function back() {
  window.location.href = 'http://localhost/'
}

export function backToList() {
  router.push({ name: 'ItemsList' }).catch(() => {})
}

// --- Toast-утилиты ---
export function showError(prefix, e) {
  const errMsg = e?.response?.data?.detail || e?.message || String(e)
  message.value = `${prefix}: ${errMsg}`
  toast.open({
    message: `${prefix}: ${errMsg}`,
    toastClassName: 'my-popup-toast my-toast-error',
    position: 'top-center',
    duration: 7000
  })
}

export function showSuccess(msg) {
  message.value = msg
  toast.open({
    message: msg,
    toastClassName: 'my-popup-toast my-toast-success',
    position: 'bottom-left',
    duration: 5000
  })
}
