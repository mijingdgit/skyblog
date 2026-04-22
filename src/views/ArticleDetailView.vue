<script setup lang="ts">
import { computed, defineAsyncComponent, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import {
  fetchPublicCategories,
  fetchPublishedArticle,
  fetchPublishedArticles,
  incrementArticleView,
} from '../api/public'
import type { AdminArticle, AdminCategory } from '../types/admin'
import { categoryById, formatDate, getArticleDisplayDate, sortArticlesByLatest } from '../utils/content'
import {
  extractMarkdownHeadings,
  isXmindContent,
  parseXmindContent,
  renderMarkdown,
} from '../utils/renderMarkdown'
import { applySeo } from '../utils/seo'

const route = useRoute()
const XmindEmbedArticle = defineAsyncComponent(() => import('../components/XmindEmbedArticle.vue'))
const XmindMap = defineAsyncComponent(() => import('../components/XmindMap.vue'))

const categories = ref<AdminCategory[]>([])
const article = ref<AdminArticle | null>(null)
const articles = ref<AdminArticle[]>([])
const isLoading = ref(true)
const loadError = ref('')
const articleContentRef = ref<HTMLElement | null>(null)
const tocLinksRef = ref<HTMLElement | null>(null)
const copyMessage = ref('')
const activeHeadingId = ref('')
const tocCollapsed = ref(false)
let copyMessageTimer: number | undefined
let activeHeadingFrame: number | undefined

const articleId = computed(() => Number(route.params.id))
const currentCategory = computed(() => categoryById(categories.value, article.value?.category ?? null))
const orderedArticles = computed(() => sortArticlesByLatest(articles.value))
const currentArticleIndex = computed(() =>
  orderedArticles.value.findIndex((item) => item.id === article.value?.id),
)
const previousArticle = computed(() => {
  const index = currentArticleIndex.value
  return index > 0 ? orderedArticles.value[index - 1] : null
})
const nextArticle = computed(() => {
  const index = currentArticleIndex.value
  return index >= 0 && index < orderedArticles.value.length - 1 ? orderedArticles.value[index + 1] : null
})

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

const isXmindArticle = computed(() => {
  if (!article.value?.content) {
    return false
  }

  return isXmindContent(article.value.content)
})

const xmindTree = computed(() => {
  if (!article.value?.content) {
    return null
  }

  return parseXmindContent(article.value.content)
})

const hasXmindFile = computed(() => Boolean(article.value?.xmind_file))

const articleHeadings = computed(() => {
  if (!article.value?.content || isXmindArticle.value || hasXmindFile.value) {
    return []
  }

  return extractMarkdownHeadings(article.value.content)
})

function estimateReadTime(content: string) {
  const minutes = Math.max(1, Math.round(content.replace(/\s+/g, '').length / 500))
  return `${minutes} 分钟阅读`
}

function scrollToHeading(id: string) {
  activeHeadingId.value = id
  document.getElementById(id)?.scrollIntoView({
    behavior: 'smooth',
    block: 'start',
  })
}

function updateActiveHeading() {
  if (articleHeadings.value.length === 0) {
    activeHeadingId.value = ''
    return
  }

  let currentId = articleHeadings.value[0].id

  for (const heading of articleHeadings.value) {
    const element = document.getElementById(heading.id)
    if (!element) {
      continue
    }

    if (element.getBoundingClientRect().top <= 140) {
      currentId = heading.id
    } else {
      break
    }
  }

  activeHeadingId.value = currentId
  scrollActiveTocLinkIntoView()
}

function scrollActiveTocLinkIntoView() {
  void nextTick(() => {
    if (!tocLinksRef.value || !activeHeadingId.value || tocCollapsed.value) {
      return
    }

    const activeLink = tocLinksRef.value.querySelector<HTMLElement>(
      `[data-heading-id="${CSS.escape(activeHeadingId.value)}"]`,
    )

    activeLink?.scrollIntoView({
      block: 'nearest',
      inline: 'nearest',
    })
  })
}

function scheduleActiveHeadingUpdate() {
  if (activeHeadingFrame !== undefined) {
    return
  }

  activeHeadingFrame = window.requestAnimationFrame(() => {
    activeHeadingFrame = undefined
    updateActiveHeading()
  })
}

function decorateCodeBlocks() {
  if (!articleContentRef.value) {
    return
  }

  articleContentRef.value.querySelectorAll('pre').forEach((pre) => {
    pre.classList.add('code-block-shell')

    if (pre.querySelector('.copy-code-btn')) {
      return
    }

    const button = document.createElement('button')
    button.type = 'button'
    button.className = 'copy-code-btn'
    button.textContent = '复制'
    button.setAttribute('aria-label', '复制代码')
    pre.appendChild(button)
  })
}

async function handleContentClick(event: MouseEvent) {
  const target = event.target as HTMLElement | null
  const button = target?.closest<HTMLButtonElement>('.copy-code-btn')

  if (!button) {
    return
  }

  const code = button.closest('pre')?.querySelector('code')?.textContent || ''
  if (!code) {
    return
  }

  try {
    await navigator.clipboard.writeText(code)
    button.textContent = '已复制'
    copyMessage.value = '代码已复制'
  } catch {
    copyMessage.value = '复制失败，请手动选择代码'
  }

  window.clearTimeout(copyMessageTimer)
  copyMessageTimer = window.setTimeout(() => {
    button.textContent = '复制'
    copyMessage.value = ''
  }, 1600)
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
    void incrementArticleView(articleData.id)
      .then(({ views }) => {
        if (article.value?.id === articleData.id) {
          article.value = { ...article.value, views }
        }
      })
      .catch(() => {
        // 阅读量统计失败不影响正文阅读。
      })
    applySeo({
      title: articleData.title,
      description: articleData.excerpt || `阅读 SkyBlog 技术文章：${articleData.title}`,
      image: articleData.cover,
      path: route.fullPath,
      type: 'article',
    })
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

watch(formattedContent, async () => {
  await nextTick()
  decorateCodeBlocks()
  updateActiveHeading()
})

watch(articleHeadings, async () => {
  await nextTick()
  updateActiveHeading()
})

onMounted(async () => {
  if (!article.value) {
    await loadArticle()
  }

  await nextTick()
  decorateCodeBlocks()
  updateActiveHeading()
  window.addEventListener('scroll', scheduleActiveHeadingUpdate, { passive: true })
})

onBeforeUnmount(() => {
  window.clearTimeout(copyMessageTimer)
  window.removeEventListener('scroll', scheduleActiveHeadingUpdate)

  if (activeHeadingFrame !== undefined) {
    window.cancelAnimationFrame(activeHeadingFrame)
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
        <div class="container article-shell">
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
        <div class="container article-shell">
          <img
            :src="article.cover"
            :alt="article.title"
            class="article-cover"
            loading="lazy"
            decoding="async"
          />
        </div>
      </section>

      <section class="article-body">
          <div
            class="container article-shell reader-container"
            :class="{
              'mindmap-container': isXmindArticle || hasXmindFile,
              'has-reader-toc': articleHeadings.length > 0,
            }"
          >
          <XmindEmbedArticle v-if="hasXmindFile && article?.xmind_file" :file-url="article.xmind_file" />
          <XmindMap v-else-if="isXmindArticle && xmindTree" :root="xmindTree" />
          <div
            v-else
            class="reader-layout"
            :class="{
              'with-toc': articleHeadings.length > 0,
              'toc-collapsed': tocCollapsed,
            }"
          >
            <aside
              v-if="articleHeadings.length > 0"
              class="reader-toc"
              :class="{ collapsed: tocCollapsed }"
            >
              <div class="toc-head">
                <p class="toc-title">文章目录</p>
                <button
                  type="button"
                  class="toc-toggle"
                  :title="tocCollapsed ? '展开文章目录' : '收起文章目录'"
                  :aria-label="tocCollapsed ? '展开文章目录' : '收起文章目录'"
                  :aria-expanded="!tocCollapsed"
                  @click="tocCollapsed = !tocCollapsed"
                >
                  <svg
                    v-if="tocCollapsed"
                    viewBox="0 0 24 24"
                    aria-hidden="true"
                    class="toc-toggle-icon"
                  >
                    <path d="M9 5l7 7-7 7" />
                  </svg>
                  <svg v-else viewBox="0 0 24 24" aria-hidden="true" class="toc-toggle-icon">
                    <path d="M15 5l-7 7 7 7" />
                  </svg>
                </button>
              </div>

              <div v-show="!tocCollapsed" ref="tocLinksRef" class="toc-links">
                <button
                  v-for="heading in articleHeadings"
                  :key="heading.id"
                  type="button"
                  class="toc-link"
                  :data-heading-id="heading.id"
                  :class="[`level-${heading.level}`, { active: activeHeadingId === heading.id }]"
                  @click="scrollToHeading(heading.id)"
                >
                  {{ heading.text }}
                </button>
              </div>
            </aside>

            <article
              ref="articleContentRef"
              class="article-content markdown-body"
              @click="handleContentClick"
              v-html="formattedContent"
            ></article>
          </div>

          <div class="article-actions">
            <div class="share">
              <span class="share-label">当前链接</span>
              <code class="share-link">{{ route.fullPath }}</code>
            </div>
            <span v-if="copyMessage" class="copy-message">{{ copyMessage }}</span>
          </div>
        </div>
      </section>

      <section v-if="previousArticle || nextArticle" class="prev-next-section">
        <div class="container article-shell prev-next-grid">
          <RouterLink
            v-if="previousArticle"
            :to="`/article/${previousArticle.id}`"
            class="prev-next-card"
          >
            <span class="nav-label">上一篇</span>
            <strong>{{ previousArticle.title }}</strong>
          </RouterLink>
          <div v-else></div>

          <RouterLink v-if="nextArticle" :to="`/article/${nextArticle.id}`" class="prev-next-card next">
            <span class="nav-label">下一篇</span>
            <strong>{{ nextArticle.title }}</strong>
          </RouterLink>
        </div>
      </section>

      <section v-if="relatedArticles.length > 0" class="related-section">
        <div class="container article-shell">
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
        <div class="container article-shell">
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

.article-shell {
  max-width: 1180px;
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
  max-width: 900px;
  margin-bottom: 20px;
}

.article-excerpt {
  max-width: 900px;
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

.mindmap-container {
  max-width: 1320px;
}

.reader-container.has-reader-toc {
  max-width: 1180px;
}

.reader-layout {
  display: grid;
  gap: 24px;
}

.reader-layout.with-toc {
  grid-template-columns: minmax(0, 1fr) 260px;
  align-items: start;
  transition: grid-template-columns 0.25s ease;
}

.reader-layout.with-toc.toc-collapsed {
  grid-template-columns: minmax(0, 1fr) 52px;
}

.reader-toc {
  position: sticky;
  top: 100px;
  order: 2;
  max-height: calc(100vh - 140px);
  padding: 18px;
  border: 1px solid rgba(0, 191, 255, 0.14);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.03);
  overflow: hidden;
  transition: padding 0.25s ease, border-color 0.2s, background 0.2s;
}

.reader-toc.collapsed {
  padding: 10px;
  border-color: rgba(0, 191, 255, 0.22);
  background: rgba(0, 191, 255, 0.06);
}

.toc-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.reader-toc.collapsed .toc-head {
  justify-content: center;
}

.toc-title {
  margin: 0;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.48);
}

.reader-toc.collapsed .toc-title {
  display: none;
}

.toc-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 auto;
  width: 34px;
  height: 34px;
  padding: 0;
  border: 1px solid rgba(0, 191, 255, 0.18);
  border-radius: 999px;
  background: rgba(0, 191, 255, 0.08);
  color: #00ffff;
  font-size: 0.78rem;
  cursor: pointer;
}

.reader-toc.collapsed .toc-toggle {
  width: 30px;
  height: 54px;
  border-radius: 16px;
}

.toc-toggle-icon {
  width: 16px;
  height: 16px;
}

.toc-toggle-icon path {
  fill: none;
  stroke: currentColor;
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.toc-toggle:hover {
  border-color: rgba(0, 255, 255, 0.42);
}

.toc-links {
  margin-top: 12px;
  max-height: calc(100vh - 220px);
  overflow-y: auto;
  padding-right: 4px;
  padding-bottom: 20px;
  scroll-behavior: smooth;
  overscroll-behavior: contain;
}

.toc-links::-webkit-scrollbar {
  width: 6px;
}

.toc-links::-webkit-scrollbar-thumb {
  border-radius: 999px;
  background: rgba(0, 191, 255, 0.28);
}

.toc-links::-webkit-scrollbar-track {
  background: transparent;
}

.toc-link {
  display: block;
  width: 100%;
  padding: 7px 10px;
  background: none;
  border: none;
  border-left: 2px solid transparent;
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.62);
  line-height: 1.5;
  text-align: left;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s, background 0.2s;
}

.toc-link:hover {
  color: #00ffff;
}

.toc-link.active {
  border-left-color: #00ffff;
  background: rgba(0, 191, 255, 0.12);
  color: #00ffff;
  font-weight: 700;
}

.toc-link.level-3 {
  padding-left: 24px;
  font-size: 0.86rem;
}

.article-content {
  min-width: 0;
  font-size: 1.05rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.88);
}

