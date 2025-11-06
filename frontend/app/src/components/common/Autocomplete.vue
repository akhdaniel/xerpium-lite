<template>
  <div class="autocomplete">
    <input
      type="text"
      v-model="searchTerm"
      @input="onInput"
      @focus="onFocus"
      @blur="onBlur"
      placeholder="Search..."
      class="form-control"
      :required="required"
    />
    <ul v-if="showSuggestions" class="suggestions">
      <li
        v-for="suggestion in suggestions"
        :key="suggestion.id"
        @mousedown="selectSuggestion(suggestion)"
      >
        {{ suggestion.name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';

const props = defineProps({
  modelValue: [String, Number, Object],
  url: String,
  required: Boolean,
});

const emit = defineEmits(['update:modelValue']);

const searchTerm = ref('');
const suggestions = ref([]);
const showSuggestions = ref(false);

let timeout = null;

const onInput = () => {
  showSuggestions.value = true;
  if (timeout) {
    clearTimeout(timeout);
  }
  timeout = setTimeout(fetchSuggestions, 300);
};

const fetchSuggestions = async () => {
  if (searchTerm.value.length < 1) {
    suggestions.value = [];
    return;
  }
  try {
    const token = localStorage.getItem('authToken');
    const response = await fetch(`http://localhost:8000${props.url}?q=${searchTerm.value}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (response.ok) {
      suggestions.value = await response.json();
    }
  } catch (error) {
    console.error('Error fetching suggestions:', error);
  }
};

const selectSuggestion = (suggestion) => {
  searchTerm.value = suggestion.name;
    emit('update:modelValue', suggestion);
  showSuggestions.value = false;
};

const onFocus = () => {
  if (searchTerm.value) {
    showSuggestions.value = true;
  }
};

const onBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false;
  }, 200);
};

const fetchRecord = async (id) => {
  if (!id) {
    searchTerm.value = '';
    return;
  }
  try {
    const token = localStorage.getItem('authToken');
    // The URL for a single record is usually props.url + '/' + id
    const response = await fetch(`http://localhost:8000${props.url}/${id}`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });
    if (response.ok) {
      const record = await response.json();
      searchTerm.value = record.name;
    }
  } catch (error) {
    console.error('Error fetching record:', error);
  }
};

onMounted(() => {
  if (props.modelValue) {
    if (typeof props.modelValue === 'object') {
      searchTerm.value = props.modelValue.name;
    } else {
      fetchRecord(props.modelValue);
    }
  }
});

watch(() => props.modelValue, (newValue) => {
  if (typeof newValue === 'object') {
    searchTerm.value = newValue.name;
  } else {
    fetchRecord(newValue);
  }
});
</script>

<style scoped>
.autocomplete {
  position: relative;
}

.suggestions {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  list-style: none;
  margin: 0;
  padding: 0;
  z-index: 10;
}

.suggestions li {
  padding: 8px 12px;
  cursor: pointer;
}

.suggestions li:hover {
  background-color: #f0f0f0;
}
</style>
