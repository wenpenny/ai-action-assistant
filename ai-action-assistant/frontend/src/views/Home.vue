<template>
  <div class="home">
    <van-nav-bar title="AI 行动助手" fixed />
    <div class="content">
      <div class="header">
        <h1 class="title">AI 行动助手</h1>
        <p class="description">基于截图与系统上下文理解的智能助手，帮您自动识别日程、任务和出行信息，并提供智能建议</p>
      </div>
      
      <ImageUploader />
      
      <div class="features">
        <h2 class="section-title">功能特点</h2>
        <van-grid :column-num="2" gap="16">
          <van-grid-item class="feature-item">
            <van-icon name="calendar" size="32" color="#1989fa" />
            <p class="feature-text">日程识别</p>
          </van-grid-item>
          <van-grid-item class="feature-item">
            <van-icon name="todo-list" size="32" color="#ff9900" />
            <p class="feature-text">任务管理</p>
          </van-grid-item>
          <van-grid-item class="feature-item">
            <van-icon name="location" size="32" color="#52c41a" />
            <p class="feature-text">出行规划</p>
          </van-grid-item>
          <van-grid-item class="feature-item">
            <van-icon name="bell" size="32" color="#722ed1" />
            <p class="feature-text">智能提醒</p>
          </van-grid-item>
        </van-grid>
      </div>
      
      <div class="quick-links">
        <van-button 
          type="default" 
          class="link-button" 
          @click="goToHistory"
        >
          <van-icon name="history" slot="left" />
          查看历史记录
        </van-button>
        <van-button 
          type="default" 
          class="link-button" 
          @click="goToExample"
        >
          <van-icon name="picture" slot="left" />
          示例截图
        </van-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import ImageUploader from '../components/ImageUploader.vue';

const router = useRouter();

const goToHistory = () => {
  router.push('/history');
};

const goToExample = () => {
  // 这里可以跳转到示例页面，暂时跳转到历史记录页
  router.push('/history');
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.content {
  padding-top: 60px;
  padding: 60px 16px 20px;
}

.header {
  text-align: center;
  margin-bottom: 32px;
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: #333;
  margin-bottom: 16px;
}

.description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  max-width: 80%;
  margin: 0 auto;
}

.features {
  margin: 32px 0;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 16px;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 0;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.feature-text {
  margin-top: 12px;
  font-size: 14px;
  color: #333;
}

.quick-links {
  display: flex;
  gap: 12px;
  margin-top: 32px;
}

.link-button {
  flex: 1;
}
</style>
