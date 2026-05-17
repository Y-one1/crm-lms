<template>
  <Layout>
    <div class="p-8">

      <div class="mb-8">
        <h1 class="text-4xl font-black mb-2">📅 Расписание</h1>
        <p class="text-gray-400">Общий график занятий всех учеников</p>
      </div>

      <!-- Скелетон только при первой загрузке детей -->
      <Transition name="fade" mode="out-in">
        <ScheduleSkeleton v-if="loading" key="skeleton" />

        <!-- Календарь показываем как только дети загружены, даже если уроков ещё нет -->
        <div v-else key="content" class="space-y-8">
          <WeeklyCalendar
            :lessons="lessons"
            :children="children"
            @date-change="onDateChange"
            @cell-click="handleCellClick"
            @lesson-click="editLesson"
          />

          <LessonModal
            v-if="showLessonModal"
            :show="showLessonModal"
            :initialData="selectedLesson"
            :isFixedChild="false"
            :children="children"
            @close="showLessonModal = false"
            @saved="loadLessons"
            @deleted="loadLessons"
          />
        </div>
      </Transition>

    </div>
  </Layout>
</template>

<script setup>
// --- ИМПОРТЫ ---
import { ref, onMounted } from 'vue';
import Layout from '../../components/Layout.vue';
import WeeklyCalendar from '../../components/WeeklyCalendar.vue';
import LessonModal from '../../components/modals/LessonModal.vue';
import ScheduleSkeleton from '../../components/skeletons/ScheduleSkeleton.vue';
import { getChildren, getChildLessons } from '../../api/client.js';
import Swal from 'sweetalert2';

// --- СОСТОЯНИЕ ---
const children        = ref([]);
const lessons         = ref([]);
const loading         = ref(true);
const showLessonModal = ref(false);
const selectedLesson  = ref(null);

// Текущий диапазон и режим лога — приходят из WeeklyCalendar через @date-change.
// Не реактивный ref: нам не нужен watcher, только актуальное значение при вызове loadLessons.
let currentRange = { weekStart: null, weekEnd: null, showFullLog: false };

// Защита от race condition: если пользователь быстро листает недели,
// игнорируем ответы от предыдущих запросов.
let loadRequestId = 0;

// --- ЗАГРУЗКА ---

async function loadChildren() {
  try {
    children.value = await getChildren();
  } catch (e) {
    console.error('Ошибка загрузки детей:', e);
    Swal.fire({
      icon: 'error',
      title: 'Ошибка загрузки',
      text: 'Не удалось получить список учеников',
      background: '#111827',
      color: '#fff',
    });
  } finally {
    loading.value = false;
  }
}

async function loadLessons() {
  const requestId = ++loadRequestId;

  try {
    const { weekStart, weekEnd, showFullLog } = currentRange;

    // В обычном режиме грузим текущую неделю + 4 недели вперёд,
    // чтобы счётчик "В будущем" в WeeklyCalendar видел запланированные уроки.
    // В сетке всё равно отображается только текущая неделя (getLessonsForDay фильтрует по дню).
    const lookahead = new Date(weekEnd);
    lookahead.setDate(lookahead.getDate() + 28);

    const startStr = showFullLog ? '2020-01-01' : weekStart.toISOString().split('T')[0];
    const endStr   = showFullLog ? '2029-12-31' : lookahead.toISOString().split('T')[0];

    const results = await Promise.all(
      children.value.map(child =>
        getChildLessons(child.child_id, startStr, endStr).catch(err => {
          console.error(`Ошибка загрузки уроков child_id=${child.child_id}:`, err);
          return [];
        })
      )
    );

    // Если пока ждали ответа успел запуститься новый запрос — отбрасываем устаревший результат
    if (requestId !== loadRequestId) return;

    lessons.value = results.flat();
  } catch (e) {
    console.error('Ошибка в loadLessons:', e);
    Swal.fire({
      icon: 'error',
      title: 'Ошибка загрузки',
      text: 'Не удалось получить данные расписания',
      background: '#111827',
      color: '#fff',
    });
  }
}

// --- UI-ЛОГИКА ---

// WeeklyCalendar эмитит @date-change при монтировании и при каждой смене недели/режима лога.
// Это единственная точка входа для обновления диапазона и перезагрузки уроков.
function onDateChange(range) {
  currentRange = range;
  loadLessons();
}

// --- МОДАЛКА ---

function handleCellClick({ dateStr, hour }) {
  selectedLesson.value = {
    date:          dateStr,
    time:          `${String(hour).padStart(2, '0')}:00`,
    child_id:      null,
    status:        'planned',
    theme:         '',
    homework_done: false,
    grade:         null,
  };
  showLessonModal.value = true;
}

function editLesson(lesson) {
  const [date, fullTime] = lesson.lesson_datetime.split('T');
  selectedLesson.value   = { ...lesson, date, time: fullTime.substring(0, 5) };
  showLessonModal.value  = true;
}

// --- ИНИЦИАЛИЗАЦИЯ ---

onMounted(async () => {
  // Загружаем детей. После этого скелетон скрывается и монтируется WeeklyCalendar,
  // который сам эмитит @date-change → onDateChange → loadLessons.
  // Явно вызывать loadLessons здесь не нужно.
  await loadChildren();
});
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