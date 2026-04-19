<script setup lang="ts">
import { ref } from 'vue'

// 个人简介
const profile = {
  name: 'Sky',
  title: 'Python 开发者 & AI 应用工程师',
  location: '中国',
  email: 'hello@example.com',
  github: 'https://github.com',
  slogan: '用代码改变世界，让 AI 创造未来'
}

// 技术技能
const skills = {
  'Python 核心': ['异步编程', '装饰器', '生成器', '元编程'],
  'Web 框架': ['FastAPI', 'Django', 'Flask', 'Tornado'],
  'AI/ML': ['LangChain', 'OpenAI API', 'Claude API', 'RAG', 'Vector DB'],
  'AI 绘画': ['Stable Diffusion', 'ComfyUI', 'LoRA', 'ControlNet'],
  '前端技术': ['Vue3', 'TypeScript', 'Three.js', 'Element Plus'],
  'DevOps': ['Docker', 'Linux', 'Nginx', 'Git']
}

// 项目经验
const experiences = [
  {
    period: '2024 - 至今',
    title: 'AI 应用开发工程师',
    company: '某科技公司',
    description: '负责企业级 AI 知识库问答系统开发，基于 RAG 架构实现私有文档智能问答'
  },
  {
    period: '2022 - 2024',
    title: 'Python 后端开发',
    company: '某互联网公司',
    description: '负责 RESTful API 开发，高并发服务架构设计，微服务化改造'
  },
  {
    period: '2020 - 2022',
    title: '全栈开发工程师',
    company: '某创业公司',
    description: '从 0 到 1 构建多个 Web 项目，包括电商平台、数据可视化后台'
  }
]

// 发展方向
const directions = [
  {
    icon: '🧠',
    title: '大模型应用开发',
    desc: '专注于 LLM 应用落地，包括 RAG、Agent、Prompt 工程等'
  },
  {
    icon: '🎨',
    title: 'AI 动漫生成',
    desc: '探索 Stable Diffusion、ComfyUI 工作流自动化、AI 视频生成等'
  },
  {
    icon: '⚡',
    title: '高性能 Python',
    desc: '深入异步编程、性能优化、高并发架构设计'
  }
]

// 认证证书
const certifications = [
  'AWS Certified Solutions Architect',
  '阿里云 ACE 认证',
  'Python Institute PCAP',
  'DeepLearning.AI TensorFlow 开发者证书'
]

const activeTab = ref('profile')

const tabs = [
  { key: 'profile', label: '个人简介' },
  { key: 'skills', label: '技能栈' },
  { key: 'experience', label: '项目经验' },
  { key: 'contact', label: '联系方式' }
]
</script>

