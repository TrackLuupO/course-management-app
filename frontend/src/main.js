import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios';

createApp(App).mount('#app')
// Configure axios defaults
axios.defaults.baseURL = 'http://localhost:8000';