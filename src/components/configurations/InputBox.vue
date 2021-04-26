<template>
  <p>
    {{ description }} - <code>{{ name }}</code>
  </p>
  <input
    type="number"
    v-if="type === 'number'"
    v-model.number="inputValue"
    @change="$emit('onAddConfig', name, inputValue)"
    placeholder="Please fill out this field."
  />
  <input
    type="text"
    v-else-if="type === 'text'"
    v-model.trim="inputValue"
    @change="$emit('onAddConfig', name, inputValue)"
    placeholder="Please fill out this field."
  />
  <input
    :type="type"
    v-else
    v-model="inputValue"
    @change="$emit('onAddConfig', name, inputValue)"
    placeholder="Please fill out this field."
  />
</template>

<script>
export default {
  data() {
    return {
      inputValue: ''
    }
  },
  emits: ['onAddConfig'],
  props: {
    name: String,
    description: String,
    type: String
  }
}
</script>
