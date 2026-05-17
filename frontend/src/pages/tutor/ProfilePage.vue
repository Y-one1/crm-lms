<template>
  <Layout>
    <div class="p-8 max-w-3xl mx-auto">

      <!-- Шапка -->
      <div class="mb-10">
        <div class="flex items-center gap-4 mb-2">
          <div class="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-cyan-500 flex items-center justify-center text-2xl font-black text-white shadow-lg">
            {{ initials }}
          </div>
          <div>
            <h1 class="text-3xl font-black text-white">{{ profileForm.tutor_name || user?.name || 'Профиль' }}</h1>
            <p class="text-gray-500 text-sm">{{ user?.email }}</p>
          </div>
        </div>
      </div>

      <div class="space-y-6">

        <!-- ===== СЕКЦИЯ: ПРОФИЛЬ ===== -->
        <div class="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden">
          <div class="flex justify-between items-center px-6 py-4 border-b border-gray-700">
            <h2 class="text-sm font-bold text-gray-400 uppercase tracking-wider">👤 Данные репетитора</h2>
            <button
              v-if="!editingProfile"
              @click="startEditProfile"
              class="px-4 py-1.5 text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
            >
              ✏️ Редактировать
            </button>
          </div>

          <div class="px-6 py-5">
            <!-- Просмотр -->
            <div v-if="!editingProfile" class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <p class="text-xs text-gray-500 uppercase mb-1">Имя</p>
                  <p class="text-white font-medium">{{ profileForm.tutor_name || '—' }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500 uppercase mb-1">Телефон</p>
                  <p class="text-white font-medium">{{ profileForm.tutor_phone || '—' }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500 uppercase mb-1">Предмет</p>
                  <p class="text-white font-medium">{{ profileForm.tutor_subject || '—' }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500 uppercase mb-1">Email</p>
                  <p class="text-white font-medium">{{ user?.email || '—' }}</p>
                </div>
              </div>
              <div v-if="profileForm.tutor_bio">
                <p class="text-xs text-gray-500 uppercase mb-1">О себе</p>
                <p class="text-gray-300 text-sm whitespace-pre-wrap">{{ profileForm.tutor_bio }}</p>
              </div>
            </div>

            <!-- Редактирование -->
            <div v-else class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Имя *</label>
                  <input
                    v-model="profileForm.tutor_name"
                    type="text"
                    placeholder="Иван Иванович"
                    class="w-full px-3 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Телефон</label>
                  <input
                    :value="phoneDisplay"
                    @input="handlePhoneInput"
                    type="text"
                    placeholder="+7 (900) 000-00-00"
                    class="w-full px-3 py-2 bg-gray-900 border rounded-lg text-white text-sm focus:outline-none transition"
                    :class="phoneError ? 'border-red-500 focus:border-red-500' : 'border-gray-600 focus:border-blue-500'"
                  />
                  <p v-if="phoneError" class="text-xs text-red-400 mt-1">{{ phoneError }}</p>
                </div>
                <div>
                  <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Предмет</label>
                  <input
                    v-model="profileForm.tutor_subject"
                    type="text"
                    placeholder="Математика"
                    class="w-full px-3 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
                  />
                </div>
                <div>
                  <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Email</label>
                  <input
                    :value="user?.email"
                    type="text"
                    disabled
                    class="w-full px-3 py-2 bg-gray-900/50 border border-gray-700 rounded-lg text-gray-500 text-sm cursor-not-allowed"
                  />
                </div>
              </div>
              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">О себе</label>
                <textarea
                  v-model="profileForm.tutor_bio"
                  rows="3"
                  placeholder="Коротко о себе, опыте, подходе к обучению..."
                  class="w-full px-3 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none resize-none"
                ></textarea>
              </div>
              <div class="flex gap-3">
                <button
                  @click="saveProfile"
                  class="px-5 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm font-semibold transition"
                >
                  Сохранить
                </button>
                <button
                  @click="editingProfile = false"
                  class="px-5 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white text-sm transition"
                >
                  Отмена
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ===== СЕКЦИЯ: РЕКВИЗИТЫ ===== -->
        <div class="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden">
          <div class="flex justify-between items-center px-6 py-4 border-b border-gray-700">
            <h2 class="text-sm font-bold text-gray-400 uppercase tracking-wider">💳 Реквизиты для оплаты</h2>
            <button
              v-if="!editingPayment"
              @click="startEditPayment"
              class="px-4 py-1.5 text-xs font-semibold bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
            >
              ✏️ Редактировать
            </button>
          </div>

          <div class="px-6 py-5">
            <div v-if="loadingPaymentDetails" class="text-gray-600 text-sm">Загрузка...</div>

            <div v-else-if="!editingPayment">
              <div v-if="profileForm.details_text" class="whitespace-pre-wrap text-gray-300 text-sm leading-relaxed bg-gray-900/50 rounded-xl p-4 border border-gray-700 font-mono">{{ profileForm.details_text }}</div>
              <div v-else class="text-center py-8">
                <div class="text-4xl mb-3">💳</div>
                <p class="text-gray-600 text-sm">Реквизиты ещё не добавлены</p>
                <button
                  @click="startEditPayment"
                  class="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm rounded-lg transition"
                >
                  + Добавить
                </button>
              </div>
            </div>

            <div v-else class="space-y-4">
              <div>
                <label class="block text-xs font-semibold text-gray-500 uppercase mb-1">Текст реквизитов</label>
                <textarea
                  v-model="paymentDetailsForm"
                  rows="6"
                  placeholder="Номер карты: 4276 XXXX XXXX XXXX&#10;Получатель: Иван Иванович И.&#10;Банк: Сбербанк&#10;&#10;СБП: +7 900 000 00 00&#10;&#10;Комментарий к переводу: за обучение"
                  class="w-full px-3 py-2 bg-gray-900 border border-gray-600 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none resize-none font-mono"
                ></textarea>
                <p class="text-xs text-gray-600 mt-1">Этот текст будут видеть ученики в личном кабинете</p>
              </div>
              <div class="flex gap-3">
                <button
                  @click="savePaymentDetails"
                  class="px-5 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white text-sm font-semibold transition"
                >
                  Сохранить
                </button>
                <button
                  @click="editingPayment = false"
                  class="px-5 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg text-white text-sm transition"
                >
                  Отмена
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- ===== СЕКЦИЯ: БЕЗОПАСНОСТЬ ===== -->
        <div class="bg-gray-800 rounded-2xl border border-gray-700 overflow-hidden">
          <div class="px-6 py-4 border-b border-gray-700">
            <h2 class="text-sm font-bold text-gray-400 uppercase tracking-wider">🔐 Выход из системы</h2>
          </div>
          <div class="px-6 py-5 flex items-center justify-between">
            <p class="text-sm text-gray-500">Завершить текущую сессию</p>
            <button
              @click="handleLogout"
              class="px-5 py-2 bg-red-900/40 hover:bg-red-900/70 border border-red-800 text-red-300 hover:text-red-100 text-sm font-semibold rounded-lg transition"
            >
              Выйти
            </button>
          </div>
        </div>

      </div>
    </div>
  </Layout>
</template>

<script setup>
// --- ИМПОРТЫ ---
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { usePhone } from '../../composables/usePhone.js';
import Layout from '../../components/Layout.vue';
import { user, logout, saveTutorProfile } from '../../stores/auth.js';
import { createPaymentDetails, getLatestPaymentDetails, updatePaymentDetails } from '../../api/client.js';
import Swal from 'sweetalert2';

const router = useRouter();
const { phoneDisplay, phoneError, phoneValue, handlePhoneInput, setPhone, resetPhone } = usePhone();

// --- СОСТОЯНИЕ ---

const editingProfile = ref(false);
const editingPayment = ref(false);
const loadingPaymentDetails = ref(true);
const currentDetailsId = ref(null);

const profileForm = ref({
  tutor_name:    '',
  tutor_phone:   '',
  tutor_subject: '',
  tutor_bio:     '',
  details_text:  '',
});

const paymentDetailsForm = ref('');

// --- ЗАГРУЗКА ---

async function loadData() {
  try {
    loadingPaymentDetails.value = true;
    const data = await getLatestPaymentDetails();
    currentDetailsId.value = data.payment_details_id;
    profileForm.value = {
      tutor_name:    data.tutor_name    || '',
      tutor_phone:   data.tutor_phone   || '',
      tutor_subject: data.tutor_subject || '',
      tutor_bio:     data.tutor_bio     || '',
      details_text:  data.details_text  || '',
    };
    if (data.tutor_name) saveTutorProfile({ name: data.tutor_name });
  } catch {
    // записей ещё нет — норм
  } finally {
    loadingPaymentDetails.value = false;
  }
}

onMounted(loadData);

// --- МОДАЛКА / UI-логика ---

function startEditProfile() {
  setPhone(profileForm.value.tutor_phone);
  editingProfile.value = true;
}

function startEditPayment() {
  paymentDetailsForm.value = profileForm.value.details_text;
  editingPayment.value = true;
}

// --- ВСПОМОГАТЕЛЬНЫЕ ---

async function persistDetails(patch) {
  const payload = {
    details_text:  profileForm.value.details_text  || '',
    tutor_name:    profileForm.value.tutor_name    || '',
    tutor_phone:   profileForm.value.tutor_phone   || '',
    tutor_subject: profileForm.value.tutor_subject || '',
    tutor_bio:     profileForm.value.tutor_bio     || '',
    ...patch,
  };
  if (currentDetailsId.value) {
    return updatePaymentDetails(currentDetailsId.value, payload);
  }
  return createPaymentDetails(payload);
}

// --- ДЕЙСТВИЯ ---

async function saveProfile() {
  if (!profileForm.value.tutor_name?.trim()) {
    return Swal.fire({ icon: 'warning', title: 'Введите имя', background: '#111827', color: '#fff' });
  }
  if (phoneDisplay.value && !phoneValue.value) {
    return Swal.fire({ icon: 'warning', title: 'Неверный формат телефона', text: 'Введите полный номер +7XXXXXXXXXX', background: '#111827', color: '#fff' });
  }
  profileForm.value.tutor_phone = phoneValue.value;
  try {
    await persistDetails({
      tutor_name:    profileForm.value.tutor_name.trim(),
      tutor_phone:   profileForm.value.tutor_phone,
      tutor_subject: profileForm.value.tutor_subject.trim(),
      tutor_bio:     profileForm.value.tutor_bio.trim(),
    });
    saveTutorProfile({ name: profileForm.value.tutor_name });
    editingProfile.value = false;
    await loadData();
    Swal.fire({ icon: 'success', title: 'Профиль сохранён', timer: 1200, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

async function savePaymentDetails() {
  if (!paymentDetailsForm.value.trim()) {
    return Swal.fire({ icon: 'warning', title: 'Введите реквизиты', background: '#111827', color: '#fff' });
  }
  try {
    await persistDetails({ details_text: paymentDetailsForm.value.trim() });
    editingPayment.value = false;
    await loadData();
    Swal.fire({ icon: 'success', title: 'Реквизиты сохранены', timer: 1200, showConfirmButton: false, background: '#111827', color: '#fff' });
  } catch (e) {
    Swal.fire({ icon: 'error', title: 'Ошибка', text: e.message, background: '#111827', color: '#fff' });
  }
}

function handleLogout() {
  logout();
  router.push('/login');
}

// --- УТИЛИТЫ ---

const initials = computed(() => {
  const name = profileForm.value.tutor_name || user.value?.name || '';
  return name.split(' ').map(w => w[0]).slice(0, 2).join('').toUpperCase() || '?';
});
</script>