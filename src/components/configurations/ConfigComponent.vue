<template>
  <div class="px-8 py-4">
    <h1 for="config-select">{{ title }}</h1>
    <input-box
      v-for="(config, index) of configs"
      :key="index"
      :name="config.name"
      :description="config.description"
      :type="config.type"
      @on-add-config="addConfig"
    ></input-box>
  </div>
</template>

<script>
import InputBox from './InputBox.vue'

export default {
  components: {
    InputBox
  },
  data() {
    return {
      configs: this.configsFromFile,
      inputValues: {}
    }
  },
  emits: ['add-config'],
  methods: {
    addConfig(key, value) {
      this.$emit('add-config', key, value)
    }
  },
  props: {
    title: String,
    configsFromFile: Object
  }
}
</script>
