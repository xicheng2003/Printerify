import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductIntroView from '../views/ProductIntroView.vue'
import AuthView from '../views/AuthView.vue'
import ProfileView from '../views/ProfileView.vue'

// 引入新页面组件
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // ▼▼▼ 2. 修改和添加下面的路由配置 ▼▼▼
    {
      path: '/',
      name: 'intro', // 将 name 从 'home' 改为 'intro'
      component: ProductIntroView // 将 component 指向新创建的页面
    },
    {
      path: '/order',
      name: 'order',
      component: HomeView,
      meta: { title: '自助下单' }
    },
    {
      path: '/query',
      name: 'query',
      // 使用路由懒加载，优化性能
      component: () => import('../views/QueryView.vue'),
      meta: { title: '订单查询' }
    },
    // --- 新增的路由配置 ---
    {
      path: '/terms',
      name: 'terms',
      component: () => import('../views/TermsView.vue'),
      meta: { title: '关于' }
    },
    // 认证路由
    {
      path: '/auth/login',
      name: 'login',
      component: AuthView,
      meta: { title: '用户登录' },
      props: { isLogin: true }
    },
    {
      path: '/auth/register',
      name: 'register',
      component: AuthView,
      meta: { title: '用户注册' },
      props: { isLogin: false }
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { title: '个人资料' }
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