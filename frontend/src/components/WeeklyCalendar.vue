<template>
  <div class="space-y-6">

    <!-- Статистика периода + кнопка лога -->
    <div class="flex justify-between items-center bg-gray-900/50 p-4 rounded-xl border border-gray-800">
      <div>
        <p class="text-xs uppercase tracking-widest text-gray-500 mb-2 font-bold">Статистика периода</p>
        <div class="flex items-baseline gap-6">
          <!-- Запланировано на текущей неделе -->
          <div>
            <span class="text-xs text-gray-500 block mb-0.5">На этой неделе</span>
            <span class="text-xl font-black" :class="plannedThisWeek > 0 ? 'text-blue-400' : 'text-gray-600'">
              {{ plannedThisWeek }}
            </span>
            <span class="text-xs text-gray-500 ml-1">запл.</span>
          </div>
          <!-- Запланировано за пределами текущей недели -->
          <div>
            <span class="text-xs text-gray-500 block mb-0.5">В будущем</span>
            <span class="text-xl font-black" :class="plannedFuture > 0 ? 'text-purple-400' : 'text-gray-600'">
              {{ plannedFuture }}
            </span>
            <span class="text-xs text-gray-500 ml-1">запл.</span>
          </div>
        </div>
      </div>
      <button
        @click="toggleLog"
        class="px-4 py-2 rounded-lg border transition text-sm font-semibold"
        :class="
          showFullLog
            ? 'bg-blue-600 border-blue-400 text-white'
            : 'bg-gray-800 border-gray-700 text-gray-400 hover:text-white'
        "
      >
        {{ showFullLog ? '📖 Весь лог включен' : '📜 Показать весь лог' }}
      </button>
    </div>

    <!-- Навигация по неделям -->
    <div class="flex items-center justify-between">
      <button
        @click="previousWeek"
        class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition border border-gray-700"
      >
        ← Назад
      </button>
      <div class="text-center">
        <p class="text-sm text-gray-400 mb-1">Неделя {{ weekNumber }}</p>
        <p class="text-2xl font-black">
          {{ formatDate(weekStart) }} — {{ formatDate(weekEnd) }}
        </p>
        <button
          @click="goToToday"
          class="text-xs bg-blue-600/20 text-blue-400 px-2 py-1 rounded hover:bg-blue-600 hover:text-white transition mt-1"
        >
          Сегодня
        </button>
      </div>
      <button
        @click="nextWeek"
        class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition border border-gray-700"
      >
        Вперед →
      </button>
    </div>

    <!-- Сетка календаря -->
    <!-- overflow-x-auto на внешнем контейнере — шапка и тело скроллятся вместе как единый блок -->
    <div class="overflow-x-auto rounded-lg shadow-2xl">
    <div class="bg-gray-800 border border-gray-700 min-w-[740px]">

      <!-- ШАПКА: дни недели -->
      <!-- sticky убран: внутри overflow-x-auto он прилипает к скролл-контейнеру, а не к странице,
           из-за чего шапка и тело при горизонтальном скролле едут независимо -->
      <div class="flex bg-gray-900 border-b border-gray-700">
        <div class="w-20 flex-shrink-0 flex items-center justify-center text-xs text-gray-300 font-bold border-r border-gray-700 bg-gray-900">
          ВРЕМЯ
        </div>
        <div class="flex flex-1 w-full">
          <div
            v-for="(day, index) in weekDays"
            :key="index"
            class="flex-1 min-w-[160px] p-4 text-center border-r border-gray-700"
            :class="isToday(day) ? 'bg-blue-900/50 border-b-2 border-b-blue-500' : ''"
          >
            <p class="text-2xs uppercase tracking-widest text-gray-300 mb-1">{{ DAY_NAMES[day.getDay()] }}</p>
            <p class="text-2xl font-black" :class="isToday(day) ? 'text-blue-400' : ''">
              {{ day.getDate() }}
            </p>
          </div>
        </div>
      </div>

      <!-- ТЕЛО: временные слоты + колонки дней -->
      <div class="flex relative">

        <!-- Колонка с часами -->
        <div class="w-20 flex-shrink-0 border-r border-gray-700 bg-gray-900">
          <div
            v-for="hour in HOURS"
            :key="hour"
            class="h-20 flex items-center justify-center text-sm text-gray-300 font-semibold border-b border-gray-700"
          >
            {{ String(hour).padStart(2, '0') }}:00
          </div>
        </div>

        <!-- Колонки для каждого дня -->
        <div class="flex flex-1 w-full">
          <div
            v-for="(day, dayIndex) in weekDays"
            :key="dayIndex"
            class="flex-1 min-w-[160px] border-r border-gray-700 relative bg-gray-950/80"
          >
            <!-- Ячейки-слоты для кликов (создание урока) -->
            <div
              v-for="hour in HOURS"
              :key="hour"
              @click="$emit('cell-click', { dateStr: toDateStr(day), hour })"
              class="h-20 border-b border-gray-800/50 hover:bg-blue-500/5 transition-colors cursor-pointer"
            ></div>

            <!-- Карточки уроков для этого дня -->
            <div
              v-for="lesson in getLessonsForDay(day)"
              :key="lesson.lesson_id"
              @click.stop="$emit('lesson-click', lesson)"
              class="absolute left-1 right-1 rounded border-l-4 p-2 text-xs shadow-lg transition-all hover:scale-[1.02] hover:z-10 cursor-pointer"
              :style="getLessonStyle(lesson)"
              :class="getStatusClasses(lesson.status)"
            >
              <!-- Строка 1: время + оценка -->
              <div class="flex justify-between items-start mb-1">
                <span class="font-black">{{ formatLessonTime(lesson.lesson_datetime) }}</span>
                <span v-if="lesson.grade" class="bg-black/20 px-1 rounded text-[10px]">
                  ⭐ {{ lesson.grade }}
                </span>
              </div>
              <!-- Строка 2: имя ученика (только если передан список детей) -->
              <div v-if="childrenMap[lesson.child_id]" class="flex items-center gap-1 mb-0.5">
                <div :class="getDotClass(lesson.status)" class="w-1.5 h-1.5 rounded-full flex-shrink-0"></div>
                <span class="truncate font-semibold text-[11px]">{{ childrenMap[lesson.child_id] }}</span>
              </div>
              <!-- Строка 3: тема -->
              <p class="font-medium leading-tight text-[11px] opacity-80 truncate">{{ lesson.theme }}</p>
            </div>

          </div>
        </div>
      </div>
    </div>
    </div>

    <!-- Легенда статусов -->
    <div class="flex gap-6 text-xs font-semibold uppercase tracking-wider text-gray-500 px-2">
      <div class="flex items-center gap-2"><div class="w-3 h-3 bg-yellow-500 rounded-full"></div>План</div>
      <div class="flex items-center gap-2"><div class="w-3 h-3 bg-green-500 rounded-full"></div>Завершено</div>
      <div class="flex items-center gap-2"><div class="w-3 h-3 bg-red-500 rounded-full"></div>Отменено</div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// --- ПРОПСЫ И ЭМИТЫ ---

