<template>
  <div>
    <Transition name="fade" mode="out-in">
      <TableSkeleton v-if="loading" key="skel" />

      <div v-else key="content" class="space-y-6">

        <!-- Пресеты периода -->
        <div class="flex flex-wrap gap-2 items-center">
          <button
            v-for="p in periods"
            :key="p.key"
            @click="applyPerfPeriod(p.key)"
            class="px-4 py-2 rounded-lg text-sm font-semibold transition border"
            :class="perfPeriod === p.key
              ? 'bg-blue-600 border-blue-500 text-white'
              : 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white'"
          >
            {{ p.label }}
          </button>

          <!-- Кастомный диапазон -->
          <div class="flex items-center gap-2 ml-2">
            <input
              v-model="perfCustomStart"
              type="date"
              class="px-2 py-1.5 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
            />
            <span class="text-gray-600 text-sm">—</span>
            <input
              v-model="perfCustomEnd"
              type="date"
              class="px-2 py-1.5 bg-gray-800 border border-gray-700 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
            />
            <button
              @click="applyCustomPerfPeriod"
              class="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 border border-gray-600 rounded-lg text-white text-sm transition"
            >
              →
            </button>
          </div>

          <button
            @click="showReportModal = true"
            class="ml-auto px-4 py-2 bg-gradient-to-r from-purple-700 to-purple-800 hover:from-purple-600 hover:to-purple-700 text-white text-sm font-semibold rounded-lg transition shadow-lg"
          >
            📄 Отчёт для родителей
          </button>
        </div>

        <!-- Нет данных -->
        <div v-if="completedLessons.length === 0" class="text-center py-16">
          <div class="text-6xl mb-4">📭</div>
          <h2 class="text-2xl font-bold text-white mb-2">Нет завершённых уроков</h2>
          <p class="text-gray-400">Попробуйте выбрать другой период</p>
        </div>

        <template v-else>
          <!-- Сводные карточки -->
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="bg-gray-800 rounded-2xl p-5 border border-gray-700">
              <p class="text-xs uppercase tracking-widest text-gray-500 mb-2">Средняя оценка</p>
              <p class="text-5xl font-black" :class="avgGradeColor">{{ avgGrade ?? '—' }}</p>
            </div>

            <div class="bg-gray-800 rounded-2xl p-5 border border-gray-700">
              <p class="text-xs uppercase tracking-widest text-gray-500 mb-2">Выполнение ДЗ</p>
              <p class="text-5xl font-black" :class="hwPercent >= 80 ? 'text-emerald-400' : hwPercent >= 50 ? 'text-yellow-400' : 'text-red-400'">
                {{ hwPercent }}<span class="text-2xl">%</span>
              </p>
              <div class="w-full bg-gray-700 rounded-full h-1.5 mt-3">
                <div
                  class="h-1.5 rounded-full transition-all"
                  :class="hwPercent >= 80 ? 'bg-emerald-500' : hwPercent >= 50 ? 'bg-yellow-500' : 'bg-red-500'"
                  :style="{ width: hwPercent + '%' }"
                ></div>
              </div>
            </div>

            <div class="bg-gray-800 rounded-2xl p-5 border border-gray-700">
              <p class="text-xs uppercase tracking-widest text-gray-500 mb-2">Посещаемость</p>
              <p class="text-5xl font-black" :class="attendancePercent >= 80 ? 'text-emerald-400' : attendancePercent >= 60 ? 'text-yellow-400' : 'text-red-400'">
                {{ attendancePercent }}<span class="text-2xl">%</span>
              </p>
              <div class="w-full bg-gray-700 rounded-full h-1.5 mt-3">
                <div class="h-1.5 rounded-full transition-all bg-emerald-500" :style="{ width: attendancePercent + '%' }"></div>
              </div>
            </div>

            <div class="bg-gray-800 rounded-2xl p-5 border border-gray-700">
              <p class="text-xs uppercase tracking-widest text-gray-500 mb-2">Уроков проведено</p>
              <p class="text-5xl font-black text-white">{{ completedLessons.length }}</p>
              <p class="text-xs text-gray-600 mt-2">{{ perfLessons.filter(l => l.status === 'cancelled').length }} отменено</p>
            </div>
          </div>

          <!-- График оценок -->
          <div v-if="gradeChartPoints.length >= 2" class="bg-gray-800 rounded-2xl border border-gray-700 p-6">
            <h3 class="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">📈 Динамика оценок</h3>
            <div class="overflow-x-auto">
              <svg viewBox="0 0 600 140" class="w-full" style="min-width: 320px; height: 140px;">
                <g>
                  <line v-for="g in [2,3,4,5]" :key="g"
                    x1="24" :y1="140 - 24 - (g - 2) * (96 / 3)"
                    x2="576" :y2="140 - 24 - (g - 2) * (96 / 3)"
                    stroke="#374151" stroke-width="1" stroke-dasharray="4,4"
                  />
                  <text v-for="g in [2,3,4,5]" :key="'l'+g"
                    x="12" :y="140 - 20 - (g - 2) * (96 / 3)"
                    fill="#6b7280" font-size="10" text-anchor="middle"
                  >{{ g }}</text>
                </g>
                <line v-if="avgGrade"
                  x1="24" :y1="140 - 24 - (parseFloat(avgGrade) - 2) * (96 / 3)"
                  x2="576" :y2="140 - 24 - (parseFloat(avgGrade) - 2) * (96 / 3)"
                  stroke="#3b82f6" stroke-width="1" stroke-dasharray="6,3" opacity="0.5"
                />
                <path
                  :d="buildChartPath(gradeChartPoints).line"
                  fill="none" stroke="#6366f1" stroke-width="2.5"
                  stroke-linejoin="round" stroke-linecap="round"
                />
                <g v-for="(dot, i) in buildChartPath(gradeChartPoints).dots" :key="i">
                  <circle :cx="dot.x" :cy="dot.y" r="6" fill="#1f2937" />
                  <circle
                    :cx="dot.x" :cy="dot.y" r="4.5"
                    :fill="dot.grade >= 4 ? '#34d399' : dot.grade === 3 ? '#fbbf24' : '#f87171'"
                  />
                  <text
                    v-if="i === 0 || i === gradeChartPoints.length - 1"
                    :x="dot.x" y="136"
                    fill="#6b7280" font-size="9" text-anchor="middle"
                  >{{ dot.date }}</text>
                </g>
              </svg>
            </div>
            <p class="text-xs text-gray-600 mt-1">— — Средняя оценка: {{ avgGrade }}</p>
          </div>

          <div
            v-else-if="gradeChartPoints.length === 1"
            class="bg-gray-800 rounded-2xl border border-gray-700 p-6 text-center text-gray-600 text-sm"
          >
            Для графика нужно минимум 2 урока с оценками
          </div>

          <!-- Таблица уроков -->
          <div class="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden">
            <div class="px-6 py-4 border-b border-gray-700">
              <h3 class="text-sm font-bold text-gray-400 uppercase tracking-wider">📋 Журнал уроков</h3>
            </div>
            <table class="w-full">
              <thead>
                <tr class="bg-gray-900/60">
                  <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Дата</th>
                  <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Тема</th>
                  <th class="px-6 py-3 text-center text-xs font-semibold text-gray-500 uppercase">Оценка</th>
                  <th class="px-6 py-3 text-center text-xs font-semibold text-gray-500 uppercase">ДЗ</th>
                  <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase">Заметка родителям</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="lesson in sortedCompletedLessons"
                  :key="lesson.lesson_id"
                  class="border-t border-gray-700/50 hover:bg-gray-700/30 transition"
                >
                  <td class="px-6 py-4 text-sm text-gray-400 whitespace-nowrap">{{ formatDateShort(lesson.lesson_datetime) }}</td>
                  <td class="px-6 py-4 text-sm text-white font-medium">{{ lesson.theme }}</td>
                  <td class="px-6 py-4 text-center">
                    <span
                      v-if="lesson.grade != null"
                      class="inline-flex items-center justify-center w-9 h-9 rounded-full text-sm font-black"
                      :class="{
                        'bg-emerald-900/60 text-emerald-400': lesson.grade === 5,
                        'bg-blue-900/60 text-blue-400':       lesson.grade === 4,
                        'bg-yellow-900/60 text-yellow-400':   lesson.grade === 3,
                        'bg-red-900/60 text-red-400':         lesson.grade === 2,
                      }"
                    >{{ lesson.grade }}</span>
                    <span v-else class="text-gray-600 text-xs italic">—</span>
                  </td>
                  <td class="px-6 py-4 text-center">
                    <span v-if="lesson.homework_done" class="text-emerald-400 text-lg">✓</span>
                    <span v-else class="text-red-400/60 text-lg">✗</span>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-400 max-w-xs">
                    <span v-if="lesson.notes_for_parents" class="italic">{{ lesson.notes_for_parents }}</span>
                    <span v-else class="text-gray-700">—</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>

        <!-- Модалка отчёта -->
        <div
          v-if="showReportModal"
          class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        >
          <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-lg border border-gray-700 shadow-2xl">
            <div class="flex justify-between items-center mb-5">
              <h2 class="text-xl font-bold text-white">📄 Отчёт для родителей</h2>
              <button @click="showReportModal = false" class="text-gray-500 hover:text-white text-xl">✕</button>
            </div>
            <div class="bg-gray-800 rounded-xl p-4 border border-gray-700 mb-5">
              <pre class="text-sm text-gray-300 whitespace-pre-wrap font-sans leading-relaxed">{{ reportText }}</pre>
            </div>
            <div class="flex gap-3">
              <button
                @click="copyReport"
                class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition text-sm"
              >
                📋 Скопировать
              </button>
              <button
                @click="showReportModal = false"
                class="flex-1 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-white font-semibold transition text-sm"
              >
                Закрыть
              </button>
            </div>
            <p class="text-xs text-gray-600 mt-3 text-center">Расширенный отчёт с аналитикой — в разработке</p>
          </div>
        </div>

      </div>
    </Transition>
  </div>
