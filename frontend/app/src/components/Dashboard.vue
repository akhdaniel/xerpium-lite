<template>
  <div class="dashboard-container">
    <h1>{{ moduleName.toUpperCase() }} Dashboard</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else class="dashboard-grid">
      <component v-for="item in dashboardItems" :key="item.id" :is="getComponent(item.type)" :item="item" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import NumberCard from './dashboard/NumberCard.vue'
import KpiCard from './dashboard/KpiCard.vue'
import Chart from './dashboard/Chart.vue'
import Table from './dashboard/Table.vue'
import api from '../utils/api'

const props = defineProps({
  moduleName: String,
})

const dashboardItems = ref([])
const loading = ref(true)
const error = ref(null)

const componentMapping = {
  number_card: NumberCard,
  kpi_card: KpiCard,
  chart: Chart,
  table: Table,
}

const getComponent = (type) => {
  return componentMapping[type] || NumberCard // Default to NumberCard
}

const fetchDashboardItems = async (module) => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get(`/${module}/dashboard`)
    dashboardItems.value = response.data
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

watch(() => props.moduleName, (newModule) => {
  if (newModule) {
    fetchDashboardItems(newModule)
  }
}, { immediate: true })

</script>


