<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl">

        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-white">
            {{ initialData ? 'Редактировать ученика' : 'Новый ученик' }}
          </h2>
          <button @click="$emit('close')" class="text-gray-500 hover:text-white transition text-xl">✕</button>
        </div>

        <form @submit.prevent="submit" class="space-y-4">

          <div class="grid grid-cols-2 gap-4">
            <div class="col-span-2">
              <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Фамилия *</label>
              <input
                v-model="form.last_name"
                type="text"
                required
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Имя *</label>
              <input
                v-model="form.first_name"
                type="text"
                required
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Отчество</label>
              <input
                v-model="form.patronymic"
                type="text"
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Класс *</label>
            <select
              v-model.number="form.school_class"
              required
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
            >
              <option value=""></option>
              <option v-for="n in 11" :key="n" :value="n">{{ n }} класс</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Телефон *</label>
            <input
              :value="phoneDisplay"
              @input="handlePhoneInput"
              type="tel"
              placeholder="+7 (999) 123-45-67"
              required
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              :class="phoneError ? 'border-red-500 focus:ring-red-500' : ''"
            />
            <p v-if="phoneError" class="text-xs text-red-400 mt-1">{{ phoneError }}</p>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Заметки</label>
            <textarea
              v-model="form.notes"
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition h-20 resize-none"
              placeholder="Особенности ученика, предпочтения..."
            ></textarea>
          </div>

          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition"
            >
              {{ initialData ? 'Обновить' : 'Сохранить' }}
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
// --- ИМПОРТЫ ---
import { ref, watch } from 'vue';
import { usePhone } from '../../composables/usePhone.js';
import { createChild, updateChild } from '../../api/client.js';
import Swal from 'sweetalert2';

// --- ПРОПСЫ И ЭМИТЫ ---

const props = defineProps({
  // null = режим создания, объект = режим редактирования
  initialData: { type: Object, default: null },
});

const emit = defineEmits(['close', 'saved']);

// --- СОСТОЯНИЕ ---

const { phoneDisplay, phoneError, phoneValue, handlePhoneInput, setPhone, resetPhone } = usePhone();

const form = ref(buildForm());

// --- ЗАГРУЗКА / СБРОС ФОРМЫ ---

function buildForm() {
  return {
    last_name:    '',
    first_name:   '',
    patronymic:   '',
    school_class: '',
    notes:        '',
  };
}

// Заполняем форму при открытии в режиме редактирования, сбрасываем при создании
watch(
  () => props.initialData,
  (data) => {
    if (data) {
      form.value = {
        last_name:    data.last_name,
        first_name:   data.first_name,
        patronymic:   data.patronymic   || '',
        school_class: data.school_class,
        notes:        data.notes        || '',
      };
      setPhone(data.phone_number);
    } else {
      form.value = buildForm();
      resetPhone();
    }
  },
  { immediate: true }
);

// --- ДЕЙСТВИЯ ---

async function submit() {
  if (phoneError.value || !phoneValue.value) {
    return Swal.fire({
      icon:       'warning',
      title:      'Проверь номер телефона',
      background: '#111827',
      color:      '#fff',
    });
  }

  const payload = {
    ...form.value,
    patronymic:   form.value.patronymic || null,
    notes:        form.value.notes      || null,
    phone_number: phoneValue.value,
  };

  try {
    const isEdit = Boolean(props.initialData);
    const result = isEdit
      ? await updateChild(props.initialData.child_id, payload)
      : await createChild(payload);

    Swal.fire({
      icon:              'success',
      title:             isEdit ? 'Данные обновлены' : 'Ученик добавлен',
      timer:             1250,
      showConfirmButton: false,
      background:        '#111827',
      color:             '#fff',
    });

    emit('saved', result);
    emit('close');
  } catch (e) {
    Swal.fire({
      icon:       'error',
      title:      'Ошибка',
      text:       e.message,
      background: '#111827',
      color:      '#fff',
    });
  }
}
</script>