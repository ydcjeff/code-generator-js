import { defineConfig } from 'windicss/helpers'

export default defineConfig({
  darkMode: 'class',
  theme: {
    extend: {
      cursor: {
        'ew-resize': 'ew-resize'
      },
      fontFamily: {
        avenir: ['Avenir']
      }
    }
  }
})
