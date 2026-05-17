<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl">

        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-white">Добавить родителя</h2>
          <button @click="$emit('close')" class="text-gray-500 hover:text-white transition text-xl">✕</button>
        </div>

        <!-- Переключатель между режимами -->
        <div class="flex gap-2 mb-6 bg-gray-800 p-1 rounded-lg border border-gray-700">
          <button
            @click="mode = 'select'"
            :class="mode === 'select' ? 'bg-blue-600 text-white' : 'bg-transparent text-gray-400 hover:text-gray-300'"
            class="flex-1 px-4 py-2 rounded-lg font-semibold transition text-sm"
          >
            Выбрать из базы
          </button>
          <button
            @click="mode = 'create'"
            :class="mode === 'create' ? 'bg-blue-600 text-white' : 'bg-transparent text-gray-400 hover:text-gray-300'"
            class="flex-1 px-4 py-2 rounded-lg font-semibold transition text-sm"
          >
            Создать нового
          </button>
        </div>

        <!-- ===== РЕЖИМ: ВЫБРАТЬ ИЗ БАЗЫ ===== -->
        <div v-if="mode === 'select'" class="space-y-4">
          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Родитель *</label>
            <div class="relative">
              <input
                v-model="parentSearchInput"
                type="text"
                placeholder="Введите ФИО родителя..."
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
              <!-- Выпадающий список -->
              <div
                v-if="parentSearchInput && filteredParents.length > 0"
                class="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg shadow-lg z-10 max-h-48 overflow-y-auto"
              >
                <div
                  v-for="parent in filteredParents"
                  :key="parent.parent_id"
                  @click="selectParent(parent)"
                  class="px-3 py-2 hover:bg-gray-700 cursor-pointer text-white transition"
                >
                  <div class="font-semibold">{{ parent.last_name }} {{ parent.first_name }}</div>
                  <div class="text-xs text-gray-400">{{ parent.relationship }} • {{ parent.phone_number }}</div>
                </div>
              </div>
              <!-- "Не найдено" -->
              <div
                v-if="parentSearchInput && filteredParents.length === 0 && allParents.length > 0"
                class="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-400 text-sm z-10"
              >
                Родитель не найден
              </div>
              <!-- "Нет родителей в базе" -->
              <div
                v-if="allParents.length === 0"
                class="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-400 text-sm z-10"
              >
                ⚠️ Нет родителей в базе. Создайте нового.
              </div>
            </div>
            <!-- Выбранный родитель -->
            <div v-if="selectedParent" class="mt-2 px-3 py-2 bg-blue-900/30 rounded-lg border border-blue-500/50 text-blue-300 text-sm">
              ✓ {{ selectedParent.last_name }} {{ selectedParent.first_name }}
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

          <!-- Основной контакт -->
          <div>
            <label class="cursor-pointer group inline-block">
                <input
                type="checkbox"
                v-model="form.is_main"
                class="hidden"
                />
                <span
                class="px-2 py-1 rounded text-[10px] uppercase tracking-wider font-bold transition-all duration-200 border block w-fit"
                :class="
                    form.is_main
                    ? 'bg-blue-500 border-blue-400 text-white shadow-lg shadow-blue-900/40'
                    : 'bg-gray-800 border-gray-700 text-gray-500 group-hover:border-gray-500 group-hover:text-gray-300'
                "
                >
                {{ form.is_main ? 'Основной контакт' : 'Сделать основным' }}
                </span>
            </label>
          </div>

          <!-- Кнопки -->
          <div class="flex gap-3 pt-2">
            <button
              @click="submitSelect"
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
        </div>

        <!-- ===== РЕЖИМ: СОЗДАТЬ НОВОГО ===== -->
        <form v-if="mode === 'create'" @submit.prevent="submitCreate" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="col-span-2">
              <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Фамилия *</label>
              <input
                v-model="createForm.last_name"
                type="text"
                required
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Имя *</label>
              <input
                v-model="createForm.first_name"
                type="text"
                required
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Отчество</label>
              <input
                v-model="createForm.patronymic"
                type="text"
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
          </div>

          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Кем приходится *</label>
            <select
              v-model="createForm.relationship"
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
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Email *</label>
            <input
              v-model="createForm.email"
              type="email"
              required
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              placeholder="example@mail.ru"
            />
          </div>

          <!-- Главный контакт -->
          <div>
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                v-model="createForm.is_main"
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
              Создать и добавить
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
import { ref, computed, onMounted } from 'vue';
import { usePhone } from '../../composables/usePhone.js';
import { getParents, createParent, createParentChildLink, getChildParents } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  childId: { type: Number, required: true },
});

