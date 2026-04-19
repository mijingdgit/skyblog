<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { fetchPublicCategories, fetchPublishedArticle, fetchPublishedArticles } from '../api/public'
import type { AdminArticle, AdminCategory } from '../types/admin'
import { categoryById, formatDate, getArticleDisplayDate, sortArticlesByLatest } from '../utils/content'
import { renderMarkdown } from '../utils/renderMarkdown'

const route = useRoute()

const categories = ref<AdminCategory[]>([])
const article = ref<AdminArticle | null>(null)
const articles = ref<AdminArticle[]>([])
const isLoading = ref(true)
const loadError = ref('')

const articleId = computed(() => Number(route.params.id))
const currentCategory = computed(() => categoryById(categories.value, article.value?.category ?? null))

const relatedArticles = computed(() => {
  if (!article.value) {
    return []
  }

  return sortArticlesByLatest(
    articles.value.filter(
      (item) => item.id !== article.value?.id && item.category === article.value?.category,
    ),
  ).slice(0, 3)
})

const formattedContent = computed(() => {
  if (!article.value?.content) {
    return ''
  }

  return renderMarkdown(article.value.content)
})

function estimateReadTime(content: string) {
  const minutes = Math.max(1, Math.round(content.replace(/\s+/g, '').length / 500))
  return `${minutes} 分钟阅读`
}

async function loadArticle() {
  if (!Number.isInteger(articleId.value) || articleId.value <= 0) {
    article.value = null
    loadError.value = '文章参数无效。'
    isLoading.value = false
    return
  }

  isLoading.value = true
  loadError.value = ''

  try {
    const [categoryData, articleData, listData] = await Promise.all([
      fetchPublicCategories(),
      fetchPublishedArticle(articleId.value),
      fetchPublishedArticles(),
    ])

    categories.value = categoryData
    article.value = articleData
    articles.value = listData
  } catch {
    article.value = null
    loadError.value = '文章加载失败，可能尚未发布或后台服务暂时不可用。'
  } finally {
    isLoading.value = false
  }
}

watch(
  () => route.params.id,
  async () => {
    await loadArticle()
  },
  { immediate: true },
)

onMounted(async () => {
  if (!article.value) {
    await loadArticle()
  }
})
</script>

<template>
  <div class="article-detail">
    <div v-if="isLoading" class="status-wrap">
      <div class="container">
        <div class="status-card">正在加载文章详情...</div>
      </div>
    </div>

    <div v-else-if="loadError || !article" class="not-found">
      <div class="container">
        <h1>文章不存在</h1>
        <p>{{ loadError || '抱歉，您访问的文章不存在或尚未发布。' }}</p>
        <RouterLink to="/articles" class="back-link">返回文章列表</RouterLink>
      </div>
    </div>

    <template v-else>
      <section class="article-header">
        <div class="container">
          <div class="breadcrumb">
            <RouterLink to="/">首页</RouterLink>
            <span>/</span>
            <RouterLink to="/articles">文章</RouterLink>
            <span>/</span>
            <span class="current">{{ article.title }}</span>
          </div>

          <div class="article-meta">
            <span class="category-badge">
              {{ currentCategory?.icon || article.category_name?.slice(0, 1) || '未' }}
              {{ currentCategory?.name || article.category_name || '未分类' }}
            </span>
            <span class="date">{{ formatDate(getArticleDisplayDate(article)) }}</span>
          </div>

          <h1 class="article-title">{{ article.title }}</h1>

          <p v-if="article.excerpt" class="article-excerpt">{{ article.excerpt }}</p>

          <div class="article-info">
            <div class="tags">
              <span v-for="tag in article.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
            </div>
            <div class="stats">
              <span class="stat">{{ estimateReadTime(article.content) }}</span>
              <span class="stat">{{ article.views }} 阅读</span>
            </div>
          </div>
        </div>
      </section>

      <section v-if="article.cover" class="article-cover-section">
        <div class="container">
          <img :src="article.cover" :alt="article.title" class="article-cover" />
        </div>
      </section>

      <section class="article-body">
        <div class="container">
          <article class="article-content markdown-body" v-html="formattedContent"></article>

          <div class="article-actions">
            <div class="share">
              <span class="share-label">当前链接</span>
              <code class="share-link">{{ route.fullPath }}</code>
            </div>
          </div>
        </div>
      </section>

      <section v-if="relatedArticles.length > 0" class="related-section">
        <div class="container">
          <h2 class="section-title">相关文章</h2>
          <div class="related-grid">
            <RouterLink
              v-for="related in relatedArticles"
              :key="related.id"
              :to="`/article/${related.id}`"
              class="related-card"
            >
              <h3>{{ related.title }}</h3>
              <p>{{ related.excerpt }}</p>
              <span class="read-more">继续阅读</span>
            </RouterLink>
          </div>
        </div>
      </section>

      <section class="article-nav">
        <div class="container">
          <RouterLink to="/articles" class="back-to-list">返回文章列表</RouterLink>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.article-detail {
  padding-bottom: 80px;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 24px;
}

