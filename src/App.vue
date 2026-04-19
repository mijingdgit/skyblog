<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
import FooterSection from './components/FooterSection.vue'
import BackToTop from './components/BackToTop.vue'
import ThreeBackground from './components/ThreeBackground.vue'

const route = useRoute()
const isHome = computed(() => route.path === '/')
</script>

<template>
  <ThreeBackground />
  <NavBar />
  <!-- 磨砂玻璃背景层 - 非首页显示 -->
  <div v-if="!isHome" class="glass-overlay"></div>
  <main :class="{ 'has-glass': !isHome }">
    <RouterView v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </RouterView>
  </main>
  <FooterSection />
  <BackToTop />
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Noto Sans SC', 'Microsoft YaHei', sans-serif;
  background: #0a0a1a;
  color: #fff;
  overflow-x: hidden;
}

main {
  position: relative;
  z-index: 1;
  min-height: 100vh;
}

/* 磨砂玻璃背景层 */
.glass-overlay {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(10, 10, 26, 0.7);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  z-index: 0;
}

main.has-glass {
  position: relative;
  z-index: 1;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 代码块样式 */
pre {
  background: #1e1e2e !important;
  border-radius: 12px;
  padding: 20px !important;
  overflow-x: auto;
  margin: 16px 0;
  border: 1px solid rgba(0, 191, 255, 0.15);
}

code {
  font-family: 'Fira Code', 'Consolas', monospace;
  font-size: 14px;
  line-height: 1.6;
}

:not(pre) > code {
  background: rgba(0, 191, 255, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
  color: #00ffff;
}

/* 文章内容样式 */
.article-content h1 {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 2rem;
  color: #00bfff;
  margin: 32px 0 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid rgba(0, 191, 255, 0.3);
}

.article-content h2 {
  font-size: 1.5rem;
  color: #fff;
  margin: 28px 0 16px;
}

.article-content h3 {
  font-size: 1.2rem;
  color: #00ffff;
  margin: 24px 0 12px;
}

.article-content p {
  line-height: 1.8;
  margin: 16px 0;
  color: rgba(255, 255, 255, 0.85);
}

.article-content ul,
.article-content ol {
  margin: 16px 0;
  padding-left: 24px;
}

.article-content li {
  line-height: 1.8;
  margin: 8px 0;
}

.article-content strong {
  color: #00ffff;
}

.article-content a {
  color: #00bfff;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s;
}

.article-content a:hover {
  border-bottom-color: #00ffff;
}

.article-content blockquote {
  margin: 20px 0;
  padding: 16px 24px;
  background: rgba(0, 191, 255, 0.05);
  border-left: 4px solid #00bfff;
  border-radius: 0 8px 8px 0;
}

.article-content img {
  max-width: 100%;
  border-radius: 12px;
  margin: 16px 0;
}

/* 滚动条 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #0a0a1a;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #00bfff, #1e90ff);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(180deg, #00ffff, #00bfff);
}

::selection {
  background: #00bfff;
  color: #fff;
}
</style>