</template>

<script setup>
// name нужен для корректной работы KeepAlive
defineOptions({ name: 'ChildPerformanceTab' });

import { ref, computed, onMounted, watch } from 'vue';
import TableSkeleton from '../skeletons/TableSkeleton.vue';
import { getChildLessons } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  childId:   { type: Number, required: true },
  childName: { type: String, default: 'ученик' },
});

const periods = [
  { key: '2weeks',  label: '2 недели' },
  { key: 'month',   label: 'Месяц'    },
  { key: 'quarter', label: 'Квартал'  },
  { key: 'all',     label: 'Всё время' },
];

// --- СОСТОЯНИЕ ---
const perfLessons     = ref([]);
const loading         = ref(true);
const perfPeriod      = ref('month');
const perfCustomStart = ref('');
const perfCustomEnd   = ref('');
const showReportModal = ref(false);

// --- ВЫЧИСЛЯЕМЫЕ ---
const perfDateRange = computed(() => {
  const today = new Date();
  const fmt = (d) => d.toISOString().split('T')[0];
  if (perfPeriod.value === 'custom') {
    return { start: perfCustomStart.value, end: perfCustomEnd.value };
  }
  const start = new Date(today);
  if (perfPeriod.value === '2weeks')       start.setDate(today.getDate() - 14);
  else if (perfPeriod.value === 'month')   start.setMonth(today.getMonth() - 1);
  else if (perfPeriod.value === 'quarter') start.setMonth(today.getMonth() - 3);
  else start.setFullYear(2020);
  const end = new Date(today);
  end.setDate(today.getDate() + 30);
  return { start: fmt(start), end: fmt(end) };
});

