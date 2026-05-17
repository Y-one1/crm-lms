<template>
  <Teleport to="body">
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
      <div class="bg-gray-900 rounded-2xl p-8 w-full max-w-md border border-gray-700 shadow-2xl">

        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-white">
            {{ initialData ? 'Редактировать тариф' : 'Новый тариф' }}
          </h2>
          <button @click="$emit('close')" class="text-gray-500 hover:text-white transition text-xl">✕</button>
        </div>

        <form @submit.prevent="submit" class="space-y-4">

          <!-- Название тарифа -->
          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Название *</label>
            <input
              v-model="form.name"
              type="text"
              required
              placeholder="например: Базовый пакет"
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 focus:outline-none transition"
            />
          </div>

          <!-- Цена -->
          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Цена (₽) *</label>
            <input
              v-model.number="form.price"
              type="number"
              required
              min="1"
              placeholder="0"
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 focus:outline-none transition"
            />
          </div>

          <!-- Количество занятий -->
          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Количество занятий *</label>
            <input
              v-model.number="form.num_of_lessons"
              type="number"
              required
              min="1"
              placeholder="10"
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 focus:outline-none transition"
            />
          </div>

          <!-- Тип тарифа -->
          <div>
            <label class="block text-sm font-semibold text-gray-500 uppercase mb-1">Тип тарифа *</label>
            <select
              v-model="form.tariff_type"
              required
              class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 focus:outline-none transition"
            >
              <option value="">Выберите тип...</option>
              <option value="basic">📚 Базовый</option>
              <option value="starter">⭐ Начальный</option>
              <option value="standard">✨ Стандартный</option>
              <option value="advanced">🚀 Продвинутый</option>
              <option value="premium">👑 Премиум</option>
              <option value="enterprise">💎 Корпоративный</option>
            </select>
          </div>

          <!-- Информация о цене за занятие -->
          <div v-if="form.price && form.num_of_lessons" class="p-3 bg-emerald-900/20 rounded-lg border border-emerald-500/30">
            <p class="text-xs text-gray-400 mb-1">Цена за одно занятие</p>
            <p class="text-lg font-bold text-emerald-400">
              {{ (form.price / form.num_of_lessons).toFixed(0) }} ₽
            </p>
          </div>

          <!-- Кнопки -->
          <div class="flex gap-3 pt-2">
            <button
              type="submit"
              class="flex-1 px-4 py-2 bg-emerald-600 hover:bg-emerald-700 rounded-lg text-white font-semibold transition"
            >
              {{ initialData ? 'Обновить' : 'Создать' }}
            </button>
            <button
              type="button"
              @click="$emit('close')"
              class="flex-1 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-white font-semibold transition"
            >
              Отмена
            </button>
          </div>

        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue';
import { createTariff, updateTariff } from '../../api/client.js';
import Swal from 'sweetalert2';

const props = defineProps({
  initialData: { type: Object, default: null },
});

const emit = defineEmits(['close', 'saved']);

const defaultForm = () => ({
  name: '',
  price: null,
  num_of_lessons: null,
  tariff_type: '',
});

const form = ref(defaultForm());

watch(() => props.initialData, (data) => {
  if (data) {
    form.value = {
      name: data.name,
      price: data.price,
      num_of_lessons: data.num_of_lessons,
      tariff_type: data.tariff_type,
    };
  } else {
    form.value = defaultForm();
  }
}, { immediate: true });

async function submit() {
  if (!form.value.name?.trim()) {
    return Swal.fire({
      icon: 'warning',
      title: 'Укажите название тарифа',
      background: '#111827',
      color: '#fff',
    });
  }

  if (!form.value.price || form.value.price <= 0) {
    return Swal.fire({
      icon: 'warning',
      title: 'Укажите корректную цену',
      background: '#111827',
      color: '#fff',
    });
  }

  if (!form.value.num_of_lessons || form.value.num_of_lessons <= 0) {
    return Swal.fire({
      icon: 'warning',
      title: 'Укажите количество занятий',
      background: '#111827',
      color: '#fff',
    });
  }

  if (!form.value.tariff_type) {
    return Swal.fire({
      icon: 'warning',
      title: 'Выберите тип тарифа',
      background: '#111827',
      color: '#fff',
    });
  }

  try {
    let result;
    if (props.initialData) {
      result = await updateTariff(props.initialData.tariff_id, form.value);
    } else {
      result = await createTariff(form.value);
    }

    Swal.fire({
      icon: 'success',
      title: props.initialData ? 'Тариф обновлен' : 'Тариф создан',
      timer: 1250,
      showConfirmButton: false,
      background: '#111827',
      color: '#fff',
    });

    emit('saved', result);
    emit('close');
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
</script>
