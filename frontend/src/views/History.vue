<template>
  <div class="history">
    <van-nav-bar
      title="历史记录"
      left-text="返回"
      @click-left="goBack"
    />

    <div v-if="loading" class="loading-container">
      <LoadingBlock />
    </div>

    <div v-else-if="error" class="error-container">
      <van-empty description="加载失败" />
      <van-button type="primary" @click="loadHistory">重试</van-button>
    </div>

    <div v-else class="history-content">
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
const historyList = ref<HistoryItem[]>([]);

const loadHistory = async () => {
  loading.value = true;
  error.value = false;
  try {
    const result = await getHistory();
    historyList.value = result;
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
  background-color: #f5f5f5;
}

.loading-container,
.error-container {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.error-container {
  gap: 20px;
}

.history-content {
  padding: 20px;
}

@media (max-width: 480px) {
  .history-content {
    padding: 15px;
  }
}
</style>