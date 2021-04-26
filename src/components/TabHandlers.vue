<template>
  <div class="handlers">
    <p>{{ _to_save.description }}</p>
    <div
      v-for="(value, key, index) in _to_save.options"
      :key="index"
      class="saving"
    >
      <input
        :id="key"
        :type="value.type"
        :value="key"
        v-model="to_save[key]"
        @change="saveConfig('to_save', to_save)"
        placeholder="Please fill out this field."
      />
      <label :for="key">{{ titleCase(key) }} ({{ value.description }})</label>
    </div>
    <div v-for="(h, index) in restHandlers" :key="index">
      <template v-if="h.type === 'checkbox'">
        <input
          :id="h.name"
          :type="h.type"
          v-model="restHandlersValue[h.name]"
          @change="saveConfig(h.name, restHandlersValue[h.name])"
        />
        <label :for="h.name">{{ h.description }}</label>
      </template>
      <template v-else-if="h.type === 'number'">
        <label :for="h.name">{{ h.description }}</label>
        <input
          :id="h.name"
          :type="h.type"
          v-model.number="restHandlersValue[h.name]"
          @change="saveConfig(h.name, restHandlersValue[h.name])"
          placeholder="Please fill out this field."
        />
      </template>
      <template v-else>
        <label :for="h.name">{{ h.description }}</label>
        <input
          :id="h.name"
          :type="h.type"
          v-model.trim="restHandlersValue[h.name]"
          @change="saveConfig(h.name, restHandlersValue[h.name])"
          placeholder="Please fill out this field."
        />
      </template>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import handlers from '../metadata/handlers.json'
import saveConfig from '../store'
const { to_save, ...restHandlers } = handlers

export default {
  setup() {
    const restHandlersObj = {}
    for (const k of Object.keys(restHandlers)) {
      restHandlersObj[k] = ''
    }
    const restHandlersValue = ref(restHandlersObj)
    const to_save = ref({})
    return { to_save, restHandlers, restHandlersValue, saveConfig }
  },
  data() {
    return {
      _to_save: to_save
    }
  },
  methods: {
    titleCase(value) {
      return value[0].toUpperCase() + value.slice(1)
    }
  }
}
</script>

<style>
.handlers {
  margin: 1.5rem;
  padding: 1.5rem;
}
.saving {
  margin: 1rem;
}
input {
  margin-right: 0.5rem !important;
}
</style>
