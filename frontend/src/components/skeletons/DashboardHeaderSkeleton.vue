<template>
  <div class="animate-pulse">
    <div class="mb-8 flex justify-between items-start">
      <div>
        <div class="h-10 w-64 bg-gray-700 rounded-lg mb-2"></div>
        <div class="h-4 w-48 bg-gray-800 rounded-md"></div>
      </div>
      <div class="h-10 w-24 bg-gray-800 rounded-lg"></div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-gray-800/40 rounded-xl border border-gray-700/50 p-4 h-[108px] flex flex-col justify-between">
        <div class="h-3 w-28 bg-blue-500/20 rounded"></div>
        <div class="h-6 w-36 bg-gray-700 rounded mt-2"></div>
        <div class="h-3 w-20 bg-gray-800 rounded mt-1"></div>
      </div>

      <div class="bg-gray-800/40 rounded-xl border border-gray-700/50 p-4 h-[108px] flex flex-col justify-between">
        <div class="h-3 w-28 bg-emerald-500/20 rounded"></div>
        <div class="h-8 w-16 bg-gray-700 rounded mt-2"></div>
        <div class="h-3 w-24 bg-gray-800 rounded mt-1"></div>
      </div>

      <div class="bg-gray-800/40 rounded-xl border border-gray-700/50 p-4 h-[108px] flex flex-col justify-between">
        <div class="h-3 w-24 bg-gray-700 rounded"></div>
        <div class="h-8 w-24 bg-gray-700 rounded mt-2"></div>
      </div>

      <div class="bg-gray-800/40 rounded-xl border border-gray-700/50 p-4 h-[108px] flex flex-col justify-between">
        <div class="h-3 w-24 bg-purple-500/20 rounded"></div>
        <div class="h-6 w-32 bg-gray-700 rounded mt-2"></div>
      </div>
    </div>
  </div>
</template>