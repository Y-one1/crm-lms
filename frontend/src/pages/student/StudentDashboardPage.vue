<template>
  <div class="p-8">

    <Transition name="fade" mode="out-in">
      <DashboardHeaderSkeleton v-if="loadingHeader" key="header-skel" />
      <div v-else key="header-content">
        <!-- Шапка приветствия -->
        <div class="mb-8 flex justify-between items-start">
          <div>
            <h1 class="text-4xl font-black mb-2">
              👋 Привет, {{ student?.first_name }}!
            </h1>
            <p class="text-gray-400">Твой личный кабинет ученика</p>
          </div>
          <button
            @click="handleLogout"
            class="px-4 py-2 bg-red-900/30 hover:bg-red-900/60 border border-red-500/30 text-red-400 rounded-lg transition text-sm font-semibold"
          >
            🚪 Выход
          </button>
        </div>

        <!-- Быстрая статистика -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <!-- Следующий урок -->
          <div class="bg-gradient-to-br from-blue-900/40 to-blue-800/20 rounded-xl border border-blue-500/30 p-4">
            <p class="text-xs uppercase tracking-widest text-blue-400 font-bold mb-2">
              📅 Следующий урок
            </p>
            <p v-if="nextLesson" class="text-lg font-black text-white">
              {{ formatTime(nextLesson.lesson_datetime) }}
            </p>
            <p v-else class="text-lg font-black text-gray-500">Не запланирован</p>
            <p v-if="nextLesson" class="text-xs text-gray-400 mt-1">
              {{ formatDateShort(nextLesson.lesson_datetime) }}
            </p>
          </div>

          <!-- Осталось уроков -->
          <div class="bg-gradient-to-br from-emerald-900/40 to-emerald-800/20 rounded-xl border border-emerald-500/30 p-4">
            <p class="text-xs uppercase tracking-widest text-emerald-400 font-bold mb-2">
              📚 Осталось уроков
            </p>
            <p v-if="activeTariff" class="text-3xl font-black text-emerald-400">
              {{ activeTariff.lessons_rest }}
            </p>
            <p v-else class="text-3xl font-black text-gray-500">—</p>
            <p v-if="activeTariff" class="text-xs text-gray-400 mt-1">
              из {{ tariffInfo?.num_of_lessons || 0 }}
            </p>
          </div>

          <!-- Задолженность -->
          <div
            :class="[
              'rounded-xl border p-4',
              activeTariff?.current_debt > 0
                ? 'bg-gradient-to-br from-red-900/40 to-red-800/20 border-red-500/30'
                : 'bg-gradient-to-br from-emerald-900/40 to-emerald-800/20 border-emerald-500/30',
            ]"
          >
            <p
              :class="[
                'text-xs uppercase tracking-widest font-bold mb-2',
                activeTariff?.current_debt > 0
                  ? 'text-red-400'
                  : 'text-emerald-400',
              ]"
            >
              💳 Задолженность
            </p>
            <p
              :class="[
                'text-3xl font-black',
                activeTariff?.current_debt > 0
                  ? 'text-red-400'
                  : 'text-emerald-400',
              ]"
            >
              {{ activeTariff?.current_debt ?? 0 }} ₽
            </p>
          </div>

          <!-- Тариф -->
          <div class="bg-gradient-to-br from-purple-900/40 to-purple-800/20 rounded-xl border border-purple-500/30 p-4">
            <p class="text-xs uppercase tracking-widest text-purple-400 font-bold mb-2">
              ✨ Твой тариф
            </p>
            <p v-if="activeTariff" class="text-lg font-black text-purple-300">
              {{ activeTariff.tariff_name }}
            </p>
            <p v-else class="text-lg font-black text-gray-500">Не подключен</p>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Вкладки -->
    <div class="flex gap-2 mb-6 border-b border-gray-700 overflow-x-auto">
      <button
        v-for="tab in tabs"
        :key="tab"
        @click="activeTab = tab"
        class="px-4 py-3 font-semibold transition border-b-2 whitespace-nowrap"
        :class="
          activeTab === tab
            ? 'text-blue-400 border-blue-500'
            : 'text-gray-400 border-transparent hover:text-gray-300'
        "
      >
        {{ tabLabels[tab] }}
      </button>
    </div>

    <!-- ===== ВКЛАДКА: РАСПИСАНИЕ ===== -->
    <div v-if="activeTab === 'schedule'">
      <Transition name="fade" mode="out-in">
        <ScheduleSkeleton v-if="!scheduleReady" key="skel" />
        <div v-else key="content">
          <WeeklyCalendar
            :lessons="childLessons"
            @lesson-click="editLesson"
          />
        </div>
      </Transition>
    </div>

    <!-- ===== ВКЛАДКА: ТАРИФ ===== -->
    <div v-if="activeTab === 'tariff'">
      <Transition name="fade" mode="out-in">
        <TariffChildSkeleton v-if="loadingTab === 'tariff'" key="skel" />

        <div v-else key="content">
          <div v-if="activeTariff" class="space-y-6">
            <!-- Основная карточка тарифа -->
            <div
              class="bg-gradient-to-br from-gray-800 to-gray-900 rounded-2xl p-6 shadow-xl border border-emerald-500/30"
            >
              <div class="flex justify-between items-start mb-6">
                <div>
                  <p
                    class="text-xs uppercase tracking-widest text-emerald-400 font-bold mb-1"
                  >
                    ✨ Твой текущий тариф
                  </p>
                  <h2 class="text-3xl font-black text-white">
                    {{ activeTariff.tariff_name }}
                  </h2>
                </div>
                <span class="text-4xl">{{ getTariffIcon(tariffInfo?.tariff_type) }}</span>
              </div>

              <!-- Три колонки информации -->
              <div class="grid grid-cols-3 gap-4 mb-6">
                <!-- Осталось уроков -->
                <div class="bg-gray-900/60 rounded-xl p-4 border border-gray-700">
                  <p class="text-xs text-gray-500 uppercase mb-1">Осталось уроков</p>
                  <p class="text-3xl font-black text-blue-400">
                    {{ activeTariff.lessons_rest }}
                  </p>
                  <p class="text-xs text-gray-600 mt-1">
                    из {{ tariffInfo?.num_of_lessons || 0 }}
                  </p>
                </div>

                <!-- Задолженность -->
                <div class="bg-gray-900/60 rounded-xl p-4 border border-gray-700">
                  <p class="text-xs text-gray-500 uppercase mb-1">Задолженность</p>
                  <p
                    class="text-3xl font-black"
                    :class="
                      activeTariff.current_debt > 0
                        ? 'text-red-400'
                        : 'text-emerald-400'
                    "
                  >
                    {{ activeTariff.current_debt }} ₽
                  </p>
                </div>

                <!-- Цена одного урока -->
                <div class="bg-gray-900/60 rounded-xl p-4 border border-gray-700">
                  <p class="text-xs text-gray-500 uppercase mb-1">Цена за урок</p>
                  <p class="text-3xl font-black text-gray-300">
                    {{
                      tariffInfo
                        ? (tariffInfo.price / tariffInfo.num_of_lessons).toFixed(0)
                        : 0
                    }}
                    ₽
                  </p>
                </div>
              </div>

              <!-- Прогресс-бар -->
              <div class="mb-6">
                <div class="flex justify-between text-xs text-gray-500 mb-1">
                  <span>Прогресс по пакету</span>
                  <span
                    >{{
                      (tariffInfo?.num_of_lessons || 0) -
                      activeTariff.lessons_rest
                    }}
                    / {{ tariffInfo?.num_of_lessons || 0 }} уроков</span
                  >
                </div>
                <div class="w-full bg-gray-700 rounded-full h-3">
                  <div
                    class="h-3 rounded-full bg-gradient-to-r from-emerald-500 to-emerald-400 transition-all"
                    :style="{
                      width:
                        ((
                          ((tariffInfo?.num_of_lessons || 0) -
                            activeTariff.lessons_rest) /
                          (tariffInfo?.num_of_lessons || 1)
                        ) *
                          100 +
                        '%') || '0%',
                    }"
                  ></div>
                </div>
              </div>

              <!-- Описание тарифа -->
              <div class="bg-gray-900/60 rounded-xl p-4 border border-gray-700">
                <p class="text-sm font-bold text-gray-300 uppercase mb-2">
                  📋 Информация о тарифе
                </p>
                <div class="space-y-2 text-sm text-gray-400">
                  <p>
                    <span class="text-gray-300 font-semibold"
                      >Тип:</span
                    >
                    {{ tariffInfo?.tariff_type || '—' }}
                  </p>
                  <p>
                    <span class="text-gray-300 font-semibold"
                      >Всего в пакете:</span
                    >
                    {{ tariffInfo?.num_of_lessons || 0 }} уроков
                  </p>
                  <p>
                    <span class="text-gray-300 font-semibold"
                      >Стоимость пакета:</span
                    >
                    {{ tariffInfo?.price || 0 }} ₽
                  </p>
                </div>
              </div>
            </div>

            <!-- Если нет активного тарифа -->
            <div v-if="!activeTariff" class="text-center py-12">
              <p class="text-gray-400 text-lg">
                У тебя пока нет активного тарифа. Свяжись с репетитором!
              </p>
            </div>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ===== ВКЛАДКА: ПЛАТЕЖИ ===== -->
    <div v-if="activeTab === 'payment'">
      <Transition name="fade" mode="out-in">
        <PaymentSkeleton v-if="loadingTab === 'payment'" key="skel" />

        <div v-else key="content">
          <!-- Реквизиты для оплаты -->
          <div v-if="paymentDetails" class="mb-8 bg-gray-800/50 rounded-2xl p-6 border border-gray-700">
            <p class="text-xs uppercase tracking-widest text-amber-400 font-bold mb-4">
              💳 Реквизиты для оплаты
            </p>
            <div class="space-y-3 text-sm">
              <div>
                <p class="text-gray-400">{{ paymentDetails.details_text }}</p>
              </div>
              <div v-if="paymentDetails.tutor_name" class="mt-4 pt-4 border-t border-gray-700">
                <p class="text-gray-300 font-semibold">{{ paymentDetails.tutor_name }}</p>
                <p v-if="paymentDetails.tutor_phone" class="text-gray-400 text-xs">
                  {{ paymentDetails.tutor_phone }}
                </p>
              </div>
            </div>
          </div>

          <!-- История платежей -->
          <div>
            <p class="text-sm uppercase tracking-widest text-gray-400 font-bold mb-4">
              📜 История платежей
            </p>
            <div v-if="payments.length > 0" class="space-y-3">
              <div
                v-for="payment in payments"
                :key="payment.payment_id"
                class="bg-gray-800/50 rounded-xl p-4 border border-gray-700 flex justify-between items-center"
              >
                <div>
                  <p class="text-gray-300 font-semibold">
                    {{ methodLabel(payment.method) }}
                  </p>
                  <p class="text-xs text-gray-500 mt-1">
                    {{ formatDateShort(payment.payment_date) }}
                  </p>
                </div>
                <p class="text-lg font-black text-emerald-400">
                  +{{ payment.amount }} ₽
                </p>
              </div>
            </div>
            <div v-else class="text-center py-8 text-gray-500">
              <p>Платежей пока нет</p>
            </div>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ===== ВКЛАДКА: ДОМАШНЕЕ ЗАДАНИЕ ===== -->
    <div v-if="activeTab === 'homework'">
      <Transition name="fade" mode="out-in">
        <HomeworkSkeleton v-if="loadingTab === 'homework'" key="skel" />

        <div v-else key="content">
          <!-- Фильтр по статусу -->
          <div class="flex gap-2 mb-6">
            <button
              v-for="status in ['all', 'done', 'undone']"
              :key="status"
              @click="homeworkFilter = status"
              class="px-4 py-2 rounded-lg text-sm font-semibold transition"
              :class="
                homeworkFilter === status
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              "
            >
              {{
                status === 'all'
                  ? 'Все'
                  : status === 'done'
                  ? '✅ Выполнено'
                  : '⏳ Не выполнено'
              }}
            </button>
          </div>

          <!-- Список домашних заданий -->
          <div v-if="filteredHomework.length > 0" class="space-y-4">
            <div
              v-for="lesson in filteredHomework"
              :key="lesson.lesson_id"
              class="bg-gray-800/50 rounded-xl p-4 border border-gray-700"
            >
              <div class="flex justify-between items-start mb-2">
                <div>
                  <p class="text-gray-300 font-semibold">{{ lesson.theme }}</p>
                  <p class="text-xs text-gray-500 mt-1">
                    {{ formatDateShort(lesson.lesson_datetime) }}
                  </p>
                </div>
                <span
                  :class="[
                    'text-xs font-bold px-2 py-1 rounded',
                    lesson.homework_done
                      ? 'bg-emerald-900/40 text-emerald-400'
                      : 'bg-amber-900/40 text-amber-400',
                  ]"
                >
                  {{ lesson.homework_done ? '✅ Выполнено' : '⏳ Не выполнено' }}
                </span>
              </div>
              <p v-if="lesson.notes_for_parents" class="text-sm text-gray-400 mt-2">
                {{ lesson.notes_for_parents }}
              </p>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-500">
            <p>Нет домашних заданий</p>
          </div>
        </div>
      </Transition>
    </div>

    <!-- ===== ВКЛАДКА: МАТЕРИАЛЫ ===== -->
    <div v-if="activeTab === 'materials'">
      <Transition name="fade" mode="out-in">
        <MaterialsSkeleton v-if="loadingTab === 'materials'" key="skel" />

        <div v-else key="content">
          <div v-if="lessonMaterials.length > 0" class="space-y-6">
            <div
              v-for="material in lessonMaterials"
              :key="material.lesson_id"
              class="bg-gray-800/50 rounded-xl p-6 border border-gray-700"
            >
              <div class="mb-4">
                <p class="text-gray-300 font-semibold text-lg">{{ material.theme }}</p>
                <p class="text-xs text-gray-500 mt-1">
                  {{ formatDateShort(material.lesson_datetime) }}
                </p>
              </div>

              <div class="space-y-2">
                <div
                  v-for="att in material.attachments"
                  :key="att.attachment_id"
                  class="flex items-center justify-between bg-gray-900/50 rounded-lg p-3 border border-gray-700 hover:border-gray-600 transition"
                >
                  <div class="flex items-center gap-3 flex-1">
                    <span class="text-2xl">{{ getFileIcon(att.file_name) }}</span>
                    <div class="flex-1">
                      <p class="text-sm text-gray-300 font-semibold truncate">
                        {{ att.file_name }}
                      </p>
                      <p class="text-xs text-gray-600">
                        {{ formatFileSize(att.file_size) }}
                      </p>
                    </div>
                  </div>
                  <button
                    @click="downloadFile(att)"
                    class="px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-xs rounded transition"
                  >
                    ⬇️ Скачать
                  </button>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="text-center py-8 text-gray-500">
            <p>Материалы пока не загружены</p>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
