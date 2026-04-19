<script setup lang="ts">
import { onMounted } from 'vue'

const props = defineProps<{
  target: string
}>()

onMounted(() => {
  window.location.replace(props.target)
})
</script>

<template>
  <section class="redirect-page">
    <div class="redirect-card">
      <p class="eyebrow">Django Admin</p>
      <h1>正在前往管理后台</h1>
      <p class="description">
        前台已不再提供登录和内容管理入口，所有编辑操作统一在 Django 管理后台完成。
      </p>
      <a class="link" :href="target">如果没有自动跳转，请点击这里</a>
    </div>
  </section>
</template>

<style scoped>
.redirect-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 96px 24px 40px;
}

.redirect-card {
  width: min(520px, 100%);
  padding: 40px 32px;
  border-radius: 24px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(0, 191, 255, 0.16);
  text-align: center;
}

.eyebrow {
  margin: 0 0 12px;
  color: rgba(0, 191, 255, 0.78);
  font-size: 0.8rem;
  letter-spacing: 0.14em;
  text-transform: uppercase;
}

.redirect-card h1 {
  margin: 0 0 14px;
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 2rem;
}

.description {
  margin: 0 0 20px;
  color: rgba(255, 255, 255, 0.72);
  line-height: 1.8;
}

.link {
  color: #00bfff;
  text-decoration: none;
}

.link:hover {
  color: #00ffff;
}
</style>
