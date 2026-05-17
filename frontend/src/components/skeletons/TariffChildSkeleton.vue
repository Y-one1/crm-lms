<template>
  <div class="space-y-6">

    <!-- Главная карточка тарифа -->
    <div class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 border border-gray-700">

      <!-- Заголовок -->
      <div class="flex justify-between items-start mb-6">
        <div>
          <div class="h-3 w-24 bg-emerald-900/50 rounded animate-pulse mb-2"></div>
          <div class="h-8 w-48 bg-gray-700 rounded animate-pulse mb-2"></div>
          <div class="h-3 w-32 bg-gray-700 rounded animate-pulse"></div>
        </div>
        <div class="h-10 w-10 bg-gray-700 rounded animate-pulse"></div>
      </div>

      <!-- 3 мини-карточки -->
      <div class="grid grid-cols-3 gap-4 mb-6">
        <div v-for="i in 3" :key="i" class="bg-gray-900/60 rounded-xl p-4 border border-gray-700">
          <div class="h-3 w-20 bg-gray-700 rounded animate-pulse mb-2"></div>
          <div class="h-8 w-16 bg-gray-700 rounded animate-pulse mb-1"></div>
          <div class="h-3 w-12 bg-gray-700 rounded animate-pulse"></div>
        </div>
      </div>

      <!-- Прогресс-бар -->
      <div class="mb-6">
        <div class="flex justify-between mb-1">
          <div class="h-3 w-28 bg-gray-700 rounded animate-pulse"></div>
          <div class="h-3 w-20 bg-gray-700 rounded animate-pulse"></div>
        </div>
        <div class="w-full bg-gray-700 rounded-full h-2">
          <div class="h-2 w-2/3 bg-gray-900/60 rounded-full animate-pulse"></div>
        </div>
      </div>

      <!-- Кнопки -->
      <div class="flex gap-3">
        <div class="flex-1 h-9 bg-blue-900/20 border border-blue-500/20 rounded-lg animate-pulse"></div>
        <div class="flex-1 h-9 bg-red-900/20 border border-red-500/20 rounded-lg animate-pulse"></div>
      </div>
    </div>

    <!-- История тарифов -->
    <div>
      <div class="h-5 w-32 bg-gray-700 rounded animate-pulse mb-3"></div>
      <div class="space-y-2">
        <div
          v-for="i in 2"
          :key="i"
          class="flex items-center justify-between px-4 py-3 bg-gray-800 rounded-lg border border-gray-700"
        >
          <div class="h-3 w-20 bg-gray-700 rounded animate-pulse"></div>
          <div class="h-3 w-16 bg-gray-700 rounded animate-pulse"></div>
          <div class="h-3 w-24 bg-gray-700 rounded animate-pulse"></div>
          <div class="h-5 w-12 bg-gray-700 rounded animate-pulse"></div>
        </div>
      </div>
    </div>

  </div>
</template>