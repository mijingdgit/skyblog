<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { fetchPublicCategories, fetchPublishedArticles, fetchPublishedProjects } from '../api/public'
import type { AdminArticle, AdminCategory, AdminProject } from '../types/admin'
import {
  buildTagCounts,
  formatDate,
  sortArticlesByLatest,
  sortArticlesByViews,
} from '../utils/content'

const categories = ref<AdminCategory[]>([])
const articles = ref<AdminArticle[]>([])
const projects = ref<AdminProject[]>([])
const hoverProject = ref<number | null>(null)
const isLoading = ref(true)
const loadError = ref('')

const latestArticles = computed(() => sortArticlesByLatest(articles.value).slice(0, 6))
const popularArticles = computed(() => sortArticlesByViews(articles.value).slice(0, 5))
const tagCounts = computed(() => buildTagCounts(articles.value))
const featuredProjects = computed(() => [...projects.value].sort((a, b) => a.order - b.order).slice(0, 3))

function estimateReadTime(content: string) {
  const minutes = Math.max(1, Math.round(content.replace(/\s+/g, '').length / 500))
  return `${minutes} 分钟阅读`
}

onMounted(async () => {
  try {
    const [categoryData, articleData, projectData] = await Promise.all([
      fetchPublicCategories(),
      fetchPublishedArticles(),
      fetchPublishedProjects(),
    ])

    categories.value = categoryData
    articles.value = articleData
    projects.value = projectData
  } catch {
    loadError.value = '公开内容加载失败，请确认 Django API 已启动。'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">Python & AI Developer</div>
        <h1 class="hero-title">
          用代码
          <span class="gradient-text">改变世界</span>
        </h1>
        <p class="hero-subtitle">
          专注于 Python 开发、AI 大模型应用与生成式内容实践。
          <br />
          这里会同步展示后台发布的文章和项目。
        </p>
        <div class="hero-actions">
          <RouterLink to="/articles" class="btn-primary">
            <span>浏览文章</span>
            <span class="icon">-></span>
          </RouterLink>
          <RouterLink to="/projects" class="btn-secondary">
            <span>查看项目</span>
          </RouterLink>
        </div>
        <div class="hero-stats">
          <div class="stat">
            <span class="stat-number">{{ articles.length }}+</span>
            <span class="stat-label">文章</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ projects.length }}+</span>
            <span class="stat-label">项目</span>
          </div>
          <div class="stat">
            <span class="stat-number">{{ categories.length }}+</span>
            <span class="stat-label">分类</span>
          </div>
        </div>
      </div>
      <div class="scroll-hint">
        <span>向下滚动</span>
        <div class="scroll-arrow"></div>
      </div>
    </section>

    <section v-if="loadError" class="status-section">
      <div class="container">
        <div class="status-card error">{{ loadError }}</div>
      </div>
    </section>

    <section v-else-if="isLoading" class="status-section">
      <div class="container">
        <div class="status-card">正在加载公开内容...</div>
      </div>
    </section>

    <template v-else>
      <section class="categories-section">
        <div class="container">
          <h2 class="section-title">
            <span class="accent">技术</span>分类
          </h2>
          <div class="categories-grid">
            <RouterLink
              v-for="category in categories"
              :key="category.id"
              :to="`/category/${category.slug}`"
              class="category-card"
            >
              <span class="category-icon">{{ category.icon || category.name.slice(0, 1) }}</span>
              <h3 class="category-name">{{ category.name }}</h3>
              <p class="category-desc">{{ category.description }}</p>
              <span class="category-count">{{ category.article_count }} 篇文章</span>
            </RouterLink>
          </div>
        </div>
      </section>

      <section class="articles-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">
              <span class="accent">最新</span>文章
            </h2>
            <RouterLink to="/articles" class="view-all">
              查看全部 <span class="arrow">-></span>
            </RouterLink>
          </div>
          <div class="articles-grid">
            <RouterLink
              v-for="article in latestArticles"
              :key="article.id"
              :to="`/article/${article.id}`"
              class="article-card"
            >
              <div class="article-meta">
                <span class="category-tag">{{ article.category_name || '未分类' }}</span>
                <span class="date">{{ formatDate(article.published_at || article.created_at) }}</span>
              </div>
              <h3 class="article-title">{{ article.title }}</h3>
              <p class="article-excerpt">{{ article.excerpt }}</p>
              <div class="article-footer">
                <div class="tags">
                  <span v-for="tag in article.tags.slice(0, 2)" :key="tag.id" class="tag">
                    {{ tag.name }}
                  </span>
                </div>
                <span class="read-time">{{ estimateReadTime(article.content) }}</span>
              </div>
            </RouterLink>
          </div>
        </div>
      </section>

      <section class="tags-section">
        <div class="container">
          <h2 class="section-title">
            <span class="accent">标签</span>云
          </h2>
          <div class="tags-cloud">
            <RouterLink
              v-for="tag in tagCounts.slice(0, 15)"
              :key="tag.name"
              :to="`/articles?tag=${encodeURIComponent(tag.name)}`"
              class="tag-item"
              :style="{ '--size': Math.min(0.8 + tag.count * 0.15, 1.5) + 'rem' }"
            >
              {{ tag.name }}
            </RouterLink>
          </div>
        </div>
      </section>

      <section class="popular-section">
        <div class="container">
          <h2 class="section-title">
            <span class="accent">热门</span>文章
          </h2>
          <div class="popular-list">
            <RouterLink
              v-for="(article, index) in popularArticles"
              :key="article.id"
              :to="`/article/${article.id}`"
              class="popular-item"
            >
              <span class="rank" :class="{ 'top-three': index < 3 }">{{ index + 1 }}</span>
              <div class="popular-content">
                <h3 class="popular-title">{{ article.title }}</h3>
                <div class="popular-meta">
                  <span>{{ estimateReadTime(article.content) }}</span>
                  <span>/</span>
                  <span>{{ article.views }} 阅读</span>
                </div>
              </div>
            </RouterLink>
          </div>
        </div>
      </section>

      <section class="projects-section">
        <div class="container">
          <div class="section-header">
            <h2 class="section-title">
              <span class="accent">项目</span>作品
            </h2>
            <RouterLink to="/projects" class="view-all">
              查看全部 <span class="arrow">-></span>
            </RouterLink>
          </div>
          <div class="projects-grid">
            <div
              v-for="project in featuredProjects"
              :key="project.id"
              class="project-card"
              @mouseenter="hoverProject = project.id"
              @mouseleave="hoverProject = null"
            >
              <div class="project-visual" :class="{ hover: hoverProject === project.id }">
                <span class="project-icon">{{ project.image || 'P' }}</span>
              </div>
              <div class="project-info">
                <h3>{{ project.title }}</h3>
                <p>{{ project.description }}</p>
                <div class="tech-stack">
                  <span v-for="tech in project.tech_stack.slice(0, 3)" :key="tech">
                    {{ tech }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="about-preview">
        <div class="container">
          <div class="about-content">
            <div class="about-text">
              <h2 class="section-title">
                关于<span class="accent">本站</span>
              </h2>
              <p>
                这个首页现在直接读取 Django 后台里发布的文章、标签、分类和项目，
                你在管理后台新增或修改内容后，前台刷新就会同步更新。
              </p>
              <p>
                接下来我们还可以继续补 SEO、文章阅读详情优化、部署配置和对象存储，让它更接近真正上线版本。
              </p>
              <RouterLink to="/about" class="btn-outline">
                了解更多
              </RouterLink>
            </div>
            <div class="about-avatar">
              <div class="avatar-ring"></div>
              <div class="avatar-ring ring-2"></div>
              <div class="avatar-inner">
                <span>S</span>
              </div>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.home {
  padding-bottom: 80px;
}

.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 120px 24px 80px;
  text-align: center;
  position: relative;
}

.hero-badge {
  display: inline-block;
  padding: 8px 20px;
  background: rgba(0, 191, 255, 0.1);
  border: 1px solid rgba(0, 191, 255, 0.3);
  border-radius: 30px;
  font-size: 0.9rem;
  color: #00bfff;
  margin-bottom: 24px;
  animation: fadeInUp 0.6s ease;
}

.hero-title {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 24px;
  animation: fadeInUp 0.6s ease 0.1s both;
}

.gradient-text {
  background: linear-gradient(135deg, #00bfff, #00ffff, #1e90ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.8;
  margin-bottom: 40px;
  animation: fadeInUp 0.6s ease 0.2s both;
}

.hero-actions {
  display: flex;
  gap: 16px;
  margin-bottom: 60px;
  animation: fadeInUp 0.6s ease 0.3s both;
}

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #00bfff, #1e90ff);
  color: #fff;
  box-shadow: 0 4px 20px rgba(0, 191, 255, 0.4);
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 30px rgba(0, 191, 255, 0.6);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 191, 255, 0.3);
  color: #fff;
}

