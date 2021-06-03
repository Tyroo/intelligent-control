import Vue from 'vue';
import VueRouter from 'vue-router';
import BaseContainer from '../views/Base/BaseContainer';

Vue.use(VueRouter);

const routes = [
  // 登录
  {
    path: '/Login',
    name: 'Login',
    component: () => import('@/views/Login/Login'),
    hidden: true,
  },
  // 登录后
  {
    path: '/',
    name: 'BaseContainer',
    component: BaseContainer,
    redirect: '/IntelligentLighting/DeviceControl',
    meta: { title: '智能照明', icon: 'bulb', requireAuth: true },
    children: [
      // -----------智能照明-----------
      {
        path: '/IntelligentLighting/DeviceControl', // 设备控制
        component: () => import('@/views/IntelligentLighting/DeviceControl'),
        meta: { title: '设备控制', level: 2, requireAuth: true },
      },
      {
        path: '/IntelligentLighting/DataAnalysis', // 数据分析
        component: () => import('@/views/IntelligentLighting/DataAnalysis'),
        meta: { title: '数据分析', level: 2, requireAuth: true },
      },
      {
        path: '/IntelligentLighting/TimerTaskManage', // 定时任务
        component: () => import('@/views/IntelligentLighting/TimerTaskManage'),
        meta: { title: '定时任务', level: 2, requireAuth: true },
      },
    ],
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.path !== '/Login') {
    const token = localStorage.getItem('x-token');
    if (token) next(); else next('/Login');
  } else next();
});

export default router;
