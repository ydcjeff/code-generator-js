import { reactive } from 'vue'

export const store = reactive({
  config: {}
})

export default function saveConfig(key, value) {
  if (store.config[key] === undefined || store.config[key] !== value) {
    store.config[key] = value
  }
}