.btn-secondary:hover {
  background: rgba(0, 191, 255, 0.1);
  border-color: rgba(0, 191, 255, 0.5);
}

.hero-stats {
  display: flex;
  gap: 60px;
  animation: fadeInUp 0.6s ease 0.4s both;
}

.stat {
  text-align: center;
}

.stat-number {
  display: block;
  font-family: 'Orbitron', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #00bfff;
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

.scroll-hint {
  position: absolute;
  bottom: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.4);
  font-size: 0.8rem;
  animation: bounce 2s infinite;
}

.scroll-arrow {
  width: 16px;
  height: 16px;
  border-right: 2px solid rgba(0, 191, 255, 0.5);
  border-bottom: 2px solid rgba(0, 191, 255, 0.5);
  transform: rotate(45deg);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(10px); }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.status-section {
  padding: 0 0 32px;
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

.section-title {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 40px;
}

.section-title .accent {
  color: #00bfff;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
}

.view-all {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s;
}

.view-all:hover {
  color: #00ffff;
}

.view-all .arrow {
  display: inline-block;
  transition: transform 0.3s;
}

.view-all:hover .arrow {
  transform: translateX(4px);
}

.categories-section,
.articles-section,
.tags-section,
.popular-section,
.projects-section,
.about-preview {
  padding: 80px 0;
}

.categories-grid,
.articles-grid,
.projects-grid {
  display: grid;
  gap: 24px;
}

.categories-grid {
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
}

.articles-grid {
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
}

.projects-grid {
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

.category-card,
.article-card,
.project-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 16px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.category-card {
  padding: 32px;
}

.article-card {
  padding: 24px;
}

.project-card {
  overflow: hidden;
}

.category-card:hover,
.article-card:hover,
.project-card:hover {
  border-color: rgba(0, 191, 255, 0.4);
  transform: translateY(-4px);
}

.category-icon {
  font-size: 2rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  margin-bottom: 16px;
  border-radius: 16px;
  background: rgba(0, 191, 255, 0.12);
}

.category-name,
.article-title,
.project-info h3 {
  color: #fff;
}

.category-desc,
.article-excerpt,
.project-info p {
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.6;
}

.category-count {
  display: inline-block;
  margin-top: 16px;
  font-size: 0.8rem;
  color: #00bfff;
}

.article-meta,
.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.article-meta {
  margin-bottom: 12px;
}

.category-tag,
.tag,
.tech-stack span {
  padding: 4px 12px;
  border-radius: 20px;
}

.category-tag {
  background: rgba(0, 191, 255, 0.15);
  font-size: 0.75rem;
  color: #00bfff;
}

.date,
.read-time {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}

.tags,
.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background: rgba(255, 255, 255, 0.05);
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.6);
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  justify-content: center;
}

