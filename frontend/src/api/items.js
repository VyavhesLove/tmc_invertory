import api from '@/api/axios'

// --- Получить один ТМЦ ---
export async function fetchItem(id) {
  const { data } = await api.get(`/items/${id}`)
  return data
}

// --- Создать новый ТМЦ ---
export async function createItem(form) {
  const payload = {
    name: form.name,
    serial_number: form.serial_missing
      ? null
      : (form.serial_number || null),
    brand: form.brand || null,
    status_id: form.status_id ?? null,
    responsible_id: form.responsible_id ?? null,
    location_id: form.location_id ?? null,
    comment: form.comment ?? null
  }
  const { data } = await api.post('/items/', payload)
  return data
}

// --- Обновить ТМЦ ---
export async function updateItem(id, form) {
  const payload = {
    name: form.name,
    serial_number: form.serial_missing
      ? null
      : (form.serial_number || null),
    brand: form.brand || null,
    status_id: form.status_id ?? null,
    responsible_id: form.responsible_id ?? null,
    location_id: form.location_id ?? null,
    comment: form.comment ?? null
  }
  const { data } = await api.put(`/items/${id}`, payload)
  return data
}

// --- Справочники ---
export async function fetchLocations() {
  const { data } = await api.get('/locations')
  return data
}

export async function fetchUsers() {
  const { data } = await api.get('/users')
  return data
}

export async function fetchStatuses() {
  const { data } = await api.get('/statuses')
  return data
}
