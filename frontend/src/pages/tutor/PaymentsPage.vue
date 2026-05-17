<template>
  <Layout>
    <div class="p-8 space-y-8">

      <!-- ═══════════════════════════════════════════
           ШАПКА + ПЕРЕКЛЮЧАТЕЛЬ ПЕРИОДА
      ════════════════════════════════════════════ -->
      <div class="flex flex-wrap justify-between items-end gap-4">
        <div>
          <h1 class="text-4xl font-black mb-1">🧾 Оплаты</h1>
          <p class="text-gray-400">Финансовая статистика и журнал транзакций</p>
        </div>

        <div class="flex flex-col items-end gap-2">
          <!-- Метка выбранного периода -->
          <p class="text-2xs font-semibold text-gray-500 uppercase tracking-widest">
            {{ periodLabel }}
          </p>

          <!-- Переключатель периода -->
          <div class="flex flex-wrap bg-gray-900 border border-gray-700 rounded-xl p-1 gap-1">
            <button
              v-for="p in PERIODS"
              :key="p.key"
              @click="selectPeriod(p.key)"
              class="px-4 py-2 rounded-lg text-sm font-semibold transition"
              :class="activePeriod === p.key
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/40'
                : 'text-gray-400 hover:text-white'"
            >
              {{ p.label }}
            </button>

            <!-- Разделитель -->
            <div class="w-px bg-gray-700 mx-1" />

            <!-- Произвольный период -->
            <div class="flex items-center gap-2 px-2 py-1">
              <input
                type="date"
                v-model="customStart"
                @change="selectPeriod('custom')"
                class="bg-gray-800 border border-gray-700 rounded-lg px-2 py-1 text-xs text-white focus:border-blue-500 focus:outline-none transition"
                :class="activePeriod === 'custom' ? 'border-blue-500' : ''"
              />
              <span class="text-gray-600 text-xs">—</span>
              <input
                type="date"
                v-model="customEnd"
                @change="selectPeriod('custom')"
                class="bg-gray-800 border border-gray-700 rounded-lg px-2 py-1 text-xs text-white focus:border-blue-500 focus:outline-none transition"
                :class="activePeriod === 'custom' ? 'border-blue-500' : ''"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════
           БЛОК 1 — ФИНАНСОВЫЙ ПУЛЬС
      ════════════════════════════════════════════ -->
      <Transition name="fade" mode="out-in">

        <PaymentsSkeleton v-if="isLoading" />

        <div v-else class="space-y-8">

        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">

        <!-- Доход за период -->
        <div class="relative overflow-hidden bg-gradient-to-br from-blue-900/60 to-blue-950 rounded-2xl border border-blue-700/40 p-5 shadow-xl">
          <div class="absolute -top-4 -right-4 w-24 h-24 bg-blue-500/10 rounded-full blur-xl" />
          <p class="text-xs font-bold text-blue-400 uppercase tracking-widest mb-2">Доход за период</p>
          <p class="text-3xl font-black text-white">{{ fmt(summary.total_income) }} <span class="text-lg text-blue-400">₽</span></p>
          <p class="text-xs text-blue-300/60 mt-2">{{ paymentsList.length }} транзакций</p>
        </div>

        <!-- Средний чек -->
        <div class="relative overflow-hidden bg-gradient-to-br from-purple-900/60 to-purple-950 rounded-2xl border border-purple-700/40 p-5 shadow-xl">
          <div class="absolute -top-4 -right-4 w-24 h-24 bg-purple-500/10 rounded-full blur-xl" />
          <p class="text-xs font-bold text-purple-400 uppercase tracking-widest mb-2">Средний чек</p>
          <p class="text-3xl font-black text-white">{{ fmt(summary.avg_payment) }} <span class="text-lg text-purple-400">₽</span></p>
          <p class="text-xs text-purple-300/60 mt-2">за одну оплату</p>
        </div>

        <!-- Суммарный долг -->
        <div class="relative overflow-hidden rounded-2xl border p-5 shadow-xl"
          :class="summary.total_debt > 0
            ? 'bg-gradient-to-br from-red-900/60 to-red-950 border-red-700/40'
            : 'bg-gradient-to-br from-gray-800 to-gray-900 border-gray-700'"
        >
          <div class="absolute -top-4 -right-4 w-24 h-24 rounded-full blur-xl"
            :class="summary.total_debt > 0 ? 'bg-red-500/10' : 'bg-gray-500/10'" />
          <p class="text-xs font-bold uppercase tracking-widest mb-2"
            :class="summary.total_debt > 0 ? 'text-red-400' : 'text-gray-400'">
            Дебиторка
          </p>
          <p class="text-3xl font-black"
            :class="summary.total_debt > 0 ? 'text-white' : 'text-gray-500'">
            {{ fmt(summary.total_debt) }} <span class="text-lg" :class="summary.total_debt > 0 ? 'text-red-400' : 'text-gray-600'">₽</span>
          </p>
          <p class="text-xs mt-2" :class="summary.total_debt > 0 ? 'text-red-300/60' : 'text-gray-600'">
            {{ summary.total_debt > 0 ? 'Ученики должны' : 'Долгов нет' }}
          </p>
        </div>

        <!-- Баланс предоплат -->
        <div class="relative overflow-hidden bg-gradient-to-br from-emerald-900/60 to-emerald-950 rounded-2xl border border-emerald-700/40 p-5 shadow-xl">
          <div class="absolute -top-4 -right-4 w-24 h-24 bg-emerald-500/10 rounded-full blur-xl" />
          <p class="text-xs font-bold text-emerald-400 uppercase tracking-widest mb-2">Предоплаты</p>
          <p class="text-3xl font-black text-white">{{ fmt(summary.total_prepaid) }} <span class="text-lg text-emerald-400">₽</span></p>
          <p class="text-xs text-emerald-300/60 mt-2">неотработанный остаток</p>
        </div>

      </div>

      <!-- ═══════════════════════════════════════════
           БЛОК 2 — ГРАФИК
      ════════════════════════════════════════════ -->
      <div class="bg-gray-900 rounded-2xl border border-gray-700 p-6 shadow-xl">
        <div class="flex justify-between items-center mb-6">
          <div>
            <p class="text-sm font-bold text-gray-300 uppercase tracking-wider">Динамика доходов</p>
            <p class="text-xs text-gray-500 mt-0.5">{{ chartSubtitle }}</p>
          </div>
          <div class="flex items-center gap-3">
            <!-- Кнопка переключения дни/недели (только для месяца) -->
            <div v-if="activePeriod === 'month'" class="flex bg-gray-800 border border-gray-700 rounded-lg p-0.5 gap-0.5">
              <button
                @click="monthGranularity = 'weeks'"
                class="px-3 py-1 rounded text-xs font-semibold transition"
                :class="monthGranularity === 'weeks' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'"
              >По неделям</button>
              <button
                @click="monthGranularity = 'days'"
                class="px-3 py-1 rounded text-xs font-semibold transition"
                :class="monthGranularity === 'days' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'"
              >По дням</button>
            </div>
            <!-- Кнопка переключения месяцы/недели (только для квартала) -->
            <div v-if="activePeriod === 'quarter'" class="flex bg-gray-800 border border-gray-700 rounded-lg p-0.5 gap-0.5">
              <button
                @click="quarterGranularity = 'months'"
                class="px-3 py-1 rounded text-xs font-semibold transition"
                :class="quarterGranularity === 'months' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'"
              >По месяцам</button>
              <button
                @click="quarterGranularity = 'weeks'"
                class="px-3 py-1 rounded text-xs font-semibold transition"
                :class="quarterGranularity === 'weeks' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'"
              >По неделям</button>
            </div>
            <!-- Кнопка переключения месяц/квартал (только для года) -->
            <div v-if="activePeriod === 'year'" class="flex bg-gray-800 border border-gray-700 rounded-lg p-0.5 gap-0.5">
              <button
                @click="yearGranularity = 'month'"
                class="px-3 py-1 rounded text-xs font-semibold transition"
                :class="yearGranularity === 'month' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'"
              >По месяцам</button>
              <button
                @click="yearGranularity = 'quarter'"
                class="px-3 py-1 rounded text-xs font-semibold transition"
                :class="yearGranularity === 'quarter' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'"
              >По кварталам</button>
            </div>
            <div v-if="chartMaxBar > 0" class="text-right">
              <p class="text-sm text-gray-300">Пик</p>
              <p class="text-sm font-bold text-emerald-400">{{ chartPeakLabel }}</p>
            </div>
          </div>
        </div>

        <!-- Пустое состояние -->
        <div v-if="!chartBars.length" class="flex items-center justify-center h-48 text-gray-600">
          <div class="text-center">
            <div class="text-4xl mb-2">📊</div>
            <p class="text-sm">Нет данных за выбранный период</p>
          </div>
        </div>

        <!-- Гистограмма -->
        <Transition name="chart-fade" mode="out-in">
          <div 
            v-if="chartBars.length" 
            :key="`chart-${activePeriod}-${monthGranularity}-${quarterGranularity}-${yearGranularity}-${customGranularity}`" 
            class="space-y-2">
            <div class="flex items-end gap-1.5 h-50">
              <div
                v-for="bar in chartBars"
                :key="bar.key"
                class="group flex-1 flex flex-col items-center justify-end gap-1 h-full min-w-0"
              >
                <!-- Значение над столбцом (всегда видно если > 0, иначе пусто) -->
                <span
                  class="text-[12px] font-bold whitespace-nowrap transition-opacity"
                  :class="bar.amount > 0 ? 'text-gray-300' : 'text-transparent'"
                >
                  {{ bar.amount > 0 ? fmt(bar.amount) + ' ₽' : '' }}
                </span>
                <!-- Столбец -->
                <div
                  class="w-full rounded-t transition-all duration-500 cursor-default"
                  :class="[
                    bar.amount === chartMaxBar && bar.amount > 0 ? 'bg-emerald-500' : '',
                    bar.amount > 0 && bar.amount !== chartMaxBar ? 'bg-blue-600 group-hover:bg-blue-500' : '',
                    bar.amount === 0 ? 'bg-gray-800' : '',
                  ]"
                  :style="{
                    height: chartMaxBar > 0 ? Math.max(bar.amount / chartMaxBar * 100, bar.amount > 0 ? 2 : 0) + '%' : '0%',
                    minHeight: bar.amount > 0 ? '6px' : '2px',
                  }"
                />
              </div>
            </div>
            <!-- Подписи оси X -->
            <div class="flex gap-1.5">
              <div
                v-for="bar in chartBars"
                :key="bar.key"
                class="flex-1 text-center text-[12px] leading-tight min-w-0"
                :class="bar.isToday || bar.isCurrent ? 'text-blue-300 font-bold' : bar.amount > 0 ? 'text-gray-300' : 'text-gray-600'"
              >
                {{ bar.label }}
              </div>
            </div>
          </div>
        </Transition>
      </div>

      <!-- ═══════════════════════════════════════════
           БЛОК 3 — ДОЛЖНИКИ
      ════════════════════════════════════════════ -->
      <div v-if="debtors.length > 0" class="bg-gray-900 rounded-2xl border border-red-900/50 p-6 shadow-xl">
        <div class="flex items-center gap-3 mb-4">
          <div class="w-2.5 h-2.5 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.8)] animate-pulse" />
          <p class="text-sm font-bold text-red-400 uppercase tracking-wider">Должники</p>
          <span class="px-2 py-0.5 rounded-full text-xs font-black bg-red-900/50 text-red-300 border border-red-700/50">
            {{ debtors.length }}
          </span>
        </div>

        <div class="space-y-2">
          <div
            v-for="debtor in debtors"
            :key="debtor.child_id"
            class="flex items-center justify-between px-4 py-3 bg-gray-800/80 rounded-xl border border-gray-700 hover:border-red-800/50 transition group"
          >
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-red-900/40 border border-red-700/40 flex items-center justify-center text-xs font-black text-red-400">
                {{ debtor.last_name[0] }}
              </div>
              <div>
                <p class="font-semibold text-white text-sm">{{ debtor.last_name }} {{ debtor.first_name }}</p>
                <p class="text-xs text-gray-500">{{ debtor.school_class }} класс</p>
              </div>
            </div>
            <div class="flex items-center gap-4">
              <p class="text-lg font-black text-red-400">{{ fmt(debtor.debt) }} ₽</p>
              <button
                @click="goToChild(debtor.child_id)"
                class="opacity-0 group-hover:opacity-100 transition px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded-lg text-xs text-gray-300 font-semibold"
              >
                Открыть →
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Пустой статус если должников нет -->
      <div v-else class="bg-gray-900 rounded-2xl border border-gray-700 p-8 shadow-xl">
        <div class="flex flex-col items-center justify-center text-center">
          <div class="text-5xl mb-4">✨</div>
          <p class="text-sm font-bold text-gray-400 uppercase tracking-wider mb-1">Отличные новости</p>
          <p class="text-gray-500">Все ученики рассчиталась. Долгов нет</p>
        </div>
      </div>

      <!-- ═══════════════════════════════════════════
           БЛОК 4 — ЖУРНАЛ ПЛАТЕЖЕЙ
      ════════════════════════════════════════════ -->
      <div class="bg-gray-900 rounded-2xl border border-gray-700 shadow-xl overflow-hidden">
        <div class="flex flex-wrap justify-between items-center gap-4 p-6 border-b border-gray-700">
          <div>
            <p class="text-sm font-bold text-gray-400 uppercase tracking-wider">Журнал платежей</p>
            <p class="text-xs text-gray-600 mt-0.5">{{ filteredPayments.length }} записей</p>
          </div>

          <!-- Поиск -->
          <div class="flex gap-3 items-center flex-wrap">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Поиск по имени..."
              class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none w-48 transition"
            />
            <!-- Фильтр по способу оплаты -->
            <select
              v-model="filterMethod"
              class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none transition"
            >
              <option value="">Все способы</option>
              <option value="cash">💵 Наличные</option>
              <option value="card">💳 Карта</option>
              <option value="sbp">⚡ СБП</option>
              <option value="bank_transfer">🏦 Перевод</option>
              <option value="online_payment">🌐 Онлайн</option>
              <option value="qr_code">📱 QR-код</option>
            </select>
            <!-- Фильтр по сумме: от -->
            <input
              v-model="filterMinAmount"
              type="number"
              placeholder="От суммы"
              class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none w-32 transition"
            />
            <!-- Фильтр по сумме: до -->
            <input
              v-model="filterMaxAmount"
              type="number"
              placeholder="До суммы"
              class="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none w-32 transition"
            />
          </div>
        </div>

        <!-- Таблица -->
        <div v-if="filteredPayments.length > 0" class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="text-xs font-bold text-gray-500 uppercase tracking-wider border-b border-gray-800">
                <th class="px-6 py-3 text-left">Дата</th>
                <th class="px-6 py-3 text-left">Ученик</th>
                <th class="px-6 py-3 text-left">Родитель</th>
                <th class="px-6 py-3 text-left">Способ</th>
                <th class="px-6 py-3 text-right">Сумма</th>
                <th class="px-6 py-3 text-right"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="payment in paginatedPayments"
                :key="payment.payment_id"
                class="border-b border-gray-800/60 hover:bg-gray-800/40 transition group"
              >
                <td class="px-6 py-4 text-sm text-gray-400 whitespace-nowrap">
                  {{ formatDate(payment.payment_date) }}
                </td>
                <td class="px-6 py-4">
                  <button
                    @click="goToChild(payment.child_id)"
                    class="text-sm font-semibold text-white hover:text-blue-400 transition text-left"
                  >
                    {{ getChildName(payment.child_id) }}
                  </button>
                </td>
                <td class="px-6 py-4 text-sm text-gray-400">
                  {{ getParentName(payment.parent_id) }}
                </td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 rounded-lg text-xs font-semibold bg-gray-800 text-gray-300 border border-gray-700">
                    {{ methodLabel(payment.method) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-right">
                  <span class="text-lg font-black text-emerald-400">+{{ fmt(payment.amount) }} ₽</span>
                </td>
                <td class="px-6 py-4 text-right">
                  <button
                    @click="deletePaymentById(payment.payment_id)"
                    class="opacity-0 group-hover:opacity-100 transition px-2 py-1 rounded-lg bg-red-900/30 hover:bg-red-900/60 text-red-400 text-xs"
                  >
                    🗑
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Пусто -->
        <div v-else class="text-center py-16 text-gray-600">
          <div class="text-5xl mb-3">📭</div>
          <p class="text-sm">Платежей за выбранный период нет</p>
        </div>

        <!-- Пагинация -->
        <div
          v-if="totalPages > 1"
          class="flex items-center justify-between px-6 py-4 border-t border-gray-800"
        >
          <p class="text-xs text-gray-500">
            Показано {{ (currentPage - 1) * PAGE_SIZE + 1 }}–{{ Math.min(currentPage * PAGE_SIZE, filteredPayments.length) }}
            из {{ filteredPayments.length }}
          </p>
          <div class="flex gap-2">
            <button
              @click="currentPage--"
              :disabled="currentPage === 1"
              class="px-3 py-1.5 rounded-lg bg-gray-800 text-gray-400 text-sm disabled:opacity-30 hover:bg-gray-700 transition"
            >
              ←
            </button>
            <button
              v-for="page in totalPages"
              :key="page"
              @click="currentPage = page"
              class="px-3 py-1.5 rounded-lg text-sm transition"
              :class="currentPage === page ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'"
            >
              {{ page }}
            </button>
            <button
              @click="currentPage++"
              :disabled="currentPage === totalPages"
              class="px-3 py-1.5 rounded-lg bg-gray-800 text-gray-400 text-sm disabled:opacity-30 hover:bg-gray-700 transition"
            >
              →
            </button>
          </div>
        </div>
      </div>

    </div> <!-- /v-else -->

      </Transition>

    </div>
  </Layout>
</template>

<script setup>
// --- ИМПОРТЫ ---
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import Layout from '../../components/Layout.vue';
import PaymentsSkeleton from '../../components/skeletons/PaymentsSkeleton.vue';
import {
  getPaymentsSummary,
  getPayments,
  getChildren,
  getParents,
  deletePayment,
  getDebtors,
} from '../../api/client.js';
import Swal from 'sweetalert2';

const router = useRouter();

// --- КОНСТАНТЫ ---

const PAGE_SIZE = 20;

const PERIODS = [
  { key: 'week',    label: 'Неделя' },
  { key: 'month',   label: 'Месяц' },
  { key: 'quarter', label: 'Квартал' },
  { key: 'year',    label: 'Год' },
];

const MONTH_NAMES = ['Янв','Фев','Мар','Апр','Май','Июн','Июл','Авг','Сен','Окт','Ноя','Дек'];
const DAY_NAMES   = ['Вс','Пн','Вт','Ср','Чт','Пт','Сб'];

// --- СОСТОЯНИЕ ---

const activePeriod  = ref('month');
const customStart   = ref('');
const customEnd     = ref('');

const summary      = ref({ total_income: 0, total_debt: 0, total_prepaid: 0, avg_payment: 0, payments_by_period: [] });
const paymentsList = ref([]);
const debtors      = ref([]);
const children     = ref([]);
const parents      = ref([]);

const isLoading = ref(true);

const searchQuery     = ref('');
const filterMethod    = ref('');
const filterMinAmount = ref('');
const filterMaxAmount = ref('');
const currentPage     = ref(1);

const customGranularity  = ref('auto');   // 'auto' | 'days' | 'weeks' | 'months'
const monthGranularity   = ref('weeks');  // 'days' | 'weeks'
const quarterGranularity = ref('months'); // 'weeks' | 'months'
const yearGranularity    = ref('month');  // 'month' | 'quarter'

// --- ЗАГРУЗКА ---

function getPeriodDates(key) {
  const now   = new Date();
  const today = now.toISOString().split('T')[0];

  if (key === 'week') {
    const d = new Date(now);
    d.setDate(d.getDate() - 7);
    return { start: d.toISOString().split('T')[0], end: today };
  }
  if (key === 'month') {
    return { start: `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-01`, end: today };
  }
  if (key === 'quarter') {
    const q     = Math.floor(now.getMonth() / 3);
    const start = new Date(now.getFullYear(), q * 3, 1);
    return { start: start.toISOString().split('T')[0], end: today };
  }
  if (key === 'year') {
    return { start: `${now.getFullYear()}-01-01`, end: today };
  }
  if (key === 'custom') {
    return { start: customStart.value || '2020-01-01', end: customEnd.value || today };
  }
  return { start: '2020-01-01', end: today };
}

async function loadAll() {
  const { start, end } = getPeriodDates(activePeriod.value);
  isLoading.value = true;

  try {
    const [summaryData, paymentsData, debtorsData] = await Promise.all([
      getPaymentsSummary(start, end),
      getPayments(0, 1000, start, end),
      getDebtors(),
    ]);
    summary.value      = summaryData;
    paymentsList.value = paymentsData;
    debtors.value      = debtorsData;
    currentPage.value  = 1;
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка загрузки', text: e.message, background: '#111827', color: '#fff' });
  } finally {
    isLoading.value = false;
  }
}

async function loadLookups() {
  try {
    const [ch, pa] = await Promise.all([getChildren(), getParents()]);
    children.value = ch;
    parents.value  = pa;
  } catch (e) {
    console.error('Ошибка загрузки справочников:', e);
  }
}

onMounted(async () => {
  await loadLookups();
  await loadAll();
});

// --- МОДАЛКА / UI-логика ---

function selectPeriod(key) {
  activePeriod.value = key;
  if (key !== 'custom') {
    customStart.value = '';
    customEnd.value   = '';
    loadAll();
  } else if (customStart.value && customEnd.value) {
    loadAll();
  }
}

// При изменении произвольных дат — перезагрузить
watch([customStart, customEnd], () => {
  if (activePeriod.value === 'custom' && customStart.value && customEnd.value) {
    loadAll();
  }
});

// Сброс пагинации при изменении фильтров
watch([searchQuery, filterMethod, filterMinAmount, filterMaxAmount], () => {
  currentPage.value = 1;
});

// --- ВЫЧИСЛЯЕМЫЕ ---

// Справочники
const childMap  = computed(() => Object.fromEntries(children.value.map(c => [c.child_id,  c])));
const parentMap = computed(() => Object.fromEntries(parents.value.map(p => [p.parent_id, p])));

function getChildName(id) {
  const c = childMap.value[id];
  return c ? `${c.last_name} ${c.first_name}` : '—';
}

function getParentName(id) {
  const p = parentMap.value[id];
  return p ? `${p.last_name} ${p.first_name}` : '—';
}

// Человекочитаемая метка выбранного периода
const periodLabel = computed(() => {
  const now = new Date();
  if (activePeriod.value === 'week') {
    const mon = new Date(now); mon.setDate(now.getDate() - ((now.getDay() + 6) % 7));
    const sun = new Date(mon); sun.setDate(mon.getDate() + 6);
    return `${mon.getDate()} ${MONTH_NAMES[mon.getMonth()]} — ${sun.getDate()} ${MONTH_NAMES[sun.getMonth()]} ${sun.getFullYear()}`;
  }
  if (activePeriod.value === 'month') {
    return `${MONTH_NAMES[now.getMonth()]} ${now.getFullYear()}`;
  }
  if (activePeriod.value === 'quarter') {
    const q = Math.floor(now.getMonth() / 3) + 1;
    return `${q}-й квартал ${now.getFullYear()}`;
  }
  if (activePeriod.value === 'year') {
    return `${now.getFullYear()} год`;
  }
  if (activePeriod.value === 'custom' && customStart.value && customEnd.value) {
    const s = new Date(customStart.value), e = new Date(customEnd.value);
    return `${s.getDate()} ${MONTH_NAMES[s.getMonth()]} ${s.getFullYear()} — ${e.getDate()} ${MONTH_NAMES[e.getMonth()]} ${e.getFullYear()}`;
  }
  return 'Произвольный период';
});

// Подзаголовок графика
const chartSubtitle = computed(() => {
  const map = {
    week:    'По дням текущей недели',
    month:   monthGranularity.value === 'days' ? 'По дням текущего месяца' : 'По неделям текущего месяца',
    quarter: quarterGranularity.value === 'months' ? 'По месяцам текущего квартала' : 'По неделям текущего квартала',
    year:    yearGranularity.value === 'quarter' ? 'По кварталам года' : 'По месяцам года',
    custom:  getCustomChartSubtitle(),
  };
  return map[activePeriod.value] || '';
});

function getCustomChartSubtitle() {
  if (!customStart.value || !customEnd.value) return '';
  const start    = new Date(customStart.value);
  const end      = new Date(customEnd.value);
  const diffDays = Math.round((end - start) / 86400000);

  if (customGranularity.value === 'auto') {
    if (diffDays <= 31)  return 'По дням выбранного периода';
    if (diffDays <= 89)  return 'По неделям выбранного периода';
    if (diffDays <= 365) return 'По месяцам выбранного периода';
    return 'По кварталам выбранного периода';
  }

  const map = { days: 'По дням', weeks: 'По неделям', months: 'По месяцам' };
  return (map[customGranularity.value] || '') + ' выбранного периода';
}

// Фильтрация журнала
const filteredPayments = computed(() => {
  let list = paymentsList.value;
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(p =>
      getChildName(p.child_id).toLowerCase().includes(q) ||
      getParentName(p.parent_id).toLowerCase().includes(q)
    );
  }
  if (filterMethod.value) {
    list = list.filter(p => p.method === filterMethod.value);
  }
  if (filterMinAmount.value !== '') {
    const minVal = parseFloat(filterMinAmount.value);
    if (!isNaN(minVal)) list = list.filter(p => Number(p.amount) >= minVal);
  }
  if (filterMaxAmount.value !== '') {
    const maxVal = parseFloat(filterMaxAmount.value);
    if (!isNaN(maxVal)) list = list.filter(p => Number(p.amount) <= maxVal);
  }
  return list;
});

// Пагинация
const totalPages       = computed(() => Math.ceil(filteredPayments.value.length / PAGE_SIZE));
const paginatedPayments = computed(() =>
  filteredPayments.value.slice((currentPage.value - 1) * PAGE_SIZE, currentPage.value * PAGE_SIZE)
);

// График — строит бакеты из paymentsList на фронте
const chartBars = computed(() => {
  const payments = paymentsList.value;
  const now      = new Date();

  // Суммируем платежи по ключу бакета
  const sumByKey = (keyFn) => {
    const map = {};
    for (const p of payments) {
      const k = keyFn(new Date(p.payment_date));
      if (k !== null) map[k] = (map[k] || 0) + Number(p.amount);
    }
    return map;
  };

  // ── НЕДЕЛЯ: 7 дней (Пн–Вс текущей недели) ──────────────────
  if (activePeriod.value === 'week') {
    const mon = new Date(now);
    mon.setDate(now.getDate() - ((now.getDay() + 6) % 7));
    mon.setHours(0, 0, 0, 0);

    const days = Array.from({ length: 7 }, (_, i) => {
      const d = new Date(mon); d.setDate(mon.getDate() + i);
      return d;
    });

    const sums = sumByKey(d => {
      const key = d.toISOString().split('T')[0];
      return days.some(day => day.toISOString().split('T')[0] === key) ? key : null;
    });

    const todayStr = now.toISOString().split('T')[0];
    return days.map(d => {
      const key = d.toISOString().split('T')[0];
      return {
        key,
        amount:    sums[key] || 0,
        label:     `${DAY_NAMES[d.getDay()]}\n${d.getDate()}`,
        isToday:   key === todayStr,
        isCurrent: false,
      };
    });
  }

  // ── МЕСЯЦ: по дням или неделям ────────────────────────────────
  if (activePeriod.value === 'month') {
    const year = now.getFullYear(), month = now.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay  = new Date(year, month + 1, 0);

    if (monthGranularity.value === 'days') {
      const days = [];
      const cur = new Date(firstDay);
      while (cur <= lastDay) {
        days.push(new Date(cur));
        cur.setDate(cur.getDate() + 1);
      }

      const sums = sumByKey(d => {
        if (d.getMonth() !== month || d.getFullYear() !== year) return null;
        return d.toISOString().split('T')[0];
      });

      const todayStr = now.toISOString().split('T')[0];
      return days.map(d => {
        const k = d.toISOString().split('T')[0];
        return {
          key:       k,
          amount:    sums[k] || 0,
          label:     `${d.getDate()}`,
          isToday:   k === todayStr,
          isCurrent: false,
        };
      });
    } else {
      // По неделям (Пн–Вс внутри месяца)
      const weeks = [];
      let cur = new Date(firstDay);
      const dow = (cur.getDay() + 6) % 7;
      cur.setDate(cur.getDate() - dow);

      while (cur <= lastDay) {
        const wStart = new Date(Math.max(cur, firstDay));
        const wEnd   = new Date(cur); wEnd.setDate(cur.getDate() + 6);
        const wEndClamped = new Date(Math.min(wEnd, lastDay));
        weeks.push({ start: new Date(wStart), end: wEndClamped });
        cur.setDate(cur.getDate() + 7);
      }

      const sums = sumByKey(d => {
        if (d.getMonth() !== month || d.getFullYear() !== year) return null;
        const dayStr = d.toISOString().split('T')[0];
        const idx = weeks.findIndex(w =>
          dayStr >= w.start.toISOString().split('T')[0] &&
          dayStr <= w.end.toISOString().split('T')[0]
        );
        return idx >= 0 ? String(idx) : null;
      });

      const todayStr = now.toISOString().split('T')[0];
      return weeks.map((w, i) => {
        const wStartStr = w.start.toISOString().split('T')[0];
        const wEndStr   = w.end.toISOString().split('T')[0];
        const isCurrent = todayStr >= wStartStr && todayStr <= wEndStr;
        return {
          key:       String(i),
          amount:    sums[String(i)] || 0,
          label:     `${w.start.getDate()}–${w.end.getDate()}`,
          isToday:   false,
          isCurrent,
        };
      });
    }
  }

  // ── КВАРТАЛ: по месяцам или неделям ───────────────────────────
  if (activePeriod.value === 'quarter') {
    const year   = now.getFullYear();
    const q      = Math.floor(now.getMonth() / 3);
    const months = [q * 3, q * 3 + 1, q * 3 + 2];

    if (quarterGranularity.value === 'months') {
      const sums = sumByKey(d => {
        if (d.getFullYear() !== year) return null;
        return months.includes(d.getMonth()) ? String(d.getMonth()) : null;
      });

      return months.map(m => ({
        key:       String(m),
        amount:    sums[String(m)] || 0,
        label:     MONTH_NAMES[m],
        isToday:   false,
        isCurrent: now.getMonth() === m && now.getFullYear() === year,
      }));
    } else {
      // По неделям квартала
      const firstMonth = months[0];
      const lastMonth  = months[2];
      const firstDay   = new Date(year, firstMonth, 1);
      const lastDay    = new Date(year, lastMonth + 1, 0);

      const weeks = [];
      let cur = new Date(firstDay);
      const dow = (cur.getDay() + 6) % 7;
      cur.setDate(cur.getDate() - dow);

      while (cur <= lastDay) {
        const wStart      = new Date(Math.max(cur, firstDay));
        const wEnd        = new Date(cur); wEnd.setDate(cur.getDate() + 6);
        const wEndClamped = new Date(Math.min(wEnd, lastDay));
        weeks.push({ start: new Date(wStart), end: wEndClamped });
        cur.setDate(cur.getDate() + 7);
      }

      const sums = sumByKey(d => {
        if (d.getFullYear() !== year) return null;
        const dayStr = d.toISOString().split('T')[0];
        const idx = weeks.findIndex(w =>
          dayStr >= w.start.toISOString().split('T')[0] &&
          dayStr <= w.end.toISOString().split('T')[0]
        );
        return idx >= 0 ? String(idx) : null;
      });

      const todayStr = now.toISOString().split('T')[0];
      return weeks.map((w, i) => {
        const wStartStr = w.start.toISOString().split('T')[0];
        const wEndStr   = w.end.toISOString().split('T')[0];
        const isCurrent = todayStr >= wStartStr && todayStr <= wEndStr;
        return {
          key:       String(i),
          amount:    sums[String(i)] || 0,
          label:     `${w.start.getDate()}.${String(w.start.getMonth()+1).padStart(2,'0')}`,
          isToday:   false,
          isCurrent,
        };
      });
    }
  }

  // ── ГОД: по месяцам или кварталам ──────────────────────────
  if (activePeriod.value === 'year') {
    const year = now.getFullYear();

    if (yearGranularity.value === 'quarter') {
      const sums = sumByKey(d => {
        if (d.getFullYear() !== year) return null;
        return String(Math.floor(d.getMonth() / 3));
      });
      return [0,1,2,3].map(q => ({
        key:       String(q),
        amount:    sums[String(q)] || 0,
        label:     `Q${q + 1}`,
        isToday:   false,
        isCurrent: Math.floor(now.getMonth() / 3) === q && now.getFullYear() === year,
      }));
    } else {
      const sums = sumByKey(d => {
        if (d.getFullYear() !== year) return null;
        return String(d.getMonth());
      });
      return Array.from({ length: 12 }, (_, m) => ({
        key:       String(m),
        amount:    sums[String(m)] || 0,
        label:     MONTH_NAMES[m],
        isToday:   false,
        isCurrent: now.getMonth() === m && now.getFullYear() === year,
      }));
    }
  }

  // ── ПРОИЗВОЛЬНЫЙ: адаптивная гранулярность ──────────────────
  if (activePeriod.value === 'custom' && customStart.value && customEnd.value) {
    const start    = new Date(customStart.value);
    const end      = new Date(customEnd.value);
    const diffDays = Math.round((end - start) / 86400000);

    let granularity = customGranularity.value;
    if (granularity === 'auto') {
      if (diffDays <= 31)       granularity = 'days';
      else if (diffDays <= 89)  granularity = 'weeks';
      else if (diffDays <= 365) granularity = 'months';
      else                      granularity = 'quarters';
    }

    // По дням
    if (granularity === 'days') {
      const days = [];
      const cur2 = new Date(start);
      while (cur2 <= end) { days.push(new Date(cur2)); cur2.setDate(cur2.getDate() + 1); }

      const sums = sumByKey(d => {
        const k = d.toISOString().split('T')[0];
        return days.some(day => day.toISOString().split('T')[0] === k) ? k : null;
      });

      const todayStr = now.toISOString().split('T')[0];
      return days.map(d => {
        const k = d.toISOString().split('T')[0];
        return { key: k, amount: sums[k] || 0, label: `${d.getDate()}`, isToday: k === todayStr, isCurrent: false };
      });
    }

    // По неделям
    if (granularity === 'weeks') {
      const weeks = [];
      const cur2  = new Date(start);
      const dow   = (cur2.getDay() + 6) % 7;
      cur2.setDate(cur2.getDate() - dow);
      while (cur2 <= end) {
        const ws = new Date(Math.max(cur2, start));
        const we = new Date(cur2); we.setDate(cur2.getDate() + 6);
        weeks.push({ start: new Date(ws), end: new Date(Math.min(we, end)) });
        cur2.setDate(cur2.getDate() + 7);
      }

      const sums = sumByKey(d => {
        const k   = d.toISOString().split('T')[0];
        const idx = weeks.findIndex(w =>
          k >= w.start.toISOString().split('T')[0] && k <= w.end.toISOString().split('T')[0]
        );
        return idx >= 0 ? String(idx) : null;
      });

      return weeks.map((w, i) => ({
        key:       String(i),
        amount:    sums[String(i)] || 0,
        label:     `${w.start.getDate()}.${String(w.start.getMonth()+1).padStart(2,'0')}`,
        isToday:   false,
        isCurrent: false,
      }));
    }

    // По месяцам
    if (granularity === 'months') {
      const months = {};
      const cur2   = new Date(start);
      while (cur2 <= end) {
        const k = `${cur2.getFullYear()}-${String(cur2.getMonth() + 1).padStart(2, '0')}`;
        if (!months[k]) months[k] = { label: `${MONTH_NAMES[cur2.getMonth()]} ${cur2.getFullYear()}`, start: new Date(cur2) };
        cur2.setMonth(cur2.getMonth() + 1);
      }

      const monthKeys = Object.keys(months).sort();
      const sums = sumByKey(d => {
        const k = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
        return monthKeys.includes(k) ? k : null;
      });

      return monthKeys.map(k => ({
        key:       k,
        amount:    sums[k] || 0,
        label:     months[k].label,
        isToday:   false,
        isCurrent: false,
      }));
    }

    // По кварталам
    if (granularity === 'quarters') {
      const quarters = {};
      const cur2     = new Date(start);
      while (cur2 <= end) {
        const q = Math.floor(cur2.getMonth() / 3) + 1;
        const k = `${cur2.getFullYear()}-Q${q}`;
        if (!quarters[k]) quarters[k] = true;
        cur2.setMonth(cur2.getMonth() + 3);
      }

      const quarterKeys = Object.keys(quarters).sort();
      const sums = sumByKey(d => {
        const q = Math.floor(d.getMonth() / 3) + 1;
        const k = `${d.getFullYear()}-Q${q}`;
        return quarterKeys.includes(k) ? k : null;
      });

      return quarterKeys.map(k => ({
        key:       k,
        amount:    sums[k] || 0,
        label:     k,
        isToday:   false,
        isCurrent: false,
      }));
    }
  }

  return [];
});

const chartMaxBar = computed(() => Math.max(0, ...chartBars.value.map(b => b.amount)));

const chartPeakLabel = computed(() => {
  if (!chartBars.value.length || chartMaxBar.value === 0) return '—';
  const peak = chartBars.value.reduce((a, b) => b.amount > a.amount ? b : a, chartBars.value[0]);
  return `${peak.label.replace('\n', ' ')} — ${fmt(peak.amount)} ₽`;
});

// --- ДЕЙСТВИЯ ---

async function deletePaymentById(paymentId) {
  const result = await Swal.fire({
    icon: 'warning',
    title: 'Удалить платёж?',
    text: 'Это действие нельзя отменить',
    showCancelButton: true,
    confirmButtonText: 'Удалить',
    cancelButtonText: 'Отмена',
    confirmButtonColor: '#dc2626',
    background: '#111827',
    color: '#fff',
  });
  if (!result.isConfirmed) return;
  try {
    await deletePayment(paymentId);
    await loadAll();
    Swal.fire({ icon: 'success', title: 'Платёж удалён', timer: 1200, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

// --- УТИЛИТЫ ---

function goToChild(childId) {
  router.push(`/children/${childId}`);
}

function fmt(n) {
  if (n === null || n === undefined) return '—';
  return Number(n).toLocaleString('ru-RU', { maximumFractionDigits: 0 });
}

function formatDate(d) {
  return new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short', year: 'numeric' });
}

function methodLabel(method) {
  const map = {
    cash:           '💵 Наличные',
    card:           '💳 Карта',
    sbp:            '⚡ СБП',
    bank_transfer:  '🏦 Перевод',
    online_payment: '🌐 Онлайн',
    qr_code:        '📱 QR-код',
  };
  return map[method] || method;
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
}

.chart-fade-enter-active,
.chart-fade-leave-active {
  transition: opacity 0.3s ease;
}

.chart-fade-enter-from,
.chart-fade-leave-to {
  opacity: 0;
}
</style>