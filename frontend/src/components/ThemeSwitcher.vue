<!-- <script setup>
import { useDark, useToggle } from "@vueuse/core"

// Хук для отслеживания тёмной темы
const isDark = useDark()

// Функция для переключения темы
const toggleDark = useToggle(isDark)
</script>

<template>
  <button @click="toggleDark()" style="margin-bottom: 12px;">
    Переключить тему: {{ isDark ? 'Тёмная' : 'Светлая' }}
  </button>
</template> -->

<script setup>
import { useDark, useToggle } from '@vueuse/core'

const isDark = useDark({
  storageKey: 'theme', // сохраняем выбор пользователя
  valueDark: 'dark',
  valueLight: 'light',
})
// const props = defineProps({ compact: Boolean }) // если компактный режим (для сайдбара) 06.10.2025
// const isDark = useDark() // отслеживаем текущую тему (тёмная/светлая) 06.10.2025
const toggleDark = useToggle(isDark)
</script>

<!--
<template>
  <button @click="toggleTheme" class="theme-btn" :title="compact ? 'Тема' : (isDark ? 'Светлая тема' : 'Тёмная тема')">
    <span v-if="!compact">{{ isDark ? '🌞 Светлая' : '🌙 Тёмная' }}</span>
    <span v-else>🌓</span>
  </button>
</template>
-->

<template>
  <button
    @click="toggleDark()"
    style="
      background: var(--btn-bg, #333);
      color: var(--btn-color, #fff);
      border: none;
      padding: 8px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: bold;
    "
  >
    {{ isDark ? '🌙 Тёмная' : '☀️ Светлая' }}
  </button>
</template>

<style>
html.light {
  --bg: #ffffff;
  --text: #000000;
  --btn-bg: #000000;
  --btn-color: #ffffff;
  background: var(--bg);
  color: var(--text);
}

html.dark {
  --bg: #1a1a1a;
  --text: #ffffff;
  --btn-bg: #ffffff;
  --btn-color: #000000;
  background: var(--bg);
  color: var(--text);
}
</style>
