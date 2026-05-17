<template>
  <Teleport to="body">
    <div
      class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
    >
      <div
        class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl"
      >
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-white">
            {{ initialData ? "Редактировать родителя" : "Новый родитель" }}
          </h2>
          <button
            @click="$emit('close')"
            class="text-gray-500 hover:text-white transition text-xl"
          >
            ✕
          </button>
        </div>

        <form @submit.prevent="submit" class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div class="col-span-2">
              <label
                class="block text-sm font-semibold text-gray-500 uppercase mb-1"
                >Фамилия *</label
              >
              <input
                v-model="form.last_name"
                type="text"
                required
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
            <div>
              <label
                class="block text-sm font-semibold text-gray-500 uppercase mb-1"
                >Имя *</label
              >
              <input
                v-model="form.first_name"
                type="text"
                required
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
            <div>
              <label
                class="block text-sm font-semibold text-gray-500 uppercase mb-1"
                >Отчество</label
              >
              <input
                v-model="form.patronymic"
                type="text"
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
            </div>
          </div>

          <!-- Выбор учеников — только при создании, при редактировании связь можно менять в карточке родителя -->
          <div v-if="!initialData">
            <div class="text-xs text-gray-500 mb-3 p-3 bg-blue-900/20 rounded border border-blue-500/30">
              💡 После создания вы сможете добавлять/удалять учеников в карточке родителя
            </div>
            <label
              class="block text-sm font-semibold text-gray-500 uppercase mb-1"
              >Ученик *</label
            >
            <div class="relative">
              <input
                v-model="childSearchInput"
                type="text"
                placeholder="Введите ФИО ученика..."
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              />
              <!-- Выпадающий список с результатами поиска -->
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
                  {{ child.last_name }} {{ child.first_name
                  }}{{ child.patronymic ? " " + child.patronymic : "" }}
                </div>
              </div>
              <!-- Сообщение, если поиск не дал результатов -->
              <div
                v-if="
                  childSearchInput &&
                  filteredChildren.length === 0 &&
                  children.length > 0
                "
                class="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-400 text-sm z-10"
              >
                Ученик не найден
              </div>
              <!-- Сообщение, если нет учеников в базе -->
              <div
                v-if="children.length === 0"
                class="absolute top-full left-0 right-0 mt-1 bg-gray-800 border border-gray-700 rounded-lg p-3 text-gray-400 text-sm z-10"
              >
                ⚠️ Нет учеников в базе. Сначала добавьте учеников.
              </div>
            </div>

            <!-- Выбранные ученики -->
            <div v-if="selectedChildren.length > 0" class="mt-3 space-y-2">
              <div
                v-for="child in selectedChildren"
                :key="child.child_id"
                class="flex items-center justify-between px-3 py-2 bg-blue-900/30 rounded-lg border border-blue-500/50 text-blue-300 text-sm"
              >
                <span class="truncate flex-1 font-medium">
                  {{ child.last_name }} {{ child.first_name }}
                </span>

                <div class="flex items-center gap-3 ml-4">
                  <label class="cursor-pointer group">
                    <input
                      type="checkbox"
                      :checked="getIsMain(child.child_id)"
                      @change="toggleIsMain(child.child_id)"
                      class="hidden"
                    />
                    <span
                      class="px-2 py-1 rounded text-[10px] uppercase tracking-wider font-bold transition-all duration-200 border"
                      :class="
                        getIsMain(child.child_id)
                          ? 'bg-blue-500 border-blue-400 text-white shadow-lg shadow-blue-900/40'
                          : 'bg-gray-800 border-gray-700 text-gray-500 group-hover:border-gray-500 group-hover:text-gray-300'
                      "
                    >
                      Осн. контакт
                    </span>
                  </label>

                  <button
                    type="button"
                    @click="removeChild(child.child_id)"
                    class="p-1.5 hover:bg-red-900/50 rounded-lg transition text-red-400 hover:text-red-300"
                    title="Удалить ученика"
                  >
                    <span class="text-sm">🗑</span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div>
            <label
              class="block text-sm font-semibold text-gray-500 uppercase mb-1"
              >Кем приходится *</label
            >
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

          <div>
            <label
              class="block text-sm font-semibold text-gray-500 uppercase mb-1"
              >Телефон *</label
            >
            <input
              :value="phoneDisplay"
              @input="handlePhoneInput"
              type="tel"
              placeholder="+7 (999) 123-45-67"
              required
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              :class="phoneError ? 'border-red-500 focus:ring-red-500' : ''"
            />
            <p v-if="phoneError" class="text-xs text-red-400 mt-1">
              {{ phoneError }}
            </p>
          </div>

          <div>
            <label
              class="block text-sm font-semibold text-gray-500 uppercase mb-1"
              >Email *</label
            >
            <input
              v-model="form.email"
              type="email"
              required
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition"
              placeholder="example@mail.ru"
            />
          </div>

          <div>
            <label
              class="block text-sm font-semibold text-gray-500 uppercase mb-1"
              >Заметки</label
            >
            <textarea
              v-model="form.notes"
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none transition h-20 resize-none"
              placeholder="Предпочтительный способ связи, особенности..."
            ></textarea>
          </div>

          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition"
            >
              {{ initialData ? "Обновить" : "Сохранить" }}
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
import { ref, watch, computed } from "vue";
import { usePhone } from "../../composables/usePhone.js";
import {
  createParent,
  updateParent,
  createParentChildLink,
} from "../../api/client.js";
import Swal from "sweetalert2";

