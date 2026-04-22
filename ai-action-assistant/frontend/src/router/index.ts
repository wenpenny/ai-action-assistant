import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/result/:id',
    name: 'Result',
    component: () => import('../views/Result.vue')
  },
  {
    path: '/history',
    name: 'History',
    component: () => import('../views/History.vue')
  },
  {
    path: '/history/:id',
    name: 'HistoryDetail',
    component: () => import('../views/HistoryDetail.vue')
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
