import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { title: '自助下单' }
    },
    {
      path: '/query',
      name: 'query',
      // 使用路由懒加载，优化性能
      component: () => import('../views/QueryView.vue'),
      meta: { title: '订单查询' }
    }
  ]
})

// 这是一个导航守卫，可以自动更新浏览器标签页的标题
router.beforeEach((to, from, next) => {
  const pageTitle = to.meta.title ? `${to.meta.title} - 自助打印服务` : '自助打印服务';
  document.title = pageTitle;
  next();
});

export default router
