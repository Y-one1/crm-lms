<template>
  <div>
    <Transition name="fade" mode="out-in">
      <TableSkeleton v-if="loading" key="skel" />

      <div v-else key="content">
        <div class="mb-6 flex justify-start">
          <button
            @click="showAddParentModal = true"
            class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-lg transition shadow-lg"
          >
            + Добавить родителя
          </button>
        </div>

        <div
          v-if="childParents.length > 0"
          class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden"
        >
          <table class="w-full">
            <thead>
              <tr class="bg-gray-900 border-b border-gray-700">
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ФИО</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Кем приходится</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Телефон</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Email</th>
                <th class="px-6 py-4 text-right text-sm font-semibold text-gray-300">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="parent in childParents"
                :key="parent.parent_id"
                class="border-b border-gray-700 hover:bg-gray-700/50 transition"
              >
                <td class="px-6 py-4">
                  <p class="font-semibold text-white">{{ parent.last_name }} {{ parent.first_name }}</p>
                  <p v-if="parent.patronymic" class="text-xs text-gray-400">{{ parent.patronymic }}</p>
                </td>
                <td class="px-6 py-4">
                  <p class="font-semibold text-white capitalize">{{ parent.relationship }}</p>
                </td>
                <td class="px-6 py-4 text-white">{{ parent.phone_number }}</td>
                <td class="px-6 py-4 text-white text-sm">{{ parent.email }}</td>
                <td class="px-6 py-4">
                  <div class="flex flex-col items-end gap-2">
                    <button
                      @click="goToParent(parent.parent_id)"
                      class="w-28 py-1 text-center text-xs bg-emerald-900/50 hover:bg-emerald-900 text-emerald-300 rounded transition"
                    >
                      Информация
                    </button>
                    <button
                      @click="confirmRemoveParent(parent.parent_id)"
                      class="w-28 py-1 text-center text-xs bg-red-900/50 hover:bg-red-900 text-red-300 rounded transition"
                    >
                      Отвязать
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-16">
          <div class="text-6xl mb-4">👨‍👩‍👧</div>
          <h2 class="text-2xl font-bold text-white mb-2">Привязанных родителей нет</h2>
          <p class="text-gray-400 mb-6">Добавьте связь между родителем и учеником</p>
        </div>
      </div>
    </Transition>
  </div>

  <AddParentToChildModal
    v-if="showAddParentModal"
    :child-id="childId"
    @close="showAddParentModal = false"
    @saved="onParentAdded"
  />

  <ConfirmModal
    :show="showConfirmRemove"
    title="Отвязать родителя?"
    message="Связь между родителем и ребенком будет удалена."
    @close="showConfirmRemove = false"
    @confirm="proceedRemoveParent"
  />
</template>

<script setup>
// name нужен для корректной работы KeepAlive
defineOptions({ name: 'ChildParentsTab' });

import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import TableSkeleton from '../skeletons/TableSkeleton.vue';
import AddParentToChildModal from '../modals/AddParentToChildModal.vue';
import ConfirmModal from '../modals/ConfirmModal.vue';
import { getChildParents, deleteParentChildLink } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  childId: { type: Number, required: true },
});

const emit = defineEmits(['parents-loaded']);

const router = useRouter();

// --- СОСТОЯНИЕ ---
const childParents = ref([]);
const loading = ref(true);
const showAddParentModal = ref(false);
const showConfirmRemove = ref(false);
const parentToRemove = ref(null);

// --- ЗАГРУЗКА ---
async function loadParents() {
  try {
    loading.value = true;
    childParents.value = await getChildParents(props.childId);
    emit('parents-loaded', childParents.value);
  } catch (e) {
    console.error('Ошибка загрузки родителей:', e);
  } finally {
    loading.value = false;
  }
}

onMounted(loadParents);

// --- ДЕЙСТВИЯ ---
function confirmRemoveParent(parentId) {
  parentToRemove.value = parentId;
  showConfirmRemove.value = true;
}

async function proceedRemoveParent() {
  try {
    await deleteParentChildLink(parentToRemove.value, props.childId);
    showConfirmRemove.value = false;
    Swal.fire({ icon: 'success', title: 'Связь удалена', timer: 1250, showConfirmButton: false, background: '#111827', color: '#fff' });
    await loadParents();
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка при удалении', text: e.message, background: '#111827', color: '#fff' });
  }
}

async function onParentAdded() {
  showAddParentModal.value = false;
  await loadParents();
}

const goToParent = (parentId) => router.push(`/parents/${parentId}`);
</script>