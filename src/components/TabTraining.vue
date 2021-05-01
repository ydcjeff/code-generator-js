<template>
  <div class="tab training">
    <h1>Training Options</h1>
    <h2 class="training">Deterministic Training</h2>
    <label :for="deterministic.name">
      <input
        :name="deterministic.name"
        :id="deterministic.name"
        :type="deterministic.type"
        v-model="isDeterministic"
        @change="saveDeterministic"
      />
      {{ deterministic.description }}</label
    >
    <h2 class="training">Distributed Training</h2>
    <div
      v-for="(d, index) in distributedConfigs"
      :key="index"
      class="inputs-wrapper distributed"
    >
      <label :for="d.name">{{ d.description }}</label>
      <input
        :name="d.name"
        :type="d.type"
        :id="d.name"
        v-if="d.type === 'number'"
        v-model.number="distributedValue[d.name]"
        @change="saveDistributed(d.name, distributedValue[d.name])"
      />
      <input
        :name="d.name"
        :type="d.type"
        :id="d.name"
        v-else
        v-model.trim="distributedValue[d.name]"
        @change="saveDistributed(d.name, distributedValue[d.name])"
      />
      <span class="expand"></span>
    </div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import {
  deterministic,
  nproc_per_node,
  nnodes,
  master_addr,
  master_port
} from '../metadata/training.json'
import { saveConfig } from '../store'

export default {
  setup() {
    const isDeterministic = ref(false)
    const distributedValue = ref({})
    const distributedConfigs = [
      nproc_per_node,
      nnodes,
      master_addr,
      master_port
    ]

    // computed properties
    const saveDeterministic = computed(() => {
      saveConfig(deterministic.name, isDeterministic.value)
    })
    return {
      deterministic,
      isDeterministic,
      saveDeterministic,
      distributedConfigs,
      distributedValue,
      saveDistributed
    }
  }
}

function saveDistributed(key, value) {
  saveConfig(key, value)
}
</script>

<style scoped>
@import url('../assets/main.css');

.training {
  margin-bottom: 0;
}
.training ~ label {
  display: block;
  margin-top: 0.5rem;
  width: max-content;
}
.tab .distributed label {
  display: block;
  margin-top: 0.5rem;
  margin-bottom: 0.25rem;
  width: max-content;
}
</style>
