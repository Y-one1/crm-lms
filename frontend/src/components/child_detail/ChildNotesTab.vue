<template>
  <div class="space-y-3">

    <!-- Основная заметка об ученике -->
    <div class="bg-gray-800 rounded-xl border border-gray-700 p-6">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-sm font-bold text-gray-400 uppercase tracking-wider">📌 Основная заметка об ученике</h3>
        <button
          v-if="!editingChildNote"
          @click="editingChildNote = true; childNoteText = child?.notes || ''"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm font-semibold transition"
        >
          ✏️ Редактировать
        </button>
      </div>
      <div v-if="!editingChildNote">
        <p v-if="child?.notes" class="text-white semibold whitespace-pre-wrap">{{ child.notes }}</p>
        <p v-else class="text-gray-600 italic">Заметка не заполнена</p>
      </div>
      <div v-else class="space-y-3">
        <textarea
          v-model="childNoteText"
          rows="4"
          class="w-full px-3 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white focus:border-blue-500 focus:outline-none resize-none"
          placeholder="Особенности ученика, предпочтения..."
        ></textarea>
        <div class="flex gap-2">
          <button @click="saveChildNote" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm font-semibold transition">
            Сохранить
          </button>
          <button @click="editingChildNote = false" class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white text-sm transition">
            Отмена
          </button>
        </div>
      </div>
    </div>

    <!-- Панель фильтров -->
    <div class="bg-gray-800 rounded-xl border border-gray-700 p-4 flex flex-wrap gap-4 items-end">
      <div class="flex-1 min-w-48">
        <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Поиск по теме / тексту</label>
        <input
          v-model="notesSearchQuery"
          type="text"
          placeholder="Введите запрос..."
          class="w-full px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
        />
      </div>
      <div>
        <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">С</label>
        <input
          v-model="notesDates.start"
          type="date"
          class="px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
        />
      </div>
      <div>
        <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">По</label>
        <input
          v-model="notesDates.end"
          type="date"
          class="px-3 py-2 bg-gray-900 border border-gray-700 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
        />
      </div>
      <button
        @click="loadNotes(showFullNotes)"
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm font-semibold transition"
      >
        🔍 Применить
      </button>
      <button
        @click="showFullNotes = !showFullNotes; loadNotes(showFullNotes)"
        class="px-4 py-2 rounded-lg text-sm font-semibold transition border"
        :class="showFullNotes ? 'bg-blue-600 border-blue-400 text-white' : 'bg-gray-700 border-gray-600 text-gray-300 hover:text-white'"
      >
        {{ showFullNotes ? '📖 Полный лог' : '📅 За 2 недели' }}
      </button>
    </div>

    <Transition name="fade" mode="out-in">
      <NotesSkeleton v-if="loading" key="skel" />

      <div v-else key="content">
        <div v-if="filteredNotes.length > 0" class="space-y-3">
          <div
            v-for="lesson in filteredNotes"
            :key="lesson.lesson_id"
            class="bg-gray-800 rounded-xl border border-gray-700 p-5"
          >
            <div class="flex justify-between items-start mb-3">
              <div>
                <span class="text-sm font-bold text-white">{{ lesson.theme }}</span>
                <span class="ml-3 text-xs text-gray-500">{{ formatDateShort(lesson.lesson_datetime) }}</span>
              </div>
              <span
                class="px-2 py-0.5 rounded text-xs font-semibold"
                :class="lesson.status === 'completed' ? 'bg-green-900/50 text-green-400' : 'bg-yellow-900/50 text-yellow-400'"
              >
                {{ lesson.status === 'completed' ? 'Завершено' : 'Запланировано' }}
              </span>
            </div>

            <div v-if="lesson.notes_for_yourself" class="mb-3">
              <div class="flex justify-between items-center mb-1">
                <p class="text-xs font-bold text-blue-400 uppercase">📝 Себе</p>
                <button @click="clearNote(lesson.lesson_id, 'notes_for_yourself')" class="text-xs text-red-500 hover:text-red-400 transition">
                  очистить
                </button>
              </div>
              <p class="text-sm text-gray-200 whitespace-pre-wrap bg-gray-900/50 rounded-lg p-3">{{ lesson.notes_for_yourself }}</p>
            </div>

            <div v-if="lesson.notes_for_parents">
              <div class="flex justify-between items-center mb-1">
                <p class="text-xs font-bold text-purple-400 uppercase">💬 Родителям</p>
                <button @click="clearNote(lesson.lesson_id, 'notes_for_parents')" class="text-xs text-red-500 hover:text-red-400 transition">
                  очистить
                </button>
              </div>
              <p class="text-sm text-gray-200 whitespace-pre-wrap bg-gray-900/50 rounded-lg p-3">{{ lesson.notes_for_parents }}</p>
            </div>
          </div>
        </div>

        <div v-else class="text-center py-12 text-gray-600">
          <div class="text-4xl mb-3">📭</div>
          <p>Заметок за выбранный период нет</p>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
