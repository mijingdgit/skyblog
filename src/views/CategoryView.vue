<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { fetchPublicCategories, fetchPublishedArticles } from '../api/public'
import type { AdminArticle, AdminCategory } from '../types/admin'
import { categoryBySlug, formatDate, getArticleDisplayDate, sortArticlesByLatest } from '../utils/content'

const route = useRoute()

const categories = ref<AdminCategory[]>([])
const articles = ref<AdminArticle[]>([])
const isLoading = ref(true)
const loadError = ref('')

const categorySlug = computed(() => String(route.params.category || ''))
const category = computed(() => categoryBySlug(categories.value, categorySlug.value))
const currentArticles = computed(() =>
  sortArticlesByLatest(
    articles.value.filter((article) => article.category === (category.value?.id ?? -1)),
  ),
)

async function loadCategoryPage() {
  isLoading.value = true
  loadError.value = ''

  try {
    const [categoryData, articleData] = await Promise.all([
      fetchPublicCategories(),
      fetchPublishedArticles(),
    ])

    categories.value = categoryData
    articles.value = articleData

    if (!categoryBySlug(categoryData, categorySlug.value)) {
      loadError.value = '未找到对应的分类。'
    }
  } catch {
    loadError.value = '分类内容加载失败，请确认 Django API 已启动。'
  } finally {
    isLoading.value = false
  }
}

watch(
  () => route.params.category,
  async () => {
    await loadCategoryPage()
  },
  { immediate: true },
)
</script>

<template>
  <div class="category-page">
    <div v-if="isLoading" class="status-wrap">
      <div class="container">
        <div class="status-card">正在加载分类内容...</div>
      </div>
    </div>

    <div v-else-if="loadError || !category" class="not-found">
      <div class="container">
        <h1>分类不存在</h1>
        <p>{{ loadError || '抱歉，您访问的分类不存在。' }}</p>
        <RouterLink to="/articles" class="back-link">返回文章列表</RouterLink>
      </div>
    </div>

    <template v-else>
      <section class="page-header">
        <div class="container">
          <div class="breadcrumb">
            <RouterLink to="/">首页</RouterLink>
            <span>/</span>
            <RouterLink to="/articles">文章</RouterLink>
            <span>/</span>
            <span class="current">{{ category.name }}</span>
          </div>

          <div class="category-header">
            <span class="category-icon">{{ category.icon || category.name.slice(0, 1) }}</span>
            <div class="category-info">
              <h1 class="category-name">{{ category.name }}</h1>
              <p class="category-desc">{{ category.description || '这里会展示该分类下的已发布文章。' }}</p>
              <span class="article-count">{{ currentArticles.length }} 篇文章</span>
            </div>
          </div>
        </div>
      </section>

      <section class="articles-section">
        <div class="container">
          <div class="articles-grid">
            <RouterLink
              v-for="article in currentArticles"
              :key="article.id"
              :to="`/article/${article.id}`"
              class="article-card"
            >
              <div class="article-meta">
                <span class="category-tag">{{ category.icon || category.name.slice(0, 1) }} {{ category.name }}</span>
                <span class="date">{{ formatDate(getArticleDisplayDate(article)) }}</span>
              </div>
              <h2 class="article-title">{{ article.title }}</h2>
              <p class="article-excerpt">{{ article.excerpt }}</p>
              <div class="article-footer">
                <div class="tags">
                  <span v-for="tag in article.tags.slice(0, 3)" :key="tag.id" class="tag">
                    {{ tag.name }}
                  </span>
                </div>
                <span class="read-time">{{ article.views }} 阅读</span>
              </div>
            </RouterLink>
          </div>

          <div v-if="currentArticles.length === 0" class="empty-state">
            <p>这个分类下暂时还没有已发布文章。</p>
          </div>
        </div>
      </section>

      <section class="other-categories">
        <div class="container">
          <h2 class="section-title">其他分类</h2>
          <div class="categories-list">
            <RouterLink
              v-for="item in categories.filter((entry) => entry.slug !== categorySlug)"
              :key="item.id"
              :to="`/category/${item.slug}`"
              class="category-chip"
            >
              <span class="chip-icon">{{ item.icon || item.name.slice(0, 1) }}</span>
              <span class="chip-name">{{ item.name }}</span>
            </RouterLink>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.category-page {
  padding-bottom: 80px;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 24px;
}

.status-wrap,
.not-found {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.status-card {
  padding: 18px 20px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 191, 255, 0.12);
  color: rgba(255, 255, 255, 0.82);
}

.not-found h1 {
  font-family: 'Orbitron', sans-serif;
  font-size: 2rem;
  margin-bottom: 16px;
}

.not-found p {
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 24px;
}

.back-link {
  color: #00bfff;
  text-decoration: none;
}

.page-header {
  padding: 120px 0 60px;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  margin-bottom: 40px;
}

.breadcrumb a {
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
}

.breadcrumb a:hover {
  color: #00ffff;
}

.breadcrumb span {
  color: rgba(255, 255, 255, 0.3);
}

.breadcrumb .current {
  color: rgba(255, 255, 255, 0.7);
}

.category-header {
  display: flex;
  align-items: center;
  gap: 24px;
}

.category-icon {
  font-size: 4rem;
}

.category-name {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 12px;
}

.category-desc {
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
  margin-bottom: 12px;
}

.article-count {
  font-size: 0.9rem;
  color: #00bfff;
}

.articles-section {
  padding: 40px 0;
}

.articles-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.article-card {
  display: block;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 16px;
  padding: 28px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.article-card:hover {
  background: rgba(0, 191, 255, 0.03);
  border-color: rgba(0, 191, 255, 0.3);
  transform: translateX(4px);
}

.article-meta,
.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.article-meta {
  margin-bottom: 12px;
}

.category-tag {
  padding: 4px 12px;
  background: rgba(0, 191, 255, 0.1);
  border-radius: 20px;
  font-size: 0.8rem;
  color: #00bfff;
}

.date {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.4);
}

.article-title {
  font-size: 1.2rem;
  color: #fff;
  margin-bottom: 12px;
  line-height: 1.4;
}

.article-card:hover .article-title {
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

.read-time {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.5);
}

.other-categories {
  padding: 60px 0;
  background: rgba(255, 255, 255, 0.02);
}

.section-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.3rem;
  margin-bottom: 20px;
}

.categories-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.category-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 30px;
  text-decoration: none;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s;
}

.category-chip:hover {
  background: rgba(0, 191, 255, 0.1);
  border-color: rgba(0, 191, 255, 0.4);
  color: #00ffff;
}

@media (max-width: 768px) {
  .page-header {
    padding: 100px 0 40px;
  }

  .category-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .category-icon {
    font-size: 3rem;
  }

  .category-name {
    font-size: 1.8rem;
  }

  .article-card {
    padding: 20px;
  }

  .article-meta,
  .article-footer {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