<template>
  <div class="about-page">
    <!-- Header -->
    <section class="page-header">
      <div class="container">
        <h1 class="page-title">关于<span class="accent">我</span></h1>
        <p class="page-desc">探索我的技术旅程和成长轨迹</p>
      </div>
    </section>

    <div class="container">
      <div class="about-layout">
        <!-- Sidebar -->
        <aside class="about-sidebar">
          <div class="avatar-section">
            <div class="avatar-wrapper">
              <div class="avatar-ring"></div>
              <div class="avatar-ring ring-2"></div>
              <div class="avatar">
                <span>◈</span>
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

        <!-- Main Content -->
        <main class="about-content">
          <!-- Profile Tab -->
          <section v-if="activeTab === 'profile'" class="content-section">
            <h2 class="section-title">你好，我是 {{ profile.name }} 👋</h2>

            <div class="intro-text">
              <p>
                一名专注于 <strong>Python 开发</strong> 和 <strong>AI 应用</strong> 的全栈工程师。
                我热爱开源技术，擅长将前沿 AI 能力落地到实际业务场景中。
              </p>
              <p>
                我的技术旅程始于大学时期对 Python 的热爱，从简单的脚本到复杂的 Web 应用，
                再到如今日火如荼的大模型应用，我始终保持着对新技术的渴望和学习热情。
              </p>
              <p>
                在这个博客中，我会分享我在 AI 应用开发、Python 进阶、动漫生成等技术领域的学习心得和实践经验。
                希望能够与志同道合的朋友们一起交流进步！
              </p>
            </div>

            <h3 class="subsection-title">我的方向</h3>
            <div class="directions-grid">
              <div v-for="dir in directions" :key="dir.title" class="direction-card">
                <span class="dir-icon">{{ dir.icon }}</span>
                <h4>{{ dir.title }}</h4>
                <p>{{ dir.desc }}</p>
              </div>
            </div>

            <h3 class="subsection-title">认证证书</h3>
            <div class="cert-list">
              <span v-for="cert in certifications" :key="cert" class="cert-item">
                🏆 {{ cert }}
              </span>
            </div>
          </section>

          <!-- Skills Tab -->
          <section v-if="activeTab === 'skills'" class="content-section">
            <h2 class="section-title">技能栈</h2>

            <div class="skills-grid">
              <div v-for="(skillsList, category) in skills" :key="category" class="skill-category">
                <h3 class="category-title">{{ category }}</h3>
                <div class="skill-tags">
                  <span v-for="skill in skillsList" :key="skill" class="skill-tag">
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>

            <h3 class="subsection-title">工具与环境</h3>
            <div class="tools-grid">
              <div class="tool-item">
                <span class="tool-icon">🐳</span>
                <span>Docker</span>
              </div>
              <div class="tool-item">
                <span class="tool-icon">🐧</span>
                <span>Linux</span>
              </div>
              <div class="tool-item">
                <span class="tool-icon">📝</span>
                <span>Git</span>
              </div>
              <div class="tool-item">
                <span class="tool-icon">💻</span>
                <span>VS Code</span>
              </div>
              <div class="tool-item">
                <span class="tool-icon">🔥</span>
                <span>Postman</span>
              </div>
              <div class="tool-item">
                <span class="tool-icon">📊</span>
                <span>Prometheus</span>
              </div>
            </div>
          </section>

          <!-- Experience Tab -->
          <section v-if="activeTab === 'experience'" class="content-section">
            <h2 class="section-title">项目经验</h2>

            <div class="timeline">
              <div v-for="exp in experiences" :key="exp.title" class="timeline-item">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                  <span class="period">{{ exp.period }}</span>
                  <h3 class="exp-title">{{ exp.title }}</h3>
                  <span class="company">{{ exp.company }}</span>
                  <p class="exp-desc">{{ exp.description }}</p>
                </div>
              </div>
            </div>

            <h3 class="subsection-title">核心能力</h3>
            <div class="abilities-grid">
              <div class="ability-item">
                <span class="ability-icon">🚀</span>
                <div>
                  <h4>高性能服务开发</h4>
                  <p>熟练使用 FastAPI/Django 构建高并发 API 服务</p>
                </div>
              </div>
              <div class="ability-item">
                <span class="ability-icon">🤖</span>
                <div>
                  <h4>AI 应用开发</h4>
                  <p>RAG 知识库、智能对话、Agent 架构设计</p>
                </div>
              </div>
              <div class="ability-item">
                <span class="ability-icon">🎨</span>
                <div>
                  <h4>AI 图像生成</h4>
                  <p>SD/ComfyUI 工作流定制、LoRA 训练</p>
                </div>
              </div>
              <div class="ability-item">
                <span class="ability-icon">⚙️</span>
                <div>
                  <h4>DevOps</h4>
                  <p>Docker 容器化、CI/CD 流程、自动化部署</p>
                </div>
              </div>
            </div>
          </section>

          <!-- Contact Tab -->
          <section v-if="activeTab === 'contact'" class="content-section">
            <h2 class="section-title">联系方式</h2>

            <div class="contact-grid">
              <a :href="`mailto:${profile.email}`" class="contact-card">
                <span class="contact-icon">📧</span>
                <span class="contact-label">邮箱</span>
                <span class="contact-value">{{ profile.email }}</span>
              </a>
              <a :href="profile.github" target="_blank" class="contact-card">
                <span class="contact-icon">⌘</span>
                <span class="contact-label">GitHub</span>
                <span class="contact-value">@yourname</span>
              </a>
              <div class="contact-card">
                <span class="contact-icon">📍</span>
                <span class="contact-label">位置</span>
                <span class="contact-value">{{ profile.location }}</span>
              </div>
            </div>

            <div class="cta-section">
              <h3>让我们一起探索 AI 的无限可能！</h3>
              <p>如果你对 AI 应用开发、Python 技术或者动漫生成感兴趣，欢迎随时联系我交流探讨。</p>
              <a :href="`mailto:${profile.email}`" class="cta-btn">
                联系我 →
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

/* Header */
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

/* Layout */
.about-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 50px;
}

/* Sidebar */
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

/* Content */
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

/* Profile */
.intro-text p {
  color: rgba(255, 255, 255, 0.75);
  line-height: 1.9;
  margin-bottom: 20px;
}

.intro-text strong {
  color: #00ffff;
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
  font-size: 2rem;
  display: block;
  margin-bottom: 12px;
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

/* Skills */
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

.tool-icon {
  font-size: 1.2rem;
}

/* Experience */
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

.ability-icon {
  font-size: 1.8rem;
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

/* Contact */
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
  font-size: 2rem;
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

/* Responsive */
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

  .directions-grid {
    grid-template-columns: 1fr;
  }

  .contact-grid {
    grid-template-columns: 1fr;
  }
}
</style>