import { ref } from 'vue'

export const isLoading = ref(false)
let loadingTimer = null
let activeRequests = 0

export const startLoadingTimer = () => {
  activeRequests++
  if (activeRequests === 1) {
    loadingTimer = setTimeout(() => {
      isLoading.value = true
    }, 3000)
  }
}

export const stopLoadingTimer = () => {
  activeRequests--
  if (activeRequests === 0) {
    clearTimeout(loadingTimer)
    isLoading.value = false
  }
}