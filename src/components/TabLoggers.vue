<template>
  <ConfigComponent
    title="Ignite Loggers Options"
    :configsFromFile="loggers"
    @add-config="addConfig"
  ></ConfigComponent>
</template>

<script>
import ConfigComponent from './configurations/ConfigComponent.vue'
import loggersConfig from '../metadata/loggers.json'
import { store } from '../store'

export default {
  components: {
    ConfigComponent
  },
  data() {
    return {
      loggers: loggersConfig
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
