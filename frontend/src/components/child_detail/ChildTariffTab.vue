<template>
  <div>
    <Transition name="fade" mode="out-in">
      <TariffChildSkeleton v-if="loading" key="skel" />

      <div v-else key="content">

        <!-- Активный тариф -->
        <div v-if="activeTariff" class="space-y-6">
          <div
            :class="[
              'bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 shadow-xl border',
              activeTariff.tariff_period.lessons_rest === 0 || activeTariff.tariff_period.debt > 0
                ? 'border-red-500/60 shadow-red-900/20'
                : 'border-emerald-500/30',
            ]"
          >
            <div class="flex justify-between items-start mb-6">
              <div>
                <p class="text-xs uppercase tracking-widest text-emerald-400 font-bold mb-1">Активный тариф</p>
                <h2 class="text-3xl font-black text-white">{{ activeTariff.tariff.name }}</h2>
                <p class="text-gray-400 text-sm mt-1">с {{ formatDateShort(activeTariff.tariff_period.start_date) }}</p>
              </div>
              <span class="text-4xl">{{ getTariffIcon(activeTariff.tariff.tariff_type) }}</span>
            </div>

            <div class="grid grid-cols-3 gap-4 mb-6">
              <div class="bg-gray-900/60 rounded-xl p-4 border border-gray-700">
                <p class="text-xs text-gray-500 uppercase mb-1">Осталось уроков</p>
                <p class="text-3xl font-black" :class="activeTariff.tariff_period.lessons_rest <= 2 ? 'text-red-400' : 'text-blue-400'">
                  {{ activeTariff.tariff_period.lessons_rest }}
                </p>
                <p class="text-xs text-gray-600 mt-1">из {{ activeTariff.tariff.num_of_lessons }}</p>
              </div>
              <div class="bg-gray-900/60 rounded-xl p-4 border border-gray-700">
                <p class="text-xs text-gray-500 uppercase mb-1">Задолженность</p>
                <p class="text-3xl font-black" :class="activeTariff.tariff_period.debt > 0 ? 'text-red-400' : 'text-emerald-400'">
                  {{ activeTariff.tariff_period.debt }} ₽
                </p>
              </div>
              <div class="bg-gray-900/60 rounded-xl p-4 border border-gray-700">
                <p class="text-xs text-gray-500 uppercase mb-1">Стоимость пакета</p>
                <p class="text-3xl font-black text-gray-300">{{ activeTariff.tariff.price }} ₽</p>
                <p class="text-xs text-gray-600 mt-1">
                  {{ (activeTariff.tariff.price / activeTariff.tariff.num_of_lessons).toFixed(0) }} ₽/урок
                </p>
              </div>
            </div>

            <div class="mb-6">
              <div class="flex justify-between text-xs text-gray-500 mb-1">
                <span>Прогресс по пакету</span>
                <span>{{ activeTariff.tariff.num_of_lessons - activeTariff.tariff_period.lessons_rest }} / {{ activeTariff.tariff.num_of_lessons }} уроков</span>
              </div>
              <div class="w-full bg-gray-700 rounded-full h-2">
                <div
                  class="h-2 rounded-full transition-all"
                  :class="activeTariff.tariff_period.lessons_rest <= 2 ? 'bg-red-500' : 'bg-emerald-500'"
                  :style="{ width: ((activeTariff.tariff.num_of_lessons - activeTariff.tariff_period.lessons_rest) / activeTariff.tariff.num_of_lessons) * 100 + '%' }"
                ></div>
              </div>
            </div>

            <div class="flex gap-3">
              <button
                @click="openEditTariffFields"
                class="flex-1 px-4 py-2 bg-blue-600/20 hover:bg-blue-600/40 border border-blue-500/50 text-blue-300 rounded-lg transition font-semibold text-sm"
              >
                ✏️ Редактировать
              </button>
              <button
                @click="confirmCloseTariff"
                class="flex-1 px-4 py-2 bg-red-900/20 hover:bg-red-900/40 border border-red-500/50 text-red-300 rounded-lg transition font-semibold text-sm"
              >
                🔒 Закрыть тариф
              </button>
            </div>
          </div>

          <!-- История тарифов (когда есть активный) -->
          <div>
            <h3 class="text-lg font-bold text-gray-300 mb-3">История тарифов</h3>
            <div v-if="tariffHistory.filter(p => !p.active).length > 0" class="space-y-2">
              <div
                v-for="period in tariffHistory.filter(p => !p.active)"
                :key="period.tariff_period_id"
                class="flex items-center justify-between px-4 py-3 bg-gray-800 rounded-lg border border-gray-700 text-sm"
              >
                <span class="text-gray-400">{{ formatDateShort(period.start_date) }}</span>
                <span class="text-gray-300">Тариф #{{ period.tariff_id }}</span>
                <span class="text-gray-500">{{ period.lessons_rest }} ур. осталось</span>
                <span class="px-2 py-0.5 rounded text-xs bg-gray-700 text-gray-500">Закрыт</span>
              </div>
            </div>
            <p v-else class="text-gray-600 text-sm">Нет закрытых тарифов</p>
          </div>
        </div>

        <!-- Нет активного тарифа -->
        <div v-else class="text-center py-16">
          <div class="text-6xl mb-4">📭</div>
          <h2 class="text-2xl font-bold text-white mb-2">Нет активного тарифа</h2>
          <p class="text-gray-400 mb-6">Подключите тариф ученику</p>
          <div class="flex gap-3 justify-center">
            <button
              @click="showAssignTariffModal = true"
              class="px-6 py-3 bg-gradient-to-r from-emerald-600 to-emerald-700 hover:from-emerald-700 hover:to-emerald-800 text-white font-semibold rounded-lg transition shadow-lg"
            >
              + Подключить тариф
            </button>
            <button
              @click="toggleHistory"
              class="px-6 py-3 bg-gray-800 hover:bg-gray-700 text-gray-300 font-semibold rounded-lg transition border border-gray-700"
              :class="showTariffHistory ? 'border-blue-500 text-blue-300' : ''"
            >
              {{ showTariffHistory ? '📜 Скрыть историю' : '📜 История тарифов' }}
            </button>
          </div>
          <div v-if="showTariffHistory && tariffHistory.length > 0" class="mt-6 space-y-2 max-w-lg mx-auto">
            <div
              v-for="period in tariffHistory"
              :key="period.tariff_period_id"
              class="flex items-center justify-between px-4 py-3 bg-gray-800 rounded-lg border border-gray-700 text-sm"
            >
              <span class="text-gray-400">{{ formatDateShort(period.start_date) }}</span>
              <span class="text-gray-300">Тариф #{{ period.tariff_id }}</span>
              <span class="text-gray-500">{{ period.lessons_rest }} ур. осталось</span>
              <span class="px-2 py-0.5 rounded text-xs bg-gray-700 text-gray-500">Закрыт</span>
            </div>
          </div>
        </div>

        <!-- Кнопка подключить другой (когда тариф есть) -->
        <div v-if="activeTariff" class="mt-4">
          <button
            @click="showAssignTariffModal = true"
            class="px-4 py-2 bg-gray-800 hover:bg-gray-700 border border-gray-700 text-gray-400 hover:text-white text-sm rounded-lg transition"
          >
            🔄 Подключить другой тариф
          </button>
        </div>

        <!-- Модалка: подключить тариф -->
        <div
          v-if="showAssignTariffModal"
          class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        >
          <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-white">Подключить тариф</h2>
              <button @click="showAssignTariffModal = false" class="text-gray-500 hover:text-white text-xl">✕</button>
            </div>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Тариф *</label>
                <select
                  v-model="assignForm.tariff_id"
                  class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
                >
                  <option :value="null" disabled>Выберите тариф...</option>
                  <option v-for="t in allTariffs" :key="t.tariff_id" :value="t.tariff_id">
                    {{ t.name }} — {{ t.price }} ₽ / {{ t.num_of_lessons }} уроков
                  </option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Дата начала *</label>
                <input
                  type="date"
                  v-model="assignForm.start_date"
                  class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-emerald-500 focus:outline-none"
                />
              </div>
              <div v-if="assignForm.tariff_id" class="p-3 bg-emerald-900/20 rounded-lg border border-emerald-500/30 text-sm">
                <p class="text-gray-400">Баланс ученика: <span class="text-emerald-400 font-bold">{{ childBalance }} ₽</span></p>
                <p class="text-gray-400 mt-1">Стоимость тарифа: <span class="text-white font-bold">{{ selectedTariffPrice }} ₽</span></p>
                <p class="text-gray-400 mt-1">
                  Долг после подключения:
                  <span :class="expectedDebt > 0 ? 'text-red-400' : 'text-emerald-400'" class="font-bold">
                    {{ Math.max(0, expectedDebt) }} ₽
                  </span>
                </p>
              </div>
              <div class="flex gap-3 pt-2">
                <button @click="submitAssignTariff" class="flex-1 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 rounded-lg text-white font-semibold transition">
                  Подключить
                </button>
                <button @click="showAssignTariffModal = false" class="flex-1 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-white font-semibold transition">
                  Отмена
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Модалка: редактировать тарифный период -->
        <div
          v-if="showEditTariffModal"
          class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        >
          <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-white">Редактировать тариф</h2>
              <button @click="showEditTariffModal = false" class="text-gray-500 hover:text-white text-xl">✕</button>
            </div>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Осталось уроков</label>
                <input
                  type="number"
                  v-model.number="editTariffForm.lessons_rest"
                  min="0"
                  class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Задолженность (₽)</label>
                <input
                  type="number"
                  v-model.number="editTariffForm.debt"
                  min="0"
                  step="0.01"
                  class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div class="flex gap-3 pt-2">
                <button @click="submitEditTariffFields" class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition">
                  Сохранить
                </button>
                <button @click="showEditTariffModal = false" class="flex-1 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-white font-semibold transition">
                  Отмена
                </button>
              </div>
            </div>
          </div>
        </div>

        <ConfirmModal
          :show="showConfirmCloseTariff"
          title="Закрыть тариф?"
          message="Текущий тариф будет деактивирован. Это действие нельзя отменить."
          @close="showConfirmCloseTariff = false"
          @confirm="proceedCloseTariff"
        />
      </div>
    </Transition>
  </div>
