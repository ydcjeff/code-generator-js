<template>
  <div class="right-pane-tabs">
    <button
      v-for="tab in tabs"
      :key="tab"
      class="tab"
      :class="{ active: currentTab === tab }"
      @click="currentTab = tab"
    >
      {{ tab }}
    </button>
  </div>
  <div class="right-pane-contexts">
    <keep-alive>
      <code-block :lang="getLang" :code="formattedCode"></code-block>
    </keep-alive>
  </div>
</template>

<script>
import CodeBlock from './CodeBlock.vue'
import { store, getTemplateFileNames, generateCode } from '../store'

export default {
  components: {
    CodeBlock
  },
  data() {
    return {
      code: store.config,
      currentTab: 'README.md',
      tabs: getTemplateFileNames()
    }
  },
  computed: {
    formattedCode() {
      return generateCode(this.currentTab)
    },
    getLang() {
      return this.currentTab.split('.')[1]
    }
  }
}
</script>

<style scoped>
.right-pane-tabs {
  padding: 2px 0;
  border-bottom: 1px solid var(--c-white-dark);
}
.tab {
  text-align: center;
  border-radius: 4px;
  padding: 0.4rem 0.8rem;
  margin: 2px;
}
.tab:hover {
  background-color: var(--c-white-dark);
}
.tab:focus {
  outline: none;
}
.active {
  background-color: var(--c-white-light);
}
</style>