// name нужен для корректной работы KeepAlive
defineOptions({ name: 'ChildNotesTab' });

import { ref, computed, onMounted } from 'vue';
import NotesSkeleton from '../skeletons/NotesSkeleton.vue';
import { getChildNotes, clearLessonNote, updateChild } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  childId: { type: Number, required: true },
  child:   { type: Object, default: null },
});

const emit = defineEmits(['child-updated']);

// --- СОСТОЯНИЕ ---
const childNotes       = ref([]);
const loading          = ref(true);
const showFullNotes    = ref(false);
const notesSearchQuery = ref('');
const notesDates       = ref({ start: '', end: '' });
const editingChildNote = ref(false);
const childNoteText    = ref('');

// --- ВЫЧИСЛЯЕМЫЕ ---
const filteredNotes = computed(() => {
  const q = notesSearchQuery.value.toLowerCase().trim();
  if (!q) return childNotes.value;
  return childNotes.value.filter((l) =>
    l.theme?.toLowerCase().includes(q) ||
    l.notes_for_yourself?.toLowerCase().includes(q) ||
    l.notes_for_parents?.toLowerCase().includes(q)
  );
});

// --- ЗАГРУЗКА ---
async function loadNotes(fullLog = false) {
  try {
    loading.value = true;
    const today = new Date();
    const twoWeeksAgo = new Date(today);
    twoWeeksAgo.setDate(today.getDate() - 14);
    const start = fullLog ? '2020-01-01' : (notesDates.value.start || twoWeeksAgo.toISOString().split('T')[0]);
    const end = fullLog ? '2029-12-31' : (notesDates.value.end || new Date(today.getTime() + 14 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]);
    childNotes.value = await getChildNotes(props.childId, start, end);
  } catch (e) {
    console.error('Ошибка загрузки заметок:', e);
  } finally {
    loading.value = false;
  }
}

onMounted(() => loadNotes(false));

// --- ДЕЙСТВИЯ ---
async function clearNote(lessonId, field) {
  const result = await Swal.fire({
    icon: 'warning', title: 'Очистить заметку?',
    showCancelButton: true, confirmButtonText: 'Да', cancelButtonText: 'Отмена',
    confirmButtonColor: '#dc2626', background: '#111827', color: '#fff',
  });
  if (result.isConfirmed) {
    try {
      await clearLessonNote(lessonId, field);
      await loadNotes(showFullNotes.value);
      Swal.fire({ icon: 'success', title: 'Заметка очищена', timer: 1200, showConfirmButton: false, background: '#111827', color: '#fff' });
    } catch (e) {
      Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
    }
  }
}

async function saveChildNote() {
  try {
    const updated = await updateChild(props.childId, { ...props.child, notes: childNoteText.value });
    editingChildNote.value = false;
    emit('child-updated', updated);
    Swal.fire({ icon: 'success', title: 'Заметка сохранена', timer: 1200, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

// --- УТИЛИТЫ ---
const formatDateShort = (d) => new Date(d).toLocaleDateString('ru-RU');
</script>