// -------------------------------------------------------
// ИМПОРТЫ
// -------------------------------------------------------
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import DashboardHeaderSkeleton from '../../components/skeletons/DashboardHeaderSkeleton.vue';
import ScheduleSkeleton from '../../components/skeletons/ScheduleSkeleton.vue';
import TariffChildSkeleton from '../../components/skeletons/TariffChildSkeleton.vue';
import PaymentSkeleton from '../../components/skeletons/PaymentSkeleton.vue';
import HomeworkSkeleton from '../../components/skeletons/HomeworkSkeleton.vue';
import MaterialsSkeleton from '../../components/skeletons/MaterialsSkeleton.vue';
import WeeklyCalendar from '../../components/WeeklyCalendar.vue';

// API (из client.js)
import {
  getChild,
  getChildLessons,
  getChildPayments,
  getStudentStatus,
  getTariffs,
  getLatestPaymentDetails,
} from '../../api/client.js';

// Auth store
import { user, logout } from '../../stores/auth.js';

// -------------------------------------------------------
// СОСТОЯНИЕ
// -------------------------------------------------------

const router = useRouter();

// Данные студента и уроков
const student = ref(null);
const lessons = ref([]);
const payments = ref([]);
const attachments = ref([]);
const activeTariff = ref(null);
const tariffInfo = ref(null);
const paymentDetails = ref(null);

