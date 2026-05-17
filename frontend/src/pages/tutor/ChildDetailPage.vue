<template>
  <Layout>
    <div class="p-8">

      <!-- Шапка -->
      <div class="mb-8 flex justify-between items-start">
        <div>
          <h1 class="text-4xl font-black mb-2">
            {{ child?.last_name }} {{ child?.first_name }} {{ child?.patronymic }}
          </h1>
          <div class="flex gap-6 text-gray-400 flex-wrap">
            <span>📚 {{ child?.school_class }} класс</span>
            <span>📱 {{ child?.phone_number }}</span>
            <span v-if="child?.day_of_addition">📅 С {{ formatDateShort(child.day_of_addition) }}</span>
            <span
              :class="child?.balance > 0 ? 'text-emerald-400' : child?.balance < 0 ? 'text-red-400' : 'text-gray-500'"
              class="font-semibold"
            >
              💳 Баланс: {{ child?.balance ?? 0 }} ₽
            </span>
          </div>
        </div>
        <router-link to="/children" class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition">
          ← Назад
        </router-link>
      </div>

      <!-- Вкладки -->
      <div class="flex gap-2 mb-6 border-b border-gray-700">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          class="px-4 py-3 font-semibold transition border-b-2"
          :class="activeTab === tab
            ? 'text-blue-400 border-blue-500'
            : 'text-gray-400 border-transparent hover:text-gray-300'"
        >
          {{ tabLabels[tab] }}
        </button>
      </div>

      <!-- Контент вкладок — KeepAlive сохраняет состояние при переключении,
           скелетон показывается только при первом монтировании каждого таба -->
      <KeepAlive>
        <ChildScheduleTab
          v-if="activeTab === 'schedule'"
          key="schedule"
          :child-id="childId"
        />
        <ChildParentsTab
          v-else-if="activeTab === 'parents'"
          key="parents"
          :child-id="childId"
          @parents-loaded="childParents = $event"
        />
        <ChildPaymentsTab
          v-else-if="activeTab === 'payments'"
          key="payments"
          :child-id="childId"
          :child-parents="childParents"
          :active-tariff="activeTariffForPayments"
          @payment-saved="loadChild"
        />
        <ChildTariffTab
          v-else-if="activeTab === 'tariff'"
          key="tariff"
          :child-id="childId"
          :child-balance="child?.balance ?? 0"
          @tariff-changed="loadChild"
          @active-tariff-updated="activeTariffForPayments = $event"
        />
        <ChildNotesTab
          v-else-if="activeTab === 'notes'"
          key="notes"
          :child-id="childId"
          :child="child"
          @child-updated="child = $event"
        />
        <ChildPerformanceTab
          v-else-if="activeTab === 'performance'"
          key="performance"
          :child-id="childId"
          :child-name="child ? `${child.first_name} ${child.last_name}` : 'ученик'"
        />
      </KeepAlive>

    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Layout from '../../components/Layout.vue';
import ChildScheduleTab     from '../../components/child_detail/ChildScheduleTab.vue';
import ChildParentsTab      from '../../components/child_detail/ChildParentsTab.vue';
import ChildPaymentsTab     from '../../components/child_detail/ChildPaymentsTab.vue';
import ChildTariffTab       from '../../components/child_detail/ChildTariffTab.vue';
import ChildNotesTab        from '../../components/child_detail/ChildNotesTab.vue';
import ChildPerformanceTab  from '../../components/child_detail/ChildPerformanceTab.vue';
import { getChild, getChildParents } from '../../api/client.js';

const route = useRoute();
const childId = parseInt(route.params.id);

// --- СОСТОЯНИЕ ---
const child = ref(null);
// childParents нужен двум вкладкам — поднимаем сюда
const childParents = ref([]);
// activeTariff нужен вкладке платежей для отображения долга
const activeTariffForPayments = ref(null);

const activeTab = ref('schedule');
const tabs = ['schedule', 'parents', 'payments', 'tariff', 'notes', 'performance'];
const tabLabels = {
  schedule:    '📅 Расписание',
  parents:     '👨‍👩‍👧 Родители',
  payments:    '🧾 Платежи',
  tariff:      '💰 Тариф',
  notes:       '📝 Заметки',
  performance: '📊 Успеваемость',
};

// --- ЗАГРУЗКА ---
async function loadChild() {
  const [childData, parents] = await Promise.all([
    getChild(childId),
    getChildParents(childId),
  ]);
  child.value = childData;
  childParents.value = parents;
}

onMounted(loadChild);

// --- УТИЛИТЫ ---
const formatDateShort = (d) => new Date(d).toLocaleDateString('ru-RU');
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

<style scoped>
input[type="date"]::-webkit-calendar-picker-indicator {
  filter: invert(1);
}
</style>