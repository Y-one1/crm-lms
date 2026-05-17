import { createRouter, createWebHistory } from 'vue-router';
import { isAuthenticated, userRole } from './stores/auth.js';

import LoginPage from            './pages/LoginPage.vue';
import SchedulePage from         './pages/tutor/SchedulePage.vue';
import ChildrenPage from         './pages/tutor/ChildrenPage.vue';
import ChildDetailPage from      './pages/tutor/ChildDetailPage.vue';
import ParentDetailPage from     './pages/tutor/ParentDetailPage.vue';
import ParentsPage from          './pages/tutor/ParentsPage.vue';
import TariffsPage from          './pages/tutor/TariffsPage.vue';
import PaymentsPage from         './pages/tutor/PaymentsPage.vue';
import ProfilePage from          './pages/tutor/ProfilePage.vue';
import StudentDashboardPage from './pages/student/StudentDashboardPage.vue';

const routes = [
  {
    path: '/login',
    component: LoginPage,
    meta: { public: true },
  },
  {
    path: '/schedule',
    component: SchedulePage,
    meta: { requiresAuth: true, role: 'tutor' },
  },
  {
    path: '/children',
    component: ChildrenPage,
    meta: { requiresAuth: true, role: 'tutor' },
  },
  {
    path: '/children/:id',
    component: ChildDetailPage,
    meta: { requiresAuth: true, role: 'tutor' },
  },
  {
    path: '/parents',
    component: ParentsPage,
    meta: { requiresAuth: true, role: 'tutor' },
  },
  {
    path: '/parents/:id',
    component: ParentDetailPage,
    meta: { requiresAuth: true, role: 'tutor' },
  },
  {
    path: '/tariffs',
    component: TariffsPage,
    meta: { requiresAuth: true, role: 'tutor' },
  },
  {
    path: '/payments',
    component: PaymentsPage,
    meta: { requiresAuth: true, role: 'tutor' },
  },
  {
    path: '/profile',
    component: ProfilePage,
    meta: { requiresAuth: true, role: 'tutor' }
  },
  {
    path: '/my/dashboard',
    component: StudentDashboardPage,
    meta: { requiresAuth: true, role: 'student' },
  },
  // Редирект по умолчанию
  {
    path: '/',
    redirect: () => {
      if (!isAuthenticated.value) return '/login';
      return userRole.value === 'tutor' ? '/schedule' : '/my/dashboard';
    },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Защита маршрутов
router.beforeEach((to, from) => {
  const requiresAuth = to.meta.requiresAuth;
  const requiredRole = to.meta.role;
  const isPublic = to.meta.public;

  if (isPublic) {
    return true;
  }

  if (requiresAuth && !isAuthenticated.value) {
    // Не залогинен — редирект на login
    return '/login';
  }

  if (requiredRole && userRole.value !== requiredRole) {
    // Залогинен, но не та роль — редирект на главный экран своей роли
    const defaultRoute = userRole.value === 'tutor' ? '/schedule' : '/my/dashboard';
    return defaultRoute;
  }

  return true;
});

export default router;