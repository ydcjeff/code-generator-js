import { reactive } from 'vue'

export const store = reactive({
  config: {}
})

export function saveConfig(key, value) {
  if (store.config[key] === undefined || store.config[key] !== value) {
    store.config[key] = value
  }
}

export function getTemplateFileNames() {
  const modules = import.meta.glob('./templates/**/*.{py,md,txt,json}?raw')
  return Object.keys(modules).map((value) => value.replace('./templates/', ''))
}
