<template>
  <h1>Training Options</h1>
  <config-component
    title="Distributed Training Options"
    :configsFromFile="tranining"
    @add-config="saveConfig"
  ></config-component>
</template>

<script>
import ConfigComponent from './configurations/ConfigComponent.vue'
import trainingConfig from '../metadata/training.json'
import saveConfig from '../store'

export default {
  components: {
    ConfigComponent
  },
  data() {
    return {
      tranining: trainingConfig,
      saveConfig
    }
  }
}
</script>

<style></style>