const props = defineProps({
  // null = режим создания, объект = режим редактирования
  initialData: { type: Object, default: null },
  // Список всех учеников для выбора при создании
  children: { type: Array, default: () => [] },
});

const emit = defineEmits(["close", "saved"]);

const {
  phoneDisplay,
  phoneError,
  phoneValue,
  handlePhoneInput,
  setPhone,
  resetPhone,
} = usePhone();

// -------------------------------------------------------
// ФОРМА
// -------------------------------------------------------

const selectedChildren = ref([]); // Массив выбранных детей: { child_id, last_name, first_name, is_main }
const childrenMainStatus = ref({}); // { child_id: is_main }
const childSearchInput = ref("");

const defaultForm = () => ({
  last_name: "",
  first_name: "",
  patronymic: "",
  relationship: "",
  email: "",
  notes: "",
});

const form = ref(defaultForm());

// Фильтруем детей по поиску и исключаем уже выбранных
const filteredChildren = computed(() => {
  if (!childSearchInput.value.trim()) return [];
  const query = childSearchInput.value.toLowerCase();
  const selectedIds = new Set(selectedChildren.value.map((c) => c.child_id));

  return props.children.filter((child) => {
    // Пропускаем уже выбранных
    if (selectedIds.has(child.child_id)) return false;

    const fullName =
      `${child.last_name} ${child.first_name} ${child.patronymic || ""}`.toLowerCase();
    return fullName.includes(query);
  });
});

// Функция выбора ребенка из списка
function selectChild(child) {
  // Проверяем, не добавлен ли уже
  if (selectedChildren.value.some((c) => c.child_id === child.child_id)) {
    return;
  }

  selectedChildren.value.push(child);
  childSearchInput.value = ""; // Очищаем поле поиска
}

// Функция удаления ребенка из выбранных
function removeChild(childId) {
  selectedChildren.value = selectedChildren.value.filter(
    (c) => c.child_id !== childId,
  );
  delete childrenMainStatus.value[childId]; // Удаляем статус главного
}

// Получить статус is_main для ребенка
function getIsMain(childId) {
  return childrenMainStatus.value[childId] || false;
}

// Переключить статус is_main для ребенка
function toggleIsMain(childId) {
  childrenMainStatus.value[childId] = !childrenMainStatus.value[childId];
}

watch(
  () => props.initialData,
  (data) => {
    if (data) {
      form.value = {
        last_name: data.last_name,
        first_name: data.first_name,
        patronymic: data.patronymic || "",
        relationship: data.relationship || "",
        email: data.email || "",
        notes: data.notes || "",
      };
      setPhone(data.phone_number);
    } else {
      form.value = defaultForm();
      selectedChildren.value = [];
      childrenMainStatus.value = {};
      childSearchInput.value = "";
      resetPhone();
    }
  },
  { immediate: true },
);

// -------------------------------------------------------
// СОХРАНЕНИЕ
// -------------------------------------------------------

async function submit() {
  if (phoneError.value || !phoneValue.value) {
    return Swal.fire({
      icon: "warning",
      title: "Проверь номер телефона",
      background: "#111827",
      color: "#fff",
    });
  }
  if (!props.initialData && selectedChildren.value.length === 0) {
    return Swal.fire({
      icon: "warning",
      title: "Выберите хотя бы одного ученика",
      background: "#111827",
      color: "#fff",
    });
  }

  const payload = {
    ...form.value,
    patronymic: form.value.patronymic || null,
    notes: form.value.notes || null,
    phone_number: phoneValue.value,
  };

  try {
    let result;
    if (props.initialData) {
      result = await updateParent(props.initialData.parent_id, payload);
    } else {
      // 1. Создаём родителя
      result = await createParent(payload);

      // 2. Привязываем ко всем выбранным ученикам с указанием is_main
      for (const child of selectedChildren.value) {
        const isMain = childrenMainStatus.value[child.child_id] || false;
        await createParentChildLink(result.parent_id, child.child_id, isMain);
      }
    }

    Swal.fire({
      icon: "success",
      title: props.initialData ? "Данные обновлены" : "Родитель добавлен",
      timer: 1250,
      showConfirmButton: false,
      background: "#111827",
      color: "#fff",
    });

    emit("saved", result);
    emit("close");
  } catch (e) {
    Swal.fire({
      icon: "error",
      title: "Ошибка",
      text: e.message,
      background: "#111827",
      color: "#fff",
    });
  }
}
</script>