.status-wrap,
.not-found {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-card,
.not-found .container {
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

.article-header {
  padding: 120px 0 40px;
  background: linear-gradient(180deg, rgba(0, 191, 255, 0.05) 0%, transparent 100%);
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  margin-bottom: 24px;
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
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 300px;
}

.article-meta,
.article-info,
.article-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.article-meta {
  margin-bottom: 20px;
}

.category-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  background: rgba(0, 191, 255, 0.15);
  border-radius: 20px;
  font-size: 0.9rem;
  color: #00bfff;
}

.date {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

.article-title {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 2.2rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 20px;
}

.article-excerpt {
  margin-bottom: 24px;
  color: rgba(255, 255, 255, 0.72);
  line-height: 1.8;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  padding: 4px 14px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 15px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.6);
}

.stats {
  display: flex;
  gap: 20px;
}

.stat {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

.article-cover-section {
  padding: 16px 0 0;
}

.article-cover {
  display: block;
  width: 100%;
  max-height: 420px;
  object-fit: cover;
  border-radius: 24px;
  border: 1px solid rgba(0, 191, 255, 0.14);
  background: rgba(255, 255, 255, 0.03);
}

.article-body {
  padding: 40px 0;
}

.article-content {
  font-size: 1.05rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.88);
}

.article-content :deep(img) {
  display: block;
  max-width: 100%;
  margin: 24px auto;
  border-radius: 18px;
  border: 1px solid rgba(0, 191, 255, 0.16);
}

.article-content :deep(a) {
  color: #00bfff;
}

.article-content :deep(blockquote) {
  margin: 24px 0;
  padding: 16px 20px;
  border-left: 4px solid rgba(0, 191, 255, 0.5);
  background: rgba(0, 191, 255, 0.06);
  border-radius: 0 16px 16px 0;
}

.article-actions {
  margin-top: 40px;
  padding-top: 24px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.share {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.share-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

.share-link {
  padding: 8px 12px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 191, 255, 0.15);
  color: rgba(255, 255, 255, 0.72);
}

.related-section {
  padding: 60px 0;
  background: rgba(255, 255, 255, 0.02);
}

.section-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.5rem;
  margin-bottom: 24px;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.related-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
  text-decoration: none;
  transition: all 0.3s;
}

.related-card:hover {
  border-color: rgba(0, 191, 255, 0.3);
}

.related-card h3 {
  font-size: 1rem;
  color: #fff;
  margin-bottom: 8px;
  line-height: 1.4;
}

.related-card p {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.6;
  margin-bottom: 12px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.read-more,
.back-to-list {
  color: #00bfff;
}

.article-nav {
  padding: 40px 0;
}

.back-to-list {
  text-decoration: none;
}

@media (max-width: 768px) {
  .article-header {
    padding: 100px 0 30px;
  }

  .article-title {
    font-size: 1.6rem;
  }

  .breadcrumb .current {
    max-width: 150px;
  }

  .article-meta,
  .article-info,
  .article-actions {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
