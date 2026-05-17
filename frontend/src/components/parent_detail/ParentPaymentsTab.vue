<template>
  <div>
    <Transition name="fade" mode="out-in">
      <PaymentTableSkeleton v-if="loading" key="skel" />

      <div v-else key="content">
        <div
          v-if="parentPayments.length > 0"
          class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden"
        >
          <table class="w-full">
            <thead>
              <tr class="bg-gray-900 border-b border-gray-700">
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Дата</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Ученик</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Сумма</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Способ</th>
                <th class="px-6 py-4 text-right text-sm font-semibold text-gray-300"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="payment in parentPayments"
                :key="payment.payment_id"
                class="border-b border-gray-700 hover:bg-gray-700/50 transition"
              >
                <td class="px-6 py-4 text-gray-300">
                  {{ formatDate(payment.payment_date) }}
                </td>
                <td class="px-6 py-4 text-gray-300">
                  {{ getChildName(payment.child_id) }}
                </td>
                <td class="px-6 py-4">
                  <span class="text-emerald-400 font-bold text-lg">
                    +{{ payment.amount }} ₽
                  </span>
                </td>
                <td class="px-6 py-4 text-gray-300 capitalize">
                  {{ methodLabel(payment.method) }}
                </td>
                <td class="px-6 py-4 text-right">
                  <button
                    @click="deletePaymentById(payment.payment_id)"
                    class="px-3 py-1 text-xs bg-red-900/30 hover:bg-red-900/60 text-red-400 rounded transition"
                  >
                    🗑
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-else class="text-center py-16">
          <div class="text-6xl mb-4">🧾</div>
          <h2 class="text-2xl font-bold text-white mb-2">Платежей ещё нет</h2>
          <p class="text-gray-400">Платежи появятся после первой оплаты</p>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
defineOptions({ name: 'ParentPaymentsTab' });

import { ref, onMounted } from 'vue';
import PaymentTableSkeleton from '../skeletons/PaymentTableSkeleton.vue';
import { getParentPayments, deletePayment } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  parentId: { type: Number, required: true },
  parentChildren: { type: Array, required: true }
});

const parentPayments = ref([]);
const loading = ref(true);

async function loadPayments() {
  try {
    loading.value = true;
    parentPayments.value = await getParentPayments(props.parentId);
  } catch (e) {
    console.error('Ошибка загрузки платежей:', e);
  } finally {
    loading.value = false;
  }
}

onMounted(loadPayments);

async function deletePaymentById(paymentId) {
  const result = await Swal.fire({
    icon: 'warning',
    title: 'Удалить платёж?',
    showCancelButton: true,
    confirmButtonText: 'Да',
    cancelButtonText: 'Отмена',
    confirmButtonColor: '#dc2626',
    background: '#111827',
    color: '#fff',
  });
  if (result.isConfirmed) {
    try {
      await deletePayment(paymentId);
      await loadPayments();
      Swal.fire({
        icon: 'success',
        title: 'Платёж удалён',
        timer: 1200,
        showConfirmButton: false,
        background: '#111827',
        color: '#fff',
      });
    } catch (e) {
      Swal.fire({
        icon: 'error',
        title: 'Ошибка',
        text: e.message,
        background: '#111827',
        color: '#fff',
      });
    }
  }
}

// --- УТИЛИТЫ ---
const formatDate = (d) => new Date(d).toLocaleDateString('ru-RU');

function getChildName(childId) {
  const c = props.parentChildren.find(c => c.child_id === childId);
  return c ? `${c.last_name} ${c.first_name}` : '—';
}

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
</script>