// UI состояние
const activeTab = ref('schedule');
const tabs = ['schedule', 'tariff', 'payment', 'homework', 'materials'];
const tabLabels = {
  schedule: '📅 Расписание',
  tariff: '✨ Тариф',
  payment: '💳 Платежи',
  homework: '📚 Д/З',
  materials: '📎 Материалы',
};

// Фильтры и флаги загрузки
const loadingHeader = ref(true);
const homeworkFilter = ref('all');
const loadedTabs = ref(new Set());
const loadingTab = ref('');
const scheduleReady = ref(false);
const loadingTariff = ref(false);

// Модальное окно урока (заглушка для будущей реализации)
const showLessonModal = ref(false);
const selectedLesson = ref(null);

// -------------------------------------------------------
// ВЫЧИСЛЯЕМЫЕ СВОЙСТВА
// -------------------------------------------------------

const childLessons = computed(() => {
  return lessons.value.filter((l) => l.status !== 'cancelled');
});

const nextLesson = computed(() => {
  const now = new Date();
  return lessons.value
    .filter((l) => new Date(l.lesson_datetime) > now && l.status !== 'cancelled')
    .sort((a, b) => new Date(a.lesson_datetime) - new Date(b.lesson_datetime))[0];
});

const filteredHomework = computed(() => {
  let hw = lessons.value.filter((l) => l.status === 'completed');

  if (homeworkFilter.value === 'undone') {
    hw = hw.filter((l) => !l.homework_done);
  } else if (homeworkFilter.value === 'done') {
    hw = hw.filter((l) => l.homework_done);
  }

  return hw.sort(
    (a, b) => new Date(b.lesson_datetime) - new Date(a.lesson_datetime)
  );
});