const completedLessons = computed(() => perfLessons.value.filter((l) => l.status === 'completed'));

const sortedCompletedLessons = computed(() =>
  completedLessons.value.slice().sort((a, b) => new Date(b.lesson_datetime) - new Date(a.lesson_datetime))
);

const avgGrade = computed(() => {
  const graded = completedLessons.value.filter((l) => l.grade != null);
  if (!graded.length) return null;
  return (graded.reduce((s, l) => s + l.grade, 0) / graded.length).toFixed(1);
});

const hwPercent = computed(() => {
  if (!completedLessons.value.length) return 0;
  const done = completedLessons.value.filter((l) => l.homework_done).length;
  return Math.round((done / completedLessons.value.length) * 100);
});

const attendancePercent = computed(() => {
  const relevant = perfLessons.value.filter((l) => l.status === 'completed' || l.status === 'cancelled');
  if (!relevant.length) return 100;
  const attended = relevant.filter((l) => l.status === 'completed').length;
  return Math.round((attended / relevant.length) * 100);
});

const gradeChartPoints = computed(() =>
  completedLessons.value
    .filter((l) => l.grade != null)
    .slice()
    .sort((a, b) => new Date(a.lesson_datetime) - new Date(b.lesson_datetime))
);

const avgGradeColor = computed(() => {
  if (!avgGrade.value) return 'text-gray-500';
  const v = parseFloat(avgGrade.value);
  if (v >= 4.5) return 'text-emerald-400';
  if (v >= 3.5) return 'text-blue-400';
  if (v >= 3.0) return 'text-yellow-400';
  return 'text-red-400';
});

