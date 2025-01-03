// src/store/index.js
import { createStore } from 'vuex';
import axios from 'axios';

const store = createStore({
  state() {
    return {
      user: null,
      token: localStorage.getItem('token') || '',
    };
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user;
    },
    SET_TOKEN(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    REMOVE_TOKEN(state) {
      state.token = '';
      localStorage.removeItem('token');
    }
  },
  actions: {
    async login({ commit }, { email, password }) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/auth/login', {
          email,
          password
        });

        const { access_token, user } = response.data;
        commit('SET_TOKEN', access_token);
        commit('SET_USER', user);
      } catch (error) {
        console.error(error);
        throw error; // Propagate error to the component
      }
    },
    async signup({ commit }, { username, email, password }) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/auth/signup', {
          username,
          email,
          password
        });

        const { access_token, user } = response.data;
        commit('SET_TOKEN', access_token);
        commit('SET_USER', user);
      } catch (error) {
        console.error(error);
        throw error; // Propagate error to the component
      }
    },
    async fetchUser({ commit }) {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/auth/profile', {
          headers: { Authorization: `Bearer ${this.state.token}` }
        });
        commit('SET_USER', response.data.user);
      } catch (error) {
        console.error(error);
      }
    },
    logout({ commit }) {
      commit('REMOVE_TOKEN');
      commit('SET_USER', null);
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    user: state => state.user
  }
});

export default store;