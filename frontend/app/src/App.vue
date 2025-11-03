<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { BRow, BCol, BCard, BForm, BFormGroup, BFormInput, BButton } from 'bootstrap-vue-next'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoggedIn = ref(false)
const user = ref({})

const router = useRouter()
const route = useRoute()

const handleUnauthorized = (response) => {
  if (response.status === 401) {
    localStorage.removeItem('authToken')
    router.push('/login')
    return true
  }
  return false
}

const handleLogin = async () => {
  errorMessage.value = ''
  try {
    const response = await fetch('http://localhost:8000/base/auth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: email.value,
        password: password.value,
      }),
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Login failed')
    }

    const data = await response.json()
    localStorage.setItem('authToken', data.access_token)
    isLoggedIn.value = true
    fetchUser()
    router.push('/') // Redirect to main menu after login
  } catch (error) {
    errorMessage.value = error.message
    console.error('Login error:', error)
  }
}

const handleLogout = () => {
  localStorage.removeItem('authToken')
  isLoggedIn.value = false
  user.value = {}
  router.push('/') // Redirect to main menu after logout
}

const fetchUser = async () => {
  const token = localStorage.getItem('authToken')
  if (token) {
    try {
      const response = await fetch('http://localhost:8000/base/users/me', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      })
      if (response.ok) {
        user.value = await response.json()
        isLoggedIn.value = true
      } else if (handleUnauthorized(response)) {
        return
      } else {
        handleLogout()
      }
    } catch (error) {
      handleLogout()
    }
  }
}

const navigateHome = () => {
  router.push('/') // Navigate to main menu
}

onMounted(() => {
  fetchUser()
})

watch(isLoggedIn, (newVal) => {
  if (newVal && route.path === '/login') {
    router.push('/')
  } else if (!newVal && route.path !== '/login') {
    router.push('/login')
  }
})
</script>

<template>
  <div v-if="isLoggedIn">
    <Navbar v-if="route.params.moduleName" :module-name="route.params.moduleName" :user="user" @logout="handleLogout" @navigate-home="navigateHome" />
    <router-view />
  </div>
  <div v-else class="container mt-5">
    <b-row class="justify-content-center">
      <b-col md="6">
        <b-card>
          <h2 class="text-center">Login</h2>
          <b-form @submit.prevent="handleLogin">
            <b-form-group label="Email:" label-for="email">
              <b-form-input id="email" v-model="email" type="email" required></b-form-input>
            </b-form-group>
            <b-form-group label="Password:" label-for="password">
              <b-form-input id="password" v-model="password" type="password" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary" block>Login</b-button>
            <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
          </b-form>
        </b-card>
      </b-col>
    </b-row>
  </div>
</template>




