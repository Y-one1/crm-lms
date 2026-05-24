<template>
  <Layout>
    <div class="p-8">

      <!-- Шапка с кнопкой -->
      <div class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-4xl font-black mb-2">💰 Тарифные планы</h1>
          <p class="text-gray-400">Управление списком тарифов</p>
        </div>
        <div class="flex gap-3">
          <button
            @click="showArchive = !showArchive; loadArchive()"
            class="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-gray-300 font-semibold rounded-lg transition border border-gray-600"
            :class="showArchive ? 'border-yellow-500/50 text-yellow-300' : ''"
          >
            🗄 Архив
          </button>
          <button
            @click="openAdd"
            :disabled="isLoading"
            class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-lg transition shadow-lg disabled:opacity-50 disabled:pointer-events-none"
          >
            + Добавить тариф
          </button>
        </div>
      </div>
      
      <Transition name="fade" mode="out-in">
        <!-- Скелетон -->
        <TariffSkeleton v-if="isLoading" />

        <!-- Пустое состояние -->
        <div v-else-if="tariffs.length === 0" class="text-center py-16">
          <div class="text-6xl mb-4">¯\_(ツ)_/¯</div>
          <h2 class="text-2xl font-bold text-white mb-2">Тарифов в базе нет!</h2>
          <p class="text-gray-400 mb-6">Добавьте первый тариф, чтобы начать</p>
        </div>

        <!-- Сетка тарифов -->
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="tariff in tariffs"
            :key="tariff.tariff_id"
            class="group relative bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl border border-gray-700 overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-300 hover:border-emerald-500/50"
          >
            <!-- Фоновый градиент при наведении -->
            <div class="absolute inset-0 bg-gradient-to-br from-emerald-500/0 to-emerald-500/0 group-hover:from-emerald-500/5 group-hover:to-emerald-500/10 transition duration-300"></div>

            <!-- Контент -->
            <div class="relative p-6 flex flex-col h-full">

              <!-- Иконка и название тарифа -->
              <div class="mb-4">
                <div class="flex items-start justify-between mb-2">
                  <h3 class="text-2xl font-black text-white">{{ tariff.name }}</h3>
                  <span class="text-3xl">{{ getTariffIcon(tariff.tariff_type) }}</span>
                </div>
                <p class="text-xs uppercase tracking-wider text-emerald-400 font-semibold">
                  {{ getTariffTypeLabel(tariff.tariff_type) }}
                </p>
              </div>

              <!-- Цена -->
              <div class="mb-6 py-4 border-y border-gray-700">
                <p class="text-sm text-white-400 mb-1">Цена за пакет</p>
                <div class="flex items-baseline gap-1">
                  <span class="text-4xl font-black text-emerald-400">{{ tariff.price }}</span>
                  <span class="text-lg text-gray-500">₽</span>
                </div>
              </div>

              <!-- Количество занятий -->
              <div class="mb-6 p-4 bg-emerald-900/20 rounded-lg border border-emerald-500/30">
                <div class="flex items-baseline">
                  <p class="text-xs uppercase tracking-wider text-white-400">Занятий в пакете:</p>
                  <span class="text-2xl px-1 font-black text-emerald-400">{{ tariff.num_of_lessons }}</span>
                </div>
                
                <div class="mt-1 border-t border-emerald-500/10 pt-1">
                  <p class="text-xs text-gray-500">
                    {{ (tariff.price / tariff.num_of_lessons).toFixed(0) }} ₽ за урок
                  </p>
                </div>
              </div>

              <!-- Кол-во учеников с тарифом -->
              <!-- TODO -->
              <div class="mb-6 flex items-center gap-2">
                <div 
                  class="w-2 h-2 rounded-full transition-colors duration-500" 
                  :class="tariffCounts[tariff.tariff_id] > 0 ? 'bg-emerald-400' : 'bg-gray-600'"
                ></div>
                <span class="text-sm"
                      :class="tariffCounts[tariff.tariff_id] > 0 ? 'text-white-400' : 'text-gray-600'">
                  Активных учеников: 
                  <span class="text-xl font-bold ml-1"
                        :class="tariffCounts[tariff.tariff_id] > 0 ? 'text-yellow-400' : 'text-gray-600'">
                    {{ tariffCounts[tariff.tariff_id] !== undefined ? tariffCounts[tariff.tariff_id] : '...' }}
                  </span>
                </span>
              </div>

              <!-- Кнопки действий -->
              <div class="flex gap-2 mt-auto pt-4 border-t border-gray-700">
                <button
                  @click.stop="openEdit(tariff)"
                  class="flex-1 px-3 py-2 bg-emerald-600/20 hover:bg-emerald-600/40 border border-emerald-500/50 text-emerald-300 hover:text-emerald-200 rounded-lg transition font-semibold text-sm"
                >
                  ✏️ Редактировать
                </button>
                <button
                  @click.stop="confirmDelete(tariff.tariff_id)"
                  class="flex-1 px-3 py-2 bg-red-900/20 hover:bg-red-900/40 border border-red-500/50 text-red-300 hover:text-red-200 rounded-lg transition font-semibold text-sm"
                >
                  🗑 Удалить
                </button>
              </div>

            </div>
          </div>
        </div>
      </Transition>

      <div v-if="showArchive" class="mt-8">
        <h2 class="text-xl font-bold text-gray-400 mb-4">🗄 Архивные тарифы</h2>
        <div v-if="archivedTariffs.length === 0" class="text-gray-600 text-sm">Архив пуст</div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="tariff in archivedTariffs"
            :key="tariff.tariff_id"
            class="bg-gray-800/50 rounded-2xl border border-gray-700 p-5 opacity-60"
          >
            <div class="flex justify-between items-start mb-2">
              <h3 class="text-lg font-bold text-gray-400">{{ tariff.name }}</h3>
              <span class="text-2xl">{{ getTariffIcon(tariff.tariff_type) }}</span>
            </div>
            <p class="text-sm text-gray-500">{{ tariff.price }} ₽ / {{ tariff.num_of_lessons }} уроков</p>
            <span class="mt-2 inline-block px-2 py-0.5 bg-gray-700 text-gray-500 text-xs rounded">Архивирован</span>
          </div>
        </div>
      </div>

      <!-- Модалка создания/редактирования тарифа -->
      <TariffModal
        v-if="showModal"
        :initial-data="editingTariff"
        @close="showModal = false"
        @saved="onSaved"
      />

      <!-- Подтверждение удаления -->
      <ConfirmModal
        :show="showConfirmDelete"
        title="Удалить тариф?"
        message="Тариф будет перемещён в архив. История учеников сохранится."
        @close="showConfirmDelete = false"
        @confirm="proceedDelete"
      />

    </div>
  </Layout>