</template>

<script setup>
// name нужен для корректной работы KeepAlive
defineOptions({ name: 'ChildTariffTab' });

import { ref, computed, onMounted, onActivated } from 'vue';
import TariffChildSkeleton from '../skeletons/TariffChildSkeleton.vue';
import ConfirmModal from '../modals/ConfirmModal.vue';
import {
  getTariffs, getStudentStatus, getChildTariffPeriods,
  assignTariff, updateTariffPeriod, closeTariffPeriod,
} from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  childId:      { type: Number, required: true },
  childBalance: { type: Number, default: 0 },
});

const emit = defineEmits(['tariff-changed', 'active-tariff-updated']);

// --- СОСТОЯНИЕ ---
const loading = ref(true);
const activeTariff = ref(null);
const allTariffs = ref([]);
const tariffHistory = ref([]);
const showAssignTariffModal = ref(false);
const showEditTariffModal = ref(false);
const showConfirmCloseTariff = ref(false);
const showTariffHistory = ref(false);
const assignForm = ref({ tariff_id: null, start_date: new Date().toISOString().split('T')[0] });
const editTariffForm = ref({ lessons_rest: 0, debt: 0 });

// --- ВЫЧИСЛЯЕМЫЕ ---
const selectedTariffPrice = computed(() => {
  if (!assignForm.value.tariff_id) return 0;
  return allTariffs.value.find((t) => t.tariff_id === assignForm.value.tariff_id)?.price ?? 0;
});

