<template>
  <div :style="{ display: 'flex', flexDirection: group.direction || 'column', gap: '10px' }">
    <div v-for="(child, index) in group.children" :key="index" :style="group.direction === 'row' ? { flex: 1 } : {}">
      <template v-if="child.type === 'group'">
        <FormGroup :group="child" :get-field-schema="getFieldSchema" :selected-record="selectedRecord" :module-name="moduleName" />
      </template>
      <template v-else>
        <div class="form-group">
          <label class="form-label" :for="child.field">
            {{ getFieldSchema(child.field).label }}
            <span v-if="getFieldSchema(child.field).required" style="color: red;">*</span>
          </label>
          <input v-if="getFieldSchema(child.field).type === 'text' || getFieldSchema(child.field).type === 'number' || getFieldSchema(child.field).type === 'password'"
                 class="form-control"
                 :type="getFieldSchema(child.field).type"
                 :id="child.field"
                 v-model="selectedRecord[child.field]"
                 :required="getFieldSchema(child.field).required">
          <EmailInput v-else-if="getFieldSchema(child.field).type === 'email'"
                      :id="child.field"
                      v-model="selectedRecord[child.field]"
                      :required="getFieldSchema(child.field).required" />
          <textarea v-else-if="getFieldSchema(child.field).type === 'textarea'"
                    :id="child.field"
                 class="form-control"
                    v-model="selectedRecord[child.field]"
                    :required="getFieldSchema(child.field).required"></textarea>
          <Many2oneSelect v-else-if="getFieldSchema(child.field).type === 'many2one'"
                          :moduleName="getFieldSchema(child.field).module_name"
                          :relatedModel="getFieldSchema(child.field).related_model"
                          :field="child.field"
                          :value="selectedRecord[child.field]"
                          :displayField="getFieldSchema(child.field).display_field || 'name'"
                          :required="getFieldSchema(child.field).required"
                          @update:value="selectedRecord[child.field] = $event">
          </Many2oneSelect>
          <Autocomplete v-else-if="getFieldSchema(child.field).type === 'autocomplete'"
                        :url="getFieldSchema(child.field).url"
                        v-model="selectedRecord[child.field]"
                        :required="getFieldSchema(child.field).required"
                        >
          </Autocomplete>
          <DateTimePicker v-else-if="getFieldSchema(child.field).type === 'datetime'"
                          :field="child.field"
                          v-model="selectedRecord[child.field]"
                          :required="getFieldSchema(child.field).required"
                          :showTime="true"
                          :type="getFieldSchema(child.field).type"
                          >
          </DateTimePicker>
          <DateTimePicker v-else-if="getFieldSchema(child.field).type === 'date'"
                          :field="child.field"
                          v-model="selectedRecord[child.field]"
                          :required="getFieldSchema(child.field).required"
                          :showTime="false"
                          :type="getFieldSchema(child.field).type"
                          >
          </DateTimePicker>
          <One2many v-else-if="getFieldSchema(child.field).type === 'one2many'"
                    :field="getFieldSchema(child.field)"
                    v-model="selectedRecord[child.field]"
                    >
          </One2many>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import Many2oneSelect from './Many2oneSelect.vue'
import DateTimePicker from './DateTimePicker.vue'
import FormGroup from './FormGroup.vue'
import Autocomplete from './Autocomplete.vue'
import EmailInput from './EmailInput.vue'
import One2many from './One2many.vue'

const props = defineProps({
  group: Object,
  getFieldSchema: Function,
  selectedRecord: Object,
  moduleName: String,
})
</script>
