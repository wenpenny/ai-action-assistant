import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { transition: 'slide' }
  },
  {
    path: '/result/:id',
    name: 'Result',
    component: () => import('../views/Result.vue'),
    meta: { transition: 'fade' }
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/History.vue'),
    meta: { transition: 'fade' }
  },
  {
    path: '/history/:id',
    name: 'HistoryDetail',
    component: () => import('../views/HistoryDetail.vue'),
    meta: { transition: 'fade' }
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
