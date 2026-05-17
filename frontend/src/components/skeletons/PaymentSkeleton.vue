<template>
  <div class="space-y-4">
    <!-- Блок реквизитов -->
    <div class="mb-8 bg-gray-800/50 rounded-2xl p-6 border border-gray-700 animate-pulse">
      <div class="h-4 w-40 bg-gray-700 rounded mb-4"></div>
      <div class="space-y-3">
        <div class="h-3 w-full bg-gray-700 rounded"></div>
        <div class="h-3 w-5/6 bg-gray-700 rounded"></div>
        <div class="h-3 w-4/5 bg-gray-700 rounded"></div>
      </div>
    </div>

    <!-- История платежей header -->
    <div class="h-4 w-48 bg-gray-700 rounded mb-4 animate-pulse"></div>

    <!-- Строки платежей -->
    <div class="space-y-3">
      <div class="bg-gray-800/50 rounded-xl p-4 border border-gray-700 animate-pulse flex justify-between">
        <div class="flex-1 space-y-2">
          <div class="h-4 w-32 bg-gray-700 rounded"></div>
          <div class="h-3 w-24 bg-gray-700 rounded"></div>
        </div>
        <div class="h-6 w-24 bg-gray-700 rounded"></div>
      </div>

      <div class="bg-gray-800/50 rounded-xl p-4 border border-gray-700 animate-pulse flex justify-between">
        <div class="flex-1 space-y-2">
          <div class="h-4 w-32 bg-gray-700 rounded"></div>
          <div class="h-3 w-24 bg-gray-700 rounded"></div>
        </div>
        <div class="h-6 w-24 bg-gray-700 rounded"></div>
      </div>

      <div class="bg-gray-800/50 rounded-xl p-4 border border-gray-700 animate-pulse flex justify-between">
        <div class="flex-1 space-y-2">
          <div class="h-4 w-32 bg-gray-700 rounded"></div>
          <div class="h-3 w-24 bg-gray-700 rounded"></div>
        </div>
        <div class="h-6 w-24 bg-gray-700 rounded"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
// PaymentSkeleton - заглушка загрузки для платежей
</script>
