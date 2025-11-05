<template>
  <div class="input-group mb-3">
    <span class="input-group-text">
      <i class="bi bi-envelope"></i>
    </span>
    <input
      type="email"
      class="form-control"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      :required="required"
    />
  </div>
</template>

<script setup>
defineProps({
  modelValue: String,
  required: Boolean,
});

defineEmits(['update:modelValue']);
</script>
