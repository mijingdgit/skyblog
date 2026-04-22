<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchProjectPageContent, fetchPublishedProjects } from '../api/public'
import type { AdminProject, ProjectPageContent, ProjectPageFilter } from '../types/admin'
import { filterProjectsByPreset } from '../utils/content'

type ProjectAction = {
  key: 'github' | 'demo'
  tooltip: string
  emptyTooltip: string
}

const activeFilter = ref('all')
const hoverProject = ref<number | null>(null)
const projects = ref<AdminProject[]>([])
const pageContent = ref<ProjectPageContent | null>(null)
const isLoading = ref(true)
const loadError = ref('')

const defaultFilters: ProjectPageFilter[] = [
  { key: 'all', label: '全部' },
  { key: 'llm', label: 'AI / 大模型' },
  { key: 'frontend', label: '前端项目' },
  { key: 'backend', label: '后端项目' },
]

const projectActions: ProjectAction[] = [
  {
    key: 'github',
    tooltip: '查看 GitHub 仓库',
    emptyTooltip: '暂未提供 GitHub 仓库地址',
  },
  {
    key: 'demo',
    tooltip: '查看在线演示',
    emptyTooltip: '暂未提供在线演示地址',
  },
]

const filters = computed(() => {
  const backendFilters = pageContent.value?.filters
  return Array.isArray(backendFilters) && backendFilters.length > 0 ? backendFilters : defaultFilters
})
const filteredProjects = computed(() => filterProjectsByPreset(projects.value, activeFilter.value))
const techCount = computed(() => new Set(projects.value.flatMap((project) => project.tech_stack)).size)

function getProjectActionUrl(project: AdminProject, key: ProjectAction['key']) {
  return key === 'github' ? project.github : project.demo
}

function getProjectActionTooltip(project: AdminProject, action: ProjectAction) {
  return getProjectActionUrl(project, action.key) ? action.tooltip : action.emptyTooltip
}

function isProjectImage(value?: string) {
  if (!value) {
    return false
  }

  return (
    value.startsWith('/media/') ||
    value.startsWith('/static/') ||
    /^https?:\/\//.test(value) ||
    /\.(jpe?g|png|webp|gif|svg)(\?.*)?$/i.test(value)
  )
}

