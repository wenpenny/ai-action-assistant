<template>
  <div class="history">
    <div class="background-effects">
      <div class="gradient-orb orb-1"></div>
      <div class="gradient-orb orb-2"></div>
    </div>

    <van-nav-bar
      title="历史记录"
      left-text="返回"
      @click-left="goBack"
      class="nav-bar"
    />

    <div v-if="loading" class="loading-container">
      <LoadingBlock />
    </div>

    <div v-else-if="error" class="error-container">
      <van-empty description="加载失败" />
      <van-button type="primary" @click="loadHistory">重试</van-button>
    </div>

    <div v-else class="history-content" :class="{ 'animate-in': mounted }">
      <div class="history-header">
        <h2 class="history-title">
          <van-icon name="clock-o" size="24" />
          记录列表
        </h2>
        <span class="history-count" v-if="historyList.length">
          {{ historyList.length }} 条记录
        </span>
      </div>
      <HistoryList
        :historyList="historyList"
        @view-detail="viewDetail"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import LoadingBlock from '../components/LoadingBlock.vue';
import HistoryList from '../components/HistoryList.vue';
import { getHistory } from '../api/history';
import type { HistoryItem } from '../types/history';

const router = useRouter();

const loading = ref(true);
const error = ref(false);
const mounted = ref(false);
const historyList = ref<HistoryItem[]>([]);

const loadHistory = async () => {
  loading.value = true;
  error.value = false;
  try {
    const result = await getHistory();
    historyList.value = result;
    setTimeout(() => {
      mounted.value = true;
    }, 100);
  } catch (err) {
    console.error('加载历史记录失败:', err);
    error.value = true;
  } finally {
    loading.value = false;
  }
};

const viewDetail = (imageId: number) => {
  router.push(`/history/${imageId}`);
};

const goBack = () => {
  router.push('/');
};

onMounted(() => {
  loadHistory();
});
</script>

<style scoped>
.history {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
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
  opacity: 0.3;
}

.orb-1 {
  width: 200px;
  height: 200px;
  background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
  top: -50px;
  right: -50px;
}

.orb-2 {
  width: 180px;
  height: 180px;
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  bottom: 100px;
  left: -60px;
}

.nav-bar {
  background: transparent;
  position: relative;
  z-index: 10;
}

:deep(.van-nav-bar) {
  background: transparent;
}

:deep(.van-nav-bar__title) {
  color: #ffffff;
  font-weight: 600;
}

:deep(.van-nav-bar__text) {
  color: #ffffff;
}

:deep(.van-nav-bar__arrow) {
  color: #ffffff;
}

.loading-container,
.error-container {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  z-index: 1;
}

.error-container {
  gap: 20px;
}

.history-content {
  padding: 20px;
  position: relative;
  z-index: 1;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.5s ease;
}

.history-content.animate-in {
  opacity: 1;
  transform: translateY(0);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
  margin: 0;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.history-title .van-icon {
  color: #ffffff;
}

.history-count {
  background: rgba(255, 255, 255, 0.2);
  color: #ffffff;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 480px) {
  .history-content {
    padding: 15px;
  }
  
  .history-title {
    font-size: 18px;
  }
}
</style>