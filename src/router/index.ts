import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

declare module 'vue-router' {
  interface RouteMeta {
    title: string
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
    meta: { title: '首页' },
  },
  {
    path: '/articles',
    name: 'Articles',
    component: () => import('../views/ArticleListView.vue'),
    meta: { title: '文章列表' },
  },
  {
    path: '/article/:id',
    name: 'ArticleDetail',
    component: () => import('../views/ArticleDetailView.vue'),
    meta: { title: '文章详情' },
  },
  {
    path: '/category/:category',
    name: 'Category',
    component: () => import('../views/CategoryView.vue'),
    meta: { title: '分类' },
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/ProjectsView.vue'),
    meta: { title: '项目作品' },
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/AboutView.vue'),
    meta: { title: '关于我' },
  },
  {
    path: '/login',
    name: 'LoginRedirect',
    component: () => import('../views/AdminRedirectView.vue'),
    props: { target: djangoAdminUrl },
    meta: { title: '跳转中' },
  },
  {
    path: '/admin',
    name: 'AdminRedirect',
    component: () => import('../views/AdminRedirectView.vue'),
    props: { target: djangoAdminUrl },
    meta: { title: '跳转中' },
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
  document.title = `${to.meta.title} | SkyBlog`
  return true
})

export default router
