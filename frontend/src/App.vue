<template>
  <div class="bg-gray-900 text-white min-h-screen">
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import { restoreSession } from './stores/auth.js';
import { onMounted } from 'vue';

// При загрузке приложения восстанавливаем сессию
onMounted(() => {
  restoreSession();
});
</script>

<style>
/* Global styles */
body {
  margin: 0;
  padding: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