.tag-item {
  padding: 8px 20px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 20px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: var(--size, 0.9rem);
  transition: all 0.3s ease;
}

.tag-item:hover {
  background: rgba(0, 191, 255, 0.15);
  border-color: rgba(0, 191, 255, 0.5);
  color: #00ffff;
  transform: scale(1.05);
}

.popular-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.popular-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 12px;
  text-decoration: none;
  transition: all 0.3s ease;
}

.popular-item:hover {
  background: rgba(0, 191, 255, 0.05);
  border-color: rgba(0, 191, 255, 0.3);
}

.rank {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  font-family: 'Orbitron', sans-serif;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.5);
}

.rank.top-three {
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.3), rgba(0, 255, 255, 0.2));
  color: #00ffff;
}

.popular-title {
  color: #fff;
  margin-bottom: 4px;
}

.popular-meta {
  display: flex;
  gap: 8px;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}

.project-visual {
  height: 140px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.1), rgba(0, 255, 255, 0.05));
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.project-visual.hover {
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.2), rgba(0, 255, 255, 0.1));
}

.project-icon {
  font-size: 2rem;
  color: #00bfff;
}

.project-info {
  padding: 24px;
}

.tech-stack span {
  background: rgba(0, 191, 255, 0.1);
  font-size: 0.75rem;
  color: #00bfff;
}

.about-content {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 60px;
  align-items: center;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 24px;
  padding: 60px;
}

.about-text p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.8;
  margin-bottom: 20px;
}

.btn-outline {
  display: inline-block;
  padding: 12px 32px;
  border: 1px solid rgba(0, 191, 255, 0.5);
  border-radius: 30px;
  color: #00bfff;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline:hover {
  background: rgba(0, 191, 255, 0.1);
  border-color: #00ffff;
  color: #00ffff;
}

.about-avatar {
  position: relative;
  width: 180px;
  height: 180px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-ring {
  position: absolute;
  width: 160px;
  height: 160px;
  border: 2px solid transparent;
  border-top-color: #00bfff;
  border-radius: 50%;
  animation: rotate 6s linear infinite;
}

.avatar-ring.ring-2 {
  width: 180px;
  height: 180px;
  border-top-color: transparent;
  border-right-color: #00ffff;
  animation-direction: reverse;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.avatar-inner {
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.2), rgba(0, 255, 255, 0.1));
  border: 2px solid rgba(0, 191, 255, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-inner span {
  font-size: 2rem;
  color: #00bfff;
}

@media (max-width: 900px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-stats {
    gap: 40px;
  }

  .about-content {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .about-avatar {
    margin: 0 auto;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 100px 16px 60px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }

  .hero-actions,
  .hero-stats,
  .article-footer {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }

  .articles-grid,
  .projects-grid {
    grid-template-columns: 1fr;
  }

  .about-content {
    padding: 40px 24px;
  }
}
</style>
