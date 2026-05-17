<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl">

        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-white">Редактировать связь</h2>
          <button @click="$emit('close')" class="text-gray-500 hover:text-white transition text-xl">✕</button>
        </div>

        <form @submit.prevent="submit" class="space-y-4">

          <!-- Информация о ребенке (только для чтения) -->
          <div class="p-3 bg-gray-800 rounded-lg border border-gray-700">
            <p class="text-xs text-gray-500 uppercase mb-1">Ученик</p>
            <p class="text-white font-semibold">
              {{ child.last_name }} {{ child.first_name }}
            </p>
          </div>

          <!-- Главный контакт -->
          <div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                v-model="form.is_main"
                class="w-4 h-4 rounded border-gray-600 bg-gray-700 accent-blue-500"
              />
              <span class="text-sm font-semibold text-gray-300">Главный контакт</span>
            </label>
            <p class="text-xs text-gray-500 mt-1">
              ✓ Включено = этот родитель основной контакт для ребенка
            </p>
          </div>

          <!-- Кнопки -->
          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition"
            >
              Сохранить
            </button>
            <button
              type="button"
              @click="$emit('close')"
              class="flex-1 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-white font-semibold transition"
            >
              Отмена
            </button>
          </div>

        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue';
import { updateParentChildLink } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  child: { type: Object, required: true },
  parentId: { type: Number, required: true },
  initialIsMain: { type: Boolean, default: false },
});

const emit = defineEmits(['close', 'saved']);

const form = ref({
  is_main: false,
});

watch(() => props.initialIsMain, (value) => {
  form.value.is_main = value;
}, { immediate: true });

async function submit() {
  try {
    // Обновляем связь parent_child
    await updateParentChildLink(props.parentId, props.child.child_id, form.value.is_main);

    Swal.fire({
      icon: 'success',
      title: 'Связь обновлена',
      timer: 1250,
      showConfirmButton: false,
      background: '#111827',
      color: '#fff',
    });

    emit('saved');
    emit('close');
  } catch (e) {
    Swal.fire({
      icon: 'error',
      title: 'Ошибка',
      text: e.message,
      background: '#111827',
      color: '#fff',
    });
  }
}
</script>