</template>

<script setup>
// --- ИМПОРТЫ ---
import { ref, onMounted } from 'vue';
import Layout from '../../components/Layout.vue';
import ConfirmModal from '../../components/modals/ConfirmModal.vue';
import TariffModal from '../../components/modals/TariffModal.vue';
import TariffSkeleton from '../../components/skeletons/TariffSkeleton.vue';
import { getTariffs, deleteTariff, getChildrenWithTariffCount, getArchivedTariffs } from '../../api/client.js';
import Swal from 'sweetalert2';

// --- СОСТОЯНИЕ ---
const tariffs = ref([]);
const tariffCounts = ref({});
const isLoading = ref(true);
const showArchive = ref(false);
const archivedTariffs = ref([]);

const showModal = ref(false);
const editingTariff = ref(null);

const showConfirmDelete = ref(false);
const tariffToDelete = ref(null);

// --- ЗАГРУЗКА ---

async function loadTariffCount(tariffId) {
  try {
    tariffCounts.value[tariffId] = await getChildrenWithTariffCount(tariffId);
  } catch (err) {
    console.error(`Ошибка счёта для тарифа ${tariffId}:`, err);
    tariffCounts.value[tariffId] = 0;
  }
}

async function loadTariffs() {
  try {
    isLoading.value = true;
    const data = await getTariffs();
    tariffs.value = data;

    // Загружаем счётчики параллельно, не блокируя основной UI
    await Promise.all(data.map(t => loadTariffCount(t.tariff_id)));
  } catch (e) {
    Swal.fire({
      icon: 'error',
      title: 'Ошибка загрузки',
      text: 'Не удалось загрузить список тарифов',
      background: '#111827',
      color: '#fff',
    });
  } finally {
    isLoading.value = false;
  }
}

async function loadArchive() {
  if (!showArchive.value) return;
  try {
    archivedTariffs.value = await getArchivedTariffs();
  } catch (e) {
    console.error('Ошибка загрузки архива:', e);
  }
}

onMounted(loadTariffs);

// --- МОДАЛКА / UI-логика ---

function openAdd() {
  editingTariff.value = null;
  showModal.value = true;
}

function openEdit(tariff) {
  editingTariff.value = tariff;
  showModal.value = true;
}

async function onSaved(result) {
  const idx = tariffs.value.findIndex(t => t.tariff_id === result.tariff_id);
  if (idx !== -1) {
    tariffs.value[idx] = result;         // редактирование
  } else {
    tariffs.value.push(result);          // создание — подгружаем счётчик
    await loadTariffCount(result.tariff_id);
  }
}

// --- ДЕЙСТВИЯ ---

async function confirmDelete(id) {
  tariffToDelete.value = id;
  const activeCount = tariffCounts.value[id] ?? 0;

  if (activeCount > 0) {
    // Двухшаговое предупреждение через SweetAlert2
    const result = await Swal.fire({
      icon: 'warning',
      title: 'Есть активные ученики',
      html: `У этого тарифа <b>${activeCount}</b> активных ученик(а/ов).<br>
             Их тарифные периоды продолжат действовать, но новым ученикам тариф будет недоступен.<br><br>
             Всё равно архивировать?`,
      showCancelButton: true,
      confirmButtonText: 'Да, архивировать',
      cancelButtonText: 'Отмена',
      confirmButtonColor: '#dc2626',
      background: '#111827',
      color: '#fff',
    });
    if (result.isConfirmed) {
      await proceedDelete();
    }
  } else {
    // Обычное подтверждение без предупреждения
    showConfirmDelete.value = true;
  }
}

async function proceedDelete() {
  try {
    await deleteTariff(tariffToDelete.value);
    tariffs.value = tariffs.value.filter(t => t.tariff_id !== tariffToDelete.value);
    delete tariffCounts.value[tariffToDelete.value];
    showConfirmDelete.value = false;
    if (showArchive.value) await loadArchive();
    Swal.fire({ icon: 'success', title: 'Тариф архивирован', timer: 1250, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

// --- УТИЛИТЫ ---

function getTariffIcon(type) {
  const icons = {
    starter: '⭐',
    standard: '✨',
    premium: '👑',
    basic: '📚',
    advanced: '🚀',
    enterprise: '💎',
  };
  return icons[type] || '📦';
}

function getTariffTypeLabel(type) {
  const labels = {
    starter: 'Начальный',
    standard: 'Стандартный',
    premium: 'Премиум',
    basic: 'Базовый',
    advanced: 'Продвинутый',
    enterprise: 'Корпоративный',
  };
  return labels[type] || type;
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>