<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-950 via-blue-950 to-gray-950 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Карточка входа -->
      <div class="bg-gradient-to-b from-gray-900 to-gray-950 rounded-2xl shadow-2xl border border-gray-800 p-8">
        <!-- Заголовок -->
        <div class="text-center mb-8">
          <div class="text-4xl font-black mb-2 bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
            CRM+LMS
          </div>
          <p class="text-gray-400 text-sm">Система управления обучением</p>
        </div>
        
        <!-- Форма -->
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Email</label>
            <input
              v-model="email"
              type="email"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
              placeholder="teacher@example.com"
            />
          </div>
          
          <div>
            <label class="block text-sm font-semibold text-gray-300 mb-2">Пароль</label>
            <input
              v-model="password"
              type="password"
              class="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition"
              placeholder="••••••••"
            />
          </div>
          
          <button
            type="submit"
            class="w-full px-4 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-lg transition duration-200 shadow-lg hover:shadow-blue-500/50"
          >
            Войти
          </button>
        </form>
        
        <!-- Помощь -->
        <div class="mt-8 pt-6 border-t border-gray-800">
          <p class="text-gray-400 text-xs font-semibold mb-3">ТЕСТОВЫЕ УЧЁТНЫЕ ЗАПИСИ:</p>
          <div class="space-y-2">
            <div class="bg-gray-800/50 rounded p-3">
              <p class="text-xs text-gray-400">Репетитор:</p>
              <p class="text-sm font-mono text-blue-300">tutor@example.com</p>
            </div>
            <div class="bg-gray-800/50 rounded p-3">
              <p class="text-xs text-gray-400">Ученик:</p>
              <p class="text-sm font-mono text-cyan-300">student@example.com</p>
            </div>
          </div>
          <p class="text-xs text-gray-500 mt-3">Пароль: любой</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// --- ИМПОРТЫ ---
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { login } from '../stores/auth.js';

// --- ЗАВИСИМОСТИ ---
const router = useRouter();

// --- СОСТОЯНИЕ ---
const email = ref('');
const password = ref('');

// --- ДЕЙСТВИЯ  ---
/**
 * Обработка отправки формы авторизации
 */
async function handleLogin() {
  // Простая валидация на заполненность полей
  if (!email.value || !password.value) return;

  try {
    // Вызов метода авторизации из стора
    await login(email.value, password.value);
    
    // Редирект в зависимости от роли пользователя (преподаватель или студент)
    const isTutor = email.value.includes('tutor');
    const redirectPath = isTutor ? '/schedule' : '/my/dashboard';
    
    router.push(redirectPath);
  } catch (error) {
    console.error('Ошибка при авторизации:', error);
    // Здесь позже появится вызов модалки или уведомления об ошибке
  }
}
</script>
