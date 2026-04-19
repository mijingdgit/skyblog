<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { fetchPublicCategories, fetchPublishedArticles } from '../api/public'
import type { AdminArticle, AdminCategory } from '../types/admin'
import {
  buildTagCounts,
  categoryById,
  categoryBySlug,
  formatDate,
  getArticleDisplayDate,
  sortArticlesByLatest,
  sortArticlesByViews,
} from '../utils/content'

const route = useRoute()
const router = useRouter()

const categories = ref<AdminCategory[]>([])
const articles = ref<AdminArticle[]>([])
const activeCategory = ref('all')
const activeTag = ref('')
const sortBy = ref<'date' | 'views'>('date')
const isLoading = ref(true)
const loadError = ref('')

const tagCounts = computed(() => buildTagCounts(articles.value))

const filteredArticles = computed(() => {
  let result = [...articles.value]

  if (activeCategory.value !== 'all') {
    const category = categoryBySlug(categories.value, activeCategory.value)
    result = result.filter((article) => article.category === category?.id)
  }

  if (activeTag.value) {
    result = result.filter((article) => article.tags.some((tag) => tag.name === activeTag.value))
  }

  return sortBy.value === 'views' ? sortArticlesByViews(result) : sortArticlesByLatest(result)
})

function estimateReadTime(content: string) {
  const minutes = Math.max(1, Math.round(content.replace(/\s+/g, '').length / 500))
  return `${minutes} 分钟阅读`
}

function syncFiltersFromRoute() {
  const category = typeof route.query.category === 'string' ? route.query.category : 'all'
  const tag = typeof route.query.tag === 'string' ? route.query.tag : ''
  const sort = route.query.sort === 'views' ? 'views' : 'date'

  activeCategory.value = category
  activeTag.value = tag
  sortBy.value = sort
}

function syncRouteFromFilters() {
  const nextQuery: Record<string, string> = {}

  if (activeCategory.value !== 'all') {
    nextQuery.category = activeCategory.value
  }

  if (activeTag.value) {
    nextQuery.tag = activeTag.value
  }

  if (sortBy.value !== 'date') {
    nextQuery.sort = sortBy.value
  }

  if (JSON.stringify(route.query) !== JSON.stringify(nextQuery)) {
    void router.replace({ query: nextQuery })
  }
}

function setCategory(slug: string) {
  activeCategory.value = slug
  activeTag.value = ''
}

function toggleTag(tag: string) {
  activeTag.value = activeTag.value === tag ? '' : tag
}

function clearFilters() {
  activeCategory.value = 'all'
  activeTag.value = ''
  sortBy.value = 'date'
}

watch(
  () => route.query,
  () => {
    syncFiltersFromRoute()
  },
  { immediate: true },
)

watch([activeCategory, activeTag, sortBy], () => {
  syncRouteFromFilters()
})

