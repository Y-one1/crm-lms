<template>
  <div v-if="show" class="fixed inset-0 z-[100] flex items-center justify-center p-4">
    <div class="absolute inset-0 bg-black/80 backdrop-blur-sm" @click="$emit('close')"></div>

    <div class="relative bg-gray-900 border border-gray-700 rounded-2xl w-full max-w-md overflow-hidden shadow-2xl">
      <div class="p-6">
        <div class="flex justify-between items-center mb-6">
          <div class="flex items-center gap-3">
            <div :class="statusIndicatorClass" class="w-3 h-3 rounded-full shadow-[0_0_10px_currentColor]"></div>
            <h2 class="text-2xl font-black text-white">
              {{ lessonData.lesson_id ? 'Занятие' : 'Новый урок' }}
            </h2>
          </div>
          <button @click="$emit('close')" class="text-gray-500 hover:text-white transition text-xl">✕</button>
        </div>

        <form @submit.prevent="save" class="space-y-5">

          <!-- Выбор ученика (только когда модалка открыта из расписания, не из карточки ребёнка) -->
          <div v-if="!isFixedChild">
            <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Ученик</label>
            <select
              v-model="lessonData.child_id"
              required
              class="w-full bg-gray-800 border border-gray-700 rounded-xl p-3 text-white focus:border-blue-500 outline-none transition cursor-pointer"
            >
              <option :value="null" disabled>Выберите ученика</option>
              <option v-for="child in children" :key="child.child_id" :value="child.child_id">
                {{ child.last_name }} {{ child.first_name }}
              </option>
            </select>
          </div>

          <!-- Дата и время -->
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Дата</label>
              <input
                type="date"
                v-model="lessonData.date"
                required
                class="w-full bg-gray-800 border border-gray-700 rounded-xl p-3 text-white focus:border-blue-500 outline-none"
              >
            </div>
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Время</label>
              <input
                type="time"
                v-model="lessonData.time"
                required
                class="w-full bg-gray-800 border border-gray-700 rounded-xl p-3 text-white focus:border-blue-500 outline-none"
              >
            </div>
          </div>

          <!-- Тема -->
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Тема занятия</label>
            <input
              v-model="lessonData.theme"
              type="text"
              required
              class="w-full bg-gray-800 border border-gray-700 rounded-xl p-3 text-white focus:border-blue-500 outline-none"
            >
          </div>

          <!-- Переключатель статуса -->
          <div>
            <label class="block text-xs font-bold text-gray-500 uppercase mb-2">Статус</label>
            <div class="flex bg-gray-800 p-1 rounded-xl border border-gray-700 gap-1">
              <button
                type="button"
                @click="lessonData.status = 'planned'"
                :class="lessonData.status === 'planned' ? 'bg-yellow-500/20 text-yellow-500 border border-yellow-500/50' : 'text-gray-500'"
                class="flex-1 py-2 rounded-lg text-[14px] font-black uppercase transition"
              >
                План
              </button>
              <button
                type="button"
                @click="lessonData.status = 'completed'"
                :class="lessonData.status === 'completed' ? 'bg-green-500/20 text-green-500 border border-green-500/50' : 'text-gray-500'"
                class="flex-1 py-2 rounded-lg text-[14px] font-black uppercase transition"
              >
                Завершено
              </button>
              <button
                type="button"
                @click="lessonData.status = 'cancelled'"
                :class="lessonData.status === 'cancelled' ? 'bg-red-500/20 text-red-500 border border-red-500/50' : 'text-gray-500'"
                class="flex-1 py-2 rounded-lg text-[14px] font-black uppercase transition"
              >
                Отменено
              </button>
            </div>
          </div>

          <!-- Блок отчёта — появляется только для завершённых занятий -->
          <div
            v-if="lessonData.status === 'completed'"
            class="space-y-4 p-4 bg-blue-500/5 rounded-2xl border border-dashed border-blue-500/30"
          >
            <!-- Оценка -->
            <div>
              <label class="block text-xs font-bold text-gray-500 uppercase mb-3 text-center">
                Оценка
              </label>
              <div class="flex justify-between gap-2">
                <label v-for="g in [2, 3, 4, 5]" :key="g" class="flex-1 cursor-pointer">
                  <input type="radio" :value="g" v-model="lessonData.grade" class="hidden peer">
                  <div
                    @click.prevent="lessonData.grade = lessonData.grade === g ? null : g"
                    class="py-2 text-center rounded-lg border border-gray-700 peer-checked:border-blue-500 peer-checked:bg-blue-600 peer-checked:text-white text-gray-500 font-bold transition"
                  >
                    {{ g }}
                  </div>
                </label>
              </div>
            </div>

            <!-- ДЗ -->
            <div class="flex items-center justify-between">
              <span class="text-xs font-bold text-gray-500 uppercase">Домашнее задание:</span>
              <div class="flex gap-2">
                <button
                  type="button"
                  @click="lessonData.homework_done = true"
                  :class="lessonData.homework_done ? 'bg-green-600 text-white shadow-[0_0_10px_rgba(22,163,74,0.4)]' : 'bg-gray-800 text-gray-500'"
                  class="px-6 py-1.5 rounded-lg text-[14px] font-black uppercase transition"
                >
                  Да
                </button>
                <button
                  type="button"
                  @click="lessonData.homework_done = false"
                  :class="!lessonData.homework_done ? 'bg-red-600 text-white shadow-[0_0_10px_rgba(220,38,38,0.4)]' : 'bg-gray-800 text-gray-500'"
                  class="px-6 py-1.5 rounded-lg text-[14px] font-black uppercase transition"
                >
                  Нет
                </button>
              </div>
            </div>
          </div>

          <!-- Заметки -->
          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-black text-blue-400 uppercase mb-2">📝 Себе</label>
              <textarea
                v-model="lessonData.notes_for_yourself"
                rows="2"
                class="w-full bg-gray-800 border border-gray-700 rounded-xl p-2 text-xs text-white resize-none focus:border-blue-500 outline-none"
              ></textarea>
            </div>
            <div>
              <label class="block text-xs font-black text-purple-400 uppercase mb-2">💬 Родителям</label>
              <textarea
                v-model="lessonData.notes_for_parents"
                rows="2"
                class="w-full bg-gray-800 border border-gray-700 rounded-xl p-2 text-xs text-white resize-none focus:border-purple-500 outline-none"
              ></textarea>
            </div>
          </div>

          <!-- Кнопки действий -->
          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              :disabled="!hasActiveTariff"
              :class="!hasActiveTariff ? 'opacity-40 cursor-not-allowed bg-blue-600' : 'bg-blue-600 hover:bg-blue-500'"
              class="flex-1 text-white font-black py-4 rounded-xl transition shadow-lg shadow-blue-900/40 uppercase tracking-widest text-sm"
            >
              {{ hasActiveTariff ? 'Сохранить' : 'Нет активного тарифа' }}
            </button>
            <button
              v-if="lessonData.lesson_id"
              type="button"
              @click="requestDelete"
              class="px-6 bg-gray-800 hover:bg-red-900/30 text-red-500 rounded-xl transition border border-gray-700"
            >
              🗑
            </button>
          </div>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
