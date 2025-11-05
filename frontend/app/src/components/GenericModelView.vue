<template>
  <div class="generic-model-view-container">
    <BRow class="px-3 pt-3">
      <BCol lg="8" md="8"  xs="12" sm="12" class="text-start">
        <button class="btn btn-secondary btn-sm" @click="createNew">New</button>
        <button v-if="selectedRecords.length > 0 && !showForm" class="btn btn-danger btn-sm ms-2" @click="deleteSelectedRecords">Delete Selected</button>
        <span v-if="showForm" class="pt-2 px-2 text-bold fw-bold" style="text-align:left">
          {{ formMode === 'create' ? 'Create New' : 'Edit' }} {{ modelName.charAt(0).toUpperCase() + modelName.slice(1) }}
        </span>
        <span v-if="!showForm" class="pt-2 px-2 text-bold fw-bold" style="text-align:left">
          {{ modelName.charAt(0).toUpperCase() + modelName.slice(1) }}
        </span>
      </BCol>
        
      <BCol lg="4" md="4" xs="12" sm="12" v-if="!showForm">
        <div class="input-group mb-3">
          <span class="input-group-text" id="basic-addon1">
            <i class="bi bi-search"></i> 
          </span>
          <input type="text" class="form-control" placeholder="Search anything.." aria-label="Search" aria-describedby="basic-addon1">
        </div>
        
      </BCol>
    </BRow>

    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>

    <div v-else-if="showForm" class="form-view">
      <form @submit.prevent="submitForm">
        <template v-if="uiSchema.views.form.layout">
          <FormGroup :group="uiSchema.views.form.layout" :get-field-schema="getFieldSchema" :selected-record="selectedRecord" :module-name="moduleName" />
        </template>
        <template v-else>
          <div v-for="field in uiSchema.views.form.fields" :key="field.field" class="form-group">
            {{ console.log(field) }}
            <label :for="field.field">{{ field.label }}</label>
            <input v-if="field.type === 'text' || field.type === 'number' || field.type === 'password'"
                   :type="field.type"
                   :id="field.field"
                   class="form-control"
                   v-model="selectedRecord[field.field]"
                   :required="field.required">
            <EmailInput v-else-if="field.type === 'email'"
                        :id="field.field"
                        v-model="selectedRecord[field.field]"
                        :required="field.required" />
            <textarea v-else-if="field.type === 'textarea'"
                      :id="field.field"
                   class="form-control"
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
            <Autocomplete v-else-if="field.type === 'autocomplete'"
                          :url="field.url"
                          v-model="selectedRecord[field.field]"
                          :required="field.required"
                          >
            </Autocomplete>
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
      <table class="data-table">
        <thead>
          <tr>
            <th style="width: 1%;"><input type="checkbox" class="form-check-input" @click="toggleSelectAll" /></th>
            <th v-for="column in uiSchema.views.list.columns" :key="column.field" @click="sortBy(column.field)" style="cursor: pointer;">
              {{ column.headerName }}
              <i v-if="sortKey === column.field" :class="['bi', sortOrder === 'asc' ? 'bi-sort-alpha-down' : 'bi-sort-alpha-up']"></i>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in sortedRecords" :key="record.id" @click="openForm(record)" style="cursor: pointer;">
            <td><input type="checkbox" class="form-check-input" :value="record.id" v-model="selectedRecords" @click.stop /></td>
            <td v-for="column in uiSchema.views.list.columns" :key="column.field">
              {{ getNestedValue(record, column.field) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Many2oneSelect from './common/Many2oneSelect.vue'
import DateTimePicker from './common/DateTimePicker.vue'
import FormGroup from './common/FormGroup.vue'
import Autocomplete from './common/Autocomplete.vue'
import EmailInput from './common/EmailInput.vue'
import { BRow, BCol, BCard, BForm, BFormGroup, BFormInput, BButton } from 'bootstrap-vue-next'

const props = defineProps({
  moduleName: String,
  modelName: String,
})

const sortKey = ref('');
const sortOrder = ref('asc');
const selectedRecords = ref([]);

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
const formMode = ref('')

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortKey.value = key;
    sortOrder.value = 'asc';
  }
};

const sortedRecords = computed(() => {
  if (!sortKey.value) {
    return records.value;
  }
  return [...records.value].sort((a, b) => {
    const aValue = getNestedValue(a, sortKey.value);
    const bValue = getNestedValue(b, sortKey.value);

    if (aValue < bValue) {
      return sortOrder.value === 'asc' ? -1 : 1;
    }
    if (aValue > bValue) {
      return sortOrder.value === 'asc' ? 1 : -1;
    }
    return 0;
  });
});

const toggleSelectAll = (event) => {
  if (event.target.checked) {
    selectedRecords.value = sortedRecords.value.map(record => record.id);
  } else {
    selectedRecords.value = [];
  }
};

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

const deleteSelectedRecords = async () => {
  if (selectedRecords.value.length === 0) {
    alert('Please select records to delete.');
    return;
  }
  if (!confirm(`Are you sure you want to delete ${selectedRecords.value.length} selected records?`)) {
    return;
  }

  loading.value = true;
  error.value = null;
  try {
    const token = localStorage.getItem('authToken');
    const promises = selectedRecords.value.map(recordId => {
      return fetch(`http://localhost:8000/${props.moduleName}/${props.modelName.toLowerCase()}/${recordId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
    });

    const responses = await Promise.all(promises);

    responses.forEach(response => {
      if (handleUnauthorized(response)) return;
      if (!response.ok) {
        throw new Error('Failed to delete one or more records');
      }
    });

    await fetchRecords();
    selectedRecords.value = [];
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};

watch(() => props.modelName, () => {
  if (props.modelName) {
    fetchUISchema()
  }
}, { immediate: true })
</script>




