<template>
  <Teleport to="body">
    <Transition name="confirm-modal">
      <div
        v-if="show"
        class="fixed inset-0 z-[120] flex items-center justify-center p-4"
      >
        <div
          class="absolute inset-0 bg-black/60 backdrop-blur-md"
          @click="$emit('close')"
        ></div>

        <div class="relative bg-gray-900 border border-gray-700 rounded-2xl w-full max-w-sm overflow-hidden shadow-2xl">
          <div class="p-6 text-center">
            <div class="w-16 h-16 bg-red-900/30 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4 border border-red-900/50">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                />
              </svg>
            </div>

            <h3 class="text-xl font-black text-white mb-2">{{ title }}</h3>
            <p class="text-gray-400 text-sm mb-6">{{ message }}</p>

            <div class="flex gap-3">
              <button
                @click="$emit('close')"
                class="flex-1 px-4 py-2 bg-gray-800 text-gray-300 rounded-lg hover:bg-gray-700 transition font-bold"
              >
                Отмена
              </button>
              <button
                @click="$emit('confirm')"
                class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-500 transition font-bold shadow-lg shadow-red-900/20"
              >
                {{ confirmText }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
defineProps({
  show:        { type: Boolean, default: false },
  title:       { type: String,  default: 'Вы уверены?' },
  message:     { type: String,  default: 'Это действие нельзя будет отменить.' },
  // Текст кнопки подтверждения — компонент универсальный, не только для удаления
  confirmText: { type: String,  default: 'Удалить' },
});

defineEmits(['close', 'confirm']);
</script>

<style scoped>
.confirm-modal-enter-active,
.confirm-modal-leave-active {
  transition: opacity 0.2s ease;
}
.confirm-modal-enter-active .relative,
.confirm-modal-leave-active .relative {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.confirm-modal-enter-from,
.confirm-modal-leave-to {
  opacity: 0;
}
.confirm-modal-enter-from .relative {
  transform: scale(0.95);
  opacity: 0;
}
.confirm-modal-leave-to .relative {
  transform: scale(0.95);
  opacity: 0;
}
</style>