const emit = defineEmits(['close', 'saved']);

const { phoneDisplay, phoneError, phoneValue, handlePhoneInput, setPhone, resetPhone } = usePhone();

// -------------------------------------------------------
// СОСТОЯНИЕ
// -------------------------------------------------------

const mode = ref('select');

// Режим выбора из базы
const parentSearchInput = ref('');
const selectedParent = ref(null);
const allParents = ref([]);
const linkedParentIds = ref([]); // ID уже привязанных родителей

const form = ref({
  relationship: '',
  is_main: false,
});

// Режим создания нового
const createForm = ref({
  last_name: '',
  first_name: '',
  patronymic: '',
  relationship: '',
  email: '',
  is_main: false,
});

// -------------------------------------------------------
// ЗАГРУЗКА РОДИТЕЛЕЙ
// -------------------------------------------------------

async function loadParents() {
  try {
    allParents.value = await getParents(0, 1000);
    
    // Загружаем родителей текущего ребенка, чтобы исключить их из поиска
    const childParents = await getChildParents(props.childId);
    linkedParentIds.value = childParents.map(p => p.parent_id);
  } catch (e) {
    console.error('Ошибка загрузки родителей:', e);
  }
}

onMounted(loadParents);

// -------------------------------------------------------
// ВЫЧИСЛЯЕМЫЕ
// -------------------------------------------------------

const filteredParents = computed(() => {
  if (!parentSearchInput.value.trim()) return [];
  const query = parentSearchInput.value.toLowerCase();
  
  // Загружаем родителей текущего ребенка при открытии модалки
  // (используется только при режиме "Выбрать из базы")
  
  return allParents.value.filter(parent => {
    const fullName = `${parent.last_name} ${parent.first_name} ${parent.patronymic || ''}`.toLowerCase();
    
    // Исключаем уже привязанных родителей
    const isAlreadyLinked = linkedParentIds.value.includes(parent.parent_id);
    
    return fullName.includes(query) && !isAlreadyLinked;
  });
});

// -------------------------------------------------------
// РЕЖИМ: ВЫБРАТЬ ИЗ БАЗЫ
// -------------------------------------------------------

function selectParent(parent) {
  selectedParent.value = parent;
  parentSearchInput.value = '';
}

async function submitSelect() {
  if (!selectedParent.value) {
    return Swal.fire({
      icon: 'warning',
      title: 'Выберите родителя',
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
    // Создаём связь между родителем и ребенком
    await createParentChildLink(selectedParent.value.parent_id, props.childId, form.value.is_main);

    Swal.fire({
      icon: 'success',
      title: 'Родитель добавлен',
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

// -------------------------------------------------------
// РЕЖИМ: СОЗДАТЬ НОВОГО
// -------------------------------------------------------

async function submitCreate() {
  if (phoneError.value || !phoneValue.value) {
    return Swal.fire({
      icon: 'warning',
      title: 'Проверь номер телефона',
      background: '#111827',
      color: '#fff',
    });
  }

  if (!createForm.value.relationship) {
    return Swal.fire({
      icon: 'warning',
      title: 'Укажите роль',
      background: '#111827',
      color: '#fff',
    });
  }

  const payload = {
    ...createForm.value,
    patronymic: createForm.value.patronymic || null,
    phone_number: phoneValue.value,
  };

  try {
    // 1. Создаём родителя
    const newParent = await createParent(payload);

    // 2. Привязываем его к ребенку
    await createParentChildLink(newParent.parent_id, props.childId, createForm.value.is_main);

    Swal.fire({
      icon: 'success',
      title: 'Родитель создан и добавлен',
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