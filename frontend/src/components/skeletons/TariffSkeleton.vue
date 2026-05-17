<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div 
      v-for="i in 3" 
      :key="i" 
      class="bg-gray-800/50 rounded-2xl border border-gray-700 p-6 animate-pulse flex flex-col h-full"
    >
      <div class="mb-4">
        <div class="flex items-start justify-between mb-2">
          <div class="h-8 w-40 bg-gray-700 rounded-md"></div>
          <div class="h-10 w-10 bg-gray-700 rounded-full"></div>
        </div>
        <div class="h-3 w-20 bg-gray-700/50 rounded"></div>
      </div>

      <div class="mb-6 py-4 border-y border-gray-700">
        <div class="h-4 w-24 bg-gray-700/50 rounded mb-2"></div>
        <div class="h-10 w-32 bg-gray-700 rounded"></div>
      </div>

      <div class="mb-6 p-4 bg-gray-700/20 rounded-lg border border-gray-700/30">
        <div class="h-8 w-full bg-gray-700/50 rounded"></div>
      </div>

      <div class="mb-6 flex items-center gap-2">
        <div class="w-2 h-2 rounded-full bg-gray-700"></div>
        <div class="h-4 w-32 bg-gray-700/50 rounded"></div>
      </div>

      <div class="flex gap-2 mt-auto pt-4 border-t border-gray-700">
        <div class="h-10 flex-1 bg-gray-700/50 rounded-lg"></div>
        <div class="h-10 flex-1 bg-gray-700/50 rounded-lg"></div>
      </div>
    </div>
  </div>
</template>