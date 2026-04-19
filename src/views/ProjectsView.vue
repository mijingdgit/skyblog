<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchPublishedProjects } from '../api/public'
import type { AdminProject } from '../types/admin'
import { filterProjectsByPreset } from '../utils/content'

const activeFilter = ref('all')
const hoverProject = ref<number | null>(null)
const projects = ref<AdminProject[]>([])
const isLoading = ref(true)
const loadError = ref('')

const filters = [
  { key: 'all', label: '全部' },
  { key: 'llm', label: 'AI / 大模型' },
  { key: 'frontend', label: '前端项目' },
  { key: 'backend', label: '后端项目' },
]

const filteredProjects = computed(() => filterProjectsByPreset(projects.value, activeFilter.value))
const techCount = computed(() => new Set(projects.value.flatMap((project) => project.tech_stack)).size)

onMounted(async () => {
  try {
    projects.value = await fetchPublishedProjects()
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
        <h1 class="page-title">项目<span class="accent">作品</span></h1>
        <p class="page-desc">这里展示的项目内容，已经改为直接读取后台已发布数据。</p>

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
              <div class="project-visual" :class="{ hover: hoverProject === project.id }">
                <div class="visual-content">
                  <span class="project-icon">{{ project.image || project.title.slice(0, 1) }}</span>
                </div>
              </div>

              <div class="project-body">
                <div class="project-header">
                  <h2 class="project-title">{{ project.title }}</h2>
                  <div class="project-links">
                    <a
                      v-if="project.github"
                      :href="project.github"
                      target="_blank"
                      rel="noreferrer"
                      class="link-btn"
                      title="GitHub"
                    >
                      GitHub
                    </a>
                    <a
                      v-if="project.demo"
                      :href="project.demo"
                      target="_blank"
                      rel="noreferrer"
                      class="link-btn"
                      title="在线演示"
                    >
                      Demo
                    </a>
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

.project-visual::before {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at 50% 50%, rgba(0, 191, 255, 0.15) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s;
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
  gap: 12px;
  margin-bottom: 12px;
}

.project-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #fff;
}

.project-links {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.link-btn {
  padding: 6px 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.8rem;
  transition: all 0.3s;
}

.link-btn:hover {
  background: rgba(0, 191, 255, 0.15);
  color: #00ffff;
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
}
</style>
