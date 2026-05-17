<template>
  <div>
    <Transition name="fade" mode="out-in">
      <Table2Skeleton v-if="loading" key="skel" />

      <div v-else key="content">
        <div class="mb-6 flex justify-start">
          <button
            @click="showAddChildModal = true"
            class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-lg transition shadow-lg"
          >
            + Добавить ученика
          </button>
        </div>

        <div
          v-if="parentChildren.length > 0"
          class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden"
        >
          <table class="w-full">
            <thead>
              <tr class="bg-gray-900 border-b border-gray-700">
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">ФИО</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Класс</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Главный контакт</th>
                <th class="px-6 py-4 text-right text-sm font-semibold text-gray-300">Действия</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="child in parentChildren"
                :key="child.child_id"
                class="border-b border-gray-700 hover:bg-gray-700/50 transition cursor-pointer"
                @click="goToChild(child.child_id)"
              >
                <td class="px-6 py-4">
                  <p class="font-semibold text-white">
                    {{ child.last_name }} {{ child.first_name }}
                  </p>
                  <p v-if="child.patronymic" class="text-xs text-gray-400">
                    {{ child.patronymic }}
                  </p>
                </td>
                <td class="px-6 py-4 text-gray-300">{{ child.school_class }} класс</td>
                <td class="px-6 py-4">
                  <span
                    v-if="child.is_main"
                    class="px-2 py-1 text-xs rounded-full bg-blue-900/50 text-blue-300 font-semibold"
                  >
                    ✓ Да
                  </span>
                  <span v-else class="px-2 py-1 text-xs rounded-full bg-gray-700 text-gray-400">
                    —
                  </span>
                </td>
                <td class="px-6 py-4">
                  <div class="flex flex-col items-end gap-2">
                    <button
                      @click.stop="editChildRelation(child)"
                      class="w-28 py-1 text-center text-xs bg-blue-900/50 hover:bg-blue-900 text-blue-300 rounded transition"
                    >
                      Изменить
                    </button>
                    <button
                      @click.stop="confirmRemoveChild(child.child_id)"
                      class="w-28 py-1 text-center text-xs bg-red-900/50 hover:bg-red-900 text-red-300 rounded transition"
                    >
                      Удалить связь
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-16">
          <div class="text-6xl mb-4">👤</div>
          <h2 class="text-2xl font-bold text-white mb-2">Привязанных учеников нет</h2>
          <p class="text-gray-400 mb-6">Добавьте связь между родителем и учеником</p>
        </div>
      </div>
    </Transition>

    <AddChildModal
      v-if="showAddChildModal"
      :parent-id="parentId"
      :available-children="availableChildren"
      @close="showAddChildModal = false"
      @saved="onDataChanged"
    />

    <EditChildRelationModal
      v-if="showEditRelationModal"
      :child="selectedChildForEdit"
      :parent-id="parentId"
      :initial-is-main="selectedChildIsMain"
      @close="showEditRelationModal = false"
      @saved="onDataChanged"
    />

    <ConfirmModal
      :show="showConfirmRemove"
      title="Удалить связь?"
      message="Ребенок будет отвязан от этого родителя."
      @close="showConfirmRemove = false"
      @confirm="proceedRemoveChild"
    />
  </div>
</template>

<script setup>
defineOptions({ name: 'ParentChildrenTab' });

import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import Table2Skeleton from '../skeletons/Table2Skeleton.vue';
import AddChildModal from '../modals/AddChildModal.vue';
import EditChildRelationModal from '../modals/EditChildRelationModal.vue';
import ConfirmModal from '../modals/ConfirmModal.vue';
import { deleteParentChildLink } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  parentId: { type: Number, required: true },
  parentChildren: { type: Array, required: true },
  allChildren: { type: Array, required: true },
  loading: { type: Boolean, default: false }
});

const emit = defineEmits(['refresh-children']);
const router = useRouter();

// --- СОСТОЯНИЕ ---
const showAddChildModal = ref(false);
const showEditRelationModal = ref(false);
const showConfirmRemove = ref(false);

const selectedChildForEdit = ref(null);
const selectedChildIsMain = ref(false);
const childToRemove = ref(null);

// --- ВЫЧИСЛЯЕМЫЕ ---
const availableChildren = computed(() => {
  const linkedIds = new Set(props.parentChildren.map(c => c.child_id));
  return props.allChildren.filter(child => !linkedIds.has(child.child_id));
});

// --- ДЕЙСТВИЯ ---
function editChildRelation(child) {
  selectedChildForEdit.value = child;
  selectedChildIsMain.value = child.is_main || false;
  showEditRelationModal.value = true;
}

function confirmRemoveChild(childId) {
  childToRemove.value = childId;
  showConfirmRemove.value = true;
}

async function proceedRemoveChild() {
  try {
    await deleteParentChildLink(props.parentId, childToRemove.value);
    showConfirmRemove.value = false;
    emit('refresh-children');
    Swal.fire({
      icon: 'success',
      title: 'Связь удалена',
      timer: 1250,
      showConfirmButton: false,
      background: '#111827',
      color: '#fff',
    });
  } catch (e) {
    Swal.fire({
      icon: 'error',
      title: 'Ошибка при удалении',
      text: e.message,
      background: '#111827',
      color: '#fff',
    });
  }
}

function onDataChanged() {
  showAddChildModal.value = false;
  showEditRelationModal.value = false;
  emit('refresh-children');
}

const goToChild = (childId) => router.push(`/children/${childId}`);
</script>