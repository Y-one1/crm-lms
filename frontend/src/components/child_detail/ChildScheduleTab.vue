<template>
  <div>
    <Transition name="fade" mode="out-in">
      <ScheduleSkeleton v-if="!scheduleReady" key="skel" />
      <WeeklyCalendar v-else key="cal"
        :lessons="childLessons"
        @date-change="onDateChange"
        @cell-click="handleCellClick"
        @lesson-click="editLesson"
      />
    </Transition>

    <LessonModal
      :show="showLessonModal"
      :initial-data="selectedLesson"
      :is-fixed-child="true"
      @close="showLessonModal = false"
      @saved="loadSchedule"
      @deleted="loadSchedule"
    />
  </div>
</template>

<script setup>
// name нужен для корректной работы KeepAlive
defineOptions({ name: 'ChildScheduleTab' });

import { ref, onMounted } from 'vue';
import WeeklyCalendar from '../WeeklyCalendar.vue';
import LessonModal from '../modals/LessonModal.vue';
import ScheduleSkeleton from '../skeletons/ScheduleSkeleton.vue';
import { getChildLessons } from '../../api/client.js';

const props = defineProps({
  childId: { type: Number, required: true },
});

// --- СОСТОЯНИЕ ---
const childLessons = ref([]);
const scheduleReady = ref(false); // false только до первой загрузки, потом всегда true
const showLessonModal = ref(false);
const selectedLesson = ref({});
let currentRange = { weekStart: null, weekEnd: null, showFullLog: false };

// --- ЗАГРУЗКА ---
function getInitialRange() {
  const today = new Date();
  const day = today.getDay();
  const weekStart = new Date(today);
  weekStart.setDate(today.getDate() - (day === 0 ? 6 : day - 1));
  weekStart.setHours(0, 0, 0, 0);
  const weekEnd = new Date(weekStart);
  weekEnd.setDate(weekStart.getDate() + 6);
  weekEnd.setHours(23, 59, 59, 999);
  return { weekStart, weekEnd, showFullLog: false };
}

async function loadSchedule() {
  const { weekStart, weekEnd, showFullLog } = currentRange;
  if (!weekStart || !weekEnd) return;
  try {
    const startStr = showFullLog ? '2020-01-01' : weekStart.toISOString().split('T')[0];
    
    // По умолчанию берем конец текущей недели
    let endStr = showFullLog ? '2029-12-31' : weekEnd.toISOString().split('T')[0];
    
    // Если мы смотрим обычную неделю (не весь лог), расширяем запрос на 28 дней вперед.
    // Это нужно, чтобы сервер прислал будущие уроки, и счетчик в календаре их увидел.
    if (!showFullLog) {
      const extendedEnd = new Date(weekEnd);
      extendedEnd.setDate(extendedEnd.getDate() + 28);
      endStr = extendedEnd.toISOString().split('T')[0];
    }

    childLessons.value = await getChildLessons(props.childId, startStr, endStr);
  } catch (e) {
    console.error('Ошибка загрузки расписания:', e);
  } finally {
    scheduleReady.value = true;
  }
}

onMounted(() => {
  currentRange = getInitialRange();
  loadSchedule();
});

// --- UI-ЛОГИКА ---
function onDateChange(range) {
  currentRange = range;
  loadSchedule();
}

function handleCellClick({ dateStr, hour }) {
  selectedLesson.value = {
    date: dateStr,
    time: `${String(hour).padStart(2, '0')}:00`,
    child_id: props.childId,
    status: 'planned',
    theme: '',
    homework_done: false,
    grade: null,
  };
  showLessonModal.value = true;
}

function editLesson(lesson) {
  const [date, fullTime] = lesson.lesson_datetime.split('T');
  selectedLesson.value = { ...lesson, date, time: fullTime.substring(0, 5) };
  showLessonModal.value = true;
}
</script>