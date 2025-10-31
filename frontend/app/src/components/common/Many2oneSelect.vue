<template>
  <select :id="field" :value="value" @change="handleChange" :required="required">
    <option value="">-- Select a {{ relatedModel }} --</option>
    <option v-for="item in items" :key="item.id" :value="item.id">
      {{ item[displayField] }}
    </option>
  </select>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  moduleName: {
    type: String,
    required: true
  },
  relatedModel: {
    type: String,
    required: true
  },
  field: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    default: null
  },
  displayField: {
    type: String,
    default: 'name'
  },
  required: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:value'])
const items = ref([])
const router = useRouter()

const handleUnauthorized = (response) => {
  if (response.status === 401) {
    localStorage.removeItem('authToken')
    router.push('/login')
    return true
  }
  return false
}

const fetchItems = async () => {
  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch(`http://localhost:8000/${props.moduleName}/${props.relatedModel.toLowerCase()}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    })
    if (handleUnauthorized(response)) return
    if (!response.ok) {
      throw new Error(`Failed to fetch ${props.relatedModel}`)
    }
    items.value = await response.json()
  } catch (e) {
    console.error(`Error fetching ${props.relatedModel}:`, e)
  }
}

const handleChange = (event) => {
  emit('update:value', event.target.value ? parseInt(event.target.value) : null)
}

onMounted(fetchItems)
</script>


