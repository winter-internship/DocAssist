<template>
  <div class="app">
    <!-- Mobile overlay -->
    <div class="overlay" v-if="sidebarOpen" @click="closeSidebar" />

    <!-- Sidebar Component -->
    <Sidebar :isOpen="sidebarOpen" @close="closeSidebar" />

    <!-- Main Content Area -->
    <div class="main">
      <slot :toggleSidebar="toggleSidebar" :sidebarOpen="sidebarOpen"></slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Sidebar from './Sidebar.vue';

const sidebarOpen = ref(false);

function toggleSidebar() {
  sidebarOpen.value = !sidebarOpen.value;
}

function closeSidebar() {
  sidebarOpen.value = false;
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 280px 1fr;
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, "Noto Sans KR", Arial;
  color: var(--ink);
  background: var(--bg);
}

.main {
  display: grid;
  grid-template-rows: 76px 1fr; /* TopBar Height 76px */
  min-height: 100vh;
}

/* Mobile responsive */
@media (max-width: 820px) {
  .app {
    grid-template-columns: 1fr;
  }
  
  .overlay {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 900;
  }
}

/* Global variable support if needed */
:global(:root) {
  --b1: #1d4ed8;
  --b2: #0ea5e9;
  --ring: rgba(29, 78, 216, 0.18);
}
</style>


