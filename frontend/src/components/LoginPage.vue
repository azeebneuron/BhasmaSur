<template>
  <div class="login">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <router-link to="/signup">Sign up</router-link></p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post('http://127.0.0.1:5000/api/auth/login', {
          email: this.email,
          password: this.password
        });

        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/dashboard');  // Navigation happens here
        console.log(response.data.access_token);
      } catch (error) {
        alert('Invalid credentials or server error');
      }
    }
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>