onMounted(async () => {
  try {
    const [categoryData, articleData] = await Promise.all([
      fetchPublicCategories(),
      fetchPublishedArticles(),
    ])

    categories.value = categoryData
    articles.value = articleData
  } catch {
    loadError.value = '文章内容加载失败，请确认 Django API 已启动。'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="article-list">
    <section class="page-header">
      <div class="container">
        <h1 class="page-title">技术<span class="accent">文章</span></h1>
        <p class="page-desc">文章列表已经切换到 Django 后台发布数据。</p>
      </div>
    </section>

    <div class="container">
      <div class="content-layout">
        <aside class="sidebar">
          <div class="sidebar-section">
            <h3 class="sidebar-title">分类</h3>
            <div class="category-list">
              <button
                class="category-item"
                :class="{ active: activeCategory === 'all' }"
                @click="setCategory('all')"
              >
                <span class="cat-name">全部文章</span>
                <span class="cat-count">{{ articles.length }}</span>
              </button>
              <button
                v-for="category in categories"
                :key="category.id"
                class="category-item"
                :class="{ active: activeCategory === category.slug }"
                @click="setCategory(category.slug)"
              >
                <span class="cat-icon">{{ category.icon || category.name.slice(0, 1) }}</span>
                <span class="cat-name">{{ category.name }}</span>
                <span class="cat-count">{{ category.article_count }}</span>
              </button>
            </div>
          </div>

          <div class="sidebar-section">
            <h3 class="sidebar-title">标签</h3>
            <div class="tag-list">
              <button
                v-for="tag in tagCounts.slice(0, 12)"
                :key="tag.name"
                class="tag-item"
                :class="{ active: activeTag === tag.name }"
                @click="toggleTag(tag.name)"
              >
                {{ tag.name }}
                <span class="tag-count">{{ tag.count }}</span>
              </button>
            </div>
          </div>

          <div class="sidebar-section">
            <h3 class="sidebar-title">排序</h3>
            <div class="sort-options">
              <button
                class="sort-btn"
                :class="{ active: sortBy === 'date' }"
                @click="sortBy = 'date'"
              >
                最新发布
              </button>
              <button
                class="sort-btn"
                :class="{ active: sortBy === 'views' }"
                @click="sortBy = 'views'"
              >
                最多阅读
              </button>
            </div>
          </div>
        </aside>

        <main class="main-content">
          <div v-if="loadError" class="status-card error">
            {{ loadError }}
          </div>

          <div v-else-if="isLoading" class="status-card">
            正在加载文章列表...
          </div>

          <template v-else>
            <div v-if="activeCategory !== 'all' || activeTag" class="active-filters">
              <span class="filter-label">当前筛选</span>
              <span v-if="activeCategory !== 'all'" class="filter-tag">
                {{ categoryBySlug(categories, activeCategory)?.name || activeCategory }}
                <button @click="activeCategory = 'all'">×</button>
              </span>
              <span v-if="activeTag" class="filter-tag">
                {{ activeTag }}
                <button @click="activeTag = ''">×</button>
              </span>
              <button class="clear-btn" @click="clearFilters">清除筛选</button>
            </div>

            <div class="articles-list">
              <RouterLink
                v-for="article in filteredArticles"
                :key="article.id"
                :to="`/article/${article.id}`"
                class="article-item"
              >
                <div class="article-content">
                  <div class="article-header">
                    <span class="category-badge">
                      {{
                        categoryById(categories, article.category)?.icon ||
                        article.category_name?.slice(0, 1) ||
                        '未'
                      }}
                      {{ article.category_name || categoryById(categories, article.category)?.name || '未分类' }}
                    </span>
                    <span class="article-date">{{ formatDate(getArticleDisplayDate(article)) }}</span>
                  </div>
                  <h2 class="article-title">{{ article.title }}</h2>
                  <p class="article-excerpt">{{ article.excerpt }}</p>
                  <div class="article-meta">
                    <div class="tags">
                      <span v-for="tag in article.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
                    </div>
                    <div class="stats">
                      <span class="stat">{{ estimateReadTime(article.content) }}</span>
                      <span class="stat">{{ article.views }} 阅读</span>
                    </div>
                  </div>
                </div>
              </RouterLink>

              <div v-if="filteredArticles.length === 0" class="empty-state">
                <span class="empty-icon">暂无内容</span>
                <p>当前筛选条件下还没有已发布文章。</p>
                <button class="btn-reset" @click="clearFilters">恢复默认视图</button>
              </div>
            </div>
          </template>
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
.article-list {
  padding-bottom: 80px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.page-header {
  padding: 120px 0 60px;
  text-align: center;
}

.page-title {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 16px;
}

.page-title .accent {
  color: #00bfff;
}

.page-desc {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.6);
}

.content-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 40px;
}

.sidebar {
  position: sticky;
  top: 100px;
  height: fit-content;
}

.sidebar-section {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 24px;
}

.sidebar-title {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-bottom: 16px;
}

.category-list,
.sort-options {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-item,
.sort-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: none;
  border: 1px solid transparent;
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.7);
  cursor: pointer;
  transition: all 0.3s;
  text-align: left;
  width: 100%;
}

.category-item:hover,
.sort-btn:hover {
  background: rgba(0, 191, 255, 0.1);
}

.category-item.active,
.sort-btn.active {
  background: rgba(0, 191, 255, 0.15);
  border-color: rgba(0, 191, 255, 0.3);
  color: #00ffff;
}

.cat-name {
  flex: 1;
}

.cat-count {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.tag-item:hover {
  background: rgba(0, 191, 255, 0.1);
  border-color: rgba(0, 191, 255, 0.3);
}

.tag-item.active {
  background: rgba(0, 191, 255, 0.15);
  border-color: #00bfff;
  color: #00ffff;
}

.tag-count {
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.4);
}

.main-content {
  min-height: 60vh;
}

.status-card {
  padding: 18px 20px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 191, 255, 0.12);
  color: rgba(255, 255, 255, 0.82);
}

.status-card.error {
  border-color: rgba(255, 59, 48, 0.24);
  color: #ff918b;
}

.active-filters {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
  margin-bottom: 24px;
  padding: 16px 20px;
  background: rgba(0, 191, 255, 0.05);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 12px;
}

.filter-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

.filter-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  background: rgba(0, 191, 255, 0.15);
  border-radius: 20px;
  font-size: 0.85rem;
  color: #00ffff;
}

.filter-tag button {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  font-size: 1rem;
}

.clear-btn {
  margin-left: auto;
  padding: 6px 16px;
  background: none;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.clear-btn:hover {
  border-color: rgba(255, 255, 255, 0.4);
  color: #fff;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-item {
  display: block;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 16px;
  padding: 28px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.article-item:hover {
  background: rgba(0, 191, 255, 0.03);
  border-color: rgba(0, 191, 255, 0.3);
  transform: translateX(4px);
}

.article-header,
.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.article-header {
  margin-bottom: 12px;
}

.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: rgba(0, 191, 255, 0.1);
  border-radius: 20px;
  font-size: 0.8rem;
  color: #00bfff;
}

.article-date {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.4);
}

.article-title {
  font-size: 1.25rem;
  color: #fff;
  margin-bottom: 12px;
  line-height: 1.4;
  transition: color 0.3s;
}

.article-item:hover .article-title {
  color: #00ffff;
}

.article-excerpt {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.7;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 4px 12px;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
}

.stats {
  display: flex;
  gap: 16px;
}

.stat {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.4);
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-icon {
  display: block;
  margin-bottom: 16px;
  font-size: 1.1rem;
  color: #00bfff;
}

.empty-state p {
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 20px;
}

.btn-reset {
  padding: 10px 24px;
  background: rgba(0, 191, 255, 0.15);
  border: 1px solid rgba(0, 191, 255, 0.3);
  border-radius: 25px;
  color: #00bfff;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-reset:hover {
  background: rgba(0, 191, 255, 0.25);
  border-color: #00bfff;
}

@media (max-width: 900px) {
  .content-layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: static;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
  }

  .sidebar-section {
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 100px 0 40px;
  }

  .page-title {
    font-size: 1.8rem;
  }

  .sidebar {
    grid-template-columns: 1fr;
  }

  .article-item {
    padding: 20px;
  }

  .article-header,
  .article-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .clear-btn {
    margin-left: 0;
  }
}
</style>
