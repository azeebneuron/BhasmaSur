import { createApp } from 'vue'; // Import createApp from Vue 3
import App from './App.vue';
import router from './router';
import store from './store';
import axios from 'axios';

const app = createApp(App); // Create the Vue app instance

// Set up axios globally
axios.defaults.baseURL = 'http://127.0.0.1:5000'; // Set the base URL for your API
axios.defaults.headers.common['Authorization'] = `Bearer ${localStorage.getItem('token')}`; // Attach token

app.config.globalProperties.$axios = axios; // Make axios globally available in the app

app.use(router);  // Use the router
app.use(store);   // Use the store

app.mount('#app');  // Mount the app to the DOM