<!-- не подключено -->
 <template>
  <header class="header">
    <h1>Система учёта ТМЦ</h1>
    <div class="user-info">
      <span>{{ username }}</span>
      <button @click="logout">Выйти</button>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('admin')

function logout() {
  localStorage.clear()
  window.location.href = '/login'
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  background-color: #efefef;
  border-bottom: 1px solid #ccc;
}
.user-info button {
  margin-left: 10px;
}
</style>
