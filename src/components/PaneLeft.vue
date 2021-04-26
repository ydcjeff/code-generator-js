<template>
  <div class="left-pane-tabs">
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
  <div class="left-pane-contexts">
    <keep-alive>
      <component :is="currentTabComponent"></component>
    </keep-alive>
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
.left-pane-contexts {
  height: 100vh;
  overflow: auto;
}
</style>
