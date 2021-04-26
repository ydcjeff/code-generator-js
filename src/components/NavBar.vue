<template>
  <nav
    class="flex items-center justify-between p-2 border-b dark:border-true-gray-700"
  >
    <div class="flex items-center">
      <img
        src="/favicon.svg"
        alt="PyTorch-Ignite logo"
        width="50"
        height="50"
        class="w-50px h-50px"
      />
      <span class="text-2xl">Code Generator</span
      ><small class="version">v{{ version }}</small>
    </div>
    <button @click="downloadFiles">Download</button>
    <div class="flex items-center">
      <a
        href="https://github.com/pytorch-ignite/code-generator"
        target="_blank"
        rel="noopener noreferrer"
        class="m-1 border-b hover:border-0"
      >
        GitHub
      </a>
      <a
        href="https://twitter.com/pytorch_ignite"
        target="_blank"
        rel="noopener noreferrer"
        class="m-1 border-b hover:border-0"
      >
        Twitter
      </a>
    </div>
  </nav>
</template>

<script>
import pkg from '../../package.json'
import { store } from '../store'
import { saveAs } from 'file-saver'
import JSZip from 'jszip'

export default {
  data() {
    return {
      version: pkg.version
    }
  },
  methods: {
    downloadFiles() {
      if (
        !(
          store.config.constructor === Object &&
          Object.keys(store.config).length === 0
        )
      ) {
        let zip = new JSZip()
        const data = JSON.stringify(store.config)
        zip.file('config.json', data)
        zip.generateAsync({ type: 'blob' }).then(function (content) {
          saveAs(content, 'config.zip')
        })
      }
    }
  }
}
</script>

<style scoped>
.version {
  padding: 0.25rem 0.5rem;
  margin-left: 0.25rem;
  background-color: #007bff;
  border-radius: 8px 2px 8px 2px;
  color: var(--c-white-light);
  font-weight: bolder;
}
</style>
