<template>
  <div class="tab handlers">
    <h1>Ignite Handlers Options</h1>
    <h2>Checkpointing</h2>
    <p>{{ to_save.description }}</p>
    <div
      v-for="(value, key, index) in to_save.options"
      :key="index"
      class="saving"
    >
      <label :for="key">
        <input
          :id="key"
          :type="value.type"
          :value="key"
          v-model="toSave[key]"
          @change="saveConfig(to_save.name, toSave)"
        />
        {{ titleCase(key) }} ({{ value.description }})</label
      >
    </div>
    <div v-for="(h, index) in restHandlers" :key="index" class="inputs-wrapper">
      <template v-if="h.type === 'checkbox'">
        <label :for="h.name">
          <input
            :id="h.name"
            :type="h.type"
            v-model="restHandlersValue[h.name]"
            @change="saveConfig(h.name, restHandlersValue[h.name])"
          />
          {{ h.description }}</label
        >
      </template>
      <template v-else-if="h.type === 'number'">
        <label :for="h.name">{{ h.description }}</label>
        <input
          min="0"
          :id="h.name"
          :type="h.type"
          v-model.number="restHandlersValue[h.name]"
          @change="saveConfig(h.name, restHandlersValue[h.name])"
        />
        <span class="expand"></span>
      </template>
      <template v-else>
        <label :for="h.name">{{ h.description }}</label>
        <input
          :id="h.name"
          :type="h.type"
          v-model.trim="restHandlersValue[h.name]"
          @change="saveConfig(h.name, restHandlersValue[h.name])"
        />
        <span class="expand"></span>
      </template>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import {
  to_save,
  filename_prefix,
  n_saved,
  terminate_on_nan,
  limit_sec
} from '../metadata/utils.json'
import { saveConfig } from '../store'
import FormInput from './FormInput.vue'
import FormCheckbox from './FormCheckbox.vue'

export default {
  components: { FormInput, FormCheckbox },
  setup() {
    const restHandlersValue = ref({
      filename_prefix: '',
      n_saved: '',
      terminate_on_nan: '',
      limit_sec: ''
    })
    const toSave = ref({})
    const restHandlers = [terminate_on_nan, filename_prefix, n_saved, limit_sec]

    return {
      to_save,
      toSave,
      restHandlers,
      restHandlersValue,
      saveConfig,
      titleCase
    }
  }
}

function titleCase(value) {
  return value[0].toUpperCase() + value.slice(1)
}
</script>

<style scoped>
@import url('../assets/main.css');

.tab label {
  display: block;
  width: max-content;
  margin-top: 0.5rem;
  margin-bottom: 0.25rem;
}
.saving {
  margin: 0.75rem;
}
</style>
