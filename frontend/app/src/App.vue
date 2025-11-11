

<template>

  <div v-if="isLoggedIn">
    <div v-if="isLoading" class="loading-indicator">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>    
    <Navbar class="sticky-top shadow-sm" style="z-index: 1030" v-if="route.params.moduleName" :module-name="route.params.moduleName" :user="user" @logout="handleLogout" @navigate-home="navigateHome" />
    <div class="main-content">
      <router-view />
    </div>
  </div>
  <div v-else class="container mt-5">
    <BRow class="justify-content-center">
      <BCol md="6">
        <BCard>
          <h2 class="text-center">Login</h2>
          <BForm @submit.prevent="handleLogin">
            <BFormGroup label="Email:" label-for="email">
              <BFormInput id="email" v-model="email" type="email" required></BFormInput>
            </BFormGroup>
            <BFormGroup label="Password:" class="mt-2"  label-for="password">
              <BFormInput id="password" v-model="password" type="password" required></BFormInput>
            </BFormGroup>
            <BButton type="submit" class="mt-4" variant="primary" block>Login</BButton>
            <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
          </BForm>
        </BCard>
      </BCol>
    </BRow>
  </div>
</template>


<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Navbar from './components/Navbar.vue'
import { BRow, BCol, BCard, BForm, BFormGroup, BFormInput, BButton } from 'bootstrap-vue-next'
import api from './utils/api'
import { isLoading } from './utils/loading'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const isLoggedIn = ref(false)
const user = ref({})

const router = useRouter()
const route = useRoute()

const handleLogin = async () => {
  errorMessage.value = ''
  try {
    const response = await api.post('/base/auth/token', new URLSearchParams({
        username: email.value,
        password: password.value,
    }), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })

    localStorage.setItem('authToken', response.data.access_token)
    isLoggedIn.value = true
    fetchUser()
    router.push('/') // Redirect to main menu after login
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail
    } else {
      errorMessage.value = 'Login failed'
    }
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
      const response = await api.get('/base/users/me')
      user.value = response.data
      isLoggedIn.value = true
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

<style>
.loading-indicator {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.main-content {
  height: calc(100vh - 56px); /* Adjust 56px to your navbar's height */
  overflow-y: auto;
}
</style>