const lessonMaterials = computed(() => {
  const grouped = {};
  attachments.value.forEach((att) => {
    const lesson = lessons.value.find((l) => l.lesson_id === att.lesson_id);
    if (lesson) {
      if (!grouped[lesson.lesson_id]) {
        grouped[lesson.lesson_id] = {
          lesson_id: lesson.lesson_id,
          theme: lesson.theme,
          lesson_datetime: lesson.lesson_datetime,
          attachments: [],
        };
      }
      grouped[lesson.lesson_id].attachments.push(att);
    }
  });

  return Object.values(grouped).sort(
    (a, b) => new Date(b.lesson_datetime) - new Date(a.lesson_datetime)
  );
});

// -------------------------------------------------------
// ЗАГРУЗКА ДАННЫХ
// -------------------------------------------------------

async function loadStudentData() {
  try {
    // Для MVP используем user.value из auth store (содержит реальный child_id)
    if (user.value?.id) {
      student.value = await getChild(user.value.id);
    }
  } catch (e) {
    console.error('Ошибка загрузки данных студента:', e);
  }
}

async function loadSchedule() {
  try {
    loadingTab.value = 'schedule';
    const today = new Date();
    const twoMonthsAhead = new Date(today);
    twoMonthsAhead.setMonth(today.getMonth() + 2);

    const startStr = today.toISOString().split('T')[0];
    const endStr = twoMonthsAhead.toISOString().split('T')[0];

    if (student.value) {
      lessons.value = await getChildLessons(student.value.child_id, startStr, endStr);
    }
    loadedTabs.value.add('schedule');
    scheduleReady.value = true;
  } catch (e) {
    console.error('Ошибка загрузки расписания:', e);
  } finally {
    if (loadingTab.value === 'schedule') loadingTab.value = '';
  }
}

