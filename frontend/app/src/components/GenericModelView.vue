<template>
  <div class="generic-model-view-container">
    <BRow class="p-3 sticky-top bg-light shadow-sm" id="header">
      <BCol lg="8" md="8"  xs="12" sm="12" class="text-start">
        <button v-if="showForm" type="button" class="btn btn-secondary btn-sm ms-2" @click="closeForm">Back</button>
        <button v-if="!showForm" class="btn btn-secondary btn-sm" @click="createNew">New</button>
        <button v-if="showForm" type="submit" form="main-form" class="btn btn-primary btn-sm ms-2">Save</button>
        <template v-if="showForm && uiSchema.views.form.actions">
          <button v-for="action in uiSchema.views.form.actions"
                  :key="action.label"
                  type="button"
                  class="btn btn-info btn-sm ms-2"
                  @click="handleAction(action)">
            {{ action.label }}
          </button>
        </template>
        <button v-if="selectedRecords.length > 0 && !showForm" class="btn btn-danger btn-sm ms-2" @click="deleteSelectedRecords"><i class="bi bi-trash"></i> Delete Selected</button>
                        <span v-if="showForm" class="pt-2 px-2 text-bold fw-bold" style="text-align:left">
          <a href="#" @click.prevent="closeForm">{{ modelName.charAt(0).toUpperCase() + modelName.slice(1) }}</a>
          /
          <span>{{ formMode === 'create' ? 'New' : selectedRecord.name || `${modelName},${selectedRecord.id}` }}</span>
        </span>
        <span v-if="!showForm" class="pt-2 px-2 text-bold fw-bold" style="text-align:left">
          {{ modelName.charAt(0).toUpperCase() + modelName.slice(1) }}
        </span>
      </BCol>
        
      <BCol lg="4" md="4" xs="12" sm="12" v-if="!showForm">
        <div class="input-group">
          <span class="input-group-text" id="basic-addon1">
            <i class="bi bi-search"></i> 
          </span>
          <input type="text" class="form-control" placeholder="Search anything.." aria-label="Search" aria-describedby="basic-addon1">
        </div>
        
      </BCol>
    </BRow>

    <div class="scrollable-content">
      <div v-if="loading">Loading...</div>
      <div v-else-if="error" class="card m-5 text-danger">
        {{ error }}
      </div>

      <div v-if="showForm" class="form-view">
        <form id="main-form" @submit.prevent="submitForm">
          
          <template v-if="uiSchema.views.form.layout && uiSchema.views.form.layout.type === 'group'">
            <FormGroup :group="uiSchema.views.form.layout" :get-field-schema="getFieldSchema" :selected-record="selectedRecord" :module-name="moduleName" />
          </template>

          <template v-else>
            <div v-for="field in uiSchema.views.form.fields" :key="field.field" class="form-group">
              <label :for="field.field">
                {{ field.label }}
                <span v-if="field.required" style="color: red;">*</span>
              </label>
              <!-- <pre>{{JSON.parse(selectedRecord[field.field]).replace('\n','')}}</pre> -->
              <input v-if="field.type === 'text' || field.type === 'number' || field.type === 'password'"
                    :type="field.type"
                    :id="field.field"
                    class="form-control"
                    v-model="selectedRecord[field.field]"
                    :required="field.required"
                    v-bind="field.props">
              <EmailInput v-else-if="field.type === 'email'"
                          :id="field.field"
                          v-model="selectedRecord[field.field]"
                          :required="field.required" />
              <textarea v-else-if="field.type === 'textarea' && !field.props.jsonViewer"
                      :id="field.field"
                      class="form-control"
                      v-model="selectedRecord[field.field]"
                      :required="field.required"
                      v-bind="field.props"></textarea>
              <div v-else-if="field.type === 'textarea' && field.props.jsonViewer" class="json-viewer-wrapper">
                <button type="button"
                        class="btn btn-sm btn-outline-secondary mb-2"
                        @click="toggleJsonViewerExpand">
                  {{ isJsonViewerExpanded ? 'Collapse All' : 'Expand All' }}
                </button>
                <JsonViewer :id="field.field"
                            :value="JSON.parse(selectedRecord[field.field] || '{}')"
                            :expanded="isJsonViewerExpanded">
                </JsonViewer>
              </div>
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
              <One2many v-else-if="field.type === 'one2many'"
                        :field="field"
                        v-model="selectedRecord[field.field]"
                        >
              </One2many>
              <!-- Add more input types as needed -->
            </div>
          </template>
          
        </form>
      </div>

      <div v-else class="list-view">
        <table class="data-table" v-if="uiSchema">
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
import One2many from './common/One2many.vue'
import { JsonViewer } from "vue3-json-viewer"
import "vue3-json-viewer/dist/vue3-json-viewer.css"
import { BRow, BCol, BCard, BForm, BFormGroup, BFormInput, BButton } from 'bootstrap-vue-next'
import api from '../utils/api'

const props = defineProps({
  moduleName: String,
  modelName: String,
})

const sortKey = ref('');
const sortOrder = ref('asc');
const selectedRecords = ref([]);
const isJsonViewerExpanded = ref();

const getNestedValue = (obj, path) => {
  if (!path) return obj;
  return path.split('.').reduce((acc, part) => acc && acc[part], obj);
};

