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
import { getTemplateFileNames, generateCode } from '../store'
import { computed, ref } from 'vue'

export default {
  components: { CodeBlock },
  setup() {
    const currentTab = ref('README.md')
    const tabs = ref(getTemplateFileNames())

    const getLang = computed(() => {
      return currentTab.value.split('.')[1]
    })
    const formattedCode = () => {
      return generateCode(currentTab.value)
    }
    return { currentTab, tabs, getLang, formattedCode }
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
  font-size: var(--font-size);
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