// --- ИМПОРТЫ ---
import { ref, watch, computed } from 'vue';
import { createLesson, updateLesson, deleteLesson, getStudentStatus } from '../../api/client.js';
import Swal from 'sweetalert2';

// --- ПРОПСЫ И ЭМИТЫ ---

const props = defineProps({
  show:         Boolean,
  initialData:  Object,   // Данные урока (для редактирования) или предзаполненные поля (date, time, child_id)
  isFixedChild: Boolean,  // true — модалка открыта из карточки ребёнка (child_id уже известен)
  children:     Array,    // Список всех детей для выпадающего списка
});

const emit = defineEmits(['close', 'saved', 'deleted']);

// --- СОСТОЯНИЕ ---

const lessonData = ref(buildFormData());
const hasActiveTariff = ref(true);

// --- ВЫЧИСЛЯЕМЫЕ ---

// Цвет индикатора статуса в шапке модалки
const statusIndicatorClass = computed(() => {
  switch (lessonData.value.status) {
    case 'completed': return 'bg-green-400 text-green-400';
    case 'cancelled': return 'bg-red-500 text-red-500';
    default:          return 'bg-yellow-400 text-yellow-400';
  }
});

// --- ЗАГРУЗКА / СБРОС ФОРМЫ ---

// Возвращает объект с дефолтными значениями, смёрженными с входящими данными
function buildFormData(overrides = {}) {
  return {
    status:             'planned',
    homework_done:      false,
    grade:              null, // null — оценка не выставлена (бэкенд принимает)
    notes_for_yourself: '',
    notes_for_parents:  '',
    ...overrides,
  };
}

