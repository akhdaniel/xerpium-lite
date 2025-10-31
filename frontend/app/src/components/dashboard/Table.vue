<template>
  <div class="dashboard-item table-card">
    <h3>{{ item.title }}</h3>
    <table>
      <thead>
        <tr>
          <th v-for="header in item.value.headers" :key="header">{{ header }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in item.value.rows" :key="index">
          <td v-for="(cell, cellIndex) in row" :key="cellIndex">{{ cell }}</td>
        </tr>
      </tbody>
    </table>
    <p class="module">Module: {{ item.module }}</p>
  </div>
</template>

<script setup>
defineProps({
  item: Object,
})
</script>