async function loadTariff() {
  // Защита от повторной загрузки, если данные уже есть
  if (loadedTabs.value.has('tariff') && activeTariff.value) return;

  try {
    loadingTab.value = 'tariff';
    loadingTariff.value = true; // Включаем пульсацию в шапке
    
    if (student.value) {
      const status = await getStudentStatus(student.value.child_id);
      activeTariff.value = status;

      if (status?.tariff_name) {
        const tariffs = await getTariffs();
        const tariff = tariffs.find((t) => t.name === status.tariff_name);
        tariffInfo.value = tariff;
      }
    }
    loadedTabs.value.add('tariff');
  } catch (e) {
    console.error('Ошибка загрузки тарифа:', e);
  } finally {
    if (loadingTab.value === 'tariff') loadingTab.value = '';
    loadingTariff.value = false; // Выключаем пульсацию
  }
}

async function loadPayments() {
  try {
    loadingTab.value = 'payment';
    if (student.value) {
      // ИСПРАВЛЕНИЕ: используем реальные даты вместо 2020-2029
      const today = new Date();
      const oneYearAgo = new Date(today);
      oneYearAgo.setFullYear(today.getFullYear() - 1);

      const startStr = oneYearAgo.toISOString().split('T')[0];
      const endStr = today.toISOString().split('T')[0];

      payments.value = await getChildPayments(
        student.value.child_id,
        startStr,
        endStr
      );
      paymentDetails.value = await getLatestPaymentDetails();
    }
    loadedTabs.value.add('payment');
  } catch (e) {
    console.error('Ошибка загрузки платежей:', e);
    paymentDetails.value = null;
  } finally {
    if (loadingTab.value === 'payment') loadingTab.value = '';
  }
}

