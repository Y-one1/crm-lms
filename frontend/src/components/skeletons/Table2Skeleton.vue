<template>
  <div>
    <!-- Кнопка-скелетон -->
    <div class="mb-6">
      <div class="animate-pulse rounded-lg bg-gray-600" style="height: 48px; width: 176px;" />
    </div>

    <div class="overflow-hidden rounded-lg border border-gray-700 bg-gray-800">
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-700 bg-gray-900">
            <th class="px-6 py-4 text-left">
              <div class="animate-pulse rounded bg-gray-600" style="height: 16px; width: 32px;" />
            </th>
            <th class="px-6 py-4 text-left">
              <div class="animate-pulse rounded bg-gray-600" style="height: 16px; width: 48px;" />
            </th>
            <th class="px-6 py-4 text-left">
              <div class="animate-pulse rounded bg-gray-600" style="height: 16px; width: 128px;" />
            </th>
            <th class="px-6 py-4 text-right">
              <div class="animate-pulse rounded bg-gray-600 ml-auto" style="height: 16px; width: 80px;" />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="i in 3" :key="i" class="border-b border-gray-700">
            <td class="px-6 py-4">
              <div class="animate-pulse rounded bg-gray-600 mb-2" style="height: 16px; width: 160px;" />
              <div class="animate-pulse rounded bg-gray-600" style="height: 12px; width: 96px; opacity: 0.6;" />
            </td>
            <td class="px-6 py-4">
              <div class="animate-pulse rounded bg-gray-600" style="height: 16px; width: 64px;" />
            </td>
            <td class="px-6 py-4">
              <div class="animate-pulse rounded-full bg-gray-600" style="height: 24px; width: 48px;" />
            </td>
            <td class="px-6 py-4">
              <div class="flex flex-col items-end gap-2">
                <div class="animate-pulse rounded bg-gray-600" style="height: 24px; width: 112px;" />
                <div class="animate-pulse rounded bg-gray-600" style="height: 24px; width: 112px;" />
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>