.article-content :deep(h2),
.article-content :deep(h3) {
  scroll-margin-top: 110px;
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

.article-content :deep(table) {
  display: block;
  width: 100%;
  max-width: 100%;
  overflow-x: auto;
  border-collapse: collapse;
  white-space: normal;
}

.article-content :deep(th),
.article-content :deep(td) {
  min-width: 140px;
  padding: 10px 14px;
  border: 1px solid rgba(0, 191, 255, 0.14);
  word-break: keep-all;
}

.article-content :deep(th) {
  color: #00ffff;
  background: rgba(0, 191, 255, 0.08);
}

.article-content :deep(pre) {
  position: relative;
  overflow: auto;
  padding: 20px;
  border: 1px solid rgba(0, 191, 255, 0.16);
  border-radius: 16px;
  background: rgba(0, 0, 0, 0.38);
}

.article-content :deep(pre code) {
  white-space: pre;
}

.article-content :deep(.copy-code-btn) {
  position: sticky;
  left: 100%;
  top: 0;
  float: right;
  margin: -8px -8px 8px 12px;
  padding: 6px 10px;
  border: 1px solid rgba(0, 191, 255, 0.24);
  border-radius: 999px;
  background: rgba(4, 18, 32, 0.88);
  color: #00ffff;
  cursor: pointer;
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

.copy-message {
  color: #00ffff;
  font-size: 0.9rem;
}

.prev-next-section {
  padding: 20px 0 50px;
}

.prev-next-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.prev-next-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 104px;
  padding: 20px;
  border: 1px solid rgba(0, 191, 255, 0.14);
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.03);
  color: #fff;
  text-decoration: none;
  transition: all 0.25s ease;
}

.prev-next-card:hover {
  border-color: rgba(0, 191, 255, 0.36);
  transform: translateY(-2px);
}

.prev-next-card.next {
  text-align: right;
}

.nav-label {
  color: rgba(255, 255, 255, 0.46);
  font-size: 0.85rem;
}

.prev-next-card strong {
  line-height: 1.5;
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

  .reader-layout.with-toc,
  .reader-layout.with-toc.toc-collapsed,
  .prev-next-grid {
    grid-template-columns: 1fr;
  }

  .reader-toc {
    position: static;
    order: 0;
    max-height: none;
  }

  .toc-links {
    max-height: 280px;
  }

  .reader-toc.collapsed {
    padding: 14px 16px;
  }

  .reader-toc.collapsed .toc-title {
    display: block;
  }

  .reader-toc.collapsed .toc-head {
    justify-content: space-between;
  }

  .reader-toc.collapsed .toc-toggle {
    width: 34px;
    height: 34px;
    border-radius: 999px;
  }

  .prev-next-card.next {
    text-align: left;
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
