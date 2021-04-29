<template>
  <div class="right-pane-tabs">
    <button
      v-for="tab in tabs"
      :key="tab"
      class="right-pane-tab"
      :class="{ active: currentTab === tab }"
      @click="currentTab = tab"
    >
      {{ tab }}
    </button>
  </div>
  <div class="right-pane-contexts">
    <KeepAlive>
      <CodeBlock :lang="getLang" :code="formattedCode()" />
    </KeepAlive>
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
  methods: {
    formattedCode() {
      return generateCode(this.currentTab)
    }
  },
  computed: {
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
.right-pane-tabs,
.right-pane-contexts {
  padding-right: 1.5rem;
}
.right-pane-tab {
  cursor: pointer;
  font-family: var(--font-family-base);
  text-align: center;
  border-radius: 4px;
  padding: 0.4rem 0.8rem;
  margin: 2px;
  transition: background-color 0.1s ease-in;
}
.right-pane-tab:hover,
.active {
  background-color: var(--c-brand-red);
  color: var(--c-white-light);
  transition: background-color 0.25s ease-in-out;
}
</style>
