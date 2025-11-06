<template>
  <div>
    <div class="tabs">
      <button
        type="button"
        v-for="tab in notebook.tabs"
        :key="tab.label"
        :class="{ active: currentTab === tab.label }"
        @click="selectTab(tab.label)"
      >
        {{ tab.label }}
      </button>
    </div>
    <div class="tab-content">
      <template v-for="tab in notebook.tabs" :key="tab.label">
        <div v-show="currentTab === tab.label">
          <div v-if="tab.field">
            <!-- Logic to render a single field -->
            <div class="form-group">
              <label :for="tab.field">
                {{ getFieldSchema(tab.field).label }}
                <span v-if="getFieldSchema(tab.field).required" style="color: red;">*</span>
              </label>
              <input v-if="getFieldSchema(tab.field).type === 'text' || getFieldSchema(tab.field).type === 'number' || getFieldSchema(tab.field).type === 'password'"
                    :type="getFieldSchema(tab.field).type"
                    :id="tab.field"
                    class="form-control"
                    v-model="selectedRecord[tab.field]"
                    :required="getFieldSchema(tab.field).required">
              <EmailInput v-else-if="getFieldSchema(tab.field).type === 'email'"
                          :id="tab.field"
                          v-model="selectedRecord[tab.field]"
                          :required="getFieldSchema(tab.field).required" />
              <textarea v-else-if="getFieldSchema(tab.field).type === 'textarea'"
                        :id="tab.field"
                    class="form-control"
                        v-model="selectedRecord[tab.field]"
                        :required="getFieldSchema(tab.field).required"></textarea>
              <Many2oneSelect v-else-if="getFieldSchema(tab.field).type === 'many2one'"
                              :moduleName="getFieldSchema(tab.field).module_name"
                              :relatedModel="getFieldSchema(tab.field).related_model"
                              :field="tab.field"
                              :value="selectedRecord[tab.field]"
                              :displayField="getFieldSchema(tab.field).display_field || 'name'"
                              :required="getFieldSchema(tab.field).required"
                              @update:value="selectedRecord[tab.field] = $event">
              </Many2oneSelect>
              <Autocomplete v-else-if="getFieldSchema(tab.field).type === 'autocomplete'"
                            :url="getFieldSchema(tab.field).url"
                            v-model="selectedRecord[tab.field]"
                            :required="getFieldSchema(tab.field).required"
                            >
              </Autocomplete>
              <DateTimePicker v-else-if="getFieldSchema(tab.field).type === 'datetime'"
                              :field="tab.field"
                              v-model="selectedRecord[tab.field]"
                              :required="getFieldSchema(tab.field).required"
                              :showTime="true"
                              :type="getFieldSchema(tab.field).type"
                              >
              </DateTimePicker>
              <DateTimePicker v-else-if="getFieldSchema(tab.field).type === 'date'"
                              :field="tab.field"
                              v-model="selectedRecord[tab.field]"
                              :required="getFieldSchema(tab.field).required"
                              :showTime="false"
                              :type="getFieldSchema(tab.field).type"
                              >
              </DateTimePicker>
              <One2many v-else-if="getFieldSchema(tab.field).type === 'one2many'"
                        :field="getFieldSchema(tab.field)"
                        v-model="selectedRecord[tab.field]"
                        >
              </One2many>
            </div>
          </div>
          <div v-else-if="tab.children">
              <FormGroup :group="{ type: 'group', children: tab.children }" :get-field-schema="getFieldSchema" :selected-record="selectedRecord" :module-name="moduleName" />
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import Many2oneSelect from './Many2oneSelect.vue'
import DateTimePicker from './DateTimePicker.vue'
import FormGroup from './FormGroup.vue'
import Autocomplete from './Autocomplete.vue'
import EmailInput from './EmailInput.vue'
import One2many from './One2many.vue'

const props = defineProps({
  notebook: Object,
  getFieldSchema: Function,
  selectedRecord: Object,
  moduleName: String,
})

const currentTab = ref(null)

const selectTab = (tabName) => {
  currentTab.value = tabName
}

watch(() => props.notebook, (newNotebook) => {
  if (newNotebook && newNotebook.tabs && newNotebook.tabs.length > 0) {
    currentTab.value = newNotebook.tabs[0].label
  }
}, { immediate: true })
</script>

<style scoped>
.tabs {
  display: flex;
  border-bottom: 1px solid #dee2e6;
  margin-bottom: 15px;
}

.tabs button {
  padding: 10px 15px;
  border: 1px solid #dee2e6;
  background-color: #e9ecef;
  cursor: pointer;
  border-radius: 5px 5px 0 0;
  margin-right: 5px;
  margin-bottom: -1px;
}

.tabs button.active {
  background-color: #fff;
  border-bottom-color: #fff;
}
</style>
