import { createApp } from 'vue'
import App from './App.vue'
import 'virtual:windi.css'

// if (window.matchMedia('(prefers-color-scheme: dark)').matches)
//   document.documentElement.classList.add('dark')
// else document.documentElement.classList.add('light')

createApp(App).mount('#app')