const props = defineProps({
  // Все уроки (за текущую неделю или за весь период — решает родитель)
  lessons: { type: Array, default: () => [] },
  // Список детей для отображения имён на карточках. Если не передан — строка с именем не рендерится
  children: { type: Array, default: () => [] },
});

const emit = defineEmits([
  'cell-click',   // { dateStr: 'YYYY-MM-DD', hour: Number } — клик по пустой ячейке
  'lesson-click', // lesson — клик по карточке урока
  'date-change',  // { weekStart, weekEnd, showFullLog } — смена недели или режима лога
]);

// --- КОНСТАНТЫ ---

const HOURS     = Array.from({ length: 15 }, (_, i) => i + 8); // 08–22
const SLOT_H    = 80;  // px, совпадает с h-20 в Tailwind
const FIRST_H   = 8;   // первый час в сетке
const DAY_NAMES = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];

// --- СОСТОЯНИЕ ---

const currentDate = ref(new Date());
const showFullLog = ref(false);

// --- ВЫЧИСЛЯЕМЫЕ: ДАТЫ НЕДЕЛИ ---

const weekStart = computed(() => {
  const d   = new Date(currentDate.value);
  const day = d.getDay();
  d.setDate(d.getDate() - (day === 0 ? 6 : day - 1)); // Пн = начало недели
  d.setHours(0, 0, 0, 0);
  return d;
});

