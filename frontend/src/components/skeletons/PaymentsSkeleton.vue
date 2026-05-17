<template>
  <div class="space-y-8">

    <!-- Карточки пульса -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="i in 4"
        :key="i"
        class="h-32 bg-gray-800/60 rounded-2xl border border-gray-700 animate-pulse"
        :style="{ animationDelay: `${i * 0.08}s` }"
      />
    </div>

    <!-- График -->
    <div class="bg-gray-900 rounded-2xl border border-gray-700 p-6">
      <div class="flex justify-between items-center mb-6">
        <div class="space-y-2">
          <div class="h-3 w-36 bg-gray-800 rounded animate-pulse" />
          <div class="h-2 w-24 bg-gray-800/50 rounded animate-pulse" />
        </div>
        <div class="h-4 w-40 bg-gray-800 rounded animate-pulse" />
      </div>
      <div class="flex items-end gap-2 h-40">
        <div
          v-for="(h, i) in barHeights"
          :key="i"
          class="flex-1 bg-gray-800 rounded-t animate-pulse"
          :style="{ height: h + '%', animationDelay: `${i * 0.06}s` }"
        />
      </div>
      <div class="flex gap-2 mt-2">
        <div
          v-for="i in 6"
          :key="i"
          class="flex-1 h-2 bg-gray-800/50 rounded animate-pulse"
          :style="{ animationDelay: `${i * 0.06}s` }"
        />
      </div>
    </div>

    <!-- Журнал -->
    <div class="bg-gray-900 rounded-2xl border border-gray-700 overflow-hidden">
      <div class="flex justify-between items-center p-6 border-b border-gray-700">
        <div class="space-y-2">
          <div class="h-3 w-32 bg-gray-800 rounded animate-pulse" />
          <div class="h-2 w-16 bg-gray-800/50 rounded animate-pulse" />
        </div>
        <div class="flex gap-3">
          <div class="h-9 w-48 bg-gray-800 rounded-lg animate-pulse" />
          <div class="h-9 w-32 bg-gray-800 rounded-lg animate-pulse" />
        </div>
      </div>
      <div
        v-for="(w, i) in rowWidths"
        :key="i"
        class="flex items-center gap-6 px-6 py-4 border-b border-gray-800/60 animate-pulse"
        :style="{ animationDelay: `${i * 0.07}s` }"
      >
        <div class="h-4 w-24 bg-gray-800 rounded" />
        <div class="h-4 bg-gray-800 rounded flex-1" :style="{ maxWidth: w[0] + 'px' }" />
        <div class="h-4 bg-gray-800 rounded" :style="{ width: w[1] + 'px' }" />
        <div class="h-6 w-20 bg-gray-800 rounded-lg" />
        <div class="h-5 w-20 bg-gray-800 rounded ml-auto" />
      </div>
    </div>

  </div>
</template>

<script setup>
// Фиксированные высоты столбцов и ширины строк — выглядит живее чем random при каждом рендере
const barHeights = [45, 70, 55, 90, 40, 75, 60, 85, 50, 65, 80, 35]
const rowWidths  = [
  [140, 100], [160, 90], [130, 110], [155, 95], [145, 105],
  [135, 85],  [165, 100],[125, 115],
]
</script>