<template>
  <aside class="sidebar" :class="{ open: isOpen }">
    <div class="sb-brand">
      <div class="sb-logo">
        <img src="/logo.png" alt="DoQ" />
      </div>
    </div>

    <nav class="sb-nav">
      <button 
        class="sb-item" 
        :class="{ active: currentRouteName === 'home' }"
        @click="navigate('home')"
      >
        <span class="ico">🏠</span><span class="txt">홈</span>
      </button>

      <button 
        class="sb-item" 
        :class="{ active: currentRouteName === 'drive' }"
        @click="navigate('drive')"
      >
        <span class="ico">🗂️</span><span class="txt">드라이브</span>
      </button>

      <button 
        class="sb-item" 
        :class="{ active: currentRouteName === 'upload' }"
        @click="navigate('upload')"
      >
        <span class="ico">📤</span><span class="txt">업로드</span>
      </button>

      <button 
        class="sb-item" 
        :class="{ active: currentRouteName === 'qa' }"
        @click="navigate('qa')"
      >
        <span class="ico">💬</span><span class="txt">Q&A</span>
      </button>

      <button 
        class="sb-item" 
        :class="{ active: currentRouteName === 'terms' }"
        @click="navigate('terms')"
      >
        <span class="ico">📚</span><span class="txt">용어집</span>
      </button>

      <div class="sb-sep"></div>

      <button 
        class="sb-item" 
        :class="{ active: currentRouteName === 'profile' }"
        @click="navigate('profile')"
      >
        <span class="ico">👤</span><span class="txt">프로필</span>
      </button>

      <button 
        v-if="isAdmin" 
        class="sb-item" 
        :class="{ active: currentRouteName === 'admin' }"
        @click="navigate('admin')"
      >
        <span class="ico">🛡️</span><span class="txt">관리자</span>
      </button>
    </nav>

    <div class="sb-bottom">
      <button class="sb-logout" @click="handleLogout">log out</button>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const props = defineProps<{
  isOpen: boolean;
}>();

const emit = defineEmits<{
  (e: "close"): void;
}>();

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

const currentRouteName = computed(() => route.name);
const isAdmin = computed(() => authStore.user?.role === "ADMIN");

function navigate(name: string) {
  emit("close");
  router.push({ name }).catch(() => {});
}

async function handleLogout() {
  emit("close");
  authStore.logout();
  router.push({ name: "login" });
}
</script>

<style scoped>
.sidebar {
  background: #ffffff; /* var(--sidebar-bg) fallback */
  border-right: 1px solid #e5e7eb;
  backdrop-filter: blur(10px);
  padding: 16px 14px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  /* Fixed width from page styles */
  width: 280px; 
  /* Sticky sidebar */
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}

.sb-brand {
  display: flex;
  align-items: center;
  gap: 0;
  padding: 10px 12px 12px;
}

.sb-logo {
  width: 84px;
  height: 84px;
  border-radius: 22px;
  display: grid;
  place-items: center;
  overflow: hidden;
  margin-left: 0;
}
.sb-logo img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.sb-nav {
  display: grid;
  gap: 6px;
  padding: 0 6px;
}
.sb-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 14px;
  border: 1px solid transparent;
  background: transparent;
  cursor: pointer;
  color: inherit;
  font-weight: 950;
  text-align: left;
}
.sb-item:hover {
  background: rgba(29, 78, 216, 0.08);
  border-color: rgba(29, 78, 216, 0.14);
}
.sb-item.active {
  background: rgba(29, 78, 216, 0.12);
  border-color: rgba(29, 78, 216, 0.18);
}
.ico {
  width: 18px;
  display: grid;
  place-items: center;
}
.txt {
  font-size: 13px;
}
.sb-sep {
  height: 1px;
  background: #e5e7eb;
  margin: 6px 0;
}

.sb-bottom {
  margin-top: auto;
  display: flex;
  gap: 8px;
  padding: 8px 6px 0;
}
.sb-logout {
  width: 100%;
  border-radius: 14px;
  border: 1px solid #2563eb;
  background: #2563eb;
  color: #fff;
  cursor: pointer;
  font-weight: 900;
  padding: 10px 12px;
  text-align: center;
}

/* Mobile Responsive logic handles by parent layout mostly, 
   but specific sidebar transitions can be here */
@media (max-width: 820px) {
  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 260px;
    transform: translateX(-100%);
    transition: transform 0.25s ease;
    z-index: 1000;
  }
  .sidebar.open {
    transform: translateX(0);
  }
}
</style>


