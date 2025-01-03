<!-- src/components/Dashboard.vue -->
<template>
    <div v-if="user">
      <h1>Hello, {{ user.username }}!</h1>
    </div>
    <div v-else>
      <h1>Please log in to see your dashboard.</h1>
    </div>
  </template>
  
  <script>
  export default {
    computed: {
      user() {
        return this.$store.getters.user; // Get user from Vuex store
      }
    }
  };
  </script>
  
  <style scoped>
  h1 {
    font-size: 2rem;
    color: #333;
  }
  </style>