onMounted(async () => {
  try {
    const [projectData, pageData] = await Promise.all([
      fetchPublishedProjects(),
      fetchProjectPageContent(),
    ])

    projects.value = projectData
    pageContent.value = pageData

    if (!filters.value.some((filter) => filter.key === activeFilter.value)) {
      activeFilter.value = filters.value[0]?.key || 'all'
    }
  } catch {
    loadError.value = '项目内容加载失败，请确认 Django API 已启动。'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="projects-page">
    <section class="page-header">
      <div class="container">
        <h1 class="page-title">
          {{ pageContent?.title_prefix || '项目' }}<span class="accent">{{ pageContent?.title_accent || '作品' }}</span>
        </h1>
        <p class="page-desc">
          {{ pageContent?.description || '这里展示的项目内容，已经改为直接读取后台已发布数据。' }}
        </p>

        <div class="filters">
          <button
            v-for="filter in filters"
            :key="filter.key"
            class="filter-btn"
            :class="{ active: activeFilter === filter.key }"
            @click="activeFilter = filter.key"
          >
            {{ filter.label }}
          </button>
        </div>
      </div>
    </section>

    <section class="projects-section">
      <div class="container">
        <div v-if="loadError" class="status-card error">
          {{ loadError }}
        </div>

        <div v-else-if="isLoading" class="status-card">
          正在加载项目内容...
        </div>

        <template v-else>
          <div class="projects-grid">
            <div
              v-for="project in filteredProjects"
              :key="project.id"
              class="project-card"
              @mouseenter="hoverProject = project.id"
              @mouseleave="hoverProject = null"
            >
              <div
                class="project-visual"
                :class="{ hover: hoverProject === project.id, 'has-image': isProjectImage(project.image) }"
              >
                <div class="visual-content">
                  <img
                    v-if="isProjectImage(project.image)"
                    :src="project.image"
                    :alt="project.title"
                    class="project-image"
                    loading="lazy"
                    decoding="async"
                  />
                  <span v-else class="project-icon">{{ project.image || project.title.slice(0, 1) }}</span>
                </div>
              </div>

              <div class="project-body">
                <div class="project-header">
                  <h2 class="project-title">{{ project.title }}</h2>
                  <div class="project-links" aria-label="项目链接">
                    <template v-for="action in projectActions" :key="action.key">
                      <a
                        v-if="getProjectActionUrl(project, action.key)"
                        :href="getProjectActionUrl(project, action.key)"
                        target="_blank"
                        rel="noreferrer"
                        class="link-icon"
                        :title="getProjectActionTooltip(project, action)"
                        :aria-label="getProjectActionTooltip(project, action)"
                      >
                        <svg
                          v-if="action.key === 'github'"
                          viewBox="0 0 24 24"
                          aria-hidden="true"
                        >
                          <path
                            d="M12 2C6.48 2 2 6.59 2 12.25c0 4.53 2.87 8.37 6.84 9.73.5.1.68-.22.68-.49 0-.24-.01-1.05-.01-1.9-2.78.62-3.37-1.22-3.37-1.22-.45-1.2-1.11-1.51-1.11-1.51-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.35 1.12 2.92.86.09-.67.35-1.12.63-1.38-2.22-.26-4.56-1.14-4.56-5.09 0-1.13.39-2.05 1.03-2.78-.1-.26-.45-1.31.1-2.73 0 0 .84-.28 2.75 1.06A9.3 9.3 0 0 1 12 6.85c.85 0 1.71.12 2.51.36 1.91-1.34 2.75-1.06 2.75-1.06.55 1.42.2 2.47.1 2.73.64.73 1.03 1.65 1.03 2.78 0 3.96-2.35 4.82-4.58 5.08.36.32.68.95.68 1.92 0 1.38-.01 2.49-.01 2.83 0 .27.18.59.69.49A10.26 10.26 0 0 0 22 12.25C22 6.59 17.52 2 12 2Z"
                          />
                        </svg>
                        <svg
                          v-else
                          viewBox="0 0 24 24"
                          aria-hidden="true"
                        >
                          <path
                            d="M14 3h7v7h-2V6.41l-8.29 8.3-1.42-1.42 8.3-8.29H14V3Zm5 16H5V5h7V3H5a2 2 0 0 0-2 2v14c0 1.11.89 2 2 2h14a2 2 0 0 0 2-2v-7h-2v7Z"
                          />
                        </svg>
                        <span class="tooltip">{{ getProjectActionTooltip(project, action) }}</span>
                      </a>

                      <button
                        v-else
                        type="button"
                        class="link-icon is-disabled"
                        :title="getProjectActionTooltip(project, action)"
                        :aria-label="getProjectActionTooltip(project, action)"
                        tabindex="-1"
                      >
                        <svg
                          v-if="action.key === 'github'"
                          viewBox="0 0 24 24"
                          aria-hidden="true"
                        >
                          <path
                            d="M12 2C6.48 2 2 6.59 2 12.25c0 4.53 2.87 8.37 6.84 9.73.5.1.68-.22.68-.49 0-.24-.01-1.05-.01-1.9-2.78.62-3.37-1.22-3.37-1.22-.45-1.2-1.11-1.51-1.11-1.51-.91-.64.07-.63.07-.63 1 .07 1.53 1.06 1.53 1.06.9 1.57 2.35 1.12 2.92.86.09-.67.35-1.12.63-1.38-2.22-.26-4.56-1.14-4.56-5.09 0-1.13.39-2.05 1.03-2.78-.1-.26-.45-1.31.1-2.73 0 0 .84-.28 2.75 1.06A9.3 9.3 0 0 1 12 6.85c.85 0 1.71.12 2.51.36 1.91-1.34 2.75-1.06 2.75-1.06.55 1.42.2 2.47.1 2.73.64.73 1.03 1.65 1.03 2.78 0 3.96-2.35 4.82-4.58 5.08.36.32.68.95.68 1.92 0 1.38-.01 2.49-.01 2.83 0 .27.18.59.69.49A10.26 10.26 0 0 0 22 12.25C22 6.59 17.52 2 12 2Z"
                          />
                        </svg>
                        <svg
                          v-else
                          viewBox="0 0 24 24"
                          aria-hidden="true"
                        >
                          <path
                            d="M14 3h7v7h-2V6.41l-8.29 8.3-1.42-1.42 8.3-8.29H14V3Zm5 16H5V5h7V3H5a2 2 0 0 0-2 2v14c0 1.11.89 2 2 2h14a2 2 0 0 0 2-2v-7h-2v7Z"
                          />
                        </svg>
                        <span class="tooltip">{{ getProjectActionTooltip(project, action) }}</span>
                      </button>
                    </template>
                  </div>
                </div>

                <p class="project-desc">{{ project.description }}</p>

                <div class="tech-stack">
                  <span v-for="tech in project.tech_stack" :key="tech" class="tech-tag">
                    {{ tech }}
                  </span>
                </div>

                <div class="highlights">
                  <span
                    v-for="highlight in project.highlights"
                    :key="highlight"
                    class="highlight-item"
                  >
                    {{ highlight }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div v-if="filteredProjects.length === 0" class="empty-state">
            <p>当前筛选下还没有已发布项目。</p>
          </div>
        </template>
      </div>
    </section>

    <section class="stats-section">
      <div class="container">
        <div class="stats-grid">
          <div class="stat-card">
            <span class="stat-number">{{ projects.length }}</span>
            <span class="stat-label">已发布项目</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{{ techCount }}</span>
            <span class="stat-label">技术栈</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{{ projects.filter((project) => project.demo).length }}</span>
            <span class="stat-label">在线演示</span>
          </div>
          <div class="stat-card">
            <span class="stat-number">{{ projects.filter((project) => project.github).length }}</span>
            <span class="stat-label">开源仓库</span>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.projects-page {
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
  margin-bottom: 40px;
}

.filters {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 10px 24px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 25px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(0, 191, 255, 0.1);
  border-color: rgba(0, 191, 255, 0.4);
}

.filter-btn.active {
  background: linear-gradient(135deg, #00bfff, #1e90ff);
  border-color: transparent;
  color: #fff;
}

.projects-section {
  padding: 40px 0;
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

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
  gap: 28px;
}

.project-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 20px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.project-card:hover {
  border-color: rgba(0, 191, 255, 0.35);
  transform: translateY(-4px);
}

.project-visual {
  height: 160px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.08), rgba(0, 255, 255, 0.03));
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.project-visual.has-image {
  background: rgba(5, 12, 26, 0.72);
}

.project-visual::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, rgba(0, 191, 255, 0.15) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s;
}

.visual-content,
.project-image {
  width: 100%;
  height: 100%;
}

.visual-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.project-image {
  display: block;
  object-fit: cover;
  transition: transform 0.35s ease;
}

.project-card:hover .project-image {
  transform: scale(1.04);
}

.project-card:hover .project-visual::before {
  opacity: 1;
}

.project-icon {
  font-size: 2.4rem;
  color: #00bfff;
  transition: all 0.3s ease;
}

.project-card:hover .project-icon {
  transform: scale(1.12);
  color: #00ffff;
}

.project-body {
  padding: 28px;
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  margin-bottom: 12px;
}

.project-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #fff;
}

.project-links {
  display: flex;
  gap: 10px;
  align-items: center;
  min-width: 88px;
  justify-content: flex-end;
}

.link-icon {
  position: relative;
  width: 40px;
  height: 40px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 191, 255, 0.18);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.76);
  text-decoration: none;
  transition: all 0.3s ease;
}

