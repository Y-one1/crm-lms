<template>
  <div>
    <Transition name="fade" mode="out-in">
      <PaymentTableSkeleton v-if="loading" key="skel" />

      <div v-else key="content">
        <div class="mb-6 flex justify-start">
          <button
            @click="showAddPaymentModal = true"
            class="px-6 py-3 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-semibold rounded-lg transition shadow-lg"
          >
            + Добавить оплату
          </button>
        </div>

        <div
          v-if="childPayments.length > 0"
          class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden"
        >
          <table class="w-full">
            <thead>
              <tr class="bg-gray-900 border-b border-gray-700">
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Дата</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Сумма</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Способ</th>
                <th class="px-6 py-4 text-left text-sm font-semibold text-gray-300">Родитель</th>
                <th class="px-6 py-4 text-right text-sm font-semibold text-gray-300"></th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="payment in childPayments"
                :key="payment.payment_id"
                class="border-b border-gray-700 hover:bg-gray-700/50 transition"
              >
                <td class="px-6 py-4 text-gray-300">{{ formatDateShort(payment.payment_date) }}</td>
                <td class="px-6 py-4">
                  <span class="text-emerald-400 font-bold text-lg">+{{ payment.amount }} ₽</span>
                </td>
                <td class="px-6 py-4 text-gray-300 capitalize">{{ methodLabel(payment.method) }}</td>
                <td class="px-6 py-4 text-gray-400 text-sm">{{ getParentName(payment.parent_id) }}</td>
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
          <p class="text-gray-400">Добавьте первую оплату</p>
        </div>

        <!-- Модалка добавления платежа -->
        <div
          v-if="showAddPaymentModal"
          class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
        >
          <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl">
            <div class="flex justify-between items-center mb-6">
              <h2 class="text-2xl font-bold text-white">Добавить оплату</h2>
              <button @click="showAddPaymentModal = false" class="text-gray-500 hover:text-white text-xl">✕</button>
            </div>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Сумма (₽) *</label>
                <input
                  type="number"
                  v-model.number="paymentForm.amount"
                  min="1"
                  step="1"
                  class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
                />
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Способ оплаты *</label>
                <select
                  v-model="paymentForm.method"
                  class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
                >
                  <option value="">Выберите...</option>
                  <option value="cash">💵 Наличные</option>
                  <option value="card">💳 Карта</option>
                  <option value="sbp">⚡ СБП</option>
                  <option value="bank_transfer">🏦 Банковский перевод</option>
                  <option value="online_payment">🌐 Онлайн-оплата</option>
                  <option value="qr_code">📱 QR-код</option>
                </select>
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Родитель *</label>
                <select
                  v-model.number="paymentForm.parent_id"
                  class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-blue-500 focus:outline-none"
                >
                  <option :value="null" disabled>Выберите родителя...</option>
                  <option v-for="p in childParents" :key="p.parent_id" :value="p.parent_id">
                    {{ p.last_name }} {{ p.first_name }}
                  </option>
                </select>
              </div>
              <div
                v-if="activeTariff"
                class="p-3 bg-blue-900/20 rounded-lg border border-blue-500/30 text-sm space-y-1"
              >
                <p class="text-gray-400">
                  Текущий долг:
                  <span class="text-red-400 font-bold">{{ activeTariff.tariff_period.debt }} ₽</span>
                </p>
                <p v-if="paymentForm.amount" class="text-gray-400">
                  После оплаты — долг:
                  <span
                    :class="Math.max(0, activeTariff.tariff_period.debt - paymentForm.amount) === 0 ? 'text-emerald-400' : 'text-red-400'"
                    class="font-bold"
                  >
                    {{ Math.max(0, activeTariff.tariff_period.debt - paymentForm.amount) }} ₽
                  </span>
                  <span v-if="paymentForm.amount > activeTariff.tariff_period.debt" class="text-emerald-400 ml-2">
                    (+{{ (paymentForm.amount - activeTariff.tariff_period.debt).toFixed(2) }} ₽ на баланс)
                  </span>
                </p>
              </div>
              <div class="flex gap-3 pt-2">
                <button
                  @click="submitPayment"
                  class="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-semibold transition"
                >
                  Сохранить
                </button>
                <button
                  @click="showAddPaymentModal = false"
                  class="flex-1 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-white font-semibold transition"
                >
                  Отмена
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
// name нужен для корректной работы KeepAlive
defineOptions({ name: 'ChildPaymentsTab' });

import { ref, onMounted } from 'vue';
import PaymentTableSkeleton from '../skeletons/PaymentTableSkeleton.vue';
import { getChildPayments, createPayment, deletePayment } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  childId:     { type: Number,  required: true },
  childParents:{ type: Array,   default: () => [] },
  activeTariff:{ type: Object,  default: null },
});

const emit = defineEmits(['payment-saved']);

// --- СОСТОЯНИЕ ---
const childPayments = ref([]);
const loading = ref(true);
const showAddPaymentModal = ref(false);
const paymentForm = ref({ amount: null, method: '', parent_id: null });

// --- ЗАГРУЗКА ---
async function loadPayments() {
  try {
    loading.value = true;
    childPayments.value = (await getChildPayments(props.childId, '2020-01-01', '2029-12-31'))
      .sort((a, b) => new Date(b.payment_date) - new Date(a.payment_date));
  } catch (e) {
    console.error('Ошибка загрузки платежей:', e);
  } finally {
    loading.value = false;
  }
}

onMounted(loadPayments);

// --- ДЕЙСТВИЯ ---
async function submitPayment() {
  if (!paymentForm.value.amount || !paymentForm.value.method || !paymentForm.value.parent_id) {
    return Swal.fire({ icon: 'warning', title: 'Заполните все поля', background: '#111827', color: '#fff' });
  }
  try {
    await createPayment({ ...paymentForm.value, child_id: props.childId });
    showAddPaymentModal.value = false;
    paymentForm.value = { amount: null, method: '', parent_id: null };
    await loadPayments();
    emit('payment-saved');
    Swal.fire({ icon: 'success', title: 'Оплата добавлена', timer: 1250, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

async function deletePaymentById(paymentId) {
  const result = await Swal.fire({
    icon: 'warning', title: 'Удалить платёж?',
    showCancelButton: true, confirmButtonText: 'Да', cancelButtonText: 'Отмена',
    confirmButtonColor: '#dc2626', background: '#111827', color: '#fff',
  });
  if (result.isConfirmed) {
    try {
      await deletePayment(paymentId);
      await loadPayments();
      emit('payment-saved');
      Swal.fire({ icon: 'success', title: 'Платёж удалён', timer: 1200, showConfirmButton: false, background: '#111827', color: '#fff' });
    } catch (e) {
      Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
    }
  }
}

// --- УТИЛИТЫ ---
const formatDateShort = (d) => new Date(d).toLocaleDateString('ru-RU');

function getParentName(parentId) {
  const p = props.childParents.find((p) => p.parent_id === parentId);
  return p ? `${p.last_name} ${p.first_name}` : '—';
}

function methodLabel(method) {
  const map = {
    cash: '💵 Наличные', card: '💳 Карта', sbp: '⚡ СБП',
    bank_transfer: '🏦 Перевод', online_payment: '🌐 Онлайн', qr_code: '📱 QR-код',
  };
  return map[method] || method;
}
</script>