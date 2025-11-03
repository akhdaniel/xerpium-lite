<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <a class="navbar-item logo" @click="$emit('navigate-home')">
        {{ moduleName.toUpperCase() }}
      </a>
      <a role="button" class="navbar-burger burger" :class="{'is-active': showMobileMenu}" aria-label="menu" aria-expanded="false" @click="toggleMobileMenu">
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </a>
    </div>
    <div class="navbar-menu" :class="{'is-active': showMobileMenu}">
      <div class="navbar-start">
        <div v-for="item in menuItems" :key="item.id" class="navbar-item has-dropdown is-hoverable">
          <a v-if="!item.path" class="navbar-link">
            {{ item.name }}
          </a>
          <router-link v-else :to="item.path ? (item.path.startsWith('/' + moduleName) ? item.path : '/' + moduleName + item.path) : '#'" class="navbar-item" @click="showMobileMenu = false">
            {{ item.name }}
          </router-link>
          <div v-if="item.children && item.children.length" class="navbar-dropdown">
            <router-link v-for="child in item.children" :key="child.id" :to="child.path ? (child.path.startsWith('/' + moduleName) ? child.path : '/' + moduleName + child.path) : '#'" class="navbar-item" @click="showMobileMenu = false">
              {{ child.name }}
            </router-link>
          </div>
        </div>
      </div>
      <div class="navbar-end">
        <div class="navbar-item has-dropdown is-hoverable">
          <a class="navbar-link">
            {{ user.username }}
          </a>
          <div class="navbar-dropdown">
            <a class="navbar-item" @click="$emit('logout'); showMobileMenu = false">
              Logout
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  moduleName: String,
  user: Object,
})

const router = useRouter()
const menuItems = ref([])
const showMobileMenu = ref(false)

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const handleUnauthorized = (response) => {
  if (response.status === 401) {
    localStorage.removeItem('authToken')
    router.push('/login')
    return true
  }
  return false
}

const fetchMenuItems = async (module) => {
  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch(`http://localhost:8000/base/menu/${module}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    )
    if (handleUnauthorized(response)) return
    if (!response.ok) {
      throw new Error('Failed to fetch menu items')
    }
    menuItems.value = await response.json()
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