.link-icon svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
}

.link-icon:hover {
  background: rgba(0, 191, 255, 0.14);
  border-color: rgba(0, 191, 255, 0.45);
  color: #00ffff;
  transform: translateY(-2px);
}

.link-icon.is-disabled {
  cursor: default;
  color: rgba(255, 255, 255, 0.28);
  border-color: rgba(255, 255, 255, 0.08);
  background: rgba(255, 255, 255, 0.03);
}

.link-icon.is-disabled:hover {
  transform: none;
  color: rgba(255, 255, 255, 0.45);
  border-color: rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.05);
}

.tooltip {
  position: absolute;
  left: 50%;
  bottom: calc(100% + 10px);
  transform: translateX(-50%) translateY(4px);
  min-width: max-content;
  max-width: 180px;
  padding: 6px 10px;
  border-radius: 8px;
  background: rgba(8, 16, 32, 0.94);
  border: 1px solid rgba(0, 191, 255, 0.18);
  color: rgba(255, 255, 255, 0.88);
  font-size: 0.75rem;
  line-height: 1.4;
  white-space: nowrap;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.2s ease, transform 0.2s ease;
  box-shadow: 0 14px 28px rgba(0, 0, 0, 0.32);
}

.tooltip::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 100%;
  width: 8px;
  height: 8px;
  background: rgba(8, 16, 32, 0.94);
  border-right: 1px solid rgba(0, 191, 255, 0.18);
  border-bottom: 1px solid rgba(0, 191, 255, 0.18);
  transform: translateX(-50%) rotate(45deg);
}

.link-icon:hover .tooltip,
.link-icon:focus-visible .tooltip {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

.project-desc {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.7;
  margin-bottom: 20px;
}

.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.tech-tag {
  padding: 5px 14px;
  background: rgba(0, 191, 255, 0.08);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 15px;
  font-size: 0.75rem;
  color: #00bfff;
}

.highlights {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
}

.highlight-item {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.48);
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: rgba(255, 255, 255, 0.5);
}

.stats-section {
  padding: 80px 0;
  background: rgba(255, 255, 255, 0.02);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.stat-card {
  text-align: center;
  padding: 30px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 16px;
}

.stat-number {
  display: block;
  font-family: 'Orbitron', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #00bfff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

@media (max-width: 900px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 100px 0 40px;
  }

  .page-title {
    font-size: 1.8rem;
  }

  .projects-grid {
    grid-template-columns: 1fr;
  }

  .project-header {
    flex-direction: column;
  }

  .project-links {
    width: 100%;
    justify-content: flex-start;
  }
}
</style>
