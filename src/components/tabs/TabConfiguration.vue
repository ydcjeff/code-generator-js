<template>
  <config-component
    title="Distributed Training Options"
    :configsFromFile="distributed"
    @add-config="addConfig"
  ></config-component>
  <config-component
    title="Ignite Handlers Options"
    :configsFromFile="handlers"
    @add-config="addConfig"
  ></config-component>
  <config-component
    title="Ignite Loggers Options"
    :configsFromFile="loggers"
    @add-config="addConfig"
  ></config-component>
  <button @click="exportJSON">Export</button>
</template>

<script>
import ConfigComponent from '../configurations/ConfigComponent.vue'
import distributedConfig from '../../metadata/distributed.json'
import handlersConfig from '../../metadata/handlers.json'
import loggersConfig from '../../metadata/loggers.json'
import CodeBlock from '../AppCodeBlock.vue'
import { saveAs } from 'file-saver'
import JSZip from 'jszip'
import { store } from '../../store'

export default {
  components: {
    ConfigComponent,
    CodeBlock
  },
  data() {
    return {
      inputValues: store.config,
      distributed: distributedConfig,
      handlers: handlersConfig,
      loggers: loggersConfig
    }
  },
  methods: {
    addConfig(key, value) {
      if (
        this.inputValues[key] === undefined ||
        this.inputValues[key] !== value
      ) {
        this.inputValues[key] = value
        // console.log(store.config)
      }
    },
    exportJSON() {
      let zip = new JSZip()
      const data = JSON.stringify(this.inputValues)
      zip.file('config.json', data)
      zip.generateAsync({ type: 'blob' }).then(function (content) {
        saveAs(content, 'config.zip')
      })
    },
    showValue() {
      return this.inputValues
    }
  }
}
</script>
