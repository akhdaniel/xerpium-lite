<template>
  <div>
    <!-- <label>{{ field.label }}</label> -->
    <table class="data-table">
      <thead>
        <tr>
          <th style="width: 1%;"><input type="checkbox" class="form-check-input" @click="toggleSelectAll" /></th>
          <th v-for="column in field.views.list.columns" :key="column.field" @click="sortBy(column.field)" style="cursor: pointer;">
            {{ column.headerName }}
            <i v-if="sortKey === column.field" :class="['bi', sortOrder === 'asc' ? 'bi-sort-alpha-down' : 'bi-sort-alpha-up']"></i>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(record, index) in sortedRecords" :key="index" @click="editRecord(index)" style="cursor: pointer;">
          <td><input type="checkbox" class="form-check-input" :value="index" v-model="selectedRecords" @click.stop /></td>
          <td v-for="column in field.views.list.columns" :key="column.field">
            <template v-if="column.type === 'many2one' && record[column.field]">
              {{ record[column.field].name }}
            </template>
            <template v-else>
              {{ getNestedValue(record, column.field) }}
            </template>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="pt-2">
      <button class="btn btn-sm btn-secondary" type="button" @click.stop="addRecord">Add</button>
      <button v-if="selectedRecords.length > 0" class="btn btn-sm btn-danger mx-2" type="button" @click.stop="deleteSelectedRecords"><i class="bi bi-trash"></i> Delete Selected</button>
    </div>
    <!-- Modal for editing/creating records -->
    <div v-if="showModal" class="one2many-modal">
      <div class="one2many-modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h3>{{ isEditing ? 'Edit' : 'Add' }} {{ field.label }}</h3>
        <div v-for="formField in field.views.form.fields" :key="formField.field" class="form-field">
          <label :for="formField.field">
            {{ formField.label }}
            <span v-if="formField.required" style="color: red;">*</span>
          </label>
          <input v-if="formField.type === 'text' || formField.type === 'number' || formField.type === 'password'"
                 :type="formField.type"
                 :id="formField.field"
                 v-model="editingRecord[formField.field]"
                 :required="formField.required"
                 @input="validationErrors[formField.field] = null"
                 class="form-control">
          <EmailInput v-else-if="formField.type === 'email'"
                      :id="formField.field"
                      v-model="editingRecord[formField.field]"
                      :required="formField.required"
                      @update:modelValue="validationErrors[formField.field] = null" />
          <textarea v-else-if="formField.type === 'textarea'"
                    :id="formField.field"
                    v-model="editingRecord[formField.field]"
                    :required="formField.required"
                    @input="validationErrors[formField.field] = null"
                    class="form-control"></textarea>
          <Many2oneSelect v-else-if="formField.type === 'many2one'"
                          :moduleName="formField.module_name"
                          :relatedModel="formField.related_model"
                          :field="formField.field"
                          v-model="editingRecord[formField.field]"
                          :displayField="formField.display_field || 'name'"
                          :required="formField.required"
                          @update:modelValue="validationErrors[formField.field] = null">
          </Many2oneSelect>
          <Autocomplete v-else-if="formField.type === 'autocomplete'"
                        :url="formField.url"
                        v-model="editingRecord[formField.field]"
                        :required="formField.required"
                        @update:modelValue="validationErrors[formField.field] = null"
                        >
          </Autocomplete>
          <DateTimePicker v-else-if="formField.type === 'datetime'"
                          :field="formField.field"
                          v-model="editingRecord[formField.field]"
                          :required="formField.required"
                          :showTime="true"
                          :type="formField.type"
                          @update:modelValue="validationErrors[formField.field] = null"
                          >
          </DateTimePicker>
          <DateTimePicker v-else-if="formField.type === 'date'"
                          :field="formField.field"
                          v-model="editingRecord[formField.field]"
                          :required="formField.required"
                          :showTime="false"
                          :type="formField.type"
                          @update:modelValue="validationErrors[formField.field] = null"
                          >
          </DateTimePicker>
          <div v-if="validationErrors[formField.field]" class="tooltip-error">
            {{ validationErrors[formField.field] }}
          </div>
        </div>
        <button type="button" @click="saveRecord">Save</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import Many2oneSelect from './Many2oneSelect.vue';
import DateTimePicker from './DateTimePicker.vue';
import EmailInput from './EmailInput.vue';
import Autocomplete from './Autocomplete.vue';

const props = defineProps({
  field: Object,
  modelValue: Array,
});

const emit = defineEmits(['update:modelValue']);

const showModal = ref(false);
const isEditing = ref(false);
const editingRecord = ref(null);
const editingIndex = ref(null);
const selectedRecords = ref([]);
const validationErrors = ref({});
const sortKey = ref('');
const sortOrder = ref('asc');

const getNestedValue = (obj, path) => {
  if (!path) return obj;
  return path.split('.').reduce((acc, part) => acc && acc[part], obj);
};

// Helper to flatten an object for form editing
const flattenRecord = (record, fields) => {
  return { ...record };
};

// Helper to reconstruct nested objects from a flat record
const reconstructRecord = (flatRecord, fields) => {
  return { ...flatRecord };
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
    return props.modelValue;
  }
  return [...props.modelValue].sort((a, b) => {
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


const addRecord = () => {
  isEditing.value = false;
  editingRecord.value = {};
  showModal.value = true;
};

const editRecord = (index) => {
  isEditing.value = true;
  editingIndex.value = index;
  // Flatten the record for editing in the form
  editingRecord.value = flattenRecord(props.modelValue[index], props.field.views.form.fields);
  showModal.value = true;
};

const deleteRecord = (index) => {
  const updatedValue = [...props.modelValue];
  updatedValue.splice(index, 1);
  emit('update:modelValue', updatedValue);
};

const deleteSelectedRecords = () => {
  const updatedValue = props.modelValue.filter((_, index) => !selectedRecords.value.includes(index));
  selectedRecords.value = [];
  emit('update:modelValue', updatedValue);
};

const toggleSelectAll = (event) => {
  if (event.target.checked) {
    selectedRecords.value = props.modelValue.map((_, index) => index);
  } else {
    selectedRecords.value = [];
  }
};

const saveRecord = () => {
  validationErrors.value = {};
  let hasError = false;
  for (const formField of props.field.views.form.fields) {
    if (formField.required) {
      const value = editingRecord.value[formField.field];
      if (value === null || value === undefined || value === '') {
        validationErrors.value[formField.field] = `Field "${formField.label}" is required.`;
        hasError = true;
      }
    }
  }

  if (hasError) {
    return;
  }

  const updatedValue = [...props.modelValue];
  // Reconstruct the record before saving
  const recordToSave = reconstructRecord(editingRecord.value, props.field.views.form.fields);

  if (isEditing.value) {
    updatedValue[editingIndex.value] = recordToSave;
  } else {
    updatedValue.push(recordToSave);
  }
  emit('update:modelValue', updatedValue);
  closeModal();
};

const closeModal = () => {
  showModal.value = false;
  editingRecord.value = null;
  editingIndex.value = null;
  validationErrors.value = {}; // Clear errors
};
</script>

<style scoped>
.one2many-modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
}

.one2many-modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}

.tooltip-error {
  color: red;
  font-size: 0.8em;
  margin-top: 5px;
}
</style>
