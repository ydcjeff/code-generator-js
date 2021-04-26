<template>
  <div class="right-pane-tabs">
    <button></button>
    <code-block lang="json" :code="formattedCode"></code-block>
  </div>
</template>

<script>
import CodeBlock from './CodeBlock.vue'
import { store } from '../store'

export default {
  components: {
    CodeBlock
  },
  data() {
    return {
      code: store.config
    }
  },
  computed: {
    formattedCode() {
      return JSON.stringify(this.code, null, 2)
    }
  }
}
</script>
