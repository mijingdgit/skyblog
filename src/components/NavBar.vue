<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
const isMenuOpen = ref(false)

const navItems = [
  { name: '首页', path: '/' },
  { name: '文章', path: '/articles' },
  { name: '项目', path: '/projects' },
  { name: '关于', path: '/about' },
]

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const isRouteActive = (path: string) => route.path === path
</script>

<template>
  <nav class="navbar">
    <div class="navbar-container">
      <RouterLink to="/" class="logo" @click="closeMenu">
        <span class="logo-icon">*</span>
        <span class="logo-text">SkyBlog</span>
      </RouterLink>

      <div class="nav-links" :class="{ active: isMenuOpen }">
        <RouterLink
          v-for="item in navItems"
          :key="item.name"
          :to="item.path"
          class="nav-link"
          :class="{ active: isRouteActive(item.path) }"
          @click="closeMenu"
        >
          {{ item.name }}
        </RouterLink>
      </div>

      <button class="menu-toggle" :class="{ active: isMenuOpen }" @click="toggleMenu">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  z-index: 1000;
  background: rgba(10, 10, 26, 0.85);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 191, 255, 0.15);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 1.4rem;
  font-weight: bold;
  text-decoration: none;
}

.logo-icon {
  color: #00bfff;
  font-size: 1.4rem;
  animation: pulse 2s ease-in-out infinite;
}

.logo-text {
  background: linear-gradient(135deg, #00bfff, #00ffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
    transform: scale(1);
  }

  50% {
    opacity: 0.7;
    transform: scale(1.1);
  }
}

.nav-links {
  display: flex;
  gap: 8px;
  align-items: center;
}

.nav-link {
  padding: 10px 20px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  font-size: 0.95rem;
  position: relative;
  border-radius: 8px;
  transition: all 0.3s ease;
  background: none;
  border: none;
  cursor: pointer;
}

.nav-link:hover {
  color: #fff;
  background: rgba(0, 191, 255, 0.1);
}

.nav-link.active {
  color: #00ffff;
  background: rgba(0, 191, 255, 0.15);
}

.menu-toggle {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px;
}

.menu-toggle span {
  width: 24px;
  height: 2px;
  background: #00bfff;
  transition: all 0.3s ease;
}

.menu-toggle.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.menu-toggle.active span:nth-child(2) {
  opacity: 0;
}

.menu-toggle.active span:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

@media (max-width: 768px) {
  .menu-toggle {
    display: flex;
  }

  .nav-links {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    background: rgba(10, 10, 26, 0.98);
    backdrop-filter: blur(20px);
    flex-direction: column;
    align-items: center;
    padding: 24px;
    gap: 8px;
    transform: translateY(-100%);
    opacity: 0;
    transition: all 0.3s ease;
    pointer-events: none;
  }

  .nav-links.active {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
  }

  .nav-link {
    width: 100%;
    text-align: center;
    padding: 14px 20px;
  }
}
</style>
