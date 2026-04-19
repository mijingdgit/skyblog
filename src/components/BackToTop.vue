<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const isVisible = ref(false)

const handleScroll = () => {
  isVisible.value = window.scrollY > 300
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<template>
  <transition name="slide-up">
    <button
      v-if="isVisible"
      class="back-to-top"
      @click="scrollToTop"
    >
      <span class="arrow">↑</span>
    </button>
  </transition>
</template>

<style scoped>
.back-to-top {
  position: fixed;
  bottom: 40px;
  right: 40px;
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #00bfff, #1e90ff);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(0, 191, 255, 0.4);
  transition: all 0.3s ease;
  z-index: 999;
}

.back-to-top:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 30px rgba(0, 191, 255, 0.6);
}

.arrow {
  font-size: 1.5rem;
  color: #fff;
  font-weight: bold;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 768px) {
  .back-to-top {
    bottom: 20px;
    right: 20px;
    width: 44px;
    height: 44px;
  }
}
</style>