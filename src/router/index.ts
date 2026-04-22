import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { applySeo } from '../utils/seo'

declare module 'vue-router' {
  interface RouteMeta {
    title: string
    description?: string
  }
}

const djangoAdminUrl =
  import.meta.env.VITE_DJANGO_ADMIN_URL ||
  (import.meta.env.DEV ? 'http://localhost:8000/admin/' : '/admin/')

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: '首页', description: 'SkyBlog 首页，展示最新技术文章、热门文章、技术分类和项目作品。' },
  },
  {
    path: '/articles',
    name: 'Articles',
    component: () => import('../views/ArticleListView.vue'),
    meta: { title: '文章列表', description: '浏览 SkyBlog 已发布的技术文章，支持分类、标签和阅读量排序。' },
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: () => import('../views/ArticleDetailView.vue'),
    meta: { title: '文章详情', description: '阅读 SkyBlog 技术文章详情。' },
  },
  {
    path: '/category/:category',
    name: 'Category',
    component: () => import('../views/CategoryView.vue'),
    meta: { title: '分类', description: '按分类浏览 SkyBlog 技术文章。' },
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/ProjectsView.vue'),
    meta: { title: '项目作品', description: '查看 SkyBlog 展示的 Python、Vue、Django 和 AI 应用项目。' },
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutView.vue'),
    meta: { title: '关于我', description: '了解 SkyBlog 作者的技术方向、项目经历、技能栏和联系方式。' },
  },
  {
    path: '/login',
    name: 'LoginRedirect',
    component: () => import('../views/AdminRedirectView.vue'),
    props: { target: djangoAdminUrl },
    meta: { title: '跳转中', description: '正在跳转到 SkyBlog Django 管理后台。' },
  },
  {
    path: '/admin',
    name: 'AdminRedirect',
    component: () => import('../views/AdminRedirectView.vue'),
    props: { target: djangoAdminUrl },
    meta: { title: '跳转中', description: '正在跳转到 SkyBlog Django 管理后台。' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFoundView.vue'),
    meta: { title: '页面不存在', description: '你访问的页面不存在，返回 SkyBlog 首页或浏览文章列表。' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    }

    return { top: 0 }
  },
})

router.beforeEach((to) => {
  applySeo({
    title: to.meta.title,
    description: to.meta.description,
    path: to.fullPath,
  })
  return true
})

export default router
