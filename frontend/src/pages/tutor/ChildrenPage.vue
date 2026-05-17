<template>
  <Layout>
    <div class="p-8">

      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-4xl font-black mb-2">👥 Ученики</h1>
          <p class="text-gray-400">Управление списком учеников</p>
        </div>
        <button
          @click="openAdd"
          :disabled="isLoading"
          class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-lg transition shadow-lg disabled:opacity-50 disabled:pointer-events-none"
        >
          + Добавить ученика
        </button>
      </div>

      <Transition name="fade" mode="out-in">
        <TableSkeleton v-if="isLoading" key="skeleton" />

        <div v-else-if="children.length === 0" key="empty" class="text-center py-16">
          <div class="text-6xl mb-4">¯\_(ツ)_/¯</div>
          <h2 class="text-2xl font-bold text-white mb-2">Учеников в базе нет!</h2>
          <p class="text-gray-400 mb-6">Добавьте первого ученика, чтобы начать</p>
        </div>

        <div v-else key="table" class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-900 border-b border-gray-700">
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ФИО</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Класс</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Телефон</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Добавлен</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Последний урок</th>
                <th class="px-6 py-4 text-right text-sm font-semibold text-gray-300">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="child in children"
                :key="child.child_id"
                class="border-b border-gray-700 hover:bg-gray-700/50 transition cursor-pointer"
              >
                <td class="px-6 py-4">
                  <p class="font-semibold text-white">{{ child.last_name }} {{ child.first_name }}</p>
                  <p v-if="child.patronymic" class="text-xs text-gray-400">{{ child.patronymic }}</p>
                </td>
                <td class="px-6 py-4 text-white">{{ child.school_class }}</td>
                <td class="px-6 py-4 text-white">{{ child.phone_number }}</td>
                <td class="px-6 py-4 text-sm text-gray-400">{{ formatDate(child.day_of_addition) }}</td>
                <td class="px-6 py-4 text-sm">
                  <span v-if="child.day_of_last_lesson" class="text-blue-300">{{ formatDate(child.day_of_last_lesson) }}</span>
                  <span v-else class="text-gray-500">—</span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex flex-col items-end gap-2">
                    <button
                      @click="goToChild(child.child_id)"
                      class="w-28 py-1 text-center text-xs bg-emerald-900/50 hover:bg-emerald-900 text-emerald-300 rounded transition"
                    >
                      Информация
                    </button>
                    <button
                      @click="openEdit(child)"
                      class="w-28 py-1 text-center text-xs bg-blue-900/50 hover:bg-blue-900 text-blue-300 rounded transition"
                    >
                      Редактировать
                    </button>
                    <button
                      @click="confirmDelete(child.child_id)"
                      class="w-28 py-1 text-center text-xs bg-red-900/50 hover:bg-red-900 text-red-300 rounded transition"
                    >
                      Удалить
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Transition>

      <ChildModal
        v-if="showModal"
        :initial-data="editingChild"
        @close="showModal = false"
        @saved="onSaved"
      />

      <ConfirmModal
        :show="showConfirmDelete"
        title="Удалить ученика?"
        message="Все занятия и платежи этого ученика будут стерты навсегда."
        @close="showConfirmDelete = false"
        @confirm="proceedDelete"
      />

    </div>
  </Layout>
</template>

<script setup>
// --- ИМПОРТЫ ---
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Layout from '../../components/Layout.vue';
import TableSkeleton from '../../components/skeletons/TableSkeleton.vue';
import ChildModal from '../../components/modals/ChildModal.vue';
import ConfirmModal from '../../components/modals/ConfirmModal.vue';
import { getChildren, deleteChild } from '../../api/client.js';
import Swal from 'sweetalert2';

// --- СОСТОЯНИЕ ---
const router   = useRouter();
const children = ref([]);
const isLoading = ref(true);

const showModal    = ref(false);
const editingChild = ref(null);

const showConfirmDelete = ref(false);
const childToDelete    = ref(null);

// --- ЗАГРУЗКА ---

async function loadChildren() {
  try {
    isLoading.value = true;
    children.value = await getChildren();
  } catch (e) {
    Swal.fire({
      icon:       'error',
      title:      'Ошибка загрузки',
      text:       'Не удалось загрузить список учеников',
      background: '#111827',
      color:      '#fff',
    });
  } finally {
    isLoading.value = false;
  }
}

// --- UI-ЛОГИКА ---

function openAdd() {
  editingChild.value = null;
  showModal.value    = true;
}

function openEdit(child) {
  editingChild.value = child;
  showModal.value    = true;
}

// ChildModal эмитит сохранённый объект — обновляем список без перезагрузки с сервера
function onSaved(result) {
  const idx = children.value.findIndex(c => c.child_id === result.child_id);
  if (idx !== -1) children.value[idx] = result; // редактирование — заменяем запись
  else            children.value.push(result);   // создание — добавляем в конец
}

// --- УДАЛЕНИЕ ---

function confirmDelete(id) {
  childToDelete.value     = id;
  showConfirmDelete.value = true;
}

async function proceedDelete() {
  try {
    await deleteChild(childToDelete.value);
    children.value          = children.value.filter(c => c.child_id !== childToDelete.value);
    showConfirmDelete.value = false;
    Swal.fire({
      icon:              'success',
      title:             'Ученик удалён',
      timer:             1250,
      showConfirmButton: false,
      background:        '#111827',
      color:             '#fff',
    });
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

// --- УТИЛИТЫ ---

function goToChild(id) {
  router.push(`/children/${id}`);
}

function formatDate(d) {
  return d
    ? new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' })
    : '—';
}

// --- ИНИЦИАЛИЗАЦИЯ ---

onMounted(loadChildren);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>