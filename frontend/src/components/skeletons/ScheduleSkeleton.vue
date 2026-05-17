<template>
  <div class="space-y-6">

    <div class="flex justify-between items-center bg-gray-900/50 p-4 rounded-xl border border-gray-800">
      <div>
        <div class="h-3 w-32 bg-gray-700 rounded animate-pulse mb-2"></div>
        <div class="flex items-baseline gap-6">
          <div>
            <div class="h-2 w-20 bg-gray-700 rounded animate-pulse mb-1"></div>
            <div class="h-6 w-12 bg-gray-700 rounded animate-pulse"></div>
          </div>
          <div>
            <div class="h-2 w-20 bg-gray-700 rounded animate-pulse mb-1"></div>
            <div class="h-6 w-12 bg-gray-700 rounded animate-pulse"></div>
          </div>
        </div>
      </div>
      <div class="h-10 w-48 bg-gray-700 rounded-lg animate-pulse"></div>
    </div>

    <div class="flex items-center justify-between">
      <div class="h-10 w-24 bg-gray-700 rounded-lg animate-pulse"></div>
      <div class="text-center">
        <div class="h-3 w-24 bg-gray-700 rounded animate-pulse mx-auto mb-2"></div>
        <div class="h-8 w-56 bg-gray-700 rounded animate-pulse mx-auto mb-3"></div>
        <div class="h-6 w-20 bg-blue-900/50 rounded animate-pulse mx-auto"></div>
      </div>
      <div class="h-10 w-24 bg-gray-700 rounded-lg animate-pulse"></div>
    </div>

    <div class="overflow-x-auto rounded-lg shadow-2xl">
      <div class="bg-gray-800 border border-gray-700 min-w-[740px]">

        <div class="flex bg-gray-900 border-b border-gray-700">
          <div class="w-20 flex-shrink-0 flex items-center justify-center border-r border-gray-700 bg-gray-900">
            <div class="h-4 w-10 bg-gray-700 rounded animate-pulse"></div>
          </div>
          <div class="flex flex-1 w-full">
            <div
              v-for="i in 7"
              :key="i"
              class="flex-1 min-w-[160px] p-4 text-center border-r border-gray-700"
            >
              <div class="h-3 w-6 bg-gray-700 rounded animate-pulse mx-auto mb-2"></div>
              <div class="h-7 w-8 bg-gray-700 rounded animate-pulse mx-auto"></div>
            </div>
          </div>
        </div>

        <div class="flex relative">

          <div class="w-20 flex-shrink-0 border-r border-gray-700 bg-gray-900">
            <div
              v-for="i in 15"
              :key="i"
              class="h-20 flex items-center justify-center border-b border-gray-700"
            >
              <div class="h-4 w-10 bg-gray-700 rounded animate-pulse"></div>
            </div>
          </div>

          <div class="flex flex-1 w-full">
            <div
              v-for="dayIndex in 7"
              :key="dayIndex"
              class="flex-1 min-w-[160px] border-r border-gray-700 relative bg-gray-950/80"
            >
              <div
                v-for="i in 15"
                :key="i"
                class="h-20 border-b border-gray-800/50"
              ></div>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div class="flex gap-6 text-xs font-semibold uppercase tracking-wider px-2">
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
        <div class="h-2 w-8 bg-gray-700 rounded animate-pulse"></div>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-green-500 rounded-full"></div>
        <div class="h-2 w-12 bg-gray-700 rounded animate-pulse"></div>
      </div>
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 bg-red-500 rounded-full"></div>
        <div class="h-2 w-12 bg-gray-700 rounded animate-pulse"></div>
      </div>
    </div>

  </div>
</template>