<template>
  <BNavbar toggleable="lg" 
    v-b-color-mode="'dark'"
    variant="dark"
  >
    <BNavbarBrand @click="$emit('navigate-home')">{{ moduleName.toUpperCase() }}</BNavbarBrand>
    <BNavbarToggle target="nav-collapse" @click="toggleMobileMenu" />
    <BCollapse id="nav-collapse" is-nav :visible="showMobileMenu">
      <BNavbarNav>
        <template v-for="item in menuItems" :key="item.id">
          <BNavItemDropdown v-if="item.children && item.children.length" :text="item.name" >
            <BDropdownItem v-for="child in item.children" :key="child.id" :to="child.path ? (child.path.startsWith('/' + moduleName) ? child.path : '/' + moduleName + child.path) : '#'" @click="showMobileMenu = false">
              {{ child.name }}
            </BDropdownItem>
          </BNavItemDropdown>
          <BNavItem v-else :to="item.path ? (item.path.startsWith('/' + moduleName) ? item.path : '/' + moduleName + item.path) : '#'" @click="showMobileMenu = false">
            {{ item.name }}
          </BNavItem>
        </template>
      </BNavbarNav>

      <BNavbarNav class="ms-auto">
        <BNavItemDropdown right>
          <template #button-content>
            <em>{{ user.username }}</em>
          </template>
          <BDropdownItem @click="$emit('logout'); showMobileMenu = false">
            <i class="bi bi-box-arrow-right"></i> Logout
          </BDropdownItem>
        </BNavItemDropdown>
      </BNavbarNav>
    </BCollapse>
  </BNavbar>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import api from '../utils/api'
import { BNavbar, BNavbarBrand, BNavbarNav, BNavItem, BNavItemDropdown, BDropdownItem, BCollapse, BNavbarToggle } from 'bootstrap-vue-next'

const props = defineProps({
  moduleName: String,
  user: Object,
})

const menuItems = ref([])
const showMobileMenu = ref(false)

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const fetchMenuItems = async (module) => {
  try {
    const response = await api.get(`/base/menu/${module}`)
    menuItems.value = response.data
    console.log('Fetched menu items:', menuItems.value)
  } catch (error) {
    console.error('Error fetching menu items:', error)
  }
}

watch(() => props.moduleName, (newModule) => {
  if (newModule) {
    fetchMenuItems(newModule)
  }
}, { immediate: true })

</script>