const reportText = computed(() => {
  const total = completedLessons.value.length;
  const avg   = avgGrade.value ?? '—';
  return `Отчёт об успеваемости\n${props.childName}\n\nЗа выбранный период проведено уроков: ${total}\nСредняя оценка: ${avg}\nВыполнение домашних заданий: ${hwPercent.value}%\nПосещаемость: ${attendancePercent.value}%\n\n[Здесь будет развёрнутый текстовый отчёт с анализом динамики и рекомендациями — функция в разработке]`;
});

// --- ЗАГРУЗКА ---
async function loadPerformance() {
  try {
    loading.value = true;
    const { start, end } = perfDateRange.value;
    if (!start || !end) return;
    perfLessons.value = await getChildLessons(props.childId, start, end);
  } catch (e) {
    console.error('Ошибка загрузки успеваемости:', e);
  } finally {
    loading.value = false;
  }
}

watch(perfDateRange, loadPerformance, { immediate: true });

// --- ДЕЙСТВИЯ ---
async function applyPerfPeriod(preset) {
  perfPeriod.value = preset;
  // loadPerformance вызовется сам через watch
}

async function applyCustomPerfPeriod() {
  if (!perfCustomStart.value || !perfCustomEnd.value) return;
  perfPeriod.value = 'custom';
}

function copyReport() {
  navigator.clipboard.writeText(reportText.value);
  Swal.fire({ icon: 'success', title: 'Скопировано!', timer: 1000, showConfirmButton: false, background: '#111827', color: '#fff' });
}

// --- УТИЛИТЫ ---
const formatDateShort = (d) => new Date(d).toLocaleDateString('ru-RU');

function buildChartPath(points, width = 600, height = 120) {
  if (points.length < 2) return { line: '', dots: [] };
  const minG = 2, maxG = 5, pad = 24;
  const xStep = (width - pad * 2) / (points.length - 1);
  const yScale = (height - pad * 2) / (maxG - minG);
  const coords = points.map((p, i) => ({
    x: pad + i * xStep,
    y: height - pad - (p.grade - minG) * yScale,
    grade: p.grade,
    date: formatDateShort(p.lesson_datetime),
  }));
  const line = coords.map((c, i) => `${i === 0 ? 'M' : 'L'}${c.x},${c.y}`).join(' ');
  return { line, dots: coords };
}
</script>

<style scoped>
input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
</style>