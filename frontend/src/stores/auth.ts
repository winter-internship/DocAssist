import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../api/axios';

interface User {
  id: string;
  email: string;
  name: string;
  role: string;
  profile_settings?: any;
  created_at?: string;
  last_login_at?: string;
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'));
  const user = ref<User | null>(null);
  const isAuthenticated = computed(() => !!token.value);

  async function login(email: string, password: string): Promise<boolean> {
    try {
      // OAuth2PasswordRequestForm은 폼 데이터를 기대합니다
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);
      
      const response = await api.post('/auth/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });
      
      token.value = response.data.access_token;
      if (token.value) {
          localStorage.setItem('token', token.value);
          await fetchUser();
      }
      return true;
    } catch (error) {
      console.error('Login failed', error);
      throw error;
    }
  }

  async function signup(userData: { email: string; password: string; name: string }) {
    try {
      await api.post('/auth/signup', userData);
      return true;
    } catch (error) {
      console.error('Signup failed', error);
      throw error;
    }
  }

  async function fetchUser() {
    if (!token.value) return;
    try {
      const response = await api.get('/users/me');
      user.value = response.data;
      // role 저장 (Router 가드용)
      if (user.value?.role) {
        localStorage.setItem('role', user.value.role);
      }
    } catch (error) {
      console.error('Fetch user failed', error);
      // 모든 에러에서 자동 로그아웃을 하지 않음, 상태 체크는 인터셉터에서 하는 것이 좋음
    }
  }

  async function updateUser(data: Partial<User> & { profile_settings?: any }) {
    try {
      const response = await api.patch('/users/me', data);
      user.value = response.data;
      return true;
    } catch (error) {
      console.error('Update user failed', error);
      throw error;
    }
  }

  async function changePassword(currentPassword: string, newPassword: string) {
    try {
      await api.put('/users/me/password', {
        current_password: currentPassword,
        new_password: newPassword,
      });
      return true;
    } catch (error) {
      console.error('Change password failed', error);
      throw error;
    }
  }

  function logout() {
    token.value = null;
    user.value = null;
    localStorage.removeItem('token');
    localStorage.removeItem('role');
  }

  return { token, user, isAuthenticated, login, signup, fetchUser, updateUser, changePassword, logout };
});

