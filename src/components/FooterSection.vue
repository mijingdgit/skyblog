<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { fetchPublicCategories } from '../api/public'
import type { AdminCategory } from '../types/admin'

const currentYear = new Date().getFullYear()
const categories = ref<AdminCategory[]>([])

const navLinks = [
  { name: '首页', path: '/' },
  { name: '文章', path: '/articles' },
  { name: '项目', path: '/projects' },
  { name: '关于', path: '/about' },
]

const footerCategories = computed(() =>
  [...categories.value]
    .sort((a, b) => a.order - b.order)
    .slice(0, 6),
)

const socialLinks = [
  { name: 'GitHub', key: 'github', url: 'https://github.com' },
  { name: '掘金', key: 'juejin', url: '#' },
  { name: 'CSDN', key: 'csdn', url: '#' },
]

onMounted(async () => {
  try {
    categories.value = await fetchPublicCategories()
  } catch {
    categories.value = []
  }
})
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
              rel="noreferrer"
              class="social-btn"
              :title="social.name"
              :aria-label="social.name"
            >
              <svg v-if="social.key === 'github'" viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M12 2C6.48 2 2 6.58 2 12.22c0 4.52 2.87 8.35 6.84 9.7.5.1.68-.22.68-.48 0-.24-.01-1.04-.01-1.88-2.78.61-3.37-1.21-3.37-1.21-.45-1.18-1.1-1.5-1.1-1.5-.91-.63.07-.62.07-.62 1 .07 1.53 1.05 1.53 1.05.9 1.55 2.35 1.1 2.92.84.09-.66.35-1.1.63-1.36-2.22-.25-4.56-1.13-4.56-5.05 0-1.12.39-2.03 1.03-2.75-.1-.25-.45-1.3.1-2.7 0 0 .84-.27 2.75 1.04A9.35 9.35 0 0 1 12 6.93c.85 0 1.71.11 2.51.35 1.91-1.31 2.75-1.04 2.75-1.04.55 1.4.2 2.45.1 2.7.64.72 1.03 1.63 1.03 2.75 0 3.93-2.35 4.79-4.58 5.04.36.31.68.94.68 1.9 0 1.37-.01 2.47-.01 2.81 0 .26.18.58.69.48A10.2 10.2 0 0 0 22 12.22C22 6.58 17.52 2 12 2Z"
                />
              </svg>
              <svg v-else-if="social.key === 'juejin'" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M12 2.5 20.5 8 12 13.5 3.5 8 12 2.5Z" />
                <path d="M4.3 10.5 12 15.5l7.7-5 1.8 1.2L12 18 2.5 11.7l1.8-1.2Z" />
                <path d="M5.8 14.3 12 18.2l6.2-3.9 1.8 1.2L12 21.5l-8-6 1.8-1.2Z" />
              </svg>
              <svg v-else viewBox="0 0 24 24" aria-hidden="true">
                <path
                  d="M12 3.2c4.64 0 8.4 2.62 8.4 5.85 0 1.83-1.22 3.46-3.13 4.53l1.03 2.84-3.34-1.61c-.91.2-1.91.31-2.96.31-4.64 0-8.4-2.62-8.4-5.85S7.36 3.2 12 3.2Zm-3.1 3.9c-1.47 0-2.54.92-2.54 2.16 0 1.27 1.04 2.15 2.55 2.15.78 0 1.44-.22 1.95-.64l-.68-1.02c-.34.28-.73.42-1.2.42-.67 0-1.09-.35-1.09-.91 0-.55.43-.91 1.07-.91.46 0 .85.14 1.19.42l.7-1.01A3.04 3.04 0 0 0 8.9 7.1Zm4.67.07h-1.51v4.17h1.51V7.17Zm2.77 0h-1.51v4.17h1.51V7.17ZM4.4 16.9h15.2v1.9H4.4v-1.9Z"
                />
              </svg>
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
              v-for="cat in footerCategories"
              :key="cat.id"
              :to="`/category/${cat.slug}`"
              class="nav-link"
            >
              {{ cat.name }}
              <span v-if="cat.article_count > 0" class="nav-count">{{ cat.article_count }}</span>
            </RouterLink>
            <span v-if="footerCategories.length === 0" class="nav-empty">暂无分类</span>
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

.social-btn svg {
  width: 20px;
  height: 20px;
  fill: currentColor;
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
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  color: rgba(255, 255, 255, 0.5);
  text-decoration: none;
  font-size: 0.9rem;
  margin-bottom: 12px;
  transition: color 0.3s;
}

.nav-group .nav-link:hover {
  color: #00ffff;
}

.nav-count {
  min-width: 22px;
  padding: 2px 7px;
  border-radius: 999px;
  background: rgba(0, 191, 255, 0.1);
  color: rgba(0, 255, 255, 0.8);
  font-size: 0.72rem;
  text-align: center;
}

.nav-empty {
  display: block;
  color: rgba(255, 255, 255, 0.35);
  font-size: 0.9rem;
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
