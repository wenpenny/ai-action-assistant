<template>
  <div class="home">
    <div class="background-effects">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
      <div class="gradient-orb orb-3"></div>
    </div>

    <div class="header" :class="{ 'animate-in': mounted }">
      <div class="logo-container">
        <div class="logo-icon">
          <van-icon name="scan" size="32" />
        </div>
        <h1 class="title">AI 行动助手</h1>
      </div>
      <p class="subtitle">基于截图与系统上下文理解</p>
      <p class="tagline">智能识别 · 精准分析 · 高效执行</p>
    </div>

    <div class="content">
      <div class="upload-section" :class="{ 'animate-in': mounted }">
        <ImageUploader @upload-success="handleUploadSuccess" />
      </div>

      <div class="features" :class="{ 'animate-in': mounted }">
        <h2 class="section-title">核心功能</h2>
        <div class="feature-grid">
          <div class="feature-card">
            <div class="feature-icon-wrapper scan">
              <van-icon name="scan" size="28" />
            </div>
            <h3>智能识别</h3>
            <p>自动识别截图中的日程、任务和出行信息</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon-wrapper ai">
              <van-icon name="gem" size="28" />
            </div>
            <h3>AI 分析</h3>
            <p>大模型解析，提取结构化信息</p>
          </div>
          <div class="feature-card">
            <div class="feature-icon-wrapper action">
              <van-icon name="flash" size="28" />
            </div>
            <h3>智能建议</h3>
            <p>自动生成行动建议，一键执行</p>
          </div>
        </div>
      </div>

      <div class="quick-links" :class="{ 'animate-in': mounted }">
        <van-button 
          type="primary" 
          block 
          @click="goToHistory"
          icon="orders-o"
          class="action-btn"
          size="large"
        >
          查看历史记录
        </van-button>
        <van-button 
          type="default" 
          block 
          @click="showExample"
          icon="photo-o"
          class="action-btn secondary"
          size="large"
        >
          查看示例
        </van-button>
      </div>

      <div class="stats" :class="{ 'animate-in': mounted }">
        <div class="stat-item">
          <span class="stat-value">3</span>
          <span class="stat-label">场景类型</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">4</span>
          <span class="stat-label">动作执行</span>
        </div>
        <div class="stat-divider"></div>
        <div class="stat-item">
          <span class="stat-value">24h</span>
          <span class="stat-label">随时可用</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ImageUploader from '../components/ImageUploader.vue';
import { showToast, showDialog } from 'vant';

const router = useRouter();
const mounted = ref(false);

onMounted(() => {
  setTimeout(() => {
    mounted.value = true;
  }, 100);
});

const handleUploadSuccess = (imageId: number) => {
  router.push(`/result/${imageId}`);
};

const goToHistory = () => {
  router.push('/history');
};

const showExample = () => {
  const examples = [
    {
      id: 1,
      title: '会议通知',
      description: '识别会议时间、地点和主题',
      image: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400&h=300&fit=crop'
    },
    {
      id: 2,
      title: '作业通知',
      description: '识别作业内容和截止日期',
      image: 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400&h=300&fit=crop'
    },
    {
      id: 3,
      title: '航班信息',
      description: '识别航班号、起飞时间和目的地',
      image: 'https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=400&h=300&fit=crop'
    }
  ];
  
  const exampleHtml = `
    <div class="example-list">
      ${examples.map(example => `
        <div class="example-item" style="margin-bottom: 20px; padding: 15px; border: 1px solid #eee; border-radius: 12px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
          <h3 style="margin-top: 0; margin-bottom: 8px; font-size: 16px; color: #333;">${example.title}</h3>
          <p style="margin-bottom: 12px; font-size: 14px; color: #666;">${example.description}</p>
          <img src="${example.image}" alt="${example.title}" style="width: 100%; height: 150px; object-fit: cover; border-radius: 8px; cursor: pointer;" onclick="window.open('${example.image}', '_blank')">
        </div>
      `).join('')}
    </div>
  `;
  
  showDialog({
    title: '📸 示例截图',
    message: exampleHtml,
    dangerouslyUseHTMLString: true,
    confirmButtonText: '关闭',
    confirmButtonColor: '#1989fa'
  });
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  padding: 20px;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.background-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
}

.gradient-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.4;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 300px;
  height: 300px;
  background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.orb-2 {
  width: 250px;
  height: 250px;
  background: linear-gradient(135deg, #54a0ff 0%, #5f27cd 100%);
  bottom: 20%;
  left: -80px;
  animation-delay: -7s;
}

.orb-3 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #1dd1a1 0%, #10ac84 100%);
  bottom: -50px;
  right: 20%;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20px, -30px) scale(1.05);
  }
  50% {
    transform: translate(-10px, 20px) scale(0.95);
  }
  75% {
    transform: translate(-30px, -10px) scale(1.02);
  }
}

.content {
  position: relative;
  z-index: 1;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding-top: 20px;
  opacity: 0;
  transform: translateY(-20px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.header.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.logo-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 12px;
}

.logo-icon {
  width: 56px;
  height: 56px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  animation: pulse 3s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
  }
}

.title {
  font-size: 32px;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  letter-spacing: 1px;
}

.subtitle {
  font-size: 16px;
  color: rgba(255, 255, 255, 0.9);
  margin: 8px 0 0 0;
  font-weight: 400;
}

.tagline {
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  margin: 8px 0 0 0;
  letter-spacing: 2px;
}

.upload-section {
  margin-bottom: 30px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.2s;
}

.upload-section.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.features {
  margin-bottom: 30px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.4s;
}

.features.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #ffffff;
  text-align: center;
  margin-bottom: 16px;
  text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.feature-card {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 20px 12px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.feature-icon-wrapper {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 12px;
}

.feature-icon-wrapper.scan {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
}

.feature-icon-wrapper.ai {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: #ffffff;
}

.feature-icon-wrapper.action {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: #ffffff;
}

.feature-card h3 {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin: 0 0 6px 0;
}

.feature-card p {
  font-size: 11px;
  color: #888;
  margin: 0;
  line-height: 1.4;
}

.quick-links {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.6s;
}

.quick-links.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.action-btn {
  height: 48px;
  border-radius: 24px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.action-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
}

.action-btn.secondary {
  background: rgba(255, 255, 255, 0.9);
  border: none;
}

.stats {
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.8s cubic-bezier(0.4, 0, 0.2, 1) 0.8s;
}

.stats.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.stat-item {
  flex: 1;
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 24px;
  font-weight: 800;
  color: #667eea;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  font-size: 12px;
  color: #888;
}

.stat-divider {
  width: 1px;
  height: 40px;
  background: #eee;
}

@media (max-width: 480px) {
  .home {
    padding: 15px;
  }
  
  .title {
    font-size: 26px;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
    gap: 10px;
  }
  
  .feature-card {
    display: flex;
    align-items: center;
    text-align: left;
    padding: 16px;
    gap: 12px;
  }
  
  .feature-icon-wrapper {
    margin: 0;
    flex-shrink: 0;
  }
  
  .stats {
    flex-wrap: wrap;
  }
  
  .stat-divider {
    display: none;
  }
  
  .stat-item {
    flex: 1 1 33.33%;
    margin-bottom: 8px;
  }
}
</style>