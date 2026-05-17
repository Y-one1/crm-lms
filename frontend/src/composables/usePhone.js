import { ref } from 'vue';

/**
 * usePhone — composable для форматирования и валидации российского телефона.
 * Используется в ChildModal и ParentModal.
 *
 * Возвращает:
 *   phoneDisplay  — ref со строкой для <input> ("+7 (999) 123-45-67")
 *   phoneError    — ref с текстом ошибки (пустая строка = ок)
 *   phoneValue    — ref с нормализованным значением для отправки на бэкенд ("+79991234567")
 *   handlePhoneInput(event) — обработчик @input
 *   setPhone(rawString)     — заполнить поле из существующих данных (при редактировании)
 *   resetPhone()            — сбросить всё
 */
export function usePhone() {
  const phoneDisplay = ref('');
  const phoneError   = ref('');
  const phoneValue   = ref('');

  function formatDisplay(input) {
    let digits = input.replace(/\D/g, '');
    if (digits.startsWith('8')) digits = '7' + digits.slice(1);
    if (!digits.startsWith('7')) digits = '7' + digits;
    digits = digits.slice(0, 11);

    if (digits.length === 1) return '+7';
    if (digits.length <= 4)  return `+7 (${digits.slice(1)}`;
    if (digits.length <= 7)  return `+7 (${digits.slice(1, 4)}) ${digits.slice(4)}`;
    return `+7 (${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7, 9)}-${digits.slice(9, 11)}`;
  }

  function handlePhoneInput(e) {
    const digits = e.target.value.replace(/\D/g, '');
    if (digits.length > 11) {
      phoneError.value = '❌ Номер слишком длинный (макс. 11 цифр)';
      return;
    }
    phoneDisplay.value = formatDisplay(e.target.value);

    let normalized = digits;
    if (normalized.startsWith('8')) normalized = '7' + normalized.slice(1);
    if (!normalized.startsWith('7')) normalized = '7' + normalized;

    if (digits.length === 0) {
      phoneError.value = '';
      phoneValue.value = '';
    } else if (digits.length < 11) {
      phoneError.value = '⏳ Введи полный номер (11 цифр)';
      phoneValue.value = '';
    } else if (digits.length === 11 && (digits.startsWith('7') || digits.startsWith('8'))) {
      phoneError.value = '';
      phoneValue.value = '+' + normalized;
    } else {
      phoneError.value = '❌ Неверный формат';
      phoneValue.value = '';
    }
  }

  function setPhone(raw) {
    phoneDisplay.value = raw || '';
    phoneValue.value   = raw || '';
    phoneError.value   = '';
  }

  function resetPhone() {
    phoneDisplay.value = '';
    phoneValue.value   = '';
    phoneError.value   = '';
  }

  return { phoneDisplay, phoneError, phoneValue, handlePhoneInput, setPhone, resetPhone };
}