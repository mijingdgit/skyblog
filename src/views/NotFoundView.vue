<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router'

const route = useRoute()
</script>

<template>
  <div class="not-found-page">
    <section class="not-found-card">
      <span class="eyebrow">404 / Lost Signal</span>
      <h1>页面没有找到</h1>
      <p>
        这条链接暂时没有对应内容，可能是文章已移动、地址输入有误，或者它还在未来的某个分支里。
      </p>

      <div class="missing-path">
        <span>当前路径</span>
        <code>{{ route.fullPath }}</code>
      </div>

      <div class="actions">
        <RouterLink to="/" class="btn-primary">回到首页</RouterLink>
        <RouterLink to="/articles" class="btn-secondary">浏览文章</RouterLink>
      </div>
    </section>
  </div>
</template>

<style scoped>
.not-found-page {
  min-height: 72vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 24px 80px;
}

.not-found-card {
  width: min(720px, 100%);
  padding: 56px;
  border: 1px solid rgba(0, 191, 255, 0.16);
  border-radius: 28px;
  background:
    radial-gradient(circle at top left, rgba(0, 191, 255, 0.16), transparent 34%),
    rgba(255, 255, 255, 0.035);
  box-shadow: 0 28px 80px rgba(0, 0, 0, 0.28);
  text-align: center;
}

.eyebrow {
  display: inline-flex;
  padding: 8px 16px;
  margin-bottom: 22px;
  border: 1px solid rgba(0, 191, 255, 0.28);
  border-radius: 999px;
  color: #00ffff;
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 0.8rem;
  letter-spacing: 0.08em;
}

h1 {
  margin: 0 0 18px;
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: clamp(2rem, 5vw, 4rem);
  color: #fff;
}

p {
  max-width: 560px;
  margin: 0 auto 28px;
  color: rgba(255, 255, 255, 0.62);
  line-height: 1.8;
}

.missing-path {
  display: grid;
  gap: 8px;
  max-width: 560px;
  margin: 0 auto 30px;
  padding: 16px 18px;
  border: 1px solid rgba(0, 191, 255, 0.12);
  border-radius: 16px;
  background: rgba(5, 12, 26, 0.6);
  text-align: left;
}

.missing-path span {
  color: rgba(255, 255, 255, 0.42);
  font-size: 0.85rem;
}

.missing-path code {
  overflow-wrap: anywhere;
}

.actions {
  display: flex;
  justify-content: center;
  gap: 14px;
  flex-wrap: wrap;
}

.btn-primary,
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 128px;
  padding: 13px 24px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 700;
  transition: all 0.25s ease;
}

.btn-primary {
  color: #fff;
  background: linear-gradient(135deg, #00bfff, #1e90ff);
  box-shadow: 0 12px 28px rgba(0, 191, 255, 0.28);
}

.btn-secondary {
  color: #00ffff;
  border: 1px solid rgba(0, 191, 255, 0.35);
  background: rgba(0, 191, 255, 0.08);
}

.btn-primary:hover,
.btn-secondary:hover {
  transform: translateY(-2px);
}

@media (max-width: 640px) {
  .not-found-card {
    padding: 36px 22px;
  }
}
</style>
