<template>
  <div class="left-pane-tabs">
    <button
      v-for="tab in tabs"
      :key="tab"
      class="left-pane-tab"
      :class="{ active: currentTab === tab }"
      @click="currentTab = tab"
    >
      {{ tab }}
    </button>
  </div>
  <div class="left-pane-contexts">
    <KeepAlive>
      <component :is="currentTabComponent"></component>
    </KeepAlive>
  </div>
</template>

<script>
import TabModel from './TabModel.vue'
import TabTraining from './TabTraining.vue'
import TabHandlers from './TabHandlers.vue'
import TabLoggers from './TabLoggers.vue'

export default {
  components: {
    TabModel,
    TabTraining,
    TabLoggers,
    TabHandlers
  },
  computed: {
    currentTabComponent() {
      return 'tab-' + this.currentTab.toLowerCase()
    }
  },
  data() {
    return {
      currentTab: 'Model',
      tabs: ['Model', 'Training', 'Handlers', 'Loggers']
    }
  }
}
</script>

<style scoped>
.left-pane-tabs {
  padding: 2px 0;
  border-bottom: 1px solid var(--c-white-dark);
}
.left-pane-tabs,
.left-pane-contexts {
  padding-left: 1.5rem;
}
.left-pane-tab {
  cursor: pointer;
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  text-align: center;
  border-radius: 4px;
  padding: 0.4rem 0.8rem;
  margin: 2px;
  transition: background-color 0.1s ease-in;
}
.left-pane-tab:hover,
.active {
  background-color: var(--c-brand-red);
  color: var(--c-white-light);
  transition: background-color 0.25s ease-in-out;
}
.left-pane-contexts {
  height: 100vh;
  overflow: auto;
}
</style>
