<template>
  <div class="main-menu-container">
    <h1>Select a Module</h1>
    <div class="module-grid">
      <div class="module-item" @click="selectModule('base')">
        <div class="icon">B</div>
        <div class="name">Base</div>
      </div>
      <div class="module-item" @click="selectModule('crm')">
        <div class="icon">C</div>
        <div class="name">CRM</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const selectModule = (module) => {
  router.push(`/${module}/dashboard`)
}
</script>


