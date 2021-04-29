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
      />
      <label :for="key">{{ titleCase(key) }} ({{ value.description }})</label>
    </div>
    <div v-for="(h, index) in restHandlers" :key="index" class="inputs-wrapper">
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
import handlers from '../metadata/handlers.json'
import { saveConfig } from '../store'
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

<style scoped>
.handlers {
  padding: 0 1rem;
}
.saving {
  margin: 0.75rem;
}
input {
  font-family: var(--font-family-base);
  font-size: var(--font-size);
}
input[type='text'],
input[type='number'] {
  border-radius: 3px 3px 0 0;
  border: 1px solid var(--c-white-light);
  background: var(--c-white-light);
  padding: 0.5rem 1rem;
  width: 100%;
}
.inputs-wrapper {
  position: relative;
}
input[type='text'] ~ .expand,
input[type='number'] ~ .expand {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  border-bottom: 2px solid var(--c-brand-red);
  transform: scaleX(0);
  transition: transform 0.25s ease-in-out;
}
input[type='text']:focus,
input[type='number']:focus {
  outline: none;
  background: var(--c-white);
}
input[type='text']:focus ~ .expand,
input[type='number']:focus ~ .expand {
  transform: scaleX(1);
}
</style>
