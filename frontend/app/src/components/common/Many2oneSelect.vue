<template>
  <select :id="field" :value="modelValue?.id" @change="handleChange" :required="required" class="form-control">
    <option value="">-- Select a {{ relatedModel }} --</option>
    <option v-for="item in items" :key="item.id" :value="item.id">
      {{ item[displayField] }}
    </option>
  </select>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { authenticatedFetch } from '../../utils/api'

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
  modelValue: {
    type: [Number, String, Object],
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

const emit = defineEmits(['update:modelValue'])
const items = ref([])

const fetchItems = async () => {
  try {
    const response = await authenticatedFetch(`http://localhost:8000/${props.moduleName}/${props.relatedModel.toLowerCase()}`)
    if (!response.ok) {
      throw new Error(`Failed to fetch ${props.relatedModel}`)
    }
    items.value = await response.json()
  } catch (e) {
    if (e.message !== 'Unauthorized') {
      console.error(`Error fetching ${props.relatedModel}:`, e)
    }
  }
}

const handleChange = (event) => {
  const selectedId = event.target.value ? parseInt(event.target.value) : null;
  const selectedItem = items.value.find(item => item.id === selectedId);
  emit('update:modelValue', selectedItem);
}

onMounted(fetchItems)
</script>