const toggleJsonViewerExpand = () => {
  isJsonViewerExpanded.value = !isJsonViewerExpanded.value;
  console.log(isJsonViewerExpanded.value)
};

const getFieldSchema = (fieldName) => {
  // First, try to find in the top-level fields array
  let fieldSchema = uiSchema.value.views.form.fields.find(f => f.field === fieldName);

  // If not found, and a layout exists, search within the layout structure
  if (!fieldSchema && uiSchema.value.views.form.layout) {
    const searchInLayout = (layoutChildren) => {
      for (const child of layoutChildren) {
        if (child.field === fieldName) {
          // Found the field reference in the layout, now get its full schema from the fields array
          return uiSchema.value.views.form.fields.find(f => f.field === fieldName);
        }
        if (child.type === 'group' && child.children) {
          const foundInGroup = searchInLayout(child.children);
          if (foundInGroup) return foundInGroup;
        }
        if (child.type === 'notebook' && child.tabs) {
          for (const tab of child.tabs) {
            if (tab.children) {
              const foundInTab = searchInLayout(tab.children);
              if (foundInTab) return foundInTab;
            }
          }
        }
      }
      return null;
    };

    // Start searching from the top-level children of the layout, or tabs if it's a notebook
    if (uiSchema.value.views.form.layout.type === 'notebook') {
      fieldSchema = searchInLayout(uiSchema.value.views.form.layout.tabs);
    } else {
      fieldSchema = searchInLayout(uiSchema.value.views.form.layout.children);
    }
  }

  return fieldSchema || { label: fieldName, type: 'text', required: false };
};

const route = useRoute()
const uiSchema = ref(null)
const records = ref([])
const loading = ref(true)
const error = ref(null)
const showForm = ref(false)
const selectedRecord = ref(null)
const formMode = ref('');
const currentTab = ref(null);

const selectTab = (tabName) => {
  currentTab.value = tabName;
};

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

const fetchUISchema = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get(`/${props.moduleName}/ui_schemas/${props.modelName.toLowerCase()}`)
    uiSchema.value = response.data
    await fetchRecords()
  } catch (e) {
    error.value = e.message
  }
}

const fetchRecords = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await api.get(`/${props.moduleName}/${props.modelName.toLowerCase()}`)
    records.value = response.data
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
  error.value = null
  selectedRecord.value = {}
  formMode.value = 'create'
  showForm.value = true
}

const closeForm = () => {
  error.value = null
  showForm.value = false
  selectedRecord.value = null
}

const submitForm = async () => {
  loading.value = true
  error.value = null
  try {
    const url = formMode.value === 'create'
      ? `/${props.moduleName}/${props.modelName.toLowerCase()}`
      : `/${props.moduleName}/${props.modelName.toLowerCase()}/${selectedRecord.value.id}`
    const method = formMode.value === 'create' ? 'post' : 'put'

    const body = { ...selectedRecord.value };

    // If birth_date exists and is a Date object, format it to YYYY-MM-DD
    if (body.birth_date instanceof Date) {
      body.birth_date = body.birth_date.toISOString().split('T')[0];
    }

    if (body.addresses) {
      body.addresses = body.addresses.map(addr => {
        const newAddr = { ...addr };
        if (newAddr.country && typeof newAddr.country === 'object') {
          newAddr.country_id = newAddr.country.id;
          delete newAddr.country;
        }
        return newAddr;
      });
    }

    const response = await api[method](url, body)

    const savedRecord = response.data;
    selectedRecord.value = savedRecord;
    formMode.value = 'edit';
    await fetchRecords()
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
    await api.delete(`/${props.moduleName}/${props.modelName.toLowerCase()}/${recordId}`)
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
    const promises = selectedRecords.value.map(recordId => {
      return api.delete(`/${props.moduleName}/${props.modelName.toLowerCase()}/${recordId}`);
    });

    await Promise.all(promises);

    await fetchRecords();
    selectedRecords.value = [];
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};

const handleAction = async(action)=>{
  try {
    await api[action.method.toLowerCase()](`${action.route}/${selectedRecord.value.id}`)
    
    // After successful action, refetch the record to update the form
    const response = await api.get(`/${props.moduleName}/${props.modelName.toLowerCase()}/${selectedRecord.value.id}`)
    selectedRecord.value = response.data
  }
  catch (e) {
    console.log(e.message)
    error.value = e.response.data.detail || e.message
  }

}

watch(() => props.modelName, () => {
  if (props.modelName) {
    showForm.value = false; // Reset to list view
    fetchUISchema()
  }
}, { immediate: true })

watch(uiSchema, (newSchema) => {
  if (newSchema && newSchema.views.form.layout && newSchema.views.form.layout.type === 'notebook' && newSchema.views.form.layout.tabs.length > 0) {
    currentTab.value = newSchema.views.form.layout.tabs[0].label;
  }
}, { immediate: true });
</script>

<style scoped>
.tabs {
  display: flex;
  border-bottom: 1px solid #ccc;
  margin-bottom: 15px;
}

.tabs button {
  padding: 10px 15px;
  border: none;
  background-color: #f0f0f0;
  cursor: pointer;
  border-radius: 5px 5px 0 0;
  margin-right: 5px;
}

.tabs button.active {
  background-color: #fff;
  border-bottom: 1px solid #fff;
}

.scrollable-content {
  height: calc(100vh - 120px); /* Adjust this value based on your header's height */
  overflow-y: auto;
}
</style>
