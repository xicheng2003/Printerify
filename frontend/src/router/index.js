import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ProductIntroView from '../views/ProductIntroView.vue'
import AuthView from '../views/AuthView.vue'
import ProfileView from '../views/ProfileView.vue'
import OAuthCallbackView from '@/views/OAuthCallbackView.vue'
import { useUserStore } from '@/stores/user'

// 引入新页面组件
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  // 配置页面切换时的滚动行为
  scrollBehavior(to, from, savedPosition) {
    // 如果有保存的滚动位置（如浏览器前进/后退）
    if (savedPosition) {
      return savedPosition
    }
    // 如果有锚点（如 #section）
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    // 默认情况：回到页面顶部
    return { top: 0, behavior: 'smooth' }
  },
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
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: { title: '关于我们' }
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('../views/TermsView.vue'),
      meta: { title: '服务条款' }
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: () => import('../views/PrivacyView.vue'),
      meta: { title: '隐私政策' }
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
      meta: {
        title: '个人资料',
        requiresAuth: true // 需要登录
      }
    },
    // OAuth回调页面
    {
      path: '/oauth/callback',
      name: 'oauth-callback',
      component: OAuthCallbackView,
      meta: {
        title: 'OAuth登录回调'
      }
    },
    // 套餐购买页面
    {
      path: '/packages',
      name: 'packages',
      component: () => import('../views/PackageView.vue'),
      meta: {
        title: '打印套餐',
        requiresAuth: false
      }
    },
    // 404 页面 (必须放在最后)
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue'),
      meta: { title: '页面未找到' }
    }
  ]
})

// 路由守卫：检查认证状态
router.beforeEach(async (to, from, next) => {
  const pageTitle = to.meta.title ? `${to.meta.title} - 自助打印服务` : '自助打印服务';
  document.title = pageTitle;

  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    const userStore = useUserStore();

    // 如果用户未认证，尝试从本地存储恢复状态
    if (!userStore.isAuthenticated) {
      try {
        await userStore.initializeStore();
      } catch (error) {
        console.warn('Failed to initialize user store:', error);
      }
    }

    // 如果仍然未认证，重定向到登录页
    if (!userStore.isAuthenticated) {
      next({ name: 'login', query: { redirect: to.fullPath } });
      return;
    }
  }

  // 如果已登录用户访问登录/注册页，重定向到首页
  if ((to.name === 'login' || to.name === 'register') && useUserStore().isAuthenticated) {
    next({ name: 'intro' });
    return;
  }

  next();
});

export default router