const expectedDebt = computed(() => selectedTariffPrice.value - props.childBalance);

// --- ЗАГРУЗКА ---
async function loadTariff(showSkeleton = true) {
  try {
    if (showSkeleton) loading.value = true;
    const [status, history] = await Promise.all([
      getStudentStatus(props.childId),
      getChildTariffPeriods(props.childId),
    ]);
    tariffHistory.value = history;
    const active = history.find((p) => p.active);
    const tariff = active ? allTariffs.value.find((t) => t.tariff_id === active.tariff_id) : null;
    activeTariff.value = (active && tariff) ? { tariff_period: active, tariff } : null;
  } catch (e) {
    console.error('Ошибка загрузки тарифа:', e);
  } finally {
    loading.value = false;
    emit('active-tariff-updated', activeTariff.value);
  }
}

onMounted(async () => {
  allTariffs.value = await getTariffs();
  await loadTariff();
});

onActivated(async () => {
  await loadTariff(false);
});

// --- ДЕЙСТВИЯ ---
async function toggleHistory() {
  showTariffHistory.value = !showTariffHistory.value;
  if (showTariffHistory.value && tariffHistory.value.length === 0) {
    tariffHistory.value = await getChildTariffPeriods(props.childId);
  }
}

async function submitAssignTariff() {
  if (!assignForm.value.tariff_id || !assignForm.value.start_date) {
    return Swal.fire({ icon: 'warning', title: 'Заполните все поля', background: '#111827', color: '#fff' });
  }
  try {
    await assignTariff(props.childId, assignForm.value.tariff_id, assignForm.value.start_date);
    showAssignTariffModal.value = false;
    assignForm.value = { tariff_id: null, start_date: new Date().toISOString().split('T')[0] };
    await loadTariff();
    emit('tariff-changed');
    Swal.fire({ icon: 'success', title: 'Тариф подключён', timer: 1250, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

function openEditTariffFields() {
  editTariffForm.value = {
    lessons_rest: activeTariff.value.tariff_period.lessons_rest,
    debt: activeTariff.value.tariff_period.debt,
  };
  showEditTariffModal.value = true;
}

async function submitEditTariffFields() {
  try {
    await updateTariffPeriod(activeTariff.value.tariff_period.tariff_period_id, editTariffForm.value);
    showEditTariffModal.value = false;
    await loadTariff();
    Swal.fire({ icon: 'success', title: 'Обновлено', timer: 1250, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

function confirmCloseTariff() {
  showConfirmCloseTariff.value = true;
}

async function proceedCloseTariff() {
  try {
    await closeTariffPeriod(activeTariff.value.tariff_period.tariff_period_id);
    showConfirmCloseTariff.value = false;
    activeTariff.value = null;
    await loadTariff();
    emit('tariff-changed');
    Swal.fire({ icon: 'success', title: 'Тариф закрыт', timer: 1250, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

// --- УТИЛИТЫ ---
const formatDateShort = (d) => new Date(d).toLocaleDateString('ru-RU');

function getTariffIcon(type) {
  const icons = { starter: '⭐', standard: '✨', premium: '👑', basic: '📚', advanced: '🚀', enterprise: '💎' };
  return icons[type] || '📦';
}
</script>

<style scoped>
input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
</style>