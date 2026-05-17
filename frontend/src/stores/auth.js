import { ref } from 'vue';

// Глобальное состояние пользователя
export const user = ref(null);
export const isAuthenticated = ref(false);
export const userRole = ref(null); // 'tutor' или 'student'

// Функция входа (пока без реального бэкенда)
export function login(email, password) {
  const isTutor = email.includes('tutor') || email === 'teacher@example.com';

  // Для тестирования используется ID=1 (или другой существующий в БД)
  // Это Тестовый Тест
  const studentId = isTutor ? null : 1;

  user.value = {
    email,
    name: isTutor ? 'Репетитор' : 'Ученик',
    phone: '',
    subject: '',
    id: studentId,  // ← Теперь это реальный ID
  };
  
  userRole.value = isTutor ? 'tutor' : 'student';
  isAuthenticated.value = true;
  
  localStorage.setItem('user', JSON.stringify({ email, role: userRole.value, id: studentId }));
}

// Функция выхода
export function logout() {
  user.value = null;
  userRole.value = null;
  isAuthenticated.value = false;
  localStorage.removeItem('user');
}

// При загрузке приложения восстанавливаем сессию
export function restoreSession() {
  const saved = localStorage.getItem('user');
  if (saved) {
    // Шаг 1: Добавляем id в деструктуризацию
    const { email, role, id } = JSON.parse(saved); 
    const savedProfile = JSON.parse(localStorage.getItem('tutor_profile') || '{}');
    
    // Шаг 2: Прокидываем id обратно в реактивное состояние
    user.value = {
      email,
      name: savedProfile.name || (role === 'tutor' ? 'Репетитор' : 'Ученик'),
      phone: savedProfile.phone || '',
      subject: savedProfile.subject || '',
      id: id, // <-- ВОТ ТУТ ОН ВОЗВРАЩАЕТСЯ К ЖИЗНИ
    };
    userRole.value = role;
    isAuthenticated.value = true;
  }
}

// Новая функция — сохраняет профиль репетитора
export function saveTutorProfile(data) {
  localStorage.setItem('tutor_profile', JSON.stringify(data));
  user.value = { ...user.value, ...data };
}