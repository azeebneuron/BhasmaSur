// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../components/LoginPage.vue';
import SignupPage from '../components/SignupPage.vue';
import UserDashboard from '@/components/UserDashboard.vue';

const routes = [
  { path: '/login', component: LoginPage },
  { path: '/signup', component: SignupPage },
  { path: '/dashboard', component: UserDashboard }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;