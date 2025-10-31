<template>
  <div class="datetime-picker-container">
    <label v-if="label">{{ label }}</label>
    <VueDatePicker
      :model-value="modelValue"
      @update:model-value="$emit('update:modelValue', $event)"
      :required="required"
      :text-input="true"
      :enable-time-picker="showTime" 
    />
    <!-- 
          :model-type="showTime ? 'datetime' : 'date'"
      :format="showTime ? 'yyyy-MM-dd HH:mm' : 'yyyy-MM-dd'"

    -->
  </div>
</template>

<script setup>
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

const props = defineProps({
  modelValue: {
    type: [Date, String],
    default: null,
  },
  label: {
    type: String,
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
  showTime: {
    type: Boolean,
    default: true,
  },
});

defineEmits(['update:modelValue']);
</script>


