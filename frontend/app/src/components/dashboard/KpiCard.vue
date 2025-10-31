<template>
  <div class="dashboard-item kpi-card">
    <h3>{{ item.title }}</h3>
    <p class="value">{{ item.value }}</p>
    <p class="module">Module: {{ item.module }}</p>
  </div>
</template>

<script setup>
defineProps({
  item: Object,
})
</script>


