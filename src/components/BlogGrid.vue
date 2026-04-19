<script setup lang="ts">
import { ref } from 'vue'
import BlogCard from './BlogCard.vue'

interface Blog {
  id: number
  title: string
  excerpt: string
  category: string
  date: string
  readTime: string
  cover: string
}

const blogs: Blog[] = [
  {
    id: 1,
    title: 'Three.js 3D 粒子系统实现指南',
    excerpt: '深入探索如何使用 Three.js 创建令人惊叹的粒子效果，从基础到高级特效实现。',
    category: 'Three.js',
    date: '2026-04-05',
    readTime: '8 分钟阅读',
    cover: 'particle'
  },
  {
    id: 2,
    title: 'Vue3 组合式 API 最佳实践',
    excerpt: '全面解析 Vue3 组合式 API 的使用技巧，提升代码可维护性和复用性。',
    category: 'Vue3',
    date: '2026-04-03',
    readTime: '12 分钟阅读',
    cover: 'vue'
  },
  {
    id: 3,
    title: 'TypeScript 高级类型系统',
    excerpt: '深入理解 TypeScript 的高级类型特性，包括泛型、条件类型和映射类型。',
    category: 'TypeScript',
    date: '2026-04-01',
    readTime: '15 分钟阅读',
    cover: 'typescript'
  },
  {
    id: 4,
    title: 'WebGL 着色器编程入门',
    excerpt: '从零开始学习 GLSL 着色器编写，创建炫酷的 WebGL 视觉效果。',
    category: 'WebGL',
    date: '2026-03-28',
    readTime: '20 分钟阅读',
    cover: 'webgl'
  },
  {
    id: 5,
    title: 'CSS3 动画性能优化',
    excerpt: '掌握 CSS 动画技巧，优化页面性能，打造流畅的用户体验。',
    category: 'CSS3',
    date: '2026-03-25',
    readTime: '10 分钟阅读',
    cover: 'css'
  },
  {
    id: 6,
    title: 'Node.js 微服务架构设计',
    excerpt: '使用 Node.js 构建高性能微服务架构的最佳实践和设计方案。',
    category: 'Node.js',
    date: '2026-03-20',
    readTime: '18 分钟阅读',
    cover: 'node'
  }
]

const activeCategory = ref('全部')
const categories = ['全部', 'Three.js', 'Vue3', 'TypeScript', 'WebGL', 'CSS3', 'Node.js']

const filteredBlogs = () => {
  if (activeCategory.value === '全部') {
    return blogs
  }
  return blogs.filter(blog => blog.category === activeCategory.value)
}

const setCategory = (category: string) => {
  activeCategory.value = category
}
</script>

<template>
  <section id="blog" class="blog-section">
    <div class="section-header">
      <h2 class="section-title">
        <span class="title-accent">我的</span>博客
      </h2>
      <p class="section-desc">分享技术见解，记录学习历程</p>
    </div>

    <div class="category-filter">
      <button
        v-for="cat in categories"
        :key="cat"
        class="filter-btn"
        :class="{ active: activeCategory === cat }"
        @click="setCategory(cat)"
      >
        {{ cat }}
      </button>
    </div>

    <div class="blog-grid">
      <BlogCard
        v-for="blog in filteredBlogs()"
        :key="blog.id"
        :blog="blog"
      />
    </div>
  </section>
</template>

<style scoped>
.blog-section {
  min-height: 100vh;
  padding: 100px 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-title {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 3rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 16px;
}

.title-accent {
  background: linear-gradient(135deg, #00bfff, #00ffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-desc {
  font-size: 1.1rem;
  color: rgba(255, 255, 255, 0.6);
  margin: 0;
}

.category-filter {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px;
  margin-bottom: 48px;
}

.filter-btn {
  padding: 10px 24px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 191, 255, 0.2);
  border-radius: 30px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn:hover {
  background: rgba(0, 191, 255, 0.1);
  border-color: rgba(0, 191, 255, 0.5);
  color: #00ffff;
}

.filter-btn.active {
  background: linear-gradient(135deg, #00bfff, #1e90ff);
  border-color: transparent;
  color: #fff;
  box-shadow: 0 0 20px rgba(0, 191, 255, 0.4);
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

@media (max-width: 768px) {
  .blog-section {
    padding: 80px 16px;
  }

  .section-title {
    font-size: 2rem;
  }

  .blog-grid {
    grid-template-columns: 1fr;
  }
}
</style>