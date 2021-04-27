<template>
  <nav-bar />
  <split-pane>
    <template #left>
      <pane-left />
    </template>
    <template #right>
      <pane-right />
    </template>
  </split-pane>
  <footer class="px-6 py-12 text-center text-sm border-t">
    BSD-3-Clause License | Copyright &copy; 2021-present PyTorch-Ignite Team &
    Code-Generator Contributors
  </footer>
</template>

<script>
import NavBar from './components/NavBar.vue'
import SplitPane from './components/PaneSplit.vue'
import PaneRight from './components/PaneRight.vue'
import PaneLeft from './components/PaneLeft.vue'

export default {
  components: {
    NavBar,
    SplitPane,
    PaneRight,
    PaneLeft
  }
}
</script>

<style>
:root {
  --c-white: #fff;
  --c-white-light: #f6f6f6;
  --c-white-dark: rgba(200, 200, 200, 0.8);
  --c-brand-red: #ee4c2c;
  --c-brand-yellow: #eaa700;
  --font-size: 1rem;
  --font-family-base: Avenir, -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, Oxygen, Ubuntu, Cantarell, 'Fira Sans', 'Droid Sans',
    'Helvetica Neue', sans-serif;
  --code-font-family: Menlo, Monaco, Consolas, 'Courier New', monospace;
  --code-font-size: 0.85em;
  --code-line-height: 24px;
  --code-text-light: #476582;
  --code-inline-bg-color: rgba(27, 31, 35, 0.05);
}

html,
body {
  font-family: var(--font-family-base);
  font-size: var(--font-size);
  line-height: 1.5;
  height: 100%;
}

/* overriding prismjs defaults */
pre,
code {
  font-family: var(--code-font-family) !important;
  font-size: var(--code-font-size) !important;
}

/* for three backticks code block */
code {
  margin: 0;
  border-radius: 3px;
  padding: 0.25rem 0.5rem;
  color: var(--code-text-light);
  background-color: var(--code-inline-bg-color);
}
</style>
