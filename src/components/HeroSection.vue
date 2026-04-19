<script setup lang="ts">
const scrollToBlog = () => {
  const element = document.querySelector('#blog')
  if (element) {
    element.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <section id="home" class="hero">
    <div class="hero-content">
      <h1 class="hero-title">
        <span class="title-line">欢迎来到</span>
        <span class="title-gradient">SkyBlog</span>
      </h1>
      <p class="hero-subtitle">
        探索技术的星辰大海<br>
        <span class="highlight">记录 · 分享 · 成长</span>
      </p>
      <button class="hero-btn" @click="scrollToBlog">
        <span>开始阅读</span>
        <span class="btn-icon">→</span>
      </button>
    </div>
    <div class="scroll-indicator">
      <span>向下滚动</span>
      <div class="scroll-arrow"></div>
    </div>
  </section>
</template>

<style scoped>
.hero {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 0 24px;
}

.hero-content {
  text-align: center;
  z-index: 1;
}

.hero-title {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 4rem;
  font-weight: 900;
  margin: 0;
  line-height: 1.2;
}

.title-line {
  display: block;
  color: rgba(255, 255, 255, 0.9);
  font-size: 2rem;
  font-weight: 400;
  margin-bottom: 16px;
}

.title-gradient {
  display: block;
  background: linear-gradient(135deg, #00bfff 0%, #00ffff 50%, #1e90ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 0 60px rgba(0, 191, 255, 0.5);
  animation: glow 3s ease-in-out infinite;
}

@keyframes glow {
  0%, 100% {
    filter: brightness(1);
  }
  50% {
    filter: brightness(1.3);
  }
}

.hero-subtitle {
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 24px 0 48px;
  line-height: 1.8;
}

.highlight {
  color: #00ffff;
  font-weight: 600;
}

.hero-btn {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 16px 40px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff;
  background: linear-gradient(135deg, #00bfff, #1e90ff);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: 0 0 30px rgba(0, 191, 255, 0.4);
}

.hero-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  transition: left 0.5s ease;
}

.hero-btn:hover::before {
  left: 100%;
}

.hero-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 50px rgba(0, 191, 255, 0.6);
}

.btn-icon {
  font-size: 1.3rem;
  transition: transform 0.3s ease;
}

.hero-btn:hover .btn-icon {
  transform: translateX(5px);
}

.scroll-indicator {
  position: absolute;
  bottom: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.875rem;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(10px); }
}

.scroll-arrow {
  width: 20px;
  height: 20px;
  border-right: 2px solid rgba(0, 191, 255, 0.6);
  border-bottom: 2px solid rgba(0, 191, 255, 0.6);
  transform: rotate(45deg);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .title-line {
    font-size: 1.5rem;
  }

  .hero-subtitle {
    font-size: 1rem;
  }
}
</style>