<template>
  <Layout>
    <div class="p-8">

      <div class="mb-8 flex justify-between items-start">
        <div>
          <h1 class="text-4xl font-black mb-2">
            {{ parent?.last_name }} {{ parent?.first_name }} {{ parent?.patronymic }}
          </h1>
          <div class="flex gap-6 text-gray-400 flex-wrap">
            <span class="capitalize">👤 {{ parent?.relationship }}</span>
            <span>📱 {{ parent?.phone_number }}</span>
            <span>📧 {{ parent?.email }}</span>
          </div>
        </div>
        <router-link
          to="/parents"
          class="px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition"
        >
          ← Назад
        </router-link>
      </div>

      <div class="flex gap-2 mb-6 border-b border-gray-700">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          class="px-4 py-3 font-semibold transition border-b-2"
          :class="
            activeTab === tab
              ? 'text-blue-400 border-blue-500'
              : 'text-gray-400 border-transparent hover:text-gray-300'
          "
        >
          {{ tabLabels[tab] }}
        </button>
      </div>

      <div class="mt-4">
        <KeepAlive>
          <ParentChildrenTab
            v-if="activeTab === 'children'"
            :parent-id="parentId"
            :parent-children="parentChildren"
            :all-children="allChildren"
            :loading="loadingChildren"
            @refresh-children="loadChildrenData"
          />
          <ParentPaymentsTab
            v-else-if="activeTab === 'payments'"
            :parent-id="parentId"
            :parent-children="parentChildren"
          />
          <ParentNotesTab
            v-else-if="activeTab === 'notes'"
            :parent-id="parentId"
            :parent="parent"
            :parent-children="parentChildren"
            @parent-updated="parent = $event"
          />
        </KeepAlive>
      </div>

    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Layout from '../../components/Layout.vue';
import ParentChildrenTab from '../../components/parent_detail/ParentChildrenTab.vue';
import ParentPaymentsTab from '../../components/parent_detail/ParentPaymentsTab.vue';
import ParentNotesTab    from '../../components/parent_detail/ParentNotesTab.vue';
import { getParent, getParentChildren, getChildren } from '../../api/client.js';

const route = useRoute();
const parentId = parseInt(route.params.id);

// --- СОСТОЯНИЕ ---
const parent = ref(null);
const activeTab = ref('children');

// Shared State — состояние, нужное нескольким вкладкам
const parentChildren = ref([]);
const allChildren = ref([]);
const loadingChildren = ref(true);

const tabs = ['children', 'payments', 'notes'];
const tabLabels = {
  children: '👨‍🎓 Ученики',
  payments: '🧾 Платежи',
  notes:    '📝 Заметки',
};

// --- ЗАГРУЗКА ДАННЫХ ---
async function loadParentData() {
  try {
    parent.value = await getParent(parentId);
  } catch (e) {
    console.error('Ошибка загрузки данных родителя:', e);
  }
}

async function loadChildrenData() {
  try {
    loadingChildren.value = true;
    // Загружаем детей, привязанных к родителю, и полный список для модалки привязки
    const [linked, all] = await Promise.all([
      getParentChildren(parentId),
      getChildren()
    ]);
    parentChildren.value = linked;
    allChildren.value = all;
  } catch (e) {
    console.error('Ошибка загрузки связей с учениками:', e);
  } finally {
    loadingChildren.value = false;
  }
}

onMounted(() => {
  loadParentData();
  loadChildrenData();
});
</script>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>