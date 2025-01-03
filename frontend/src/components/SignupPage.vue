<template>
  <div class="signup">
    <h2>Sign Up</h2>
    <form @submit.prevent="signup">
      <div>
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="email">Email</label>
        <input type="email" id="email" v-model="email" required />
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div>
        <label for="confirmPassword">Confirm Password</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required />
      </div>
      <button type="submit">Sign Up</button>
    </form>
    <p>Already have an account? <router-link to="/login">Login</router-link></p>
  </div>
</template>

<script>
// You can use 'mapActions' if you're directly dispatching actions from Vuex, but
// here it is not being used so you can remove it.
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    async signup() {
      if (this.password !== this.confirmPassword) {
        alert("Passwords don't match");
        return;
      }
      try {
        const response = await this.$axios.post('http://127.0.0.1:5000/api/auth/signup', {
          username: this.username,
          email: this.email,
          password: this.password
        });

        localStorage.setItem('token', response.data.access_token);
        this.$router.push('/');  // Redirect after successful signup
      } catch (error) {
        alert('Error signing up');
      }
    }
  }
};
</script>

<style scoped>
/* Add your styles here */
</style>