// Следим за изменением initialData.
// immediate: true — чтобы подхватить данные при первом открытии модалки.
watch(
  () => props.initialData,
  (newVal) => {
    lessonData.value = buildFormData(newVal ?? {});
  },
  { deep: true, immediate: true }
);

watch(
  () => lessonData.value.child_id,
  async (newId) => {
    if (!newId) return;
    try {
      const status = await getStudentStatus(newId);
      hasActiveTariff.value = status !== null;
    } catch {
      hasActiveTariff.value = false;
    }
  }
);

// --- ДЕЙСТВИЯ ---

async function save() {
  // Валидация
  if (!lessonData.value.theme?.trim()) {
    return showWarning('Укажите тему занятия');
  }
  if (!props.isFixedChild && !lessonData.value.child_id) {
    return showWarning('Выберите ученика');
  }
  const hour = parseInt(lessonData.value.time?.split(':')[0]);
  if (isNaN(hour) || hour < 8 || hour >= 22) {
    return showWarning('Время занятия должно быть в диапазоне 08:00 – 22:00');
  }
  if (lessonData.value.status === 'completed' && lessonData.value.grade == null) {
    return showWarning('Выставьте оценку за занятие');
  }

  try {
    // Убираем служебные поля date/time, которых нет в схеме бэкенда,
    // и формируем lesson_datetime в формате ISO, который ждёт FastAPI
    const { date, time, lesson_id, ...rest } = lessonData.value;
    const payload = { ...rest, lesson_datetime: `${date}T${time}:00` };

    const isEdit = Boolean(lessonData.value.lesson_id);

    if (isEdit) {
      await updateLesson(lessonData.value.lesson_id, payload);
    } else {
      await createLesson(payload);
    }

    Swal.fire({
      icon:              'success',
      title:             isEdit ? 'Занятие обновлено' : 'Занятие добавлено в расписание',
      timer:             1250,
      showConfirmButton: false,
      background:        '#111827',
      color:             '#fff',
    });

    emit('saved');
    emit('close');
  } catch (e) {
    Swal.fire({
      icon:       'error',
      title:      'Ошибка API',
      text:       e.message,
      background: '#111827',
      color:      '#fff',
    });
  }
}

async function requestDelete() {
  const result = await Swal.fire({
    icon:               'warning',
    title:              'Удалить урок?',
    text:               'Это действие нельзя отменить',
    showCancelButton:   true,
    confirmButtonText:  'Да, удалить',
    cancelButtonText:   'Отмена',
    confirmButtonColor: '#dc2626',
    background:         '#111827',
    color:              '#fff',
  });

  if (result.isConfirmed) {
    try {
      await deleteLesson(lessonData.value.lesson_id);
      emit('deleted');
      emit('close');
    } catch (e) {
      Swal.fire({
        icon:       'error',
        title:      'Ошибка при удалении',
        text:       e.message,
        background: '#111827',
        color:      '#fff',
      });
    }
  }
}

// --- УТИЛИТЫ ---

function showWarning(text) {
  return Swal.fire({
    icon:               'warning',
    title:              'Внимание',
    text,
    background:         '#111827',
    color:              '#fff',
    confirmButtonColor: '#3b82f6',
  });
}
</script>

<style scoped>
input[type="date"]::-webkit-calendar-picker-indicator,
input[type="time"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
</style>