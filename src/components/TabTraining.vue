<template>
  <h1>Training Options</h1>
  <ConfigComponent
    title="Distributed Training Options"
    :configsFromFile="tranining"
    @add-config="saveConfig"
  ></ConfigComponent>
</template>

<script>
import ConfigComponent from './configurations/ConfigComponent.vue'
import trainingConfig from '../metadata/training.json'
import { saveConfig } from '../store'

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
