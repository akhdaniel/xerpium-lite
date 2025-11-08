<template>
  <div class="main-menu-container">
    <h1>Select a Module</h1>
    <div class="module-grid">
      <div v-for="module in activeModules" :key="module.name" class="module-item" @click="selectModule(module.name)">
        <div class="icon">{{ module.name.charAt(0).toUpperCase() }}</div>
        <div class="name">{{ module.name.charAt(0).toUpperCase() + module.name.slice(1) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authenticatedFetch } from '../utils/api'

const router = useRouter()
const modules = ref([])
const loading = ref(true)
const error = ref(null)

const activeModules = computed(() => {
  return modules.value.filter(module => module.is_active)
})

const fetchModules = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await authenticatedFetch('http://localhost:8000/base/modules/')
    if (!response.ok) {
      throw new Error('Failed to fetch modules')
    }
    modules.value = await response.json()
  } catch (e) {
    if (e.message !== 'Unauthorized') {
      error.value = e.message
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchModules()
})

const selectModule = (moduleName) => {
  router.push(`/${moduleName}/dashboard`)
}
</script>


