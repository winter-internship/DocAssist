<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup lang="ts">
import { onMounted, watch } from 'vue';
import { useAuthStore } from './stores/auth';

const authStore = useAuthStore();

function applyFontSize(size: string) {
  const s = size || 'md';
  document.documentElement.setAttribute('data-size', s);
}

// Watch for changes in user settings
watch(
  () => authStore.user?.profile_settings?.ui?.fontSize,
  (newSize) => {
    if (newSize) {
      applyFontSize(newSize);
    }
  },
  { immediate: true }
);

onMounted(() => {
  // Initial load from localStorage if user not yet loaded or as fallback
  const localSettings = localStorage.getItem('profile_settings');
  if (localSettings) {
    try {
      const parsed = JSON.parse(localSettings);
      if (parsed.ui?.fontSize) {
        applyFontSize(parsed.ui.fontSize);
      }
    } catch (e) {
      console.error('Failed to parse local profile settings', e);
    }
  }
});
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  width: 100%;
  min-height: 100vh;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
</style>

