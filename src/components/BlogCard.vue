<script setup lang="ts">
import { ref } from 'vue'

interface Blog {
  id: number
  title: string
  excerpt: string
  category: string
  date: string
  readTime: string
  cover: string
}

defineProps<{
  blog: Blog
}>()

const isHovered = ref(false)
</script>

<template>
  <article
    class="blog-card"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div class="card-glow" :class="{ active: isHovered }"></div>
    <div class="card-content">
      <div class="card-header">
        <span class="category">{{ blog.category }}</span>
        <span class="date">{{ blog.date }}</span>
      </div>
      <h3 class="title">{{ blog.title }}</h3>
      <p class="excerpt" :class="{ visible: isHovered }">{{ blog.excerpt }}</p>
      <div class="card-footer">
        <span class="read-time">{{ blog.readTime }}</span>
        <button class="read-more">
          阅读全文
          <span class="arrow">→</span>
        </button>
      </div>
    </div>
  </article>
</template>

<style scoped>
.blog-card {
  position: relative;
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 191, 255, 0.15);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s ease;
}

.blog-card:hover {
  transform: translateY(-8px);
  border-color: rgba(0, 191, 255, 0.5);
  box-shadow: 0 20px 40px rgba(0, 191, 255, 0.15);
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.1), rgba(0, 255, 255, 0.05));
  opacity: 0;
  transition: opacity 0.4s ease;
}

.card-glow.active {
  opacity: 1;
}

.card-content {
  position: relative;
  padding: 24px;
  z-index: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.category {
  padding: 4px 12px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.2), rgba(0, 255, 255, 0.1));
  border: 1px solid rgba(0, 191, 255, 0.3);
  border-radius: 20px;
  font-size: 0.75rem;
  color: #00bfff;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.date {
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.5);
}

.title {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: #fff;
  margin: 0 0 12px;
  line-height: 1.4;
  transition: color 0.3s ease;
}

.blog-card:hover .title {
  color: #00ffff;
}

.excerpt {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.6;
  margin: 0;
  max-height: 0;
  overflow: hidden;
  opacity: 0;
  transition: all 0.4s ease;
}

.excerpt.visible {
  max-height: 100px;
  opacity: 1;
  margin-bottom: 16px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.read-time {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.4);
}

.read-more {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  color: #00bfff;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.read-more:hover {
  color: #00ffff;
  gap: 10px;
}

.read-more .arrow {
  transition: transform 0.3s ease;
}

.read-more:hover .arrow {
  transform: translateX(4px);
}
</style>