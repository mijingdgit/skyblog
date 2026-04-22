<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { fetchAboutProfile } from '../api/public'
import type { AboutProfile } from '../types/admin'
import { applySeo } from '../utils/seo'

const defaultProfile: AboutProfile = {
  id: 0,
  name: 'Sky',
  title: 'Python 开发者 & AI 应用实践者',
  location: '中国',
  email: 'hello@example.com',
  github: 'https://github.com',
  slogan: '用代码记录学习，用 AI 扩展创造。',
  avatar_text: 'S',
  page_title: '关于我',
  page_description: '探索我的技术旅程和成长轨迹',
  intro_title: '你好，我是 Sky',
  intro_paragraphs: [
    '一名专注于 Python 开发和 AI 应用落地的全栈开发者，喜欢把新技术拆解成可以被实际项目使用的能力。',
    '我的学习路线从 Python、Django、Vue 开始，逐步延伸到大模型应用、知识库问答、自动化工作流和内容生产工具。',
    '这个博客会记录技术学习、项目实践和踩坑经验，也会持续整理 AI 工具链在真实场景中的使用方式。',
  ],
  skills: [
    { category: 'Python 核心', items: ['异步编程', 'Django', 'FastAPI', '自动化脚本'] },
    { category: '前端技术', items: ['Vue3', 'TypeScript', 'Vite', 'CSS3'] },
    { category: 'AI 应用', items: ['RAG', 'Agent', 'Prompt 工程', 'XMind 知识整理'] },
  ],
  directions: [
    { icon: 'AI', title: '大模型应用开发', desc: '关注 LLM 在知识库、自动化办公和学习系统中的落地。' },
    { icon: 'Py', title: 'Python 全栈开发', desc: '使用 Django、FastAPI 和 Vue 构建稳定、可维护的 Web 应用。' },
    { icon: 'Ops', title: '部署与工程化', desc: '整理项目上线、媒体资源和持续迭代中的实践。' },
  ],
  experiences: [
    {
      period: '2026 - 至今',
      title: 'SkyBlog 个人技术站',
      company: '个人项目',
      description: '基于 Vue3 与 Django 搭建内容发布系统，支持文章、项目、Markdown、XMind 和后台管理。',
    },
  ],
  certifications: ['持续学习 Python / Django / Vue3', 'AI 大模型应用实践', '个人技术博客建设'],
  tools: [
    { icon: 'Code', name: 'VS Code' },
    { icon: 'Git', name: 'Git' },
    { icon: 'API', name: 'Postman' },
    { icon: 'Docker', name: 'Docker' },
  ],
  abilities: [
    { icon: 'API', title: '后端接口开发', desc: '使用 Django/FastAPI 构建内容管理和业务 API。' },
    { icon: 'Web', title: '前端页面实现', desc: '使用 Vue3 和 TypeScript 完成响应式交互页面。' },
    { icon: 'AI', title: 'AI 内容工具', desc: '将 Markdown、XMind、Word 等学习资料接入内容展示流程。' },
  ],
  contact_title: '一起交流技术与 AI 实践',
  contact_description: '如果你对 Python、Django、Vue 或 AI 应用开发感兴趣，欢迎随时联系我交流。',
  is_active: true,
  created_at: '',
  updated_at: '',
}

const profile = ref<AboutProfile>(defaultProfile)
const activeTab = ref('profile')
const isLoading = ref(true)
const loadError = ref('')

const tabs = [
  { key: 'profile', label: '个人简介' },
  { key: 'skills', label: '技能栏' },
  { key: 'experience', label: '项目经历' },
  { key: 'contact', label: '联系方式' },
]

const githubName = computed(() => {
  if (!profile.value.github) return '未填写'

  try {
    const url = new URL(profile.value.github)
    return url.pathname.replace(/^\/|\/$/g, '') || url.hostname
  } catch {
    return profile.value.github
  }
})

const pageTitlePrefix = computed(() => {
  const title = profile.value.page_title || '关于我'
  if (title.includes(profile.value.name)) {
    return title.replace(profile.value.name, '')
  }
  if (title.endsWith('我')) {
    return title.slice(0, -1)
  }
  return title
})

