<template>
  <div class="dashboard-item">
    <h3>{{ item.title }}</h3>
    <div class="chart-container">
      <Bar :data="item.value" :options="chartOptions" />
    </div>
    <p class="module">Module: {{ item.module }}</p>
  </div>
</template>

<script setup>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

defineProps({
  item: Object,
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
}
</script>


