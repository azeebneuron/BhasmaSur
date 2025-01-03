<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'user'])
  },
  created() {
    if (this.isAuthenticated) {
      this.$store.dispatch('fetchUser');
    }
  }
};
</script>

<style>
/* Simple CSS */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  color: #2c3e50;
  margin-top: 60px;
}
</style>