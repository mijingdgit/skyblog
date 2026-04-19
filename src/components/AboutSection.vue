<script setup lang="ts">
const skills = [
  { name: 'Vue3', level: 90 },
  { name: 'TypeScript', level: 85 },
  { name: 'Three.js', level: 80 },
  { name: 'Node.js', level: 75 },
  { name: 'WebGL', level: 70 },
  { name: 'CSS3', level: 85 }
]
</script>

<template>
  <section id="about" class="about-section">
    <div class="about-container">
      <div class="about-content">
        <div class="section-label">关于我</div>
        <h2 class="about-title">
          热爱<span class="highlight">技术</span>，追求<span class="highlight">创新</span>
        </h2>
        <p class="about-text">
          嗨，我是 SkyBlog 的创始人！一个热爱编程的开发者，
          专注于前端开发和3D可视化领域。我喜欢探索新技术，
          将复杂的技术概念转化为优雅的解决方案。
        </p>
        <p class="about-text">
          在这个博客中，我会分享我的学习心得、技术见解和项目经验。
          希望这些内容能够帮助到和我一样热爱技术的朋友们。
        </p>

        <div class="skills">
          <h3 class="skills-title">技能标签</h3>
          <div class="skill-list">
            <span v-for="skill in skills" :key="skill.name" class="skill-tag">
              {{ skill.name }}
              <span class="skill-level" :style="{ width: skill.level + '%' }"></span>
            </span>
          </div>
        </div>
      </div>

      <div class="about-visual">
        <div class="avatar-container">
          <div class="avatar-ring"></div>
          <div class="avatar-ring ring-2"></div>
          <div class="avatar">
            <span class="avatar-icon">◈</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.about-section {
  min-height: 100vh;
  padding: 100px 24px;
  display: flex;
  align-items: center;
}

.about-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 80px;
  align-items: center;
}

.section-label {
  display: inline-block;
  padding: 8px 16px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.2), rgba(0, 255, 255, 0.1));
  border: 1px solid rgba(0, 191, 255, 0.3);
  border-radius: 20px;
  font-size: 0.875rem;
  color: #00bfff;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 24px;
}

.about-title {
  font-family: 'Orbitron', 'Noto Sans SC', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 24px;
  line-height: 1.3;
}

.highlight {
  background: linear-gradient(135deg, #00bfff, #00ffff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.about-text {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.8;
  margin: 0 0 16px;
}

.skills {
  margin-top: 40px;
}

.skills-title {
  font-size: 1.1rem;
  color: #fff;
  margin: 0 0 16px;
}

.skill-list {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.skill-tag {
  position: relative;
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 191, 255, 0.2);
  border-radius: 8px;
  color: #fff;
  font-size: 0.875rem;
  overflow: hidden;
}

.skill-tag::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  height: 100%;
  background: linear-gradient(90deg, rgba(0, 191, 255, 0.3), rgba(0, 255, 255, 0.1));
  z-index: 0;
}

.skill-level {
  position: absolute;
  bottom: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #00bfff, #00ffff);
  z-index: 1;
}

.about-visual {
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-container {
  position: relative;
  width: 250px;
  height: 250px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.avatar-ring {
  position: absolute;
  width: 200px;
  height: 200px;
  border: 2px solid transparent;
  border-top-color: #00bfff;
  border-radius: 50%;
  animation: rotate 4s linear infinite;
}

.avatar-ring.ring-2 {
  width: 230px;
  height: 230px;
  border-top-color: transparent;
  border-right-color: #00ffff;
  animation: rotate 6s linear infinite reverse;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.avatar {
  width: 150px;
  height: 150px;
  background: linear-gradient(135deg, rgba(0, 191, 255, 0.2), rgba(0, 255, 255, 0.1));
  border: 2px solid rgba(0, 191, 255, 0.5);
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 0 40px rgba(0, 191, 255, 0.3);
}

.avatar-icon {
  font-size: 4rem;
  color: #00bfff;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.1); }
}

@media (max-width: 900px) {
  .about-container {
    grid-template-columns: 1fr;
    gap: 60px;
    text-align: center;
  }

  .about-visual {
    order: -1;
  }

  .skill-list {
    justify-content: center;
  }

  .about-title {
    font-size: 2rem;
  }
}
</style>