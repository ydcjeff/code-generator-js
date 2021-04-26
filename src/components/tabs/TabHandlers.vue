<template>
  <template v-for="(key, index) in Object.keys(handlers)" :key="index">
    <p>
      {{ handlers[key].description }} -
      <code>{{ key }}</code>
    </p>
    <input
      type="text"
      v-for="(value, key, index) in handlers[key].options"
      :key="index"
      placeholder="Please fill out this field."
    />
    {{ key }}
  </template>
</template>

<script>
import ConfigComponent from '../configurations/ConfigComponent.vue'
import handlersConfig from '../../metadata/handlers.json'
import { store } from '../../store'

export default {
  components: {
    ConfigComponent
  },
  data() {
    return {
      handlers: handlersConfig
    }
  },
  methods: {
    addConfig(key, value) {
      if (store.config[key] === undefined || store.config[key] !== value) {
        store.config[key] = value
      }
    }
  }
}
</script>

<style></style>
