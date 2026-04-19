<script setup lang="ts">
import { RouterLink } from 'vue-router'

const currentYear = new Date().getFullYear()

const navLinks = [
  { name: '首页', path: '/' },
  { name: '文章', path: '/articles' },
  { name: '项目', path: '/projects' },
  { name: '关于', path: '/about' },
]

const categories = [
  { name: '大模型实战', path: '/category/llm' },
  { name: 'AI 动漫生成', path: '/category/ai-anime' },
  { name: 'Python 开发', path: '/category/python' },
  { name: '踩坑记录', path: '/category/debug' },
]

const socialLinks = [
  { name: 'GitHub', icon: 'GH', url: 'https://github.com' },
  { name: '掘金', icon: 'J', url: '#' },
  { name: 'CSDN', icon: 'C', url: '#' },
]
</script>

<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-main">
        <div class="footer-brand">
          <RouterLink to="/" class="logo">
            <span class="logo-icon">*</span>
            <span class="logo-text">SkyBlog</span>
          </RouterLink>
          <p class="footer-desc">
            用代码改变世界
            <br />
            让 AI 创造未来
          </p>
          <div class="social-links">
            <a
              v-for="social in socialLinks"
              :key="social.name"
              :href="social.url"
              target="_blank"
              class="social-btn"
              :title="social.name"
            >
              {{ social.icon }}
            </a>
          </div>
        </div>

        <div class="footer-nav">
          <div class="nav-group">
            <h4>导航</h4>
            <RouterLink
              v-for="link in navLinks"
              :key="link.name"
              :to="link.path"
              class="nav-link"
            >
              {{ link.name }}
            </RouterLink>
          </div>
          <div class="nav-group">
            <h4>分类</h4>
            <RouterLink
              v-for="cat in categories"
              :key="cat.name"
              :to="cat.path"
              class="nav-link"
            >
              {{ cat.name }}
            </RouterLink>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p>(c) {{ currentYear }} SkyBlog. All rights reserved.</p>
        <div class="footer-decoration">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: rgba(10, 10, 26, 0.9);
  border-top: 1px solid rgba(0, 191, 255, 0.1);
  padding: 60px 24px 30px;
  position: relative;
  z-index: 1;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
}

.footer-main {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 60px;
  padding-bottom: 40px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.footer-brand .logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 1.4rem;
  font-weight: bold;
  text-decoration: none;
  margin-bottom: 16px;
}

.logo-icon {
  color: #00bfff;
  font-size: 1.4rem;
}

.logo-text {
  background: linear-gradient(135deg, #00bfff, #00ffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.footer-desc {
  color: rgba(255, 255, 255, 0.5);
  line-height: 1.8;
  margin-bottom: 20px;
}

.social-links {
  display: flex;
  gap: 12px;
}

.social-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 10px;
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.3s;
}

.social-btn:hover {
  background: rgba(0, 191, 255, 0.15);
  border-color: rgba(0, 191, 255, 0.4);
  color: #00ffff;
  transform: translateY(-2px);
}

.footer-nav {
  display: flex;
  justify-content: flex-end;
  gap: 80px;
}

.nav-group h4 {
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem;
  color: #fff;
  margin: 0 0 16px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.nav-group .nav-link {
  display: block;
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  font-size: 0.9rem;
  margin-bottom: 12px;
  transition: color 0.3s;
}

.nav-group .nav-link:hover {
  color: #00ffff;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 24px;
}

.footer-bottom p {
  color: rgba(255, 255, 255, 0.35);
  font-size: 0.85rem;
  margin: 0;
}

.footer-decoration {
  display: flex;
  gap: 8px;
}

.footer-decoration span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #00bfff;
  animation: blink 1.5s ease-in-out infinite;
}

.footer-decoration span:nth-child(2) {
  animation-delay: 0.3s;
  background: #00ffff;
}

.footer-decoration span:nth-child(3) {
  animation-delay: 0.6s;
  background: #1e90ff;
}

@keyframes blink {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1.2); }
}

@media (max-width: 768px) {
  .footer-main {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }

  .footer-nav {
    justify-content: center;
    gap: 40px;
  }

  .social-links {
    justify-content: center;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
