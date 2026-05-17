<template>
  <div class="bg-gray-900 rounded-lg border border-gray-800 overflow-hidden">
    <table class="w-full">
      <thead>
        <!-- 6 колонок: ФИО, Класс, Телефон, Добавлен, Последний урок, Действия -->
        <tr class="bg-black/40 border-b border-gray-800 animate-pulse">
          <th v-for="i in 5" :key="i" class="px-6 py-4 text-left">
            <div class="h-4 bg-gray-800 rounded w-24"></div>
          </th>
          <th class="px-6 py-4 text-right">
            <div class="h-4 bg-gray-800 rounded w-16 ml-auto"></div>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="row in 4"
          :key="row"
          class="border-b border-gray-800 animate-pulse"
          :style="{ animationDelay: `${row * 0.1}s` }"
        >
          <!-- ФИО: две строки -->
          <td class="px-6 py-6">
            <div class="h-5 bg-gray-800 rounded w-40 mb-2"></div>
            <div class="h-3 bg-gray-800/40 rounded w-24"></div>
          </td>
          <!-- Класс, Телефон, Добавлен, Последний урок -->
          <td v-for="col in 4" :key="col" class="px-6 py-6">
            <div class="h-4 bg-gray-800 rounded w-28"></div>
          </td>
          <!-- Действия: три кнопки -->
          <td class="px-6 py-6">
            <div class="flex flex-col items-end gap-2">
              <div class="w-28 h-6 bg-gray-800/40 rounded"></div>
              <div class="w-28 h-6 bg-gray-800/40 rounded"></div>
              <div class="w-28 h-6 bg-gray-800/40 rounded"></div>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>