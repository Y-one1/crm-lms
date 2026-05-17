<template>
  <div class="space-y-6">
    <div class="bg-gray-800 rounded-xl border border-gray-700 p-6">
      <div class="flex justify-between items-center mb-3">
        <h3 class="text-sm font-bold text-gray-400 uppercase tracking-wider">
          📌 Основная заметка о родителе
        </h3>
        <button
          v-if="!editingParentNote"
          @click="startEditing"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm font-semibold transition"
        >
          ✏️ Редактировать
        </button>
      </div>
      <div v-if="!editingParentNote">
        <p v-if="parent?.notes" class="text-gray-200 whitespace-pre-wrap">
          {{ parent.notes }}
        </p>
        <p v-else class="text-gray-600 italic">Заметка не заполнена</p>
      </div>
      <div v-else class="space-y-3">
        <textarea
          v-model="parentNoteText"
          rows="4"
          class="w-full px-3 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white focus:border-blue-500 focus:outline-none resize-none"
          placeholder="Предпочтительный способ связи, особенности..."
        ></textarea>
        <div class="flex gap-2">
          <button
            @click="saveParentNote"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm font-semibold transition"
          >
            Сохранить
          </button>
          <button
            @click="editingParentNote = false"
            class="px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white text-sm transition"
          >
            Отмена
          </button>
        </div>
      </div>
    </div>

    <div class="bg-gray-800 rounded-xl border border-gray-700 p-4 flex flex-wrap gap-4 items-end">
      <div class="flex-1 min-w-48">
        <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">
          Поиск по теме / тексту
        </label>
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
        @click="toggleFullLog"
        class="px-4 py-2 rounded-lg text-sm font-semibold transition border"
        :class="
          showFullNotes
            ? 'bg-blue-600 border-blue-400 text-white'
            : 'bg-gray-700 border-gray-600 text-gray-300 hover:text-white'
        "
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
                <span class="ml-3 text-xs text-gray-500">
                  {{ formatDate(lesson.lesson_datetime) }}
                </span>
                <span class="ml-3 text-xs text-gray-600">
                  {{ getChildName(lesson.child_id) }}
                </span>
              </div>
            </div>
            <div v-if="lesson.notes_for_parents">
              <p class="text-xs font-bold text-purple-400 uppercase mb-1">
                💬 Для родителей
              </p>
              <p class="text-sm text-gray-200 whitespace-pre-wrap bg-gray-900/50 rounded-lg p-3">
                {{ lesson.notes_for_parents }}
              </p>
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
defineOptions({ name: 'ParentNotesTab' });

import { ref, computed, onMounted } from 'vue';
import NotesSkeleton from '../skeletons/NotesSkeleton.vue';
import { getParentNotes, updateParent } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  parentId: { type: Number, required: true },
  parent: { type: Object, required: true },
  parentChildren: { type: Array, required: true }
});

const emit = defineEmits(['parent-updated']);

// --- СОСТОЯНИЕ ---
const parentNotes = ref([]);
const loading = ref(true);
const showFullNotes = ref(false);
const notesSearchQuery = ref('');
const notesDates = ref({ start: '', end: '' });
const editingParentNote = ref(false);
const parentNoteText = ref('');

// --- ВЫЧИСЛЯЕМЫЕ ---
const filteredNotes = computed(() => {
  const q = notesSearchQuery.value.toLowerCase().trim();
  if (!q) return parentNotes.value;
  return parentNotes.value.filter(l =>
    l.theme?.toLowerCase().includes(q) ||
    l.notes_for_parents?.toLowerCase().includes(q)
  );
});

// --- ЗАГРУЗКА ДАННЫХ ---
async function loadNotes(fullLog = false) {
  try {
    loading.value = true;
    const today = new Date();
    const twoWeeksAgo = new Date(today);
    twoWeeksAgo.setDate(today.getDate() - 14);
    
    const start = fullLog ? '2020-01-01' : (notesDates.value.start || twoWeeksAgo.toISOString().split('T')[0]);
    const twoWeeksAhead = new Date(today);
    twoWeeksAhead.setDate(today.getDate() + 14);
    const end = fullLog ? '2029-12-31' : (notesDates.value.end || twoWeeksAhead.toISOString().split('T')[0]);
    
    parentNotes.value = await getParentNotes(props.parentId, start, end);
  } catch (e) {
    console.error('Ошибка загрузки заметок:', e);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadNotes(showFullNotes.value);
});

// --- ДЕЙСТВИЯ ---
function toggleFullLog() {
  showFullNotes.value = !showFullNotes.value;
  loadNotes(showFullNotes.value);
}

function startEditing() {
  parentNoteText.value = props.parent?.notes || '';
  editingParentNote.value = true;
}

async function saveParentNote() {
  try {
    const updated = await updateParent(props.parentId, { ...props.parent, notes: parentNoteText.value });
    emit('parent-updated', updated);
    editingParentNote.value = false;
    Swal.fire({
      icon: 'success',
      title: 'Заметка сохранена',
      timer: 1200,
      showConfirmButton: false,
      background: '#111827',
      color: '#fff',
    });
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

// --- УТИЛИТЫ ---
const formatDate = (d) => new Date(d).toLocaleDateString('ru-RU');

function getChildName(childId) {
  const c = props.parentChildren.find(c => c.child_id === childId);
  return c ? `${c.last_name} ${c.first_name}` : '—';
}
</script>

<style scoped>
input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
</style>