const weekEnd = computed(() => {
  const d = new Date(weekStart.value);
  d.setDate(d.getDate() + 6);
  d.setHours(23, 59, 59, 999);
  return d;
});

const weekDays = computed(() =>
  Array.from({ length: 7 }, (_, i) => {
    const d = new Date(weekStart.value);
    d.setDate(d.getDate() + i);
    return d;
  })
);

const weekNumber = computed(() => {
  const d        = new Date(weekStart.value);
  const firstJan = new Date(d.getFullYear(), 0, 1);
  return Math.ceil(((d - firstJan) / 86400000 + firstJan.getDay() + 1) / 7);
});

// --- ВЫЧИСЛЯЕМЫЕ: СТАТИСТИКА ---

// Запланировано на текущей неделе (статус planned, дата внутри weekStart–weekEnd)
const plannedThisWeek = computed(() =>
  props.lessons.filter(l => {
    if (l.status !== 'planned') return false;
    const d = new Date(l.lesson_datetime);
    return d >= weekStart.value && d <= weekEnd.value;
  }).length
);

// Запланировано в будущем (статус planned, дата строго после текущего момента)
const plannedFuture = computed(() =>
  props.lessons.filter(l => {
    if (l.status !== 'planned') return false;
    return new Date(l.lesson_datetime) > new Date();
  }).length
);

// --- ВЫЧИСЛЯЕМЫЕ: MAP ДЛЯ ИМЁН ДЕТЕЙ ---

// { child_id: "Фамилия И." } — быстрый поиск без find() в рендере
const childrenMap = computed(() => {
  const map = {};
  for (const c of props.children) {
    map[c.child_id] = `${c.last_name} ${c.first_name[0]}.`;
  }
  return map;
});

// --- НАВИГАЦИЯ ---

function previousWeek() {
  const d = new Date(currentDate.value);
  d.setDate(d.getDate() - 7);
  currentDate.value = d;
  notifyParent();
}

function nextWeek() {
  const d = new Date(currentDate.value);
  d.setDate(d.getDate() + 7);
  currentDate.value = d;
  notifyParent();
}

function goToToday() {
  currentDate.value = new Date();
  notifyParent();
}

function toggleLog() {
  showFullLog.value = !showFullLog.value;
  notifyParent();
}

// Сообщаем родителю новый диапазон и режим лога — он перезагрузит данные
function notifyParent() {
  emit('date-change', {
    weekStart:   weekStart.value,
    weekEnd:     weekEnd.value,
    showFullLog: showFullLog.value,
  });
}

// --- РЕНДЕР КАРТОЧЕК ---

// Формируем строку даты локально, а не через toISOString() (который даёт UTC).
// Иначе при положительных timezone-смещениях дата может уйти на день назад.
function toDateStr(day) {
  const y = day.getFullYear();
  const m = String(day.getMonth() + 1).padStart(2, '0');
  const d = String(day.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function getLessonsForDay(day) {
  return props.lessons.filter(l => l.lesson_datetime.startsWith(toDateStr(day)));
}

function getLessonStyle(lesson) {
  const dt         = new Date(lesson.lesson_datetime);
  const hourOffset = dt.getHours() - FIRST_H;
  const minOffset  = dt.getMinutes();
  return {
    top:    `${hourOffset * SLOT_H + (minOffset / 60) * SLOT_H}px`,
    height: `${SLOT_H - 4}px`,
  };
}

function formatLessonTime(iso) {
  return iso?.split('T')[1]?.substring(0, 5) ?? '';
}

function getStatusClasses(status) {
  if (status === 'completed') return 'bg-green-900/40 border-green-500 text-green-100';
  if (status === 'cancelled') return 'bg-red-900/40 border-red-500 text-red-100 opacity-60';
  return 'bg-yellow-900/40 border-yellow-500 text-yellow-100';
}

function getDotClass(status) {
  if (status === 'completed') return 'bg-green-400';
  if (status === 'cancelled') return 'bg-red-400';
  return 'bg-yellow-400';
}

// --- УТИЛИТЫ ---

function isToday(d) {
  return new Date().toDateString() === d.toDateString();
}

function formatDate(d) {
  return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
}

// --- ИНИЦИАЛИЗАЦИЯ ---

// Уведомляем родителя при монтировании — он получит начальный диапазон и загрузит уроки
onMounted(() => {
  notifyParent();
});
</script>