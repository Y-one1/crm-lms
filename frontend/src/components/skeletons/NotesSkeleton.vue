<template>
  <div class="space-y-3">
    <div
      v-for="i in 3"
      :key="i"
      class="bg-gray-800 rounded-xl border border-gray-700 p-5"
    >
      <!-- Шапка карточки -->
      <div class="flex justify-between items-start mb-3">
        <div class="flex items-center gap-3">
          <div class="h-4 w-40 bg-gray-700 rounded animate-pulse"></div>
          <div class="h-3 w-20 bg-gray-700 rounded animate-pulse"></div>
        </div>
        <div class="h-5 w-20 bg-gray-700 rounded animate-pulse"></div>
      </div>

      <!-- Заметка себе -->
      <div class="mb-3">
        <div class="h-3 w-10 bg-blue-900/50 rounded animate-pulse mb-2"></div>
        <div class="bg-gray-900/50 rounded-lg p-3 space-y-2">
          <div class="h-3 w-full bg-gray-700 rounded animate-pulse"></div>
          <div class="h-3 w-3/4 bg-gray-700 rounded animate-pulse"></div>
        </div>
      </div>

      <!-- Заметка родителям -->
      <div>
        <div class="h-3 w-16 bg-purple-900/50 rounded animate-pulse mb-2"></div>
        <div class="bg-gray-900/50 rounded-lg p-3 space-y-2">
          <div class="h-3 w-full bg-gray-700 rounded animate-pulse"></div>
          <div class="h-3 w-1/2 bg-gray-700 rounded animate-pulse"></div>
        </div>
      </div>
    </div>
  </div>
</template>