function loadHomework() {
  // Данные загружаются в loadSchedule() вместе с lessons
  loadedTabs.value.add('homework');
}

async function loadMaterials() {
  try {
    loadingTab.value = 'materials';
    // TODO: Добавить загрузку вложений из API когда будет реализовано на бэкенде
    // attachments.value = await getLessonAttachments(...);
    loadedTabs.value.add('materials');
  } catch (e) {
    console.error('Ошибка загрузки материалов:', e);
  } finally {
    if (loadingTab.value === 'materials') loadingTab.value = '';
  }
}

// -------------------------------------------------------
// ДЕЙСТВИЯ / ОБРАБОТЧИКИ
// -------------------------------------------------------

function handleLogout() {
  logout();
  router.push('/login');
}

function editLesson(lesson) {
  selectedLesson.value = lesson;
  showLessonModal.value = true;
  // TODO: Реализовать модальное окно для редактирования урока
}

function downloadFile(attachment) {
  // TODO: Реализовать скачивание файла
  console.log('Скачивание файла:', attachment.file_name);
}

// -------------------------------------------------------
// ЖИЗНЕННЫЙ ЦИКЛ И НАБЛЮДАТЕЛИ
// -------------------------------------------------------

onMounted(async () => {
  try {
    loadingHeader.value = true;
    
    // Сначала обязательно получаем ID студента
    await loadStudentData();
    
    // Когда ID у нас, запускаем параллельно базовые запросы для верхних карточек
    await Promise.all([
      loadSchedule(), // Загрузит уроки для блока "Следующий урок"
      loadTariff()    // Загрузит баланс уроков, долг и название тарифа
    ]);
    
  } catch (e) {
    console.error('Критическая ошибка инициализации дашборда:', e);
  } finally {
    // Выключаем скелетон шапки — все данные для неё прилетели!
    loadingHeader.value = false;
  }
});

watch(activeTab, (tab) => {
  if (tab === 'tariff' && !loadedTabs.value.has('tariff')) loadTariff();
  if (tab === 'payment' && !loadedTabs.value.has('payment')) loadPayments();
  if (tab === 'homework' && !loadedTabs.value.has('homework')) loadHomework();
  if (tab === 'materials' && !loadedTabs.value.has('materials')) loadMaterials();
});

// -------------------------------------------------------
// УТИЛИТЫ
// -------------------------------------------------------

const formatDateShort = (d) =>
  new Date(d).toLocaleDateString('ru-RU', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });

const formatTime = (d) =>
  new Date(d).toLocaleTimeString('ru-RU', {
    hour: '2-digit',
    minute: '2-digit',
  });

function methodLabel(method) {
  const map = {
    cash: '💵 Наличные',
    card: '💳 Карта',
    sbp: '⚡ СБП',
    bank_transfer: '🏦 Перевод',
    online_payment: '🌐 Онлайн',
    qr_code: '📱 QR-код',
  };
  return map[method] || method;
}

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

function getFileIcon(filename) {
  if (filename.match(/\.(pdf)$/i)) return '📄';
  if (filename.match(/\.(doc|docx)$/i)) return '📝';
  if (filename.match(/\.(xls|xlsx)$/i)) return '📊';
  if (filename.match(/\.(ppt|pptx)$/i)) return '🎯';
  if (filename.match(/\.(jpg|jpeg|png|gif)$/i)) return '🖼️';
  if (filename.match(/\.(mp4|avi|mov)$/i)) return '🎬';
  if (filename.match(/\.(mp3|wav)$/i)) return '🎵';
  if (filename.match(/\.(zip|rar|7z)$/i)) return '📦';
  return '📎';
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
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