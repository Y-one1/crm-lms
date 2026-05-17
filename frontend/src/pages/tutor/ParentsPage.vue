<template>
  <Layout>
    <div class="p-8">

      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-4xl font-black mb-2">👨‍👩‍👧 Родители</h1>
          <p class="text-gray-400">Управление списком родителей</p>
        </div>
        <button
          @click="openAdd"
          :disabled="isLoading"
          class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-lg transition shadow-lg disabled:opacity-50 disabled:pointer-events-none"
        >
          + Добавить родителя
        </button>
      </div>

      <Transition name="fade" mode="out-in">
        <!-- Скелетон -->
        <TableSkeleton v-if="isLoading" />

        <!-- Пустое состояние -->
        <div v-else-if="parents.length === 0" class="text-center py-16">
          <div class="text-6xl mb-4">¯\_(ツ)_/¯</div>
          <h2 class="text-2xl font-bold text-white mb-2">Родителей в базе нет!</h2>
          <p class="text-gray-400 mb-6">Добавьте первого родителя, чтобы начать</p>
        </div>

        <!-- Таблица -->
        <div v-else class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
          <table class="w-full">
            <thead>
              <tr class="bg-gray-900 border-b border-gray-700">
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ФИО</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Роль</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Телефон</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Email</th>
                <th class="px-6 py-4 text-right text-sm font-semibold text-gray-300">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="parent in parents"
                :key="parent.parent_id"
                class="border-b border-gray-700 hover:bg-gray-700/50 transition cursor-pointer"
              >
                <td class="px-6 py-4">
                  <p class="font-semibold text-white">{{ parent.last_name }} {{ parent.first_name }}</p>
                  <p v-if="parent.patronymic" class="text-xs text-gray-400">{{ parent.patronymic }}</p>
                </td>
                <td class="px-6 py-4">
                  <p class="font-semibold text-white capitalize">{{ parent.relationship }}</p>
                </td>
                <td class="px-6 py-4">
                  <p class="text-white">{{ parent.phone_number }}</p>
                </td>
                <td class="px-6 py-4">
                  <p class="text-white text-sm">{{ parent.email }}</p>
                </td>
                <td class="px-6 py-4">
                  <div class="flex flex-col items-end gap-2">
                    <button 
                      @click="goToParent(parent.parent_id)" 
                      class="w-28 py-1 text-center text-xs bg-emerald-900/50 hover:bg-emerald-900 text-emerald-300 rounded transition"
                    >
                      Информация
                    </button>
                    <button 
                      @click="openEdit(parent)" 
                      class="w-28 py-1 text-center text-xs bg-blue-900/50 hover:bg-blue-900 text-blue-300 rounded transition"
                    >
                      Редактировать
                    </button>
                    <button 
                      @click="confirmDelete(parent.parent_id)" 
                      class="w-28 py-1 text-center text-xs bg-red-900/50 hover:bg-red-900 text-red-300 rounded transition"
                    >
                      Удалить
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="parents.length === 0">
                <td colspan="5" class="px-6 py-12 text-center text-gray-400">
                  📭 Нет добавленных родителей. Нажми кнопку выше!
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Transition>

      <ParentModal
        v-if="showModal"
        :initial-data="editingParent"
        :children="children"
        @close="showModal = false"
        @saved="onSaved"
      />

      <ConfirmModal
        :show="showConfirmDelete"
        title="Удалить родителя?"
        message="Родитель будет отвязан от всех учеников и удалён из системы."
        @close="showConfirmDelete = false"
        @confirm="proceedDelete"
      />

    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Layout from '../../components/Layout.vue';
import ParentModal from '../../components/modals/ParentModal.vue';
import ConfirmModal from '../../components/modals/ConfirmModal.vue';
import { getParents, deleteParent, getChildren } from '../../api/client.js';
import TableSkeleton from '../../components/skeletons/TableSkeleton.vue';
import Swal from 'sweetalert2';

const router  = useRouter();
const parents = ref([]);
const children = ref([]);
const isLoading = ref(true);

const showModal     = ref(false);
const editingParent = ref(null);

const showConfirmDelete = ref(false);
const parentToDelete    = ref(null);

// -------------------------------------------------------
// ЗАГРУЗКА
// -------------------------------------------------------

async function loadParents() {
  try {
    isLoading.value = true;
    parents.value = await getParents();
  } catch (e) {
    Swal.fire({
      icon: 'error',
      title: 'Ошибка загрузки',
      text: 'Не удалось загрузить список родителей',
      background: '#111827',
      color: '#fff'
    });
  } finally {
    isLoading.value = false;
  }
}

async function loadChildren() {
  try {
    children.value = await getChildren();
  } catch (e) {
    console.error('Ошибка загрузки списка детей:', e);
  }
}

onMounted(() => {
  loadParents();
  loadChildren();
});

// -------------------------------------------------------
// МОДАЛКА
// -------------------------------------------------------

function openAdd() {
  editingParent.value = null;
  showModal.value     = true;
}

function openEdit(parent) {
  editingParent.value = parent;
  showModal.value     = true;
}

function onSaved(result) {
  const idx = parents.value.findIndex(p => p.parent_id === result.parent_id);
  if (idx !== -1) parents.value[idx] = result;
  else            parents.value.push(result);
}

// -------------------------------------------------------
// УДАЛЕНИЕ
// -------------------------------------------------------

function confirmDelete(id) {
  parentToDelete.value    = id;
  showConfirmDelete.value = true;
}

async function proceedDelete() {
  try {
    await deleteParent(parentToDelete.value);
    parents.value           = parents.value.filter(p => p.parent_id !== parentToDelete.value);
    showConfirmDelete.value = false;
    Swal.fire({ icon: 'success', title: 'Родитель удалён', timer: 1250, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка при удалении', text: e.message, background: '#111827', color: '#fff' });
  }
}

// -------------------------------------------------------
// НАВИГАЦИЯ
// -------------------------------------------------------

const goToParent = (id) => router.push(`/parents/${id}`);
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