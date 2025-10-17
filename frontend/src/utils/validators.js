export function validateItemForm(form) {
  if (!form.name) return 'Поле "Наименование" обязательно'
  if (!form.responsible_id) return 'Нужно выбрать ответственного'
  if (!form.location_id) return 'Нужно выбрать локацию'
  return null
}