const pageTitleAccent = computed(() => {
  const title = profile.value.page_title || '关于我'
  if (title.includes(profile.value.name)) {
    return profile.value.name
  }
  if (title.endsWith('我')) {
    return '我'
  }
  return ''
})

function mergeWithDefaults(data: AboutProfile): AboutProfile {
  return {
    ...defaultProfile,
    ...data,
    intro_paragraphs: Array.isArray(data.intro_paragraphs) ? data.intro_paragraphs : defaultProfile.intro_paragraphs,
    skills: Array.isArray(data.skills) ? data.skills : defaultProfile.skills,
    directions: Array.isArray(data.directions) ? data.directions : defaultProfile.directions,
    experiences: Array.isArray(data.experiences) ? data.experiences : defaultProfile.experiences,
    certifications: Array.isArray(data.certifications) ? data.certifications : defaultProfile.certifications,
    tools: Array.isArray(data.tools) ? data.tools : defaultProfile.tools,
    abilities: Array.isArray(data.abilities) ? data.abilities : defaultProfile.abilities,
  }
}

onMounted(async () => {
  try {
    profile.value = mergeWithDefaults(await fetchAboutProfile())
    applySeo({
      title: profile.value.page_title || '关于我',
      description: profile.value.page_description || profile.value.slogan,
      path: '/about',
    })
  } catch {
    loadError.value = '关于资料加载失败，当前显示本地默认内容。'
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="about-page">
    <section class="page-header">
      <div class="container">
        <h1 class="page-title">
          {{ pageTitlePrefix }}<span v-if="pageTitleAccent" class="accent">{{ pageTitleAccent }}</span>
        </h1>
        <p class="page-desc">{{ profile.page_description }}</p>
      </div>
    </section>

    <section v-if="isLoading || loadError" class="status-section">
      <div class="container">
        <div class="status-card" :class="{ error: loadError }">
          {{ isLoading ? '正在读取后台关于资料...' : loadError }}
        </div>
      </div>
    </section>

    <div class="container">
      <div class="about-layout">
        <aside class="about-sidebar">
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <div class="avatar-ring"></div>
              <div class="avatar-ring ring-2"></div>
              <div class="avatar">
                <span>{{ profile.avatar_text || profile.name.slice(0, 1) }}</span>
              </div>
            </div>
            <h2 class="name">{{ profile.name }}</h2>
            <p class="title">{{ profile.title }}</p>
            <p class="slogan">"{{ profile.slogan }}"</p>
          </div>

          <nav class="about-nav">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              class="nav-item"
              :class="{ active: activeTab === tab.key }"
              @click="activeTab = tab.key"
            >
              {{ tab.label }}
            </button>
          </nav>
        </aside>

        <main class="about-content">
          <section v-if="activeTab === 'profile'" class="content-section">
            <h2 class="section-title">{{ profile.intro_title }}</h2>

            <div class="intro-text">
              <p v-for="paragraph in profile.intro_paragraphs" :key="paragraph">
                {{ paragraph }}
              </p>
            </div>

            <h3 class="subsection-title">我的方向</h3>
            <div class="directions-grid">
              <div v-for="direction in profile.directions" :key="direction.title" class="direction-card">
                <span class="dir-icon">{{ direction.icon }}</span>
                <h4>{{ direction.title }}</h4>
                <p>{{ direction.desc }}</p>
              </div>
            </div>

            <h3 class="subsection-title">证书 / 学习记录</h3>
            <div class="cert-list">
              <span v-for="cert in profile.certifications" :key="cert" class="cert-item">
                {{ cert }}
              </span>
            </div>
          </section>

          <section v-if="activeTab === 'skills'" class="content-section">
            <h2 class="section-title">技能栏</h2>

            <div class="skills-grid">
              <div v-for="group in profile.skills" :key="group.category" class="skill-category">
                <h3 class="category-title">{{ group.category }}</h3>
                <div class="skill-tags">
                  <span v-for="skill in group.items" :key="skill" class="skill-tag">
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>

            <h3 class="subsection-title">工具与环境</h3>
            <div class="tools-grid">
              <div v-for="tool in profile.tools" :key="tool.name" class="tool-item">
                <span class="tool-icon">{{ tool.icon }}</span>
                <span>{{ tool.name }}</span>
              </div>
            </div>
          </section>

          <section v-if="activeTab === 'experience'" class="content-section">
            <h2 class="section-title">项目经历</h2>

            <div class="timeline">
              <div v-for="experience in profile.experiences" :key="experience.title" class="timeline-item">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                  <span class="period">{{ experience.period }}</span>
                  <h3 class="exp-title">{{ experience.title }}</h3>
                  <span class="company">{{ experience.company }}</span>
                  <p class="exp-desc">{{ experience.description }}</p>
                </div>
              </div>
            </div>

            <h3 class="subsection-title">核心能力</h3>
            <div class="abilities-grid">
              <div v-for="ability in profile.abilities" :key="ability.title" class="ability-item">
                <span class="ability-icon">{{ ability.icon }}</span>
                <div>
                  <h4>{{ ability.title }}</h4>
                  <p>{{ ability.desc }}</p>
                </div>
              </div>
            </div>
          </section>

          <section v-if="activeTab === 'contact'" class="content-section">
            <h2 class="section-title">联系方式</h2>

            <div class="contact-grid">
              <a :href="`mailto:${profile.email}`" class="contact-card">
                <span class="contact-icon">Mail</span>
                <span class="contact-label">邮箱</span>
                <span class="contact-value">{{ profile.email || '未填写' }}</span>
              </a>
              <a :href="profile.github" target="_blank" rel="noreferrer" class="contact-card">
                <span class="contact-icon">GitHub</span>
                <span class="contact-label">GitHub</span>
                <span class="contact-value">{{ githubName }}</span>
              </a>
              <div class="contact-card">
                <span class="contact-icon">Map</span>
                <span class="contact-label">位置</span>
                <span class="contact-value">{{ profile.location || '未填写' }}</span>
              </div>
            </div>

            <div class="cta-section">
              <h3>{{ profile.contact_title }}</h3>
              <p>{{ profile.contact_description }}</p>
              <a :href="`mailto:${profile.email}`" class="cta-btn">
                联系我 ->
              </a>
            </div>
          </section>
        </main>
      </div>
    </div>
  </div>
</template>

<style scoped>
.about-page {
  padding-bottom: 80px;
}

.container {
  max-width: 1100px;
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

.status-section {
  margin-bottom: 32px;
}

.status-card {
  padding: 16px 18px;
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.04);
  color: rgba(255, 255, 255, 0.74);
}

.status-card.error {
  border-color: rgba(255, 113, 103, 0.28);
  color: #ff9b94;
}

.about-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 50px;
}

.about-sidebar {
  position: sticky;
  top: 100px;
  height: fit-content;
}

.avatar-section {
  text-align: center;
  margin-bottom: 30px;
}

.avatar-wrapper {
  position: relative;
  width: 160px;
  height: 160px;
  margin: 0 auto 20px;
}

.avatar-ring {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: 2px solid transparent;
  border-top-color: #00bfff;
  border-radius: 50%;
  animation: rotate 6s linear infinite;
}

.avatar-ring.ring-2 {
  border-top-color: transparent;
  border-right-color: #00ffff;
  animation-direction: reverse;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.avatar {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100px;
  height: 100px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.2), rgba(0, 255, 255, 0.1));
  border: 2px solid rgba(0, 191, 255, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar span {
  font-size: 2.5rem;
  color: #00bfff;
}

.name {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.title {
  font-size: 0.95rem;
  color: #00bfff;
  margin-bottom: 12px;
}

.slogan {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
  font-style: italic;
}

.about-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.nav-item {
  padding: 14px 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
}

.nav-item:hover {
  background: rgba(0, 191, 255, 0.08);
}

.nav-item.active {
  background: rgba(0, 191, 255, 0.12);
  border-color: rgba(0, 191, 255, 0.4);
  color: #00ffff;
}

.content-section {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.section-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.8rem;
  margin-bottom: 30px;
}

.subsection-title {
  font-size: 1.2rem;
  color: #fff;
  margin: 40px 0 20px;
  padding-bottom: 12px;
  border-bottom: 1px solid rgba(0, 191, 255, 0.15);
}

.intro-text p {
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.9;
  margin-bottom: 20px;
}

.directions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}

.direction-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  transition: all 0.3s;
}

.direction-card:hover {
  border-color: rgba(0, 191, 255, 0.3);
  transform: translateY(-2px);
}

.dir-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 42px;
  height: 42px;
  padding: 0 10px;
  margin-bottom: 12px;
  border-radius: 14px;
  background: rgba(0, 191, 255, 0.1);
  color: #00ffff;
  font-size: 0.9rem;
  font-weight: 700;
}

.direction-card h4 {
  font-size: 1.05rem;
  color: #fff;
  margin-bottom: 8px;
}

.direction-card p {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.6;
}

.cert-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.cert-item {
  padding: 10px 18px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 10px;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.skills-grid {
  display: grid;
  gap: 24px;
}

.skill-category {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
}

.category-title {
  font-size: 1rem;
  color: #00bfff;
  margin-bottom: 14px;
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.skill-tag {
  padding: 6px 16px;
  background: rgba(0, 191, 255, 0.08);
  border-radius: 15px;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.8);
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.tool-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 10px;
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
}

.tool-icon,
.ability-icon {
  color: #00bfff;
  font-weight: 700;
}

.timeline {
  position: relative;
  padding-left: 30px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, #00bfff, #00ffff);
}

.timeline-item {
  position: relative;
  padding-bottom: 30px;
}

.timeline-marker {
  position: absolute;
  left: -34px;
  top: 4px;
  width: 10px;
  height: 10px;
  background: #00bfff;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(0, 191, 255, 0.5);
}

.timeline-content {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 12px;
  padding: 20px;
}

.period {
  font-size: 0.8rem;
  color: #00bfff;
  display: block;
  margin-bottom: 8px;
}

.exp-title {
  font-size: 1.1rem;
  color: #fff;
  margin-bottom: 4px;
}

.company {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
  display: block;
  margin-bottom: 10px;
}

.exp-desc {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
}

.abilities-grid {
  display: grid;
  gap: 20px;
}

.ability-item {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 12px;
}

.ability-item h4 {
  font-size: 1rem;
  color: #fff;
  margin-bottom: 6px;
}

.ability-item p {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.5);
}

.contact-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.contact-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 30px 20px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(0, 191, 255, 0.1);
  border-radius: 16px;
  text-decoration: none;
  transition: all 0.3s;
}

.contact-card:hover {
  background: rgba(0, 191, 255, 0.05);
  border-color: rgba(0, 191, 255, 0.3);
}

.contact-icon {
  color: #00bfff;
  font-weight: 700;
  margin-bottom: 12px;
}

.contact-label {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 6px;
}

.contact-value {
  font-size: 0.95rem;
  color: #fff;
}

.cta-section {
  text-align: center;
  padding: 40px;
  background: rgba(0, 191, 255, 0.05);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 20px;
}

.cta-section h3 {
  font-size: 1.3rem;
  margin-bottom: 12px;
}

.cta-section p {
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 24px;
}

.cta-btn {
  display: inline-block;
  padding: 14px 36px;
  background: linear-gradient(135deg, #00bfff, #1e90ff);
  border-radius: 30px;
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s;
}

.cta-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 191, 255, 0.4);
}

@media (max-width: 900px) {
  .about-layout {
    grid-template-columns: 1fr;
  }

  .about-sidebar {
    position: static;
    max-width: 400px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 100px 0 40px;
  }

  .page-title {
    font-size: 1.8rem;
  }

  .directions-grid,
  .contact-grid {
    grid-template-columns: 1fr;
  }
}
</style>
