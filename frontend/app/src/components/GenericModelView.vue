<template>
  <div class="generic-model-view-container">
    <h1>{{ modelName.charAt(0).toUpperCase() + modelName.slice(1) }}</h1>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>

    <div v-else-if="showForm" class="form-view">
      <h2>{{ formMode === 'create' ? 'Create New' : 'Edit' }} {{ modelName.charAt(0).toUpperCase() + modelName.slice(1) }}</h2>
      <form @submit.prevent="submitForm">
        <template v-if="uiSchema.views.form.layout">
          <FormGroup :group="uiSchema.views.form.layout" :get-field-schema="getFieldSchema" :selected-record="selectedRecord" :module-name="moduleName" />
        </template>
        <template v-else>
          <div v-for="field in uiSchema.views.form.fields" :key="field.field" class="form-field">
            <label :for="field.field">{{ field.label }}</label>
            <input v-if="field.type === 'text' || field.type === 'email' || field.type === 'number' || field.type === 'password'"
                   :type="field.type"
                   :id="field.field"
                   v-model="selectedRecord[field.field]"
                   :required="field.required">
            <textarea v-else-if="field.type === 'textarea'"
                      :id="field.field"
                      v-model="selectedRecord[field.field]"
                      :required="field.required"></textarea>
            <Many2oneSelect v-else-if="field.type === 'many2one'"
                            :moduleName="field.module_name"
                            :relatedModel="field.related_model"
                            :field="field.field"
                            :value="selectedRecord[field.field]"
                            :displayField="field.display_field || 'name'"
                            :required="field.required"
                            @update:value="selectedRecord[field.field] = $event">
            </Many2oneSelect>
            <DateTimePicker v-else-if="field.type === 'datetime'"
                            :field="field.field"
                            v-model="selectedRecord[field.field]"
                            :required="field.required"
                            :showTime="true"
                            :type="field.type"
                            >
            </DateTimePicker>
            <DateTimePicker v-else-if="field.type === 'date'"
                            :field="field.field"
                            v-model="selectedRecord[field.field]"
                            :required="field.required"
                            :showTime="false"
                            :type="field.type"
                            >
            </DateTimePicker>
            <!-- Add more input types as needed -->
          </div>
        </template>
        <div class="form-actions">
          <button type="submit">Save</button>
          <button type="button" @click="closeForm">Cancel</button>
        </div>
      </form>
    </div>

    <div v-else class="list-view">
      <button @click="createNew">Create New {{ modelName.charAt(0).toUpperCase() + modelName.slice(1) }}</button>
      <table class="data-table">
        <thead>
          <tr>
            <th v-for="column in uiSchema.views.list.columns" :key="column.field">
              {{ column.headerName }}
            </th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in records" :key="record.id">
            <td v-for="column in uiSchema.views.list.columns" :key="column.field">
              {{ getNestedValue(record, column.field) }}
            </td>
            <td>
              <button @click="openForm(record)">Edit</button>
              <button @click="deleteRecord(record.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Many2oneSelect from './common/Many2oneSelect.vue'
import DateTimePicker from './common/DateTimePicker.vue'
import FormGroup from './common/FormGroup.vue'

const props = defineProps({
  moduleName: String,
  modelName: String,
})

const getNestedValue = (obj, path) => {
  if (!path) return obj;
  return path.split('.').reduce((acc, part) => acc && acc[part], obj);
};

const getFieldSchema = (fieldName) => {
  return uiSchema.value.views.form.fields.find(f => f.field === fieldName);
};

const route = useRoute()
const uiSchema = ref(null)
const records = ref([])
const loading = ref(true)
const error = ref(null)
const showForm = ref(false)
const selectedRecord = ref(null)
const formMode = ref('create')

const handleUnauthorized = (response) => {
  if (response.status === 401) {
    localStorage.removeItem('authToken')
    router.push('/login')
    return true
  }
  return false
}

const fetchUISchema = async () => {
  loading.value = true
  error.value = null
  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch(`http://localhost:8000/${props.moduleName}/ui_schemas/${props.modelName.toLowerCase()}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    )
    if (handleUnauthorized(response)) return
    if (!response.ok) {
      throw new Error('Failed to fetch UI schema')
    }
    uiSchema.value = await response.json()
    fetchRecords()
  } catch (e) {
    error.value = e.message
  }
}

const fetchRecords = async () => {
  loading.value = true
  error.value = null
  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch(`http://localhost:8000/${props.moduleName}/${props.modelName.toLowerCase()}`,
      {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    )
    if (handleUnauthorized(response)) return
    if (!response.ok) {
      throw new Error('Failed to fetch records')
    }
    records.value = await response.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const openForm = (record) => {
  selectedRecord.value = { ...record }
  formMode.value = 'edit'
  showForm.value = true
}

const createNew = () => {
  selectedRecord.value = {}
  formMode.value = 'create'
  showForm.value = true
}

const closeForm = () => {
  showForm.value = false
  selectedRecord.value = null
}

const submitForm = async () => {
  loading.value = true
  error.value = null
  try {
    const token = localStorage.getItem('authToken')
    const url = formMode.value === 'create'
      ? `http://localhost:8000/${props.moduleName}/${props.modelName.toLowerCase()}`
      : `http://localhost:8000/${props.moduleName}/${props.modelName.toLowerCase()}/${selectedRecord.value.id}`
    const method = formMode.value === 'create' ? 'POST' : 'PUT'

    const body = { ...selectedRecord.value };

    // If birth_date exists and is a Date object, format it to YYYY-MM-DD
    if (body.birth_date instanceof Date) {
      body.birth_date = body.birth_date.toISOString().split('T')[0];
    }

    const response = await fetch(url, {
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(body),
    })

    if (handleUnauthorized(response)) return
    if (!response.ok) {
      throw new Error('Failed to save record')
    }
    await fetchRecords()
    closeForm()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

const deleteRecord = async (recordId) => {
  if (!confirm('Are you sure you want to delete this record?')) {
    return
  }

  loading.value = true
  error.value = null
  try {
    const token = localStorage.getItem('authToken')
    const response = await fetch(`http://localhost:8000/${props.moduleName}/${props.modelName.toLowerCase()}/${recordId}`,
      {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      }
    )
    if (handleUnauthorized(response)) return
    if (!response.ok) {
      throw new Error('Failed to delete record')
    }
    await fetchRecords()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

watch(() => props.modelName, () => {
  if (props.modelName) {
    fetchUISchema()
  }
}, { immediate: true })

</script>


