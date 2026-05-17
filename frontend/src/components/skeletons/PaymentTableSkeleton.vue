<template>
  <div class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
    <div class="bg-gray-900 px-6 py-4 border-b border-gray-700 flex justify-between items-center">
      <div class="h-4 bg-gray-700 rounded w-24 animate-pulse"></div>
      <div class="h-4 bg-gray-700 rounded w-48 animate-pulse"></div>
      <div class="h-4 bg-gray-700 rounded w-20 animate-pulse"></div>
      <div class="h-4 bg-gray-700 rounded w-16 animate-pulse"></div>
    </div>

    <div class="divide-y divide-gray-700">
      <div v-for="i in 3" :key="i" class="px-6 py-5 flex justify-between items-center">
        <div class="w-24">
          <div class="h-4 bg-gray-700 rounded w-20 animate-pulse"></div>
        </div>
        <div class="flex-1 px-4">
          <div class="h-4 bg-gray-700 rounded w-2/3 mb-2 animate-pulse"></div>
          <div class="h-3 bg-gray-700/60 rounded w-1/3 animate-pulse"></div>
        </div>
        <div class="w-32 flex justify-start">
          <div class="h-6 bg-gray-700 rounded-full w-24 animate-pulse"></div>
        </div>
        <div class="w-20 text-right flex justify-end">
          <div class="h-4 bg-gray-700 rounded w-16 animate-pulse"></div>
        </div>
      </div>
    </div>
  </div>
</template>