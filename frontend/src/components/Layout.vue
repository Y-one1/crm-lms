<template>
  <div class="flex h-screen bg-gray-950 text-white">
    <!-- Сайдбар -->
    <aside class="w-64 bg-gradient-to-b from-gray-900 to-gray-950 border-r border-gray-800 p-6 flex flex-col shadow-2xl">
      <div class="mb-8">
        <h2 class="text-2xl font-black bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
          CRM+LMS
        </h2>
        <p class="text-xs text-gray-500 mt-1">Управление обучением</p>
      </div>
      
      <nav class="space-y-1 flex-1">
        <RouterLink
          to="/schedule"
          class="flex items-center px-4 py-3 rounded-lg hover:bg-gray-800 transition duration-200 text-gray-300 hover:text-white"
          :class="{ 'bg-blue-900 text-blue-300': isActive('/schedule') }"
        >
          <span class="text-lg mr-3">📅</span>
          <span class="font-medium">Расписание</span>
        </RouterLink>
        
        <RouterLink
          to="/children"
          class="flex items-center px-4 py-3 rounded-lg hover:bg-gray-800 transition duration-200 text-gray-300 hover:text-white"
          :class="{ 'bg-blue-900 text-blue-300': isActive('/children') }"
        >
          <span class="text-lg mr-3">👥</span>
          <span class="font-medium">Ученики</span>
        </RouterLink>
        
        <RouterLink
          to="/parents"
          class="flex items-center px-4 py-3 rounded-lg hover:bg-gray-800 transition duration-200 text-gray-300 hover:text-white"
          :class="{ 'bg-blue-900 text-blue-300': isActive('/parents') }"
        >
          <span class="text-lg mr-3">👨‍👩‍👧</span>
          <span class="font-medium">Родители</span>
        </RouterLink>
        
        <RouterLink
          to="/tariffs"
          class="flex items-center px-4 py-3 rounded-lg hover:bg-gray-800 transition duration-200 text-gray-300 hover:text-white"
          :class="{ 'bg-blue-900 text-blue-300': isActive('/tariffs') }"
        >
          <span class="text-lg mr-3">💰</span>
          <span class="font-medium">Тарифы</span>
        </RouterLink>
        
        <RouterLink
          to="/payments"
          class="flex items-center px-4 py-3 rounded-lg hover:bg-gray-800 transition duration-200 text-gray-300 hover:text-white"
          :class="{ 'bg-blue-900 text-blue-300': isActive('/payments') }"
        >
          <span class="text-lg mr-3">🧾</span>
          <span class="font-medium">Платежи</span>
        </RouterLink>
      </nav>
      
      <div class="border-t border-gray-800 pt-4">
        <RouterLink
          to="/profile"
          class="block px-4 py-3 mb-3 bg-gray-900 hover:bg-gray-800 rounded-lg transition cursor-pointer"
          :class="{ 'ring-1 ring-blue-500': isActive('/profile') }"
        >
          <p class="text-xs text-gray-500 mb-1">Авторизован как</p>
          <p class="text-sm font-medium text-gray-200">{{ user?.name || 'Гость' }}</p>
          <p class="text-xs text-gray-600 mt-0.5">⚙️ Профиль</p>
        </RouterLink>
        <button
          @click="handleLogout"
          class="w-full px-4 py-2 bg-red-900/50 hover:bg-red-900 text-red-300 hover:text-red-100 font-medium rounded-lg transition duration-200 border border-red-800"
        >
          Выход
        </button>
      </div>
    </aside>
    
    <!-- Основной контент -->
    <main class="flex-1 overflow-auto bg-gray-950">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { RouterLink, useRoute } from 'vue-router';
import { useRouter } from 'vue-router';
import { logout, user } from '../stores/auth.js';

const router = useRouter();
const route = useRoute();

function handleLogout() {
  logout();
  router.push('/login');
}

function isActive(path) {
  return route.path === path;
}
</script>
