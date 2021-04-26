<template>
  <div class="code-block-wrapper">
    <div :class="className">
      <pre><code v-html="highlightCode"></code></pre>
      <div class="line-numbers-wrapper">
        <template v-for="i in getlineNumbers()" :key="i">
          <span class="line-numbers">{{ i }}</span>
          <br />
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import prism from 'prismjs'
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-python'
import 'prismjs/themes/prism-tomorrow.css'

export default {
  data() {
    return {
      className: `language-${this.lang}`
    }
  },
  computed: {
    highlightCode() {
      return prism.highlight(this.code, prism.languages[this.lang], this.lang)
    }
  },
  methods: {
    getlineNumbers() {
      return this.code.split('\n').length
    }
  },
  props: {
    lang: {
      type: String,
      default: 'py'
    },
    code: String
  }
}
</script>

<style scoped>
.code-block-wrapper {
  overflow: auto;
  height: 100vh;
}
div[class*='language-'] {
  position: relative;
}

div[class*='language-']::before {
  position: absolute;
  color: var(--c-white-dark);
  font-size: 0.75rem;
  z-index: 3;
  right: 1em;
  top: 0.5em;
}

[class*='language-'] pre {
  position: relative;
  margin: 0.85rem 0;
  padding: 1.25rem 1.5rem;
  padding-left: 4.5rem;
  vertical-align: middle;
  overflow: auto;
  border-radius: 0 3px 3px 0;
  font-size: var(--font-size) !important;
}

/* font-size is pre's font-size * code's font-size */
[class*='language-'] code {
  padding: 0;
  border-radius: 0;
  line-height: var(--code-line-height);
}

.line-numbers-wrapper {
  position: absolute;
  top: 0;
  bottom: 0;
  z-index: 3;
  border-right: 1px solid rgba(0, 0, 0, 0.5);
  padding: 1.25rem 0;
  width: 3.5rem;
  text-align: center;
  font-family: var(--code-font-family);
  font-size: var(--font-size);
  line-height: var(--code-line-height);
  color: var(--c-white-dark);
  background-color: #2d2d2d;
}

/* font-size is .line-numbers-wrapper's font-size * .line-numbers's font-size */
.line-numbers {
  position: relative;
  font-size: var(--code-font-size);
  z-index: 4;
  user-select: none;
}

div[class~='language-md']::before,
div[class~='language-markdown']::before {
  content: 'md';
}

div[class~='language-json']::before {
  content: 'json';
}

div[class~='language-py']::before,
div[class~='language-python']::before {
  content: 'py';
}

div[class~='language-sh']::before,
div[class~='language-bash']::before {
  content: 'sh';
}

div[class~='language-yaml']::before {
  content: 'yaml';
}
</style>
