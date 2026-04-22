<template>
  <div class="home">
    <div class="header">
      <h1 class="title">AI 行动助手</h1>
      <p class="subtitle">基于截图与系统上下文理解</p>
    </div>

    <div class="content">
      <div class="upload-section">
        <ImageUploader @upload-success="handleUploadSuccess" />
      </div>

      <div class="features">
        <div class="feature-item">
          <div class="feature-icon">📸</div>
          <div class="feature-text">
            <h3>智能识别</h3>
            <p>自动识别截图中的日程、任务和出行信息</p>
          </div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">🤖</div>
          <div class="feature-text">
            <h3>AI 分析</h3>
            <p>大模型解析，提取结构化信息</p>
          </div>
        </div>
        <div class="feature-item">
          <div class="feature-icon">⚡</div>
          <div class="feature-text">
            <h3>智能建议</h3>
            <p>自动生成行动建议，一键执行</p>
          </div>
        </div>
      </div>

      <div class="quick-links">
        <van-button 
          type="primary" 
          block 
          @click="goToHistory"
          icon="history"
        >
          查看历史记录
        </van-button>
        <van-button 
          type="default" 
          block 
          @click="showExample"
          icon="image"
        >
          查看示例
        </van-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router';
import ImageUploader from '../components/ImageUploader.vue';
import { showToast } from 'vant';

const router = useRouter();

const handleUploadSuccess = (imageId: number) => {
  router.push(`/result/${imageId}`);
};

const goToHistory = () => {
  router.push('/history');
};

const showExample = () => {
  showToast('示例功能开发中');
};
</script>

<style scoped>
.home {
  min-height: 100vh;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding-top: 20px;
}

.title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 16px;
  color: #666;
}

.upload-section {
  margin-bottom: 30px;
}

.features {
  margin-bottom: 30px;
}

.feature-item {
  display: flex;
  align-items: center;
  padding: 15px;
  background-color: #f8f8f8;
  border-radius: 8px;
  margin-bottom: 10px;
}

.feature-icon {
  font-size: 24px;
  margin-right: 15px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e6f7ff;
  border-radius: 50%;
}

.feature-text h3 {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 4px;
  color: #333;
}

.feature-text p {
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.quick-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

@media (max-width: 480px) {
  .home {
    padding: 15px;
  }
  
  .title {
    font-size: 24px;
  }
  
  .subtitle {
    font-size: 14px;
  }
}
</style>