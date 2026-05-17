<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl">

        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-white">Добавить ученика</h2>
          <button @click="$emit('close')" class="text-gray-500 hover:text-white transition text-xl">✕</button>
        </div>

        <form @submit.prevent="submit" class="space-y-4">

          <!-- Выбор ребенка -->
          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Ученик *</label>
            <div class="relative">
              <input
                v-model="childSearchInput"
                type="text"
                placeholder="Введите ФИО ученика..."
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
              <!-- Выпадающий список -->
              <div
                v-if="childSearchInput && filteredChildren.length > 0"
                class="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg z-10 max-h-48 overflow-y-auto"
              >
                <div
                  v-for="child in filteredChildren"
                  :key="child.child_id"
                  @click="selectChild(child)"
                  class="px-3 py-2 hover:bg-gray-700 cursor-pointer text-white transition"
                >
                  {{ child.last_name }} {{ child.first_name }}{{ child.patronymic ? ' ' + child.patronymic : '' }}
                </div>
              </div>
              <!-- "Не найдено" (только если пользователь ввел текст и нет результатов) -->
              <div
                v-if="childSearchInput && filteredChildren.length === 0 && availableChildren.length > 0"
                class="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-400 text-sm z-10"
              >
                Ученик не найден
              </div>
              <!-- "Нет доступных учеников" (только если все уже привязаны) -->
              <div
                v-if="availableChildren.length === 0"
                class="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-400 text-sm z-10"
              >
                ⚠️ Все ученики уже привязаны к этому родителю
              </div>
            </div>
            <!-- Выбранный ученик -->
            <div v-if="selectedChild" class="mt-2 px-3 py-2 bg-blue-900/30 rounded-lg border border-blue-500/50 text-blue-300 text-sm">
              ✓ {{ selectedChild.last_name }} {{ selectedChild.first_name }}
            </div>
          </div>

          <!-- Роль (relationship) -->
          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Кем приходится *</label>
            <select
              v-model="form.relationship"
              required
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
            >
              <option value="">Выберите...</option>
              <option value="мать">Мать</option>
              <option value="отец">Отец</option>
              <option value="бабушка">Бабушка</option>
              <option value="дедушка">Дедушка</option>
              <option value="опекун">Опекун</option>
              <option value="другое">Другое</option>
            </select>
          </div>

          <!-- Главный контакт -->
          <div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                v-model="form.is_main"
                class="w-4 h-4 rounded border-gray-600 bg-gray-700 accent-blue-500"
              />
              <span class="text-sm font-semibold text-gray-300">Сделать главным контактом</span>
            </label>
          </div>

          <!-- Кнопки -->
          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition"
            >
              Добавить
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
import { ref, computed } from 'vue';
import { updateParent, createParentChildLink } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  parentId: { type: Number, required: true },
  availableChildren: { type: Array, default: () => [] },
});

const emit = defineEmits(['close', 'saved']);

const childSearchInput = ref('');
const selectedChild = ref(null);

const form = ref({
  relationship: '',
  is_main: false,
});

const filteredChildren = computed(() => {
  if (!childSearchInput.value.trim()) return [];
  const query = childSearchInput.value.toLowerCase();
  
  return props.availableChildren.filter(child => {
    const fullName = `${child.last_name} ${child.first_name} ${child.patronymic || ''}`.toLowerCase();
    return fullName.includes(query);
  });
});

function selectChild(child) {
  selectedChild.value = child;
  childSearchInput.value = '';
}

async function submit() {
  if (!selectedChild.value) {
    return Swal.fire({
      icon: 'warning',
      title: 'Выберите ученика',
      background: '#111827',
      color: '#fff',
    });
  }

  if (!form.value.relationship) {
    return Swal.fire({
      icon: 'warning',
      title: 'Укажите роль',
      background: '#111827',
      color: '#fff',
    });
  }

  try {
    // Создаем связь между родителем и ребенком
    await createParentChildLink(props.parentId, selectedChild.value.child_id, form.value.is_main);

    Swal.fire({
      icon: 'success',
      